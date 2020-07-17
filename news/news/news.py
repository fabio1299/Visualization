import os
import pandas as pd
from sqlalchemy import create_engine


FOLDER_CONSTANTS = dict(
    root='/asrc/ecr/NEWS/Visualization',
    model_variations=[
     'NorESM1-M_RCP2p6_Final925',
     'GFDL-ESM2M_RCP2p6_Final925',
     'MIROC-ESM-CHEM_RCP2p6_Final925',
     'GFDL-ESM2M_RCP8p5_Final925',
     'IPSL-CM5A-LR_RCP8p5_Final925',
     'IPSL-CM5A-LR_RCP2p6_Final925',
     'HadGEM2-ES_RCP2p6_Final925',
     'HadGEM2-ES_RCP8p5_Final925_float',
     'NorESM1-M_RCP8p5_Final925',
     'MIROC-ESM-CHEM_RCP8p5_Final925',
     'HadGEM2-ES_RCP8p5_Final925',
    ],
    netcdf_folders=['airtemperature', 'Discharge', 'qxt_watertemp', 'wetbulbtemp', 'Runoff']
)

def get_netcdf_paths():
    """"""
    abs_paths = {}
    for root,dirs,files in os.walk(FOLDER_CONSTANTS['root']):
        for model in FOLDER_CONSTANTS['model_variations']:
            if model in root:
                if model not in abs_paths.keys():
                    abs_paths[model] = {}
                for nc in FOLDER_CONSTANTS['netcdf_folders']:
                    if nc in root:
                        dir_path = os.path.abspath(root)
                        dir_contents = [os.path.abspath(os.path.join(dir_path, file)) for file in os.listdir(dir_path)]
                        abs_paths[model][nc] = sorted(dir_contents)
    return abs_paths

def melt_date_columns(df,id_vars,var_name,value_name):
    date_columns = []
    non_date_columns = []
    for c in df.columns:
        if c[0] not in ['1', '2']:
            non_date_columns.append(c)
        else:
            date_columns.append(c)

    dates_df = df[date_columns + id_vars]
    non_date_df = df[non_date_columns]
    date_melt_df = dates_df.melt(id_vars=id_vars, var_name=var_name, value_name=value_name)
    return non_date_df, date_melt_df


def get_sql_engine(uri):
    engine = create_engine(uri)
    return engine


def to_db(df, table, post_sql):
    engine = get_sql_engine()
    with engine.connect() as connection:
        df.to_sql(table, connection, if_exists='replace')
        for sql in post_sql:
            connection.execute(sql)

