import glob
import random
import json
import bz2
import numpy as np
import rich.progress
import faiss


num_words_to_keep = 10000

files = list(glob.glob('/data/htrc/**/*.json.bz2', recursive=True))
random.shuffle(files)
print(files[:10])
subset_files = files[:20]

word_counts = {}
for file in subset_files:
	print(file)
	with bz2.open(file, 'rt') as f:
		data = json.load(f)
		for page in data['features']['pages']:
			if 'body' in page and page['body'] is not None and 'tokenPosCount' in page['body'] and page['body']['tokenPosCount'] is not None:
				for word in page['body']['tokenPosCount']:
					word_counts[word] = word_counts.get(word, 0) + 1

sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
print(sorted_word_counts[:1000])



# among this random set of docs, make a list of the most frequent 10k words

most_freq_words = []
for word_pair in sorted_word_counts[:num_words_to_keep]:
	most_freq_words.append(word_pair[0])
most_freq_words_idxs = dict(zip(most_freq_words, range(len(most_freq_words))))
print(most_freq_words_idxs)

# Now for each document in the glob (start with just 50 or so)
# Mae a vector representing the % of occurances of each word among the top 10K
# (And if that word doesn't occur, it's 0.0)

#for file in files[:50]:
#	print(file)
#	docvec = np.zeros(len(most_freq_words))
#	with bz2.open(file, 'rt') as f:
#		data = json.load(f)
#		for page in data['features']['pages']:
#			if 'body' in page and page['body'] is not None and 'tokenPosCount' in page['body'] and page['body']['tokenPosCount'] is not None:
#				for word in page['body']['tokenPosCount']:
#					if word in most_freq_words_idxs:
#						docvec[most_freq_words_idxs[word]] = 1
#	print(docvec)


num_to_process = len(files)

faiss_index = faiss.IndexFlatL2(len(most_freq_words))
#docvecs = np.zeros((num_to_process, len(most_freq_words)))
files_to_process = random.sample(files, num_to_process)
with rich.progress.Progress() as progress:
	task = progress.add_task("Processing files..", total=num_to_process)
	for idx, file in enumerate(files[:num_to_process]):
		print(file)
		docvec = np.zeros(len(most_freq_words))
		with bz2.open(file, 'rt') as f:
			data = json.load(f)
			for page in data['features']['pages']:
				if 'body' in page and page['body'] is not None and 'tokenPosCount' in page['body'] and page['body']['tokenPosCount'] is not None:
					for word in page['body']['tokenPosCount']:
						if word in most_freq_words_idxs:
							docvecs[most_freq_words_idxs[word]] = 1
		faiss_index.add(np.array([docvec]))
		progress.update[date(task,advance=1)

print(docvecs)
#np.save('docvecs.npy', docvecs)
faiss.write_index(faiss_index, 'index.faiss')

