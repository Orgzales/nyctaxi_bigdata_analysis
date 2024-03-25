import pandas as pd

df = pd.read_csv('/data/iris/iris.csv')

print(df.head())

#cluster

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

X = df[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]

kmeans = KMeans(n_clusters = 3)
kmeans.fit(X)
df['cluster'] = kmeans.predict(X)

print(df.head())

#plot

colors = ['red', 'green', 'blue']
for i in range(3):
	plt.scatter(df[df['cluster'] == i]['sepal.length'], df[df['cluster'] == i]['sepal.width'], c=colors[i])
plt.savefig('iris-clusters.png')

#t-sne
plt.clf()

from sklearn.manifold import TSNE
import seaborn as sns
tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)
df['tsne1'] = X_tsne[:, 0]
df['tsne2'] = X_tsne[:, 1]
sns.scatterplot(x='tsne1', y='tsne2', hue='cluster', data=df)
plt.savefig('iris-tsne.png')

