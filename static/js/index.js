$(function () {
  $('#container').highcharts({
    title: {
      text: '前10网站抓取量',
      x: -20 //center
    },
    colors: ['blue', 'red','black','blue','green','orange','yellow','brown','purple','gray'],
    plotOptions: {
      line: {
        lineWidth: 3
      },
      tooltip: {
        hideDelay: 200
      }
    },
    subtitle: {
      text: 'chart 1',
      x: -20
    },
    xAxis: {
      categories: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6',
                   'Day 7','Day8','Day9','Day10']
    },
    yAxis: {
      title: {
        text: 'Num'
      },
      plotLines: [{
        value: 0,
        width: 1
      }]
    },
    tooltip: {
      valueSuffix: ' num',
      crosshairs: true,
      shared: true
    },
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'middle',
      borderWidth: 0
    },
    series: [{
      name: 'Ideal Burn',
      color: 'rgba(255,0,0,0.25)',
      lineWidth: 2,
      data: [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    }, {
      name: 'Actual Burn',
      color: 'rgba(0,120,200,0.75)',
      marker: {
        radius: 6
      },
      data: [100, 110, 85, 60, 60, 30, 32, 63, 9, 2]
    }, {
      name: 'Actual Burn3',
      color: 'rgba(220,220,220,0.75)',
      marker: {
        radius: 6
      },
      data: [100, 110, 85, 60, 60, 30, 32, 23, 78, 2]
    }, {
      name: 'Actual Burn4',
      color: 'rgba(255,218,185,0.75)',
      marker: {
        radius: 6
      },
      data: [110, 110, 85, 60, 60, 30, 32, 23, 9, 9]
    }, {
      name: 'Actual Burn5',
      color: 'rgba(0,255,255,0.75)',
      marker: {
        radius: 6
      },
      data: [100, 79, 85, 60, 60, 30, 32, 23, 9, 2]
    }, {
      name: 'Actual Burn6',
      color: 'rgba(0,0,0,0.75)',
      marker: {
        radius: 6
      },
      data: [100, 110, 85, 80, 60, 20, 42, 23, 9, 2]
    }, {
      name: 'Actual Burn7',
      color: 'rgba(0,255,0,0.75)',
      marker: {
        radius: 6
      },
      data: [100, 90, 85, 40, 60, 30, 32, 23, 9, 2]
    }, {
      name: 'Actual Burn8',
      color: 'rgba(25,25,122,0.75)',
      marker: {
        radius: 6
      },
      data: [100, 110, 55, 60, 30, 30, 32, 23, 9, 2]
    }, {
      name: 'Actual Burn9',
      color: 'rgba(255,255,0,0.75)',
      marker: {
        radius: 6
      },
      data: [10, 110, 85, 60, 60, 30, 32, 23, 9, 2]
    }, {
      name: 'Actual Burn10',
      color: 'rgba(160,32,240,0.75)',
      marker: {
        radius: 6
      },
      data: [100, 110, 78, 60, 60, 30, 32, 23, 9, 2]
    }]
  });
});