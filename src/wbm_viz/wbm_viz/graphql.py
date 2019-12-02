# An example to get the remaining rate limit using the Github GraphQL API.

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
                RecordName
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

result = run_query(stats_monthly("TerraClimate","AirTemperature","Subbasin",100,1958,))  # Execute the query
print(result)