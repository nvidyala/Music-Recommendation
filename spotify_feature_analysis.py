from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
from scipy.spatial.distance import cityblock
import sqlite3
from pprint import pprint
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from numpy import array

FEATURE_SET = ['energy','liveness','tempo','speechiness','acousticness','instrumentalness','danceability','key','loudness','valence','time_signature']
CLIENT_ID = '83798b6bb93246869a16310ee165075b'
CLIENT_SECRET = 'ad1dc4ad54174ed2afbbd098cf2db64a'
ARTISTS = ['Eminem','Kanye West','Nickelback']
SONGS = [[] for i in range(len(ARTISTS))]
EXTRACTED_FEATURES = []
TRACK_IDS = [[] for i in range(len(ARTISTS))]


def taste_profile_to_spotify(ARTISTS):
	conn = sqlite3.connect('track_metadata.db')

	for idx,artist in enumerate(ARTISTS):

		# query = "SELECT artist_name FROM songs WHERE track_id='%s'" % tid
		# cursor = conn.execute(query)
		# for row in cursor:
		# 	artist_name = row
		# print(artist_name)

		query = "SELECT DISTINCT title FROM songs WHERE artist_name='%s' LIMIT 10" % artist
		cursor = conn.execute(query)
		for row in cursor:
			try: 
				result = sp.search(row)
				TRACK_IDS[idx].append(result['tracks']['items'][0]['id'])
				SONGS[idx].append(row)
			except IndexError, e:
				continue

	return TRACK_IDS

def extract_audio_features(TRACK_IDS):
	artist_features = []
	for artist in TRACK_IDS:
		features = sp.audio_features(artist)	
		for feature in features:
			result = []
			for metric in feature: 
				if metric in FEATURE_SET:	
					result.append(feature[metric])
			print(result)
			artist_features.append(result)
		print('\n\n')

	return array(artist_features)
	

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

TRACK_IDS = taste_profile_to_spotify(ARTISTS)
EXTRACTED_FEATURES = extract_audio_features(TRACK_IDS)
print(EXTRACTED_FEATURES)
#sp_artist_name = result['tracks']['items'][0]['album']['artists'][0]['name']

pca = PCA(n_components=2)
X_r = pca.fit(EXTRACTED_FEATURES).transform(EXTRACTED_FEATURES)
target_names = array(['em','ye','nb'])
colors = ['navy', 'turquoise', 'darkorange']
y = array([0]*10+[1]*10+[2]*6)
for color, i, target_name in zip(colors, [0, 1, 2], target_names):
    plt.scatter(X_r[y == i, 0], X_r[y == i, 1], color=color, alpha=.8, lw=2,
                label=target_name)
plt.legend(loc='best', shadow=False, scatterpoints=1)

plt.title('PCA of IRIS dataset')
plt.show()