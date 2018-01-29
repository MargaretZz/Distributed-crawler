#!--encoding=utf-8

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans

def loadData():
    f = open('data_jieba.txt','r')
    data = []
    last = None
    for line in f.readlines():
        if 'MyFlag' in line:
            if last:
                data.append(last)
            last = line
        else:
            last += line
    if last:
        data.append(last)
    f.close()
    return data

def transform(dataset,n_features=1000):
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2,use_idf=True)
    X = vectorizer.fit_transform(dataset)
    return X,vectorizer

def train(X,vectorizer,true_k=10):

    km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)    
  
    print("Top terms per cluster:")
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    print (vectorizer.get_stop_words())
    for i in range(true_k):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()
    result = list(km.predict(X))
    print ('Cluster distribution:')
    print (dict([(i, result.count(i)) for i in result]))
    return -km.score(X)

    
def print_cluster():
    dataset = loadData()
    X,vectorizer = transform(dataset,n_features=400)
    score = train(X,vectorizer,true_k=10)/len(dataset)
    print(score)

if __name__ == '__main__':
    print_cluster()