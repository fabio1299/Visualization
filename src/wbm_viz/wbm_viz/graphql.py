import requests

headers = {"Authorization": "Bearer YOUR API KEY"}

def run_query(query):
    request = requests.post('http://localhost:8080/v1/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def stats_monthly(schema,parameter,unit,sample_id,year=None,month=None):
    query = """
    {
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
    }
    
    """ % (schema, parameter,unit,sample_id, year if year else "null", month if month else "null")
    return query

SAMPLE_ID =100
YEAR = 1977
print(run_query(stats_monthly("TerraClimate", "AirTemperature", "Subbasin", SAMPLE_ID, YEAR,)))
print("\nNext Scehma\n")
print(run_query(stats_monthly("WBMprist_CRUTSv401", "AirTemperature", "Subbasin", SAMPLE_ID, YEAR,)))
