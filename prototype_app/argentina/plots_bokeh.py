import plotly.offline as opy
import plotly.graph_objs as go

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components


from datetime import datetime


config = {'showLink': False,
          'modeBarButtonsToRemove': ['sendDataToCloud'],
          'displaylogo': False
          }


def TimeseriesAllModels(dfDischarge,code,name):

    models={
        'obs': ['Observed', 'Observed'],
        'terraclimate_ro': ['TerraClimate (Accumulated Runoff)','TerraClimate'],
        'terraclimate_wbm': ['TerraClimate (WBM model)', 'TerraClimate'],
        'crutsv401' : ['CRU TS', 'CRU TS Ver. 4.01'],
        'gpccv7' : ['GPCC','GPCC Ver. 7']
    }

    maxDischarge = max(dfDischarge[list(models.keys())].max())
    maxDischarge = maxDischarge + maxDischarge * 0.05

    maxTime=dfDischarge.index.max()



    trace1 = go.Scatter(x=dfDischarge.index, y=dfDischarge['obs'], marker={'color': 'red', 'symbol': 104, 'size': "1"},
                        mode='lines', name='Observed')
    trace2 = go.Scatter(x=dfDischarge.index, y=dfDischarge['terraclimate_ro'],
                        marker={'color': 'blue', 'symbol': 103, 'size': "1"},
                        mode='lines', name='TerraClimate (runoff accumulation)')
    trace3 = go.Scatter(x=dfDischarge.index, y=dfDischarge['terraclimate_wbm'],
                        marker={'color': 'green', 'symbol': 102, 'size': "1"},
                        mode='lines', name='TerraClimate (WBM model)')
    trace4 = go.Scatter(x=dfDischarge.index, y=dfDischarge['crutsv401'],
                        marker={'color': 'yellow', 'symbol': 101, 'size': "1"},
                        mode='lines', name='CRU TS Ver. 4.01')
    trace5 = go.Scatter(x=dfDischarge.index, y=dfDischarge['gpccv7'],
                        marker={'color': 'cyan', 'symbol': 100, 'size': "1"},
                        mode='lines', name='GPCC Ver. 7')
    data = go.Data([trace1, trace5, trace4, trace2, trace3])
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
        )
    )
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', config=config)
    return div

def ObsVsModeled(dfDischarge,model,code,name):
    models={
        'obs': ['Observed','Observed'],
        'terraclimate_ro': ['TerraClimate (Accumulated Runoff)','TerraClimate'],
        'terraclimate_wbm': ['TerraClimate (WBM model)', 'TerraClimate'],
        'crutsv401' : ['CRU TS', 'CRU TS Ver. 4.01'],
        'gpccv7' : ['GPCC','GPCC Ver. 7']
    }

    maxDischarge = max(dfDischarge[list(models.keys())].max())
    maxDischarge = maxDischarge + maxDischarge * 0.05

    TOOLTIPS = [
        ("date", "$index"),
        ("(x,y)", "($x, $y)"),
    ]

    plot = figure(title= 'Observed vs {}'.format(models[model][0]) ,
        x_axis_label= 'Observerd',
        x_range=[0,maxDischarge],
        y_axis_label= models[model][1],
        y_range=[0,maxDischarge],
        plot_width =400,
        plot_height =400,)
#        tooltips=TOOLTIPS,)

    plot.scatter(dfDischarge['obs'], dfDischarge[model], legend='') #, line_width=2)
    plot.line(x=[0,maxDischarge],y=[0,maxDischarge],
              line_dash='dotted',
              line_color=('lightgrey'),
              line_width=2)


    # Store components
    script, div = components(plot)

    return {'script': script, 'div': div}
