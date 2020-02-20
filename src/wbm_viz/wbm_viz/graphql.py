import requests
import time
import pandas as pd

headers = {"Authorization": "Bearer YOUR API KEY"}

MEASUREMENTS = [
    "AirTemperature",
    "Evapotranspiration",
    "Precipitation",
    "Runoff",
    "SoilMoisture",
]

MODELS = [
    "TerraClimate",
    "WBMprist_CRUTSv401",
]


def run_query(query):
    request = requests.post('http://10.16.12.60:42170/v1/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def stats_monthly(schema, parameter, unit, sample_id, year=None, month=None):
    query = """
          %s_%s_%s_monthly(where: {SampleID: {_eq: %d}, Year: {_eq: %s}, Month: {_eq: %s}},
            order_by: {Date: asc}){
                Date
                Month
                SampleID
                Year
                ZonalMax
                ZonalMean
                ZonalMin
                ZoneArea
          }
    """ % (schema, parameter, unit, sample_id, year if year else "null", month if month else "null")
    return query


def query_concat(*args):
    """Join one or more graphql queries into. Hasura will execute in parallel, then return together"""

    all_query = "{%s}" % "".join(*args)
    return all_query


def query_model_stats_monthly(schemas, unit, sample_id):
    queries = []
    for schema in schemas:
        for measurement in MEASUREMENTS:
            queries.append(stats_monthly(schema, measurement, unit, sample_id))
    return query_concat(queries)


def to_df(table_dict):
    """Convert Table from database to usable Dataframe"""
    df = pd.DataFrame(table_dict)

    # Date as index
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')

    return df


def query_to_df(query_result):
    """Returns dictionary of pandas dataframe corresponding to all querys within query_result"""
    querys = query_result['data']
    return {key: to_df(val) for key, val in querys.items()}


def main():
    result = run_query(
        query_model_stats_monthly("TerraClimate", "Subbasin", 1)
    )

    return result


if __name__ == "__main__":
    s = time.perf_counter()
    result = main()
    dfs = query_to_df(result)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
