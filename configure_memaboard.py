
import os
import sys
import json
import pandas as pd
import numpy as np
from clustergrammer import Network

sys.setrecursionlimit(10000)

sprite = True

DATA_DIR = 'SSC_Level4'
IMG_DIR = 'Thumbnails'
FEAT_FILE = 'feature_table.txt'

config = {"embeddings":[]}
col_headers = ['Feature','Location','Source','Category']
expand_src = {'CP': 'Cell Profiler', 'PA': 'Pipeline Analysis'}

def create_datatables(sscfile, feat_table):

	cell = sscfile.split('_',1)[0].upper()
	print "Building tensor for",cell,":"

	data_feats = feat_table.index.tolist()
	meta_feats = feat_table.index[ feat_table['Gradient'] == True ].tolist()

	df = pd.read_table(os.path.join(DATA_DIR, sscfile))

	if sum(df['Drug'].notnull()) == 0: meta_cats = ['MEP','ECMp','Ligand']
	else: meta_cats = ['MEP_Drug','ECMp','Ligand','Drug']

	df = df.loc[:, meta_cats + data_feats]
	data_df = df.loc[:, data_feats]
	data_df = (data_df - data_df.mean())/data_df.std()
	dim = data_df.shape

	meta_df = df[meta_cats + meta_feats]
	meta_df = meta_df.rename(columns=dict(zip(feat_table.index,feat_table['DisplayShort'])))

	print "...building the feature matrix"
	build_feature_matrices(meta_df, cell)

	data_path = os.path.join('data', cell+'.tsv')
	meta_path = os.path.join('data', cell+'_meta.tsv')
	img_path = os.path.join(IMG_DIR, cell+'_sprite.png')

	config["embeddings"].append({
	 	"tensorName": cell,
		"tensorShape": dim,
		"tensorPath": data_path,
		"metadataPath": meta_path,
		"sprite":{
			"imagePath": img_path,
			"singleImageDim": [150, 150]
		}	
	})

	meta_df.to_csv(meta_path, sep='\t', index=None)
	data_df.to_csv(data_path, sep='\t', index=None, header=None)

	net = make_clustergram(df, feat_table, meta_cats)
	net.write_json_to_file('viz', 'json/'+cell+'.json', 'indent')


def make_clustergram(df, feat_table, meta_cats):
	net = Network()

	rows = []
	for i in range(len(df.index)):
		rows.append(tuple( x+': '+df.loc[i,x] for x in meta_cats ))

	cols = []
	for i in range(len(df.columns)):
		feature = df.columns[i]
		if feature in meta_cats: continue
		loci, source, category, dispshort, dispunique, gradient  = feat_table.loc[feature]
		source = expand_src[source]

		col_fields = [ dispunique, loci, source, category ]
		cols.append(tuple( col_headers[j]+': '+col_fields[j] for j in range(4)))

	data_df = df.drop(meta_cats, axis=1)
	data_df = (data_df - data_df.mean())/data_df.std()
	data_df.index = rows
	data_df.columns = cols
	net.load_df(data_df)
	net.clip(-10,10)
	net.make_clust(dist_type='cos', views=[], sim_mat=False)
	return net


def build_feature_matrices(meta_df, cell):
	for feature in meta_df._get_numeric_data().columns:
		meta_df[feature] = (meta_df[feature] - meta_df[feature].mean())/meta_df[feature].std()
		fmat = pd.DataFrame(index=np.unique(meta_df['Ligand'].values),
							columns=np.unique(meta_df['ECMp'].values))
		for lig, ecmp in [ (x,y) for x in fmat.index for y in fmat.columns ]:
			fmat.loc[lig, ecmp] = meta_df[meta_df['MEP'] == ecmp+'_'+lig][feature].values[0]

		featname = feature.replace(' ','')
		net = make_clustergram_from_featmat(fmat)
		net.write_json_to_file('viz', 'json/'+cell+'_'+featname+'.json', 'indent')


def make_clustergram_from_featmat(fmat):
	net = Network()
	fmat.index = [ tuple(['Ligand: '+x]) for x in fmat.index.values ]
	fmat.columns = [ tuple(['ECMp: '+x]) for x in fmat.columns.values ]
	net.load_df(fmat)
	net.clip(-10,10)
	net.make_clust(dist_type='cos', views=[], sim_mat=False)
	return net


def main():
	feat_table = pd.read_table(FEAT_FILE, index_col=0)

	# If the folder does not exist, create it. If it does, empty it.
	for folder in ['json','data']:
		if folder not in os.listdir('.'): os.mkdir(folder)
		else: map(lambda f: os.remove(os.path.join(folder,f)), os.listdir(folder))

	# Build tensor files for each item in DATA_DIR
	for sscfile in os.listdir(DATA_DIR):
		if sscfile[0] == '.': continue
		create_datatables(sscfile, feat_table)

	# Save config file, which points to data
	with open(os.path.join('json','memaboard_config.json'), 'w') as out:
		json.dump(config, out, indent=2)


if __name__ == "__main__":
	main()