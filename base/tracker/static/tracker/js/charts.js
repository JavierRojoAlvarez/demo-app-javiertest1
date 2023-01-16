const moment = window.moment;
const Chart = window.Chart;
const lineEndpoint = '/api/line';

function successfn(responseObj) {
  console.log(responseObj);
  responseObj.labels = responseObj.labels.map(dateString => moment(dateString));

  const lineCtx = document.getElementById('myLine').getContext('2d');
  function userCallbackfn(value, index, values) {
    return value.toLocaleString();
  }
  const yAxes = [{
    ticks: {beginAtZero: true, userCallback: userCallbackfn}
  }];
  const xAxes = [{
    type: 'time',
    gridLines: {display: true},
    time: {minUnit: 'month'}
  }];
  const data = {
    labels: responseObj.labels,
    datasets: [{
      label: 'UK Total Covid-19 Cases ',
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)',
      data: responseObj.values
    }]
  };
  const options = {scales: {xAxes, yAxes}};
  Chart(lineCtx, {type: 'line', data, options});
  document.getElementById('spinner').style.display = 'none';
  document.getElementById('source').style.display = 'block';
  console.log('Request successful!');
};

console.log(`Request initiated to endpoint: ${lineEndpoint}`);
fetch(lineEndpoint).then(response => response.json()).then(successfn);

const pieCtx = document.getElementById('myPie').getContext('2d');
Chart(pieCtx, {
  type: 'pie',
  data: {
    labels: ['GPA', 'OGD', 'BBQ'],
    datasets: [{
      label: 'Finance Numbers',
      backgroundColor: [
        'rgb(187, 29, 250)',
        'rgb(255, 99, 132)',
        'rgb(28, 199, 132)'
      ],
      data: [2, 10, 5]
    }]
  },
  options: {}
});
