import hydrostats.analyze as ha
import pandas as pd
from argentina.hydro_stats import calc_stats
import numpy as np
from hydrostats.metrics import mae, r_squared, nse, kge_2012
import plpy

def hydro_stats(station, res, model, metrics):
    my_metrics = [metrics]
    model_table='{}_{}.discharge_gauges_monthly'.format(model, res)
    id_field='sampleid{}'.format(res)

    data=plpy.execute("select to_date(o.date,'YYYY-MM') as date, " + \
            'sim.discharge as "Simulated", o.mean as "Observed" ' + \
            "from contrib.discharge_data_monthly o " + \
            "LEFT OUTER JOIN {} sim ".format(model_table) + \
            "on o.{} = sim.sampleid and o.date = sim.date ".format(id_field) + \
            "where o.stationid = {} ".format(station) + \
            "order by date")

    #plpy.notice(type(data))

    dfData=pd.DataFrame(data[0:])

    #dfData=pd.DataFrame(data[0:])
    dfData.set_index("date",drop=True,inplace=True)
    dfData.index = pd.to_datetime(dfData.index)

    for col in dfData.columns:
        if dfData[col].dtype == 'object':
            dfData[col]=0
            dfData[col] = pd.to_numeric(dfData[col])

    #plpy.notice(dfData.dtypes)
    dfData['Simulated'].values[dfData['Simulated'].values < 0.0001] = 0
    #plpy.notice(dfData)

    #tab=ha.make_table(dfData[['Simulated','Observed']], my_metrics, remove_neg=True, remove_zero=True)

    #out={}

    #for col in tab.columns:
    #    out[col] = tab.iloc[[0]][col][0]

    return calc_stats(dfData[['Simulated','Observed']],my_metrics)

#def calc_stats(dfData,my_metrics):

#    tab=ha.make_table(dfData, my_metrics, remove_neg=True, remove_zero=True)

#    if len(my_metrics)==1:
#        return tab.iloc[[0]][tab.columns[0]][0]
#    else:
#        return tab


#my_metrics = [mae.abbr, r_squared.abbr, nse.abbr, kge_2012.abbr]

#station=1211
#res='01min'
#model='terraclimate'

