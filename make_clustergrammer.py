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
# APP_DIR = '../embedding-projector-standalone'
DATA_PATH = 'oss_data'
FEAT_PATH = 'feature_data'

row_headers = ['MEP','ECMp','Ligand']
col_headers = ['Feature','Location','Source','Category' ] #,'Marker']
expand_src = {'CP': 'Cell Profiler', 'PA': 'Pipeline Analysis'}

def make_clustergram_matrix(ss):
# print os.chdir(os.path.join(DATA_PATH, 'MCF10A_SS1_cols.txt'))
	# print ss
	net = Network()

	data = pd.read_table(os.path.join(DATA_PATH, 'MCF10A_'+ss+'.tsv'), header=None).values
	row_meta = pd.read_table(os.path.join(DATA_PATH, 'MCF10A_'+ss+'_meta.tsv'))

	with open(os.path.join(DATA_PATH, 'MCF10A_'+ss+'_cols.txt')) as f:
		col_meta = f.read().splitlines()

	rows = []
	for i in range(len(row_meta)):
		rows.append(tuple( x+': '+row_meta.loc[i,x] for x in row_headers ))

	cols = []
	for i in range(len(col_meta)):
		name = col_meta[i]
		name = name
		loci, source, category, marker = col_meta[i].split('_', 3)

		marker = marker.replace('Log2RUVLoess','').replace('LogitRUVLoess','')
		if '_' in marker: marker = '_'+''.join(marker.split('_')[::-1])

		name = marker.replace('_','') + '_(' + loci +')'

		source = expand_src[source]
		col_fields = [ name, loci, source, category ]
		cols.append(tuple( col_headers[j]+': '+col_fields[j] for j in range(4)))

	df = pd.DataFrame(data, index=rows, columns=cols)
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
	net.write_json_to_file('viz', 'json/'+ss+'.json', 'indent')

def make_clustergram_on_features(ss):

	for filename in os.listdir(FEAT_PATH):

		if ss not in filename: continue

		net = Network()

		featname = filename.split('_')[-1].replace('.tsv','')
		df = pd.read_table(os.path.join(FEAT_PATH, filename), index_col=0)

		df.index = [ tuple(['Ligand: '+x]) for x in df.index.values ]
		df.columns = [ tuple(['ECMp: '+x]) for x in df.columns.values ]

		net.load_df(df)
		net.clip(-10,10)
		net.make_clust(dist_type='cos', views=[], sim_mat=False)
		net.write_json_to_file('viz', 'json/'+ss+'_'+featname+'.json', 'indent')

def main():
	for ss in ['SS1','SS2','SS3']:
		make_clustergram_matrix(ss)
		make_clustergram_on_features(ss)


if __name__ == '__main__':
	main()

