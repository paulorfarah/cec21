import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

def pca(fname, df, features, algoritmo, titulo):
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:, [algoritmo]].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=principalComponents
                               , columns=['principal component 1', 'principal component 2'])

    finalDf = pd.concat([principalDf, df[[algoritmo]]], axis=1)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title(titulo, fontsize=20)
    targets = [0, 1, 2, 3, 4, 5, 6]
    colors = ['firebrick', 'orangered', 'orange', 'gold', 'cornsilk', 'yellowgreen', 'forestgreen']
    for target, color in zip(targets, colors):
        indicesToKeep = finalDf[algoritmo] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
                   , finalDf.loc[indicesToKeep, 'principal component 2']
                   , c=color
                   , s=4)
    ax.legend(targets)
    ax.grid()
    plt.savefig('dimreduction/pca/' + fname + '.pdf')








