import csv
import matplotlib.pyplot as plt
import math
import random
import string

def read_data(filename):
    with open(filename, 'rt') as csvfile:
        data = list(csv.reader(csvfile))
        data.pop(0)
        return data

def max_dim(data, use_chars=False):
    ''' get maximum number of dimensions '''
    max = 0
    
    if use_chars:
        for dataset in data:
            if len(dataset[0]) > max:
                max = len(dataset[0])
    else:
        for dataset in data:
            if len(dataset) > max:
                max = len(dataset)
    return max


def convert_with_dictionary(data, dictionary):
    ''' convert data: num2word or word2num '''
    for dataset in data:
        for i in range(len(dataset)):
            dataset[i] = dictionary[dataset[i]]


def get_unique_words(data):
    ''' Create list of unique words '''
    unique_words = set()    
    for datasets in data:
        for datapoint in datasets:
            unique_words.add(datapoint)
    
    return list(unique_words)    


def create_dicts(data, use_chars=False):   
    ''' create dictionarys for conversion (num<->datapoint or char<->datapoint) '''
    unique_words = get_unique_words(data)

    if use_chars == True:
        datapoint2char = {}
        char2datapoint = {}
        char = string.ascii_lowercase[0]
        
        for datapoint in unique_words:
            datapoint2char[datapoint] = char
            char2datapoint[char] = datapoint
            char = chr(ord(char) + 1) 
        return datapoint2char, char2datapoint
    
    else:
        datapoint2num = {}
        num2datapoint = {}
        num = 97
        
        for datapoint in unique_words:
            datapoint2num[datapoint] = num
            num2datapoint[num] = datapoint
            num = num+1
        return datapoint2num, num2datapoint


def join_chars(data):
    ''' join chars to str '''
    for i in range(len(data)):
        data[i] = [''.join(data[i])]
    return data


def split_chars(data):
    ''' split str to chars '''
    for i in range(len(data)):
        data[i] = list(data[i])
    return data


def plot_data(data):    
    index = 0
    for dataset in data:
        plt.plot(dataset)
        index = index+1
    plt.legend()
    plt.show()


def euclidean_distance(a, b):
    ''' euclidean distance '''
    dist = 0
    if len(a) < len(b):
        a,b = b,a
    for i in range(len(a)):
        if i < len(b):
            dist = dist + (a[i] - b[i]) ** 2
        else:
            dist = dist + a[i]**2
    return math.sqrt(dist)

 
def levenshtein_on_numbers(dataset1, dataset2):
    ''' damerau-levenshtein distance on numbers (convert strings) '''
    datapoint2char, char2datapoint = create_dicts([dataset1, dataset2], use_chars=True)        
    convert_with_dictionary([dataset1], datapoint2char)
    convert_with_dictionary([dataset2], datapoint2char)
    join_chars([dataset1])
    join_chars([dataset2])
        
    distance = d_levenshtein_distance(dataset1, dataset2)
        
    split_chars([dataset1])
    split_chars([dataset2])
        
    convert_with_dictionary([dataset1], char2datapoint)
    convert_with_dictionary([dataset2], char2datapoint)
        
    return distance
               

def d_levenshtein_distance(str1, str2):
    ''' damerau-levenshtein distance '''
    d = {}
    for i in range(len(str1) + 1):
        d[(i,0)] = i
    for j in range(len(str2) + 1):
        d[(0,j)] = j
    
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i-1] == str2[j-1]:
                subst_or_equal = d[(i-1, j-1)] + 0
            else:
                subst_or_equal = d[(i-1, j-1)] + 1
            
            deletion = d[(i-1,j)] + 1
            insertion = d[(i,j-1)] + 1
            
            if (i >= 2 and j >= 2) and (str1[i-1] == str2[j-2] and str1[i-2] == str2[j-1]):
                switch = d[(i-2,j-2)] + 1
                d[(i,j)] = min(subst_or_equal, deletion, insertion, switch)
            else:
                d[(i,j)] = min(subst_or_equal, deletion, insertion)
    
    return d[(len(str1), len(str2))]


def dtw_distance(dataset1, dataset2):
    ''' dynamic time warping '''
    dtw = {}
    for i in range(len(dataset1)):
        dtw[(i,-1)] = float('inf')
    for i in range(len(dataset2)):
        dtw[(-1,i)] = float('inf')
        
    dtw[(-1,-1)] = 0
    
    for i in range(len(dataset1)):
        for j in range(len(dataset2)):
            dist = (dataset1[i] - dataset2[j])**2
            dtw[(i,j)] = dist + min(dtw[(i-1,j)], dtw[(i,j-1)], dtw[(i-1,j-1)])
            
    return math.sqrt(dtw[len(dataset1)-1, len(dataset2)-1])


def k_means(k, data, dist_fun):
    ''' k-means with number of clusters and preferred distance function '''
    centroids = []
    old_centroids = []
    cluster_for_dataset = []
    clusters = [[] for i in range(k)]
    delta_centroid_sum = 0
    dataset_dim = max_dim(data)
    min_value = 97
    max_value = max([datapoint for dataset in data for datapoint in dataset])
    zeros = [0 for i in range(dataset_dim)]
    
    for cluster in range(k):
        randoms = [random.randint(min_value, max_value) for i in range(dataset_dim)]
        old_centroids.append(zeros)
        centroids.append(randoms)
        delta_centroid_sum = delta_centroid_sum + dist_fun(zeros, randoms)
    
    while delta_centroid_sum != 0:
        for dataset in data:
            cluster_distances = []
            for cluster in range(k):
                cluster_distances.append(dist_fun(dataset, centroids[cluster]))
            cluster_for_dataset.append(cluster_distances.index(min(cluster_distances)))
        delta_centroid_sum = 0
        
        for cluster in range(k):
            cluster_members = []
            for i in range(len(data)):
                if cluster == cluster_for_dataset[i]:
                    cluster_members.append(data[i])
    
            old_centroids[cluster] = centroids[cluster]
            datapoint_means = [0 for i in range(dataset_dim)]
            cluster_member_count = len(cluster_members)
            
            for dataset in cluster_members:
                for i in range(len(dataset)):
                    datapoint_means[i] = datapoint_means[i] + dataset[i]/cluster_member_count
           
            centroids[cluster] = datapoint_means
            clusters[cluster] = cluster_members
            delta_centroid_sum = delta_centroid_sum + dist_fun(old_centroids[cluster], centroids[cluster])
        
    return clusters, centroids


    
    
def main():
### find optimal k, elbow method
#    data = read_data('sequences_str.csv')
#    datapoint2num, num2datapoint = create_dicts(data)
#    convert_with_dictionary(data, datapoint2num)    
#    max_len = max_dim(data)
#    
#    for dataset in data:
#        if len(dataset) < max_len:
#            for i in range(max_len - len(dataset)):
#                dataset.append(0)
#                
#    sum_dists = []
#    for i in range(1,16):
#        clusters, centroids = k_means(i, data, dtw_distance)
#        
#        sum_dist = []                                                                                                                                                                                                                                                                 
#        for i in range(len(clusters)):
#            cluster = clusters[i]
#            centroid = centroids[i]
#            
#            for j in range(len(cluster)):
#                sum_dist.append((euclidean_distance(cluster[j], centroid))**2)
#        sum_dists.append(min(sum_dist))
#    
#    plt.plot(range(1,16), sum_dists, 'bx-')
#    plt.xlabel('k')
#    plt.ylabel('sum dist')
#    plt.title('Elbow Method for optimal k')
#    plt.show()    

    
    
### find optimal k, cluster counter
#    data = read_data('sequences_str.csv')
#    datapoint2num, num2datapoint = create_dicts(data)
#    convert_with_dictionary(data, datapoint2num) 
#    number_of_clusters = [0,0,0,0,0]
#    for i in range(100):
#        clusters, centroids = k_means(5, data, levenshtein_on_numbers)
#        count = 0
#        for cluster in clusters:
#            if len(cluster) > 0:
#                count = count + 1
#        number_of_clusters[count-1] = number_of_clusters[count-1] + 1         
#    print(number_of_clusters)
    
    
### plot
#    data = read_data('sequences_str.csv')
#    datapoint2num, num2datapoint = create_dicts(data)
#    convert_with_dictionary(data, datapoint2num)
#    plot_data(data)
    
    
### k-means with dtw on numbers
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
 
    
### levenshtein on strings
#    data = read_data('sequences_str.csv')
##    data = [dataset[2:] for dataset in data]
#    datapoint2num, num2datapoint = create_dicts(data)
#    convert_with_dictionary(data, datapoint2num)
#    clusters, centroids = k_means(5, data, levenshtein_on_numbers)
#    for i in range(5):
#        convert_with_dictionary(clusters[i], num2datapoint)
#        print('====================================')
#        print('Cluster ' + str(i) + ': ')
#        for j in range(len(clusters[i])):
#            print(clusters[i][j])
#        plot_data(clusters[i])

    
### k_means with euclideans on numbers  
#    data = read_data('sequences_str.csv')
#    datapoint2num, num2datapoint = create_dicts(data)
#    convert_with_dictionary(data, datapoint2num)
#    clusters, centroids = k_means(5, data, euclidean_distance)
#    for i in range(5):
#        convert_with_dictionary(clusters[i], num2datapoint)
#        print('====================================')
#        print('Cluster ' + str(i) + ': ')
#        for j in range(len(clusters[i])):
#            print(clusters[i][j])
#        plot_data(clusters[i])  
    


main()
