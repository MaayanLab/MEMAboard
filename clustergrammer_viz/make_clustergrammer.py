'''
Python 2.7
The clustergrammer python module can be installed using pip:
pip install clustergrammer

or by getting the code from the repo:
https://github.com/MaayanLab/clustergrammer-py
'''

# necessary for scipy hierarchy clustering
import os
import sys
import pandas as pd
sys.setrecursionlimit(10000)

from clustergrammer import Network
net = Network()

# load matrix tsv file
APP_DIR = '../embedding-projector-standalone'
DATA_PATH = APP_DIR + '/oss_data'

meta_fields = ['MEP','ECMp','Ligand']

# print os.chdir(os.path.join(DATA_PATH, 'MCF10A_SS1_cols.txt'))
for ss in ['SS1','SS2','SS3']:

	print ss

	data = pd.read_table(os.path.join(DATA_PATH, 'MCF10A_'+ss+'.tsv'), header=None).values
	meta = pd.read_table(os.path.join(DATA_PATH, 'MCF10A_'+ss+'_meta.tsv'))

	rows = []
	for i in range(len(meta)):
		rows.append(tuple( x+': '+meta.loc[i,x] for x in meta_fields ))

	with open(os.path.join(DATA_PATH, 'MCF10A_'+ss+'_cols.txt')) as f:
		cols = f.read().splitlines()

	df = pd.DataFrame(data, index=rows, columns=cols)
		# cols = f.read().splitlines()
	net.load_df(df)
	# optional filtering and normalization
	##########################################
	# net.filter_sum('row', threshold=20)
	# net.normalize(axis='col', norm_type='zscore', keep_orig=True)
	# net.filter_N_top('row', 250, rank_type='sum')
	# net.filter_threshold('row', threshold=3.0, num_occur=4)
	# net.swap_nan_for_zero()
	net.clip(-10,10)

	net.make_clust(dist_type='cos', views=[], sim_mat=False)
	net.write_json_to_file('viz', APP_DIR+'/json/'+ss+'.json', 'indent')

