
from celery import shared_task
import pandas as pd
import plotly
import plotly.graph_objects as go
import json
from django.db import connections
from datetime import datetime
from hydrostn.db_routines import _dict_fetch_all

@shared_task(bind=True)
def plot_watertemp(self, network_points, start_year, end_year, title="River Stretch Average Watertemp GFDL-ESM2M_RCP2p6_Final925", units="C"):
    fig = go.Figure()
    df = watertemp_avg(network_points,start_year,end_year)
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['watertemp'], mode='lines'))
    fig.update_layout(
        legend_orientation="h",
        title={
            'text': title,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title=units,
        autosize=True,
    )
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json



def get_watertemp(start_year,end_year, longitude, latitude):
    with connections['news'].cursor() as cursor:
        cursor.callproc('news_get_watertemp', (start_year,end_year, longitude, latitude))

        return _dict_fetch_all(cursor)

@shared_task(bind=True)
def watertemp_df(self, network_points, start_year, end_year):
    longs = [point['longitude'] for point in network_points]
    lats = [point['latitude'] for point in network_points]
    dist2ocean_map = {p['coord_id']: p['dist2ocean'] for p in network_points}

    sql_template = "SELECT * FROM news_get_watertemp({},{},{},{})"
    procedure_calls = [sql_template.format(start_year,end_year,long,lat) for long,lat in zip(longs,lats)]
    inner_sql = ' UNION ALL '.join(procedure_calls)
    sql = "WITH Q AS ( {} ) SELECT year,day_of_year as day,measurement as watertemp,coord_id from q ORDER BY coord_id,year,day_of_year;".format(inner_sql)

    with connections['news'].cursor() as cursor:
        cursor.execute(sql)

        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['year','day','watertemp','coord_id'])
        df.year = df.year.astype(str)
        df.day = df.day.astype(str)
        df.day = df.day.str.rjust(3, '0')
        df['datetime'] = pd.to_datetime(df.year + ' ' + df.day, format='%Y %j')
        df['dist2ocean'] = df.coord_id.map(dist2ocean_map)
        return df.to_json()

@shared_task(bind=True)
def avg_plot(self, df_json):
    df = pd.read_json(df_json)
    df = df[['datetime', 'watertemp']].groupby(['datetime']).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['watertemp'], mode='lines'))
    fig.update_layout(
        legend_orientation="h",
        title={
            'text': 'River Stretch Average Watertemp GFDL-ESM2M_RCP2p6_Final925',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title='C',
        autosize=True,
    )
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

@shared_task(bind=True)
def distance_plot(self,df_json, year, day):
    dt = datetime.strptime(str(year) + '-' + str(day),'%Y-%j')
    year = int(year)
    day = int(day)
    df = pd.read_json(df_json)
    df = df[(df.day == day) & (df.year == year)].sort_values('dist2ocean',ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['dist2ocean'], y=df['watertemp'], mode='lines', name='dist2ocean'))

    fig.update_layout(
        legend_orientation="h",
        title={
            'text': 'River Stretch Watertemp {}'.format(dt.strftime('%Y-%m-%d')),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title='C',
        xaxis_title='Distance to Ocean(km)',
        autosize=True,
        xaxis={
            'autorange':'reversed'
        }
    )
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

@shared_task(bind=True)
def distance_plot_3d(self,df_json,year):
    df = pd.read_json(df_json)
    df[(df.year == year)].sort_values('dist2ocean', ascending=True)

    layout = dict(
        showlegend=False,
        width=1000,
        height=1000,
        title="Watertemp Daily {} / Distance to Ocean".format(year),
    )
    fig = go.Figure(layout=layout)
    line = dict(color='blue')

    for name, group in df.groupby('dist2ocean'):
        trace = go.Scatter3d(mode='lines')

        trace.x = group['day']
        trace.y = group['dist2ocean']
        trace.z = group['watertemp']
        # trace.line=line
        fig.add_trace(trace)

    fig.update_layout(scene=dict(
        xaxis_title='Day of {}'.format(year),
        yaxis_title='Distance to Ocean',
        zaxis_title='Water Temperature C'),)

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

# def _union_all(selects)
def watertemp_avg(network_points,start_year,end_year):
    sql_template = "SELECT * FROM news_get_watertemp({},{},{},{})"
    longs = [point['longitude'] for point in network_points]
    lats = [point['latitude'] for point in network_points]

    procedure_calls = [sql_template.format(start_year,end_year,long,lat) for long,lat in zip(longs,lats)]
    inner_sql = ' UNION ALL '.join(procedure_calls)
    sql = "WITH Q AS ( {} ) SELECT year,day_of_year,avg(measurement) from q GROUP BY year,day_of_year ORDER BY year,day_of_year;".format(inner_sql)

    with connections['news'].cursor() as \
            cursor:
        cursor.execute(sql)

        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['year','day','watertemp'])
        df.year = df.year.astype(str)
        df.day = df.day.astype(str)
        df.day = df.day.str.rjust(3, '0')
        df['datetime'] = pd.to_datetime(df.year + ' ' + df.day, format='%Y %j')
        return df
