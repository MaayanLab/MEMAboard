

import os
import sys
import json
import pandas as pd
import numpy as np
from shutil import rmtree
from scipy.spatial.distance import cdist
# import fetch_omero_images

OMERO_URL = 'https://meplincs.ohsu.edu'

DATA_DIR = 'SSC_Level3'
ID_DIR = 'ImageIDs'
IMG_DIR = 'Thumbnails'

USERNAME = 'adohlman'
PASSWORD = 'sredna93'

with open(os.path.join(IMG_DIR,'ignore_ids.txt')) as f: IGNORE = f.read().splitlines()

def get_centroids(sscfile):

	df = pd.read_table(os.path.join(DATA_DIR,sscfile), low_memory=False)
	df.index = df['ImageID'].values

	mep2id = {}
	for MEP in np.unique(df['MEP'].values):
		data = df.loc[df['MEP'] == MEP, df.dtypes == float]
		data = data[data['QAScore'] > 0.7]
		data = data.drop([ x for x in data.columns if 'QA' in x or '_SE' in x], axis=1)
		data = data.dropna(axis=1, how='any')

		centroid = np.matrix(data.mean())
		Y = cdist(centroid, data, metric='cosine')
		centroid_ID = str(data.index.values[Y.argmin()])

		while centroid_ID in IGNORE:
			data = data.drop(int(centroid_ID))
			Y = cdist(centroid, data, metric='cosine')
			centroid_ID = str(data.index.values[Y.argmin()])

		mep2id[MEP] = centroid_ID
	return mep2id		


def get_thumbnails(mep2id):

	for cell in mep2id.keys():

		thumb_dir = os.path.join(IMG_DIR, cell)

		if cell not in os.listdir(IMG_DIR):
			os.mkdir(thumb_dir)
		print "Retrieving thumbnails for",cell,":"
		id_path = os.path.join(IMG_DIR, cell+'_ids.txt')
		out = open(id_path,'w')
		out.write('MEP\tid\n')
		for MEP in sorted(mep2id[cell].keys()):
			out.write(MEP + '\t' + mep2id[cell][MEP] + '\n')
		out.close()

		cmd = ' '.join([
			'python3','fetch_omero_images.py',
			'-o', os.path.join(IMG_DIR, cell),
			'-d', id_path,
			'-s', OMERO_URL,
			'-u', USERNAME,
			'-w', PASSWORD
		])

		print "Executing '"+cmd+"'"
		try:
			os.system(cmd)
		except:
			print "ERROR with fetch_omero_images.py"
			continue

		sprite_order = [ os.path.join(thumb_dir,mep2id[cell][x]+'_thumbnail.jpg')
					for x in sorted(mep2id[cell].keys()) ]

		cmd = ' '.join(['montage',
			'-geometry +0+0',
			'-border 0',
			'-tile 53x53']
			+ sprite_order
			+ [os.path.join(IMG_DIR, cell+'_sprite.png')]
		)

		# print cmd
		print "Building sprite:",cell
		# print "Executing '"+cmd+"'"
		try:
			os.system(cmd)
		except:
			print "ERROR with fetch_omero_images.py"
			continue


def main():

	mep2id = {}


	for sscfile in os.listdir(DATA_DIR):
		if sscfile[0] == '.': continue

		# if sscfile != 'mcf10a_ssc_Level3.tsv': continue

		cell = sscfile.split('_',1)[0].upper()
		print "Processing",cell
		print "Choosing IDs..."
		mep2id[cell] = get_centroids(sscfile)

	get_thumbnails(mep2id)


if __name__ == "__main__":
	main()

