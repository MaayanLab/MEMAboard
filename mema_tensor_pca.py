
import os
import json
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.tensorboard.plugins import projector

LOG_DIR = 'mema_logs'
DAT_DIR = 'raw_data'

with open('display_feats.json') as f: display_feats = json.load(f)

def build_metadata(df, map_feature_names):
	meta_feats = map_feature_names.keys()
	meta_df = pd.concat([	df.apply(lambda x:'%s_%s' % (x['ECMp'],x['Ligand']),axis=1).rename('MEP'),
							df[['ECMp','Ligand']],
							df[meta_feats].rename(columns=map_feature_names)], axis=1)
	# meta_df.to_csv(os.path.join(LOG_DIR, 'MCF10A_metadata.tsv'), sep='\t', index=None)
	return meta_df


def build_data(df):
	df = df._get_numeric_data().dropna(how='all',axis='columns')
	df = df[[x for x in df.columns if x[-3:]!='_SE']]
	df = df.drop([	'Spot_PA_ReplicateCount',
					'Spot_PA_SpotCellCount',
					'QA_LowReplicateCount',
					'PinDiameter'], 1)
	df = (df - df.mean())/df.std() # z-score by column
	return df


def get_mema_data(ss):
	map_feature_names = display_feats[ss]
	meta_path = os.path.join(LOG_DIR,ss+'_metadata.tsv')
	data_path = os.path.join(DAT_DIR, 'MCF10A_'+ss+'_Level4.txt')

	df = pd.read_table(data_path)
	meta_df = build_metadata(df, map_feature_names)
	meta_df.to_csv(meta_path, sep='\t', index=None)

	df = build_data(df)
	df.to_csv(data_path.replace('.txt','_norm.txt'), sep='\t')
	df.to_csv(data_path.replace('.txt','_nometa.txt'), sep='\t', header=None, index=None)
	mema_data = df.values

	return mema_data, meta_path


def main():

	# init = tf.global_variables_initializer()

	# saver = tf.train.Saver()

	sess = tf.Session()

	# summary_writer = tf.summary.FileWriter(LOG_DIR, sess.graph)
	summary_writer = tf.summary.FileWriter(LOG_DIR)

	# hist_writer = tf.summary.FileWriter(LOG_DIR)

	# sess.run(init)

	config = projector.ProjectorConfig()

	embed_tensors = []

	for ss in ['SS1','SS2','SS3']:

		mema_data, meta_path = get_mema_data(ss)

		mema_tensor = tf.Variable(mema_data, name=ss)

		embed_tensors.append(mema_tensor)

		sess.run(mema_tensor.initializer)

		embedding_config = config.embeddings.add()
		embedding_config.tensor_name = mema_tensor.name
		embedding_config.metadata_path = meta_path

		projector.visualize_embeddings(summary_writer, config)

	# result = sess.run(embed_tensors)

	print "Saving embeddings..."
	saver = tf.train.Saver(embed_tensors)
	saver.save(sess, os.path.join(LOG_DIR, 'model.ckpt'))

	# os.system("tensorboard --logdir=" + LOG_DIR )

if __name__ == '__main__':
	main()

