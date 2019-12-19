var DataFrame = dfjs.DataFrame;

const BASE_MODEL = "TerraClimate"
const MODELS = ["WBMprist_CRUTSv401", "WBMprist_GPCCv7"]

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

async function getTrace(model, parameter, id) {
    let raw_data = await getData(model, parameter, id)
    let df = new DataFrame(raw_data.data[`${model}_${parameter}_Subbasin_monthly`]);
    let trace = [{
        name: model,
        y: df.toArray("ZonalMean"),
        x: df.toArray("Date")
    }];
    return trace
}

async function addStat(graphDIV, model, parameter, id) {
    let trace = await getTrace(model, parameter, id);

    Plotly.addTraces(graphDIV, trace);
}

async function redrawPlot(graphDiv, parameter, id) {
    let baseTrace = await getTrace(BASE_MODEL, parameter, id);
    Plotly.react(graphDiv, baseTrace)

    for (model of MODELS) {
        addStat(graphDiv, model, parameter, id)
    }
}


async function main() {

    TESTER = document.getElementById('tester');
    Plotly.newPlot(TESTER);


    TESTER2 = document.getElementById('tester2');
    Plotly.newPlot(TESTER2);

    TESTER3 = document.getElementById('tester3');
    Plotly.newPlot(TESTER3);

    TESTER4 = document.getElementById('tester4');
    Plotly.newPlot(TESTER4);

    await Promise.all([
        redrawPlot(TESTER, 'AirTemperature', 1),
        redrawPlot(TESTER2, 'Evapotranspiration', 1),
        redrawPlot(TESTER3, 'Precipitation', 1),
        redrawPlot(TESTER4, 'SoilMoisture', 1),
    ])


}

main()