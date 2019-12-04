import requests
import time
import pandas as pd

headers = {"Authorization": "Bearer YOUR API KEY"}

MEASUREMENTS = [
    "AirTemperature",
    "Evapotranspiration",
    "Precipitation",
    "Runoff",
    "SoilMoisture"
]

def run_query(query):
    request = requests.post('http://localhost:8080/v1/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def stats_monthly(schema,parameter,unit,sample_id,year=None,month=None):
    query = """
          %s_%s_%s_monthly(where: {SampleID: {_eq: %d}, Year: {_eq: %s}, Month: {_eq: %s}},
            order_by: {Year: asc}){
                Date
                Month
                SampleID
                Year
                ZonalMax
                ZonalMean
                ZonalMin
                ZoneArea
          }
    """ % (schema, parameter,unit,sample_id, year if year else "null", month if month else "null")
    return query


def query_all(*args):
    """Join one or more graphql queries into. Hasura will execute in parallel, then return together"""

    all_query = "{%s}" % "".join(*args)
    return all_query

def query_model_stats_monthly(schema,unit,sample_id):
    return query_all(
        [stats_monthly(schema, measurement, unit, sample_id) for measurement in MEASUREMENTS]
    )


def query_to_df(query_result):
    '''Returns dictionary of pandas dataframe corresponding to all querys within query_result '''
    querys = query_result['data']
    return {key: pd.DataFrame(val) for key, val in querys.items()}




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
