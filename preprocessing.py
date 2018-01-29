import sqlite3
import pandas as pd
import deepdish as dd
import sys
from tqdm import tqdm
import random, math


TRAIN_SPLIT = .70
TEST_SPLIT = 1 - TRAIN_SPLIT
SEED = 42

def map_uid(df):
	uid_set = df['user id'].unique()
	global uid_mapping
	uid_mapping = {}
	for idx,elem in enumerate(tqdm(uid_set)):
		uid_mapping[elem]=idx

def map_sid(df):
	sid_set = df['song id'].unique()
	global sid_mapping
	sid_mapping = {}
	for idx,elem in enumerate(tqdm(sid_set)):
		sid_mapping[elem]=idx

def uid_lookup(row):
	return uid_mapping[row['user id']]

def sid_lookup(row):
	return sid_mapping[row['song id']]

def normalize_uid_sid():
	df = pd.read_csv('train_triplets.txt',delimiter='\t',header=None)
	df.columns = ['user id','song id','play count']
	map_uid(df)
	tqdm.pandas(desc="user id changed")
	df['user id'] = df.progress_apply(uid_lookup,axis=1)

	map_sid(df)
	tqdm.pandas(desc="song id changed")
	df['song id'] = df.progress_apply(sid_lookup,axis=1)

	dd.io.save('normalized_uid_sid.h5',df)
	print('File saved')

def train_test_split(df,seed):
	random.seed(seed)
	size = df['user id'].size
	idxs = [i for i in xrange(size+1)]
	random.shuffle(idxs)


	split_idx = int(math.floor(size*TRAIN_SPLIT))
	print(split_idx,size-split_idx)

x = dd.io.load('normalized_uid_sid.h5')
train_test_split(x,SEED)