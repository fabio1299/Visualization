import hydrostats.analyze as ha

def calc_stats(dfData,my_metrics):

    tab=ha.make_table(dfData, my_metrics, remove_neg=True, remove_zero=True)

    if len(my_metrics)==1:
        return tab.iloc[[0]][tab.columns[0]][0]
    else:
        return tab


