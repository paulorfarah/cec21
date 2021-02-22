import pandas as pd
from dimreduction import pca
from elbow_method import calculate_centroids
from cluster_interpretation import count_compositions, plot_combinations

def main():
    title = 'KMeans'
    features = ['EM', 'ES', 'MMT', 'MMS', 'PDT', 'PDS', 'PUT', 'PUS', 'IM']

    # load dataset into Pandas DataFrame
    df = pd.read_csv('data/results.csv', sep=',', header=0)

    # Separating out the features
    x = df.loc[:, features].values

    # elbow method
    calculate_centroids(x)

    kmeans_7_10 = 37 #cluster column numbers in results.csv
    for i in [kmeans_7_10]:
        algoritm = df.columns[[i]].tolist()[0].replace('\\\\', '\\')
        fname = algoritm.replace('\\', '_')
        pca(fname, df, features, algoritm, title)
        count_compositions(df, algoritm, features)

        csv_files = ['50_kmeans_7_10.csv']
        clusters = [7]
        method_names = ['km']

        for csv_file, cluster, method in zip(csv_files, clusters, method_names):
            plot_combinations(csv_file, method, cluster)


if __name__ == "__main__":
    main()


