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

DATA_PATH = '../embedding-projector-standalone/oss_data'

# print os.chdir(os.path.join(DATA_PATH, 'MCF10A_SS1_cols.txt'))
for ss in ['SS1','SS2','SS3']:

	data = pd.read_table(os.path.join(DATA_PATH, 'MCF10A_'+ss+'.tsv')).values
	meta = pd.read_table(os.path.join(DATA_PATH, 'MCF10A_'+ss+'_meta.tsv'))

	with open(os.path.join(DATA_PATH, 'MCF10A_'+ss+'_cols.txt')) as f:
		cols = f.read().splitlines()

	# cols = pd.read_table(os.path.join(DATA_PATH, 'MCF10A_'+ss+'_cols.txt')).values

# net.load_file('txt/MCF10A_SS1_matrix.txt')

# optional filtering and normalization
##########################################
# net.filter_sum('row', threshold=20)
# net.normalize(axis='col', norm_type='zscore', keep_orig=True)
# net.filter_N_top('row', 250, rank_type='sum')
# net.filter_threshold('row', threshold=3.0, num_occur=4)
# net.swap_nan_for_zero()

# net.make_clust(dist_type='cos', views=[], sim_mat=False)

# write jsons for front-end visualizations
# net.write_json_to_file('viz', 'json/mult_view.json', 'indent')
