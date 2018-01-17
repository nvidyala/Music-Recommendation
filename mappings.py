import sqlite3
import csv
import deepdish as dd
from progressbar import ProgressBar

def get_trackids():
	with open("train_triplets.txt") as fd:
		fileRead = csv.reader(fd, delimiter="\t")
		track_ids = {row[1]:"" for row in fileRead}
	return track_ids

def all_song_names(track_ids):
	conn = sqlite3.connect('track_metadata.db')
	for key,_ in track_ids.items():
		query = "SELECT title FROM songs WHERE song_id='%s'" % (key)
		cursor = conn.execute(query)
		for row in cursor:
			print(row)
			track_ids[key] = row

#-------------------- Only run first time

# track_ids = get_trackids()
# dd.io.save('track_ids.h5',track_ids)

#-------------------- For second time onwards

# track_ids = dd.io.load('track_ids.h5')
# sn_tr_mapping = all_song_names(track_ids)
# dd.io.save('sntr_mappings.h5',sn_tr_mapping)
# print('Completed')


#-------------------- For direct lookup

def name_lookup(song_id):
	conn = sqlite3.connect('track_metadata.db')
	cursor = conn.execute("SELECT title FROM songs WHERE song_id='%s'" % (song_id))
	
	for row in cursor:
		print(row)