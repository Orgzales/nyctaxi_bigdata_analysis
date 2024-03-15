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
