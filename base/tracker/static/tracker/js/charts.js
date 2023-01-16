const lineEndpoint = '/api/line';

function successfn(data) {
  data.labels = data.labels.map(dateString => new moment(dateString));

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
  const dataObj = {
    labels: data.labels,
    datasets: [{
      label: 'UK Total Covid-19 Cases ',
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)',
      data: data.values
    }]
  };
  const optionsObj = {
    scales: {
      xAxes,
      yAxes
    }
  };
  const lineChart = new Chart(
    lineCtx,
    {type: 'line', data: dataObj, options: optionsObj}
  );
  document.getElementById('spinner').style.display = 'none';
  document.getElementById('source').style.display = 'block';
  console.log('Request successful!');
};

console.log('Request initiated to endpoint: ' + lineEndpoint);
$.ajax({
  method: 'GET',
  url: lineEndpoint,
  success: successfn,
  error: function(errorData) {
    console.log(errorData);
  }
});

const pieCtx = document.getElementById('myPie').getContext('2d');
const pieChart = new Chart(pieCtx, {
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
