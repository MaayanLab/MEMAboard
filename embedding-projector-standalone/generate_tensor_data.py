
import os
import json
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.tensorboard.plugins import projector

OUT_DIR = 'oss_data'
# OUT_DIR = 'tensor_data'
DAT_DIR = '../raw_data'
config = {"embeddings":[]}

with open('display_feats.json') as f: display_feats = json.load(f)

def build_metadata(df, map_feature_names):
	meta_feats = map_feature_names.keys()
	meta_df = pd.concat([	df.apply(lambda x:'%s_%s' % (x['ECMp'],x['Ligand']),axis=1).rename('MEP'),
							df[['ECMp','Ligand']],
							df[meta_feats].rename(columns=map_feature_names)], axis=1)
	return meta_df


def build_data(df):
	df = df._get_numeric_data().dropna(how='all',axis='columns') # Remove non-numeric columns
	df = df[[x for x in df.columns if x[-3:]!='_SE']] # Remove stderr columns
	df = df.drop([	'Spot_PA_ReplicateCount', # Remove numeric metadata
					'Spot_PA_SpotCellCount',
					'QA_LowReplicateCount',
					'PinDiameter'], 1)
	df = (df - df.mean())/df.std() # z-score by column
	return df


def get_mema_data(ss):
	map_feature_names = display_feats[ss]
	DATA_PATH = os.path.join(OUT_DIR,'MCF10A_'+ss+'.tsv')
	META_PATH = os.path.join(OUT_DIR, 'MCF10A_'+ss+'_meta.tsv')

	df = pd.read_table(os.path.join(DAT_DIR,'MCF10A_'+ss+'_Level4.txt'))
	meta_df = build_metadata(df, map_feature_names)
	meta_df.to_csv(META_PATH, sep='\t', index=None)

	df = build_data(df)
	df.to_csv(DATA_PATH, sep='\t', header=None, index=None)

	with open(os.path.join(OUT_DIR,'MCF10A_'+ss+'_cols.txt'),'w') as f:
		f.write('\n'.join(df.columns.values))

	print ss, len(df.columns.values)

	return df.shape, DATA_PATH, META_PATH



def main():
	for ss in ['SS1','SS2','SS3']:
		dim, dataPath, metaPath = get_mema_data(ss)

		stain_name = ss.replace('SS','Staining Set ')

		config["embeddings"].append({
			 	"tensorName": stain_name,
				"tensorShape": dim,
				"tensorPath": dataPath,
				"metadataPath": metaPath
			})

	with open(os.path.join(OUT_DIR,'oss_demo_projector_config.json'), 'w') as outfile:
		json.dump(config, outfile, indent=2)


if __name__ == '__main__':
	main()

