from celery import shared_task
from celery_progress.backend import ProgressRecorder

import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

@shared_task(bind=True)
def plot_queryset(queryset_values,model_names):
    df = pd.DataFrame(queryset_values)
    fig = go.Figure()
    for model in model_names:
        model_df = df.loc[df['model_name'] == model]

        fig.add_trace(go.Scattergl(x=model_df['date'], y=model_df['mean_zonal_mean'], mode='lines', name=model))

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

import time
@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    result = 0
    for i in range(seconds):
        time.sleep(1)
        result += i
        progress_recorder.set_progress(i + 1, seconds)
    return result