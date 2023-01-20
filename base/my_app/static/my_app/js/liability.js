const Chart = window.Chart;
const endpoint = '/api/liability';
const id = document.getElementById('id').value;

function updateLineChart(response) {
  const lineCtx = document.getElementById('myLine').getContext('2d');
  const datasetArray = [];
  for (const dataset of response.datasets) {
    console.log(dataset.series);
    console.log(dataset.label);
    datasetArray.push({
      label: dataset.label,
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)',
      data: dataset.series,
      lineTension: 0
    });
  };
  const dataObj = {
    labels: response.labels,
    datasets: datasetArray,
  };
  new Chart(
    lineCtx, {
      type: 'line',
      data: dataObj,
    }
  );
  document.getElementById('spinner').style.display = 'none';
  document.getElementById('source').style.display = 'block';
  console.log('Request successful!');
};

console.log(
  '%c Making API request...',
  'background: cornflowerblue; color: white; padding: 2px; border-radius:2px'
);
fetch(
  `${endpoint}?id=${id}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
    credentials: 'same-origin'
  }
).then(response => response.json()).then(updateLineChart).catch(error => console.log(error));
