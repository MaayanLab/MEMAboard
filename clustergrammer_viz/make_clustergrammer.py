'''
Python 2.7
The clustergrammer python module can be installed using pip:
pip install clustergrammer

or by getting the code from the repo:
https://github.com/MaayanLab/clustergrammer-py
'''

# necessary for scipy hierarchy clustering
import sys
sys.setrecursionlimit(10000)

from clustergrammer import Network
net = Network()

# load matrix tsv file
net.load_file('txt/MCF10A_SS1_matrix.txt')

# optional filtering and normalization
##########################################
# net.filter_sum('row', threshold=20)
# net.normalize(axis='col', norm_type='zscore', keep_orig=True)
# net.filter_N_top('row', 250, rank_type='sum')
# net.filter_threshold('row', threshold=3.0, num_occur=4)
# net.swap_nan_for_zero()

net.make_clust(dist_type='cos',views=[] , sim_mat=False)

# write jsons for front-end visualizations
net.write_json_to_file('viz', 'json/mult_view.json', 'indent')
