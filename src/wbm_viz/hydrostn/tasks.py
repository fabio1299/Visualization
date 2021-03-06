"""Celery tasks"""
from celery import shared_task
import pandas as pd
import plotly
import plotly.graph_objects as go
import json
from django.apps import apps


@shared_task(bind=True)
def plot_queryset(self, model_name, queryset_ids, model_names, y_param, title="title", units="units"):
    model = apps.get_model('hydrostn', model_name)
    queryset = list(model.objects.filter(subbasin_id__in=queryset_ids).order_by('subbasin_id', 'date').values())
    df = pd.DataFrame(queryset)
    fig = go.Figure()

    for i, model in enumerate(model_names):
        model_df = df.loc[df['model_name'] == model]

        fig.add_trace(go.Scatter(x=model_df['date'], y=model_df[y_param], mode='lines', name=model))

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
