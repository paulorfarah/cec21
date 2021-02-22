from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from yellowbrick.cluster import KElbowVisualizer

def elbow(fname, x, model, metrica):
    print(x)
    fname = 'elbow/elbow_' + fname + '.pdf'
    # Instantiate the clustering model and visualizer
    visualizer = KElbowVisualizer(model, k=(2, 15), metric=metrica, timings=False)
    visualizer.fit(x)        # Fit the data to the visualizer
    # visualizer.show()        # Finalize and render the figure
    # plt.show()
    plt.xticks(fontsize=20)
    plt.xlabel('Number of clusters k', fontsize=20)
    plt.ylabel('Total Within Sum of Square', fontsize=20)
    plt.savefig(fname)
    plt.close()

def calculate_centroids(x):
    # elbow methods
    for m in ['distortion']: #, 'silhouette', 'calinski_harabasz']:
        elbow('KM_' + m, x, KMeans(), m)