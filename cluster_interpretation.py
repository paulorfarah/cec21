import re
import csv
import pandas as pd
import matplotlib.pyplot as plt

def refactorings(lista):
    match = re.match(r"([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)", lista, re.I)
    combinacao = ''
    if match:
        items = match.groups()
        # print(items)

        for i in range(1, 26, 3):
            if int(items[i]) > 0:
                if combinacao != '':
                    combinacao += '-'
                combinacao += items[i-1]
        # print(combinacao)
        if combinacao == '':
            print('ERRO: combinacao vazia!')
            print(lista)
            print('-------')
            print(items)
            exit(0)
    return combinacao

def refactorings_frequency(lista):
    # match = re.match(r"([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)", lista, re.I)
    match = re.match(r"([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)(\-)([a-z]+)([0-9]+)", lista, re.I)
    combinacao = ''
    if match:
        items = match.groups()
        print(items)

        # for i in range(1, 26, 3):
        #     if int(items[i]) > 0:
        #         freq = ''
        #         if int(items[i]) < 18:
        #             freq = 'low'
        #         elif int(items[i]) < 34:
        #             freq = 'medium'
        #         else:
        #             freq = 'high'
        #         if combinacao != '':
        #             combinacao += '-'
        #         combinacao += items[i-1] + '_' + freq
        # # print(combinacao)
        # if combinacao == '':
        #     print('ERRO: combinacao vazia!')
        #     print(lista)
        #     print('-------')
        #     print(items)
        #     exit(0)
    return combinacao

def plot_combinations(csv_file, method_name, clusters):
    # abrir csv
    df = pd.read_csv('cluster_interpretation/' + csv_file, sep=',', header=0)
    # print(df.columns)
    # print('---')
    # print(df['Refactorings'])

    result = df['Refactorings'].str.split('([A-Za-z]+)(\d+)', expand=True)
    # print(result)
    #criar lista de refactorings
    df['combinacao'] = df['Refactorings'].apply(refactorings_frequency)
    print(df['combinacao'])

    for c in range(clusters):
        df0 = df[df.Cluster == c]
        # gapminder_2002 = gapminder[gapminder.year == 2002]
        grouped = df0.groupby(['combinacao'])['quantity'].sum().sort_values()
        # grouped = grouped.sort_values(by=['quantidade'], ascending=[True, False])
        grouped.reset_index().to_csv('cluster_interpretation/freq/' + method_name + str(c) + '.csv')
        # ind = np.arange(len(grouped['quantidade']))
        # plt.set_yticks(y='quantidade' + 0.75 / 2)
        # plt.set_yticklabels(x='combinacao', minor=False)
        # ax = data['region'].value_counts().plot(kind='barh', figsize=(10, 7),
        #                                         color="coral", fontsize=13);
        ax = grouped.plot.barh(color='coral', fontsize=14)
        # for p in ax.patches:
        #     ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        # create a list to collect the plt.patches data
        totals = []

        # find the values and append to list
        for i in ax.patches:
            totals.append(i.get_width())

        # set individual bar lables using above list
        total = sum(totals)


        # set individual bar lables using above list
        for i in ax.patches:
            # get_width pulls left or right; get_y pushes up or down
            ax.text(i.get_width() + .3, i.get_y() + .38, str(round((i.get_width() / total) * 100, 2)) + '%', fontsize=15,
                    color='dimgrey')

        # plt.figure(figsize=(200, 100))
        # plt.show()
        # plt.xlabel('Combined Refactorings', fontsize=12)
        # plt.xscale('log')
        plt.tight_layout()
        plt.savefig('cluster_interpretation/freq/' + method_name + str(c) + '.pdf', dpi=300, format='pdf', bbox_inches='tight')
        plt.close()




def count_compositions(df, algoritm, features):
    print('count compositions')
    clusters_map = {}
    clusters = df[algoritm].sort_values().unique()
    fname = algoritm.replace('\\', '_')
    with open('cluster_interpretation/' + fname + '.csv', mode='w', newline='') as file:
        file_writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
        file_writer.writerow(['Method', 'Cluster', 'Refactorings', 'quantity', 'numberOfAncestors', 'numberOfSubclasses',
                              'numbeOfPrivateAttributes', 'numberOfProtectedAttributes', 'numberOfPublicAttributes',
                              'numberOfAttributes', 'numberOfCoupledClasses', 'cohesion', 'numberOfMethods',
                              'numberPublicMethods', 'numberUserDefinedAttributes', 'numberOfInheritedMethods', 'numberOfPolymorphicMethods'])



        for cluster in clusters:
            features_map = {}
            metrics_map = {}
            x = df.loc[df[algoritm] == cluster].sort_values(by=features).values
            for line in x:
                i = 27
                res = ""
                for f in features:
                    if line[i] != 0:
                        if res != "":
                            res += "-"
                        res += f + str(line[i])
                    i += 1
                if res in features_map:
                    metrics_map[res].append(line[4:17])
                    features_map[res] += 1
                else:
                    features_map[res] = 1
                    metrics_map[res] = [line[4:17]]
            clusters_map[cluster] = [features_map, metrics_map]


            # plot_compositions(features_map, "Cluster_" + str(cluster))
        for cl, j in clusters_map.items():
            for comp in j[1]:
                df_met = pd.DataFrame(j[1][comp])
                avgs = df_met.mean(axis=0)
                res = ['km', cl, comp, j[0][comp]]
                for a in avgs:
                    res.append(a)
                file_writer.writerow(res)


def plot_compositions(res, title):
    d = {k: v for k, v in sorted(res.items(), key=lambda item: item[1]) if v > 50}
    plt.barh(range(len(d)), d.values(), align='center')
    plt.yticks(range(len(d)), d.keys())
    plt.xlabel('frequency', fontsize=14)
    plt.ylabel('refactorings', fontsize=14)
    plt.title(title)
    plt.tight_layout()
    plt.savefig('compositions/' + title + '.pdf', dpi=300, format='pdf',
                bbox_inches='tight')
    plt.close()
    # plt.show()