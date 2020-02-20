var DataFrame = dfjs.DataFrame;

const BASE_MODEL = "TerraClimate"
const MODELS = ["WBMprist_CRUTSv401", "WBMprist_GPCCv7"]
const SUBBASIN_ID = document.currentScript.getAttribute('subbasin_id');
const CATCH_IDS = document.currentScript.getAttribute('catch_ids');

// Send query to graphql server and return response json
async function exec_query(myquery) {
    let response = await fetch('http://10.16.12.60:42170/v1/graphql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({query: myquery})
    })
    if (response.status == 200) {
        let json = await response.json(); // (3)
        return json;
    }
    throw new Error(response.status);
}

// Construct and execute query
//Lone Subbasin
async function getData(model, parameter, id) {
    let query = `
{
  ${model}_${parameter}_Subbasin_monthly(where: {SampleID: {_eq: ${id}}}, order_by: {Date: asc}) {
    Date
    ZonalMean
    ZonalMax
    ZonalMin
  }
}
  `
    let data = await exec_query(query);
    return data
}

//Group of Subbasins (catchment)
async function getCatchData(model, parameter, subbasin_list) {
    let query = `
{
  ${model}_${parameter}_Subbasin_monthly(where: {SampleID: {_in: ${subbasin_list}}}, order_by: {SampleID: asc Date: asc}) {
    Date
    SampleID
    ZonalMean
  }
}
  `
    let data = await exec_query(query);
    return data
}

// get data and return plotly trace
async function getTrace(model, parameter, id) {


        let raw_data = await getData(model, parameter, id);
        const df = new DataFrame(raw_data.data[`${model}_${parameter}_Subbasin_monthly`]);
        const trace = [{
            name: model,
            y: df.toArray("ZonalMean"),
            x: df.toArray("Date")
        }];
        return trace

}

async function getCatchTrace(model,parameter,catchment){
      const data = await getCatchData(model, parameter, catchment)
        const df = new DataFrame(data.data[`${model}_${parameter}_Subbasin_monthly`]);
        const groupedDF = df.groupBy('Date').aggregate(group => group.stat.mean('ZonalMean')).rename('aggregation', 'groupZonalMean');
        const trace = [{
            name: model,
            y: groupedDF.toArray("groupZonalMean"),
            x: groupedDF.toArray("Date")
        }];
        return trace
}

// Update empty plot with data
async function redrawPlot(graphDiv, parameter, identifier, layout) {
    if (identifier.catchment) {
        let baseTrace = await getCatchTrace(BASE_MODEL, parameter, identifier.catchment);
        Plotly.react(graphDiv, baseTrace, layout)
        for (model of MODELS) {
            let trace = await getCatchTrace(model, parameter, identifier.catchment);

            Plotly.addTraces(graphDiv, trace);
        }

    } else {
        let baseTrace = await getTrace(BASE_MODEL, parameter, identifier.id);
        Plotly.react(graphDiv, baseTrace, layout)

        for (model of MODELS) {
            let trace = await getTrace(model, parameter, identifier.id);

            Plotly.addTraces(graphDiv, trace);
        }
    }
}

// Basic Layout before adding data
function baseLayout(title, ylabel = "units") {
    let layout = {
        title: title,
        yaxis: {
            title: ylabel
        },
        showlegend: true

    }

    return layout
}

async function main() {
    // Setup empty plots
    AirTemperature = document.getElementById('AirTemperature');
    layout1 = baseLayout('Air Temperature Zonal Mean')
    Plotly.newPlot(AirTemperature, [], layout1);

    Evapotranspiration = document.getElementById('Evapotranspiration');
    layout2 = baseLayout('Evapotranspiration Zonal Mean')
    Plotly.newPlot(Evapotranspiration, [], layout2);

    Precipitation = document.getElementById('Precipitation');
    layout3 = baseLayout('Precipitation Zonal Mean')
    Plotly.newPlot(Precipitation, [], layout3);

    SoilMoisture = document.getElementById('SoilMoisture');
    layout4 = baseLayout('Soil Moisture Zonal Mean')
    Plotly.newPlot(SoilMoisture, [], layout4);

    let identity = {id: 1000}
    // Async populate data on plots
    await Promise.all([
        redrawPlot(AirTemperature, 'AirTemperature', identity, layout1),
        redrawPlot(Evapotranspiration, 'Evapotranspiration', identity, layout2),
        redrawPlot(Precipitation, 'Precipitation', identity, layout3),
        redrawPlot(SoilMoisture, 'SoilMoisture', identity, layout4),
    ])
}

async function catch_main() {
    // Setup empty plots
    AirTemperature = document.getElementById('AirTemperature');
    layout1 = baseLayout('Air Temperature Zonal Mean')
    Plotly.newPlot(AirTemperature, [], layout1);

    Evapotranspiration = document.getElementById('Evapotranspiration');
    layout2 = baseLayout('Evapotranspiration Zonal Mean')
    Plotly.newPlot(Evapotranspiration, [], layout2);

    Precipitation = document.getElementById('Precipitation');
    layout3 = baseLayout('Precipitation Zonal Mean')
    Plotly.newPlot(Precipitation, [], layout3);

    SoilMoisture = document.getElementById('SoilMoisture');
    layout4 = baseLayout('Soil Moisture Zonal Mean')
    Plotly.newPlot(SoilMoisture, [], layout4);

    let identity = {catchment: CATCH_IDS}
    await Promise.all([
        redrawPlot(AirTemperature, 'AirTemperature', identity, layout1),
        redrawPlot(Evapotranspiration, 'Evapotranspiration', identity, layout2),
        redrawPlot(Precipitation, 'Precipitation', identity, layout3),
        redrawPlot(SoilMoisture, 'SoilMoisture', identity, layout4),
    ])
}

catch_main()
// main()