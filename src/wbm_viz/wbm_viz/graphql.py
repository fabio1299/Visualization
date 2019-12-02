# An example to get the remaining rate limit using the Github GraphQL API.

import requests

headers = {"Authorization": "Bearer YOUR API KEY"}

def run_query(query):
    request = requests.post('http://localhost:8080/v1/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def AirTemperature_Subbasin_monthly(schema,sample_id):
    query = """
    {
          %s_AirTemperature_Subbasin_monthly(where: {SampleID: {_eq: %d}}, order_by: {Year: asc}){
            Date
            Month
            RecordName
            SampleID
            Year
            ZonalMax
            ZonalMean
            ZonalMin
            ZoneArea
          }
    }
    
    """ % (schema,sample_id)
    return query

result = run_query(AirTemperature_Subbasin_monthly("TerraClimate",1977))  # Execute the query
print(result)