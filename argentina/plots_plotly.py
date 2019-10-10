import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff

from datetime import datetime
from .hydro_stats import calc_stats
from hydrostats.metrics import *
import pandas as pd

#import hydrostats as hs
#import hydrostats.data as hd

config = {'showLink': False,
          'modeBarButtonsToRemove': ['sendDataToCloud'],
          'displaylogo': False
          }

models = {
    'obs': ['Observed', 'Observed'],
    'terraclimate_ro': ['TerraClimate (Acc. Runoff)', 'TerraClimate'],
    'terraclimate_wbm': ['TerraClimate (WBM model)', 'TerraClimate'],
    'crutsv401': ['CRU TS', 'CRU TS Ver. 4.01'],
    'gpccv7': ['GPCC', 'GPCC Ver. 7']
}

def TimeseriesAllModels(dfDischarge,code,name):

    maxDischarge = max(dfDischarge[list(models.keys())].max())
    maxDischarge = maxDischarge + maxDischarge * 0.05

    maxTime=dfDischarge.index.max()

    trace1 = go.Scatter(x=dfDischarge.index, y=dfDischarge['obs'], marker={'color': 'red', 'symbol': 104, 'size': 1},
                        mode='lines', name='Observed')
    trace2 = go.Scatter(x=dfDischarge.index, y=dfDischarge['terraclimate_ro'],
                        marker={'color': 'blue', 'symbol': 103, 'size': 1},
                        mode='lines', name='TerraClimate (runoff accumulation)')
    trace3 = go.Scatter(x=dfDischarge.index, y=dfDischarge['terraclimate_wbm'],
                        marker={'color': 'green', 'symbol': 102, 'size': 1},
                        mode='lines', name='TerraClimate (WBM model)')
    trace4 = go.Scatter(x=dfDischarge.index, y=dfDischarge['crutsv401'],
                        marker={'color': 'yellow', 'symbol': 101, 'size': 1},
                        mode='lines', name='CRU TS Ver. 4.01')
    trace5 = go.Scatter(x=dfDischarge.index, y=dfDischarge['gpccv7'],
                        marker={'color': 'cyan', 'symbol': 100, 'size': 1},
                        mode='lines', name='GPCC Ver. 7')
    data = [trace1, trace5, trace4, trace2, trace3]
#    layout = go.Layout(title="Discharge timeseries",
#                       xaxis={'title': 'Years, Months',
#                              'range':[datetime(year=1900,month=1,day=1), maxTime]},
#                       yaxis={'title': 'Discharge m3/s',
#                              'range':[0, maxDischarge]}
#                       )
    layout = dict(
        title="Discharge timeseries",
        xaxis=dict(
            range=[datetime(year=1900, month=1, day=1), maxTime],
            rangeselector=dict(
                buttons=list([
                    dict(count=5,
                         label='5y',
                         step='year',
                         stepmode='todate'),
                    dict(count=10,
                         label='10y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        ),
        yaxis=dict(
            title='Discharge m3/s',
            range=[0, maxDischarge]
        )
    )
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', config=config)
    return div

def TimeseriesAnnualAllModels(dfInput,code,name):

    dfDischarge=dfInput.groupby(dfInput.index.year).agg('mean')

    maxDischarge = max(dfDischarge[list(models.keys())].max())
    maxDischarge = maxDischarge + maxDischarge * 0.05

    maxTime=dfDischarge.index.max()



    trace1 = go.Scatter(x=dfDischarge.index, y=dfDischarge['obs'], marker={'color': 'red', 'symbol': 104, 'size': 1},
                        mode='lines', name='Observed')
    trace2 = go.Scatter(x=dfDischarge.index, y=dfDischarge['terraclimate_ro'],
                        marker={'color': 'blue', 'symbol': 103, 'size': 1},
                        mode='lines', name='TerraClimate (runoff accumulation)')
    trace3 = go.Scatter(x=dfDischarge.index, y=dfDischarge['terraclimate_wbm'],
                        marker={'color': 'green', 'symbol': 102, 'size': 1},
                        mode='lines', name='TerraClimate (WBM model)')
    trace4 = go.Scatter(x=dfDischarge.index, y=dfDischarge['crutsv401'],
                        marker={'color': 'yellow', 'symbol': 101, 'size': 1},
                        mode='lines', name='CRU TS Ver. 4.01')
    trace5 = go.Scatter(x=dfDischarge.index, y=dfDischarge['gpccv7'],
                        marker={'color': 'cyan', 'symbol': 100, 'size': 1},
                        mode='lines', name='GPCC Ver. 7')
    data = [trace1, trace5, trace4, trace2, trace3]
#    layout = go.Layout(title="Discharge timeseries",
#                       xaxis={'title': 'Years, Months',
#                              'range':[datetime(year=1900,month=1,day=1), maxTime]},
#                       yaxis={'title': 'Discharge m3/s',
#                              'range':[0, maxDischarge]}
#                       )
    layout = dict(
        title="Discharge - annual averages",
        xaxis=dict(
            range=[datetime(year=1900, month=1, day=1), maxTime],
            rangeselector=dict(
                buttons=list([
                    dict(count=5,
                         label='5y',
                         step='year',
                         stepmode='todate'),
                    dict(count=10,
                         label='10y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            #type='date'
        ),
        yaxis=dict(
            title='Discharge m3/s',
            range=[0, maxDischarge]
        )
    )
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', config=config)
    return div

def TimeseriesMonthlyAllModels(dfInput,code,name):

    labels = ['Jan', 'Feb', 'Mar', 'Apr','May', 'Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    tickvals = [1,2,3,4,5,6,7,8,9,10,11,12]

    dfTmp=dfInput.loc[dfInput['obs'].notnull()]
    dfDischarge=dfTmp.groupby(dfTmp.index.month).agg('mean')

    maxDischarge = max(dfDischarge[list(models.keys())].max())
    maxDischarge = maxDischarge + maxDischarge * 0.05

    maxTime=dfDischarge.index.max()

    trace1 = go.Scatter(x=dfDischarge.index, y=dfDischarge['obs'], marker={'color': 'red', 'symbol': 104, 'size': 1},
                        mode='lines', name='Observed')
    trace2 = go.Scatter(x=dfDischarge.index, y=dfDischarge['terraclimate_ro'],
                        marker={'color': 'blue', 'symbol': 103, 'size': 1},
                        mode='lines', name='TerraClimate (runoff accumulation)')
    trace3 = go.Scatter(x=dfDischarge.index, y=dfDischarge['terraclimate_wbm'],
                        marker={'color': 'green', 'symbol': 102, 'size': 1},
                        mode='lines', name='TerraClimate (WBM model)')
    trace4 = go.Scatter(x=dfDischarge.index, y=dfDischarge['crutsv401'],
                        marker={'color': 'yellow', 'symbol': 101, 'size': 1},
                        mode='lines', name='CRU TS Ver. 4.01')
    trace5 = go.Scatter(x=dfDischarge.index, y=dfDischarge['gpccv7'],
                        marker={'color': 'cyan', 'symbol': 100, 'size': 1},
                        mode='lines', name='GPCC Ver. 7')
    data = [trace1, trace5, trace4, trace2, trace3]
    layout = go.Layout(title="Discharge - monthly averages",
                       xaxis={'ticktext':labels,
                              'tickvals':tickvals},
                       yaxis={'title': 'Discharge m3/s',
                              'range':[0, maxDischarge]}
                       )
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', config=config)
    return div

def BoxplotMonthlyAllModels(dfInput,code,name):

    labels = ['Jan', 'Feb', 'Mar', 'Apr','May', 'Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    tickvals = [1,2,3,4,5,6,7,8,9,10,11,12]

    dfDischarge=dfInput.loc[dfInput['obs'].notnull()]
    #dfDischarge=dfTmp.groupby(dfTmp.index.month).agg('mean')

    maxDischarge = max(dfDischarge[list(models.keys())].max())
    maxDischarge = maxDischarge + maxDischarge * 0.05

    maxTime=dfDischarge.index.max()

    trace1 = go.Box(y=dfDischarge.index.month, x=dfDischarge['obs'],
                        marker={'color': 'red', 'symbol': 104, 'size': 1},
                        orientation= 'h',boxpoints = False, name='Observed')
    trace2 = go.Box(y=dfDischarge.index.month, x=dfDischarge['terraclimate_ro'],
                        marker={'color': 'blue', 'symbol': 103, 'size': 1},
                        orientation= 'h',boxpoints = False, name='TerraClimate (runoff accumulation)')
    trace3 = go.Box(y=dfDischarge.index.month, x=dfDischarge['terraclimate_wbm'],
                        marker={'color': 'green', 'symbol': 102, 'size': 1},
                        orientation= 'h',boxpoints = False, name='TerraClimate (WBM model)')
    trace4 = go.Box(y=dfDischarge.index.month, x=dfDischarge['crutsv401'],
                        marker={'color': 'yellow', 'symbol': 101, 'size': 1},
                        orientation= 'h',boxpoints = False, name='CRU TS Ver. 4.01')
    trace5 = go.Box(y=dfDischarge.index.month, x=dfDischarge['gpccv7'],
                        marker={'color': 'cyan', 'symbol': 100, 'size': 1},
                        orientation= 'h',boxpoints = False, name='GPCC Ver. 7')
    data = [trace1, trace5, trace4, trace2, trace3]
    layout = go.Layout(title="Discharge - monthly averages",
                       yaxis={'ticktext':labels,
                              'tickvals':tickvals},
                       xaxis={'title': 'Discharge m3/s'},
                       boxmode='group',
                       height=800
                       )
#    layout = dict(
#        title="Discharge - monthly averages",
#        xaxis=dict(
#            tickformat='%b'
#        )
#    )
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', config=config)
    return div

def ObsVsModeled(dfDischarge,model,code,name):

    maxDischarge = max(dfDischarge[list(models.keys())].max())
    maxDischarge = maxDischarge + maxDischarge * 0.05

    trace1 = go.Scatter(x=dfDischarge['obs'], y=dfDischarge[model],
                        text=dfDischarge.index,
                        marker={'color': 'red', 'symbol': 104, 'size': 5},
                        mode='markers',
                        name='Observed vs {}'.format(models[model][0])
                        )
    trace2 = go.Scatter(x=[0,maxDischarge],y=[0,maxDischarge],
                        mode='lines',
                        line=dict(
                            color=('rgb(205, 205, 205)'),
                            width=2,
                            dash='dot')
                        )

    table_trace1=StasData(dfDischarge[[model,'obs']])

    data = [table_trace1,trace2,trace1]
    layout = go.Layout(title='Observed vs {}'.format(models[model][0]),
                       #xaxis={'title': 'Observed<br><small>m3/s</small>','range':[0, maxDischarge],'domain':[0,0.50], 'anchor':'y','showticklabels':False},
                       #yaxis={'title': models[model][1] + '<br><small>m3/s</small>','range':[0, maxDischarge],'scaleanchor':'x'},
                       xaxis={'title': 'Observed<br>m3/s','range':[0, maxDischarge],'domain':[0,0.50], 'anchor':'y'},
                       yaxis={'title': models[model][1] + '<br>m3/s','range':[0, maxDischarge],'scaleanchor':'x'},
                       height=400,
                       width=800,
                       showlegend=False
                       )
    figure = go.Figure(data=data, layout=layout)
    #figure['data'].extend([trace1, trace2])
    #figure.layout(layout)
    div = opy.plot(figure, auto_open=False, output_type='div', config=config)

    return div

def StasTable(dfDischarge,code,name):

    stats_list=[mae, r_squared, nse, kge_2012]

    stats_compute=[]
    header_entries=['Model']

    for stat in stats_list:
        stats_compute.append(stat.abbr)
        header_entries.append(stat.name)

    header=dict(values=header_entries)

    cells=[]
    #cells=[header_entries]

    for model in list(models.keys())[1:]:
        tab=calc_stats(dfDischarge[[model, 'obs']], stats_compute)
        row=[models[model][0]]
        for stat in stats_compute:
            if tab[stat][0] != tab[stat][0]:
                row.append('N/A')
            elif isinstance(tab[stat][0], str):
                row.append(tab[stat][0])
            else:
                row.append('{:.2f}'.format(tab[stat][0]))
        cells.append(row)

    #print(cells)

    #table = ff.create_table(cells)

    cells_ok = dict(values=cells)

    trace = go.Table(
        header=header,
        cells=cells_ok)

    data = [trace]
    layout = go.Layout(title='Models performance',
                       height=400,
                       width=400,
                       showlegend=False
                       )
    figure = dict(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', config=config)
    #div = opy.plot(table, auto_open=False, output_type='div', config=config)

    return div

def StasData(dfDischarge,stats_list=[mae, r_squared, nse, kge_2012]):

    #stats_list=[mae, r_squared, nse, kge_2012]

    stats_compute=[]
    header_entries=[] #['Model']

    for stat in stats_list:
        stats_compute.append(stat.abbr)
        header_entries.append(stat.name)

    header=dict(values=None) # [])

    #cells=[]
    cells=[header_entries]

    tab=calc_stats(dfDischarge, stats_compute)
    row = []  # [st.name]
    for st in stats_list:
        stat=st.abbr
        if tab[stat][0] != tab[stat][0]:
            row.append('N/A')
        elif isinstance(tab[stat][0], str):
            row.append(tab[stat][0])
        else:
            row.append('{:.2f}'.format(tab[stat][0]))
    cells.append(row)

    cells_ok=dict(values=cells)

    #print(cells)

    #table = ff.create_table(cells)

    trace = go.Table(
        header=header,
        cells=cells_ok,
        domain=dict(x=[0.55,1.0],
                    y=[0.1, 0.9]),
        )

    #data = [trace]
    #layout = go.Layout(title='Models performance',
    #                   height=400,
    #                   width=400,
    #                   showlegend=False
    #                   )
    #figure = dict(data=data, layout=layout)
    #div = opy.plot(figure, auto_open=False, output_type='div', config=config)
    #div = opy.plot(table, auto_open=False, output_type='div', config=config)

    return trace # table

def ModPerformance(dfData):
    stations=dfData['code'].unique().tolist()
    df=pd.DataFrame(index=stations)
    models=['terraclimate_ro', 'terraclimate_wbm', 'crutsv401', 'gpccv7']
    for model in models:
        out = []
        for stat in stations:
            out.append('{:.2f}'.format(calc_stats(dfData.loc[dfData['code'] == stat, [model, 'obs']], [kge_2012.abbr])))
            #out.append(calc_stats(dfData.loc[dfData['code'] == stat, [model, 'obs']], [kge_2012.abbr]))
        df[model] = out # sum(i > 0.5 for i in out)
    trace = go.Table(
        header=dict(values=['Station'].extend(list(df.columns)),
                    fill=dict(color='#C2D4FF'),
                    align=['left'] * 5),
        cells=dict(values=[df.index.values,
                           df[models[0]].values,
                           df[models[1]].values,
                           df[models[2]].values,
                           df[models[3]].values],
                   fill=dict(color='#F5F8FF'),
                   align=['left'] * 5))

    data = [trace]
    layout = go.Layout(title='Models performance',
                       height=400,
                       width=400,
                       showlegend=False
                       )
    figure = dict(data=data, layout=layout)
    #figure['data'].extend([trace1, trace2])
    #figure.layout(layout)

    div = opy.plot(figure, auto_open=False, output_type='div', config=config)

    return div