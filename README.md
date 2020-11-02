## Clustering sequences using similarity measures in Python

Implementation of k-means clustering with the following similarity measures to choose from when evaluating the similarity of given sequences:
- Euclidean distance
- Damerau-Levenshtein edit distance
- Dynamic Time Warping.


### 1. Input
The expected input format are sequences being represented in string format, i.e., a csv file where each row represents a sequence and each column represents a singular item of a sequence of items.

| col1 | col2 | col3 | ... |
|------|------|------|-----|
| glass | bowl | spoon | ... |

### 2. Implementation
#### 2.1 K-means clustering
K-means sets initial (random) centroids, calculates their distance to all the datapoints and assigns each datapoint to the nearest cluster. Centroids are then updated in relation to the datapoints assigned to the respective cluster (minimum distance to all datapoints) and compared to the old centroid values - the centroids keep updating until the distance between all old and new centroids is zero (i.e. none of them has changed in the previous update iteration).
In order to be able to use different distance measures with k-means, k-means gets the preferred distance function as a parameter (dist_fun) as well as the number of clusters (k) and the preprocessed data (data).

#### 2.2 Damerau-Levenshtein edit distance
Damerau-Levenshtein distance calculates the distance between two strings by calculating the steps needed to transform one string into the other and returns this value as distance. In order to use Damerau-Levenshtein distance on numbers, there's a wrapper function (levenshtein_on_numbers) that converts strings to numbers so it is compatible with k-means, which works number based 
(for calculating means). For using Damerau-Levenshtein distance, each datapoint (string in list) is first converted into a letter before each dataset (list in list) is joined to a string and compared to the other datasets.

#### 2.3 Dynamic Time Warping
Takes difference sequence lenghts and non-linear similarities into account.

#### 2.4 Evaluation methods
##### 2.4.1 Cluster counter
In order to find optimal k, the algorithm is run repeatedly with a larger than expected number of clusters. After each iteration the size of the clusters is inspected and all non-empty clusters are counted. The output is a vector containing the number of non-empty clusters for a given k. E.g. [7, 69, 21, 2, 1] tells us that in 100 runs with k=5, 7 times only one cluster was filled with data, 69 times 2 clusters where filled with data, etc.

How to use:

```python
number_of_clusters = [0,0,0,0,0]
for i in range(100):
	clusters, centroids = k_means(5, data, dtw_distance)
	count = 0
	for cluster in clusters:
		if len(cluster) > 0:
			count = count + 1
	number_of_clusters[count-1] = number_of_clusters[count-1] + 1
print(number_of_clusters)
```

##### 2.4.2 Elbow method for optimal number of clusters (k)
Elbow method looks at the percentage of variance explained as a function of the number of clusters. The optimal number of clusters should be chosen so that adding another cluster doesn't result in much better modeling of the data (indicated by the angle in the graph).

How to use:
```python
max_len = max_dim(data)
for dataset in data:
  if len(dataset) < max_len:
		for i in range(max_len - len(dataset)):
			dataset.append(0)	
sum_dists = []
for i in range(1,16):
	clusters, centroids = k_means(i, data, euclidean_distance)
sum_dist = []
for i in range(len(clusters)):
	cluster = clusters[i]
	centroid = centroids[i]
	for j in range(len(cluster)):
		sum_dist.append((euclidean_distance(cluster[j], centroid))**2)
	sum_dists.append(min(sum_dist))

plt.plot(range(1,16), sum_dists, 'bx-')
plt.xlabel('k')
plt.ylabel('sum dist')
plt.title('Elbow Method for optimal k')
plt.show() 
```


### 3. Usage examples

```python
# K-means with Damerau-Levenshtein distance
    data = read_data('sequences_str.csv')
    datapoint2num, num2datapoint = create_dicts(data)
    convert_with_dictionary(data, datapoint2num)
    clusters, centroids = k_means(5, data, levenshtein_on_numbers)
    for i in range(5):
        convert_with_dictionary(clusters[i], num2datapoint)
        print('====================================')
        print('Cluster ' + str(i) + ': ')
        for j in range(len(clusters[i])):
            print(clusters[i][j])
        plot_data(clusters[i])
```
```python
# K-means with dynamic time warping
    data = read_data('sequences_str.csv')
    datapoint2num, num2datapoint = create_dicts(data)
    convert_with_dictionary(data, datapoint2num)
    clusters, centroids = k_means(5, data, dtw_distance)
    for i in range(5):
        convert_with_dictionary(clusters[i], num2datapoint)
        print('====================================')
        print('Cluster ' + str(i) + ': ')
        for j in range(len(clusters[i])):
            print(clusters[i][j])
        plot_data(clusters[i])
    print(centroids)
```
