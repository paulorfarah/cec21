
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

font = {
        'family': 'normal',
        'size': 16}
matplotlib.rc('font', **font)

def pizza_labels(pct, allvals):
    absolute = int(pct / 100. * pd.np.sum(allvals))
    return "{:.1f}%".format(pct, absolute)

def plot_refactorigns_distrib(x):
        colors = ['firebrick', 'orangered', 'orange', 'gold', 'cornsilk', 'yellowgreen', 'lightgreen', 'limegreen',
                  'forestgreen']
        fig1, ax1 = plt.subplots()
        ax1.pie(x, labels=x.index, autopct=lambda pct: pizza_labels(pct, x), colors=colors, radius=1.2, pctdistance=0.83)
        plt.savefig('img/distrib.pdf')
        # plt.show()

def plot_donut(x):
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        recipe = x.index
        data = x
        wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)
        bbox_props = dict(boxstyle="square,pad=0.1", fc="w", ec="k", lw=0.5)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")
        for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1) / 2. + p.theta1
                y = pd.np.sin(pd.np.deg2rad(ang))
                x = pd.np.cos(pd.np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(pd.np.sign(x))]
                connectionstyle = "angle,angleA=0,angleB={}".format(ang)
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                ax.annotate(recipe[i], xy=(x, y), xytext=(1.55 * pd.np.sign(x), 1.3 * y),
                            horizontalalignment=horizontalalignment, **kw)
        plt.show()

def get_features_df(fname, features):
        global x
        df = pd.read_csv(fname, sep=',', header=0)
        # Separating out the features
        features_df = df.loc[:, features]  # .values
        # Total sum per column:
        x = features_df.loc['Total', :] = features_df.sum(axis=0)
        # print(features_df.mean())
        return x

def clean_dataset():
        global index
        df = pd.read_csv('data/example.csv', sep=',', header=0)
        index = df.index
        number_of_rows = len(index)
        print(number_of_rows)
        dfu = df.drop_duplicates(subset=['repo', 'commit', 'name_class'])
        index = dfu.index
        number_of_rows = len(index)
        print(number_of_rows)
        dfu.to_csv('data/cleaned.csv')


fname = 'data/results.csv'
features = ['EM', 'ES', 'MMT', 'MMS', 'PDT', 'PDS', 'PUT', 'PUS', 'IM']

# clean_dataset()
x = get_features_df(fname, features)
plot_refactorigns_distrib(x)
# plot_donut(x)