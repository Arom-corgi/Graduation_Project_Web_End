var chartDom = document.getElementById('heart_rate');
var heart_rate_echarts = echarts.init(chartDom);
var heart_rate_option;

heart_rate_option = {
  tooltip: {
    formatter: '{a} <br/>{b} : {c}bpm'
  },
  series: [
    {
      name: '心率',
      type: 'gauge',
      min: 30,
      max: 150,
      progress: {
        show: true,
      },
      detail: {
        valueAnimation: true,
        formatter: '{value} bpm'
      },
      axisLabel: {
        formatter: function(value) {
          return Math.round(value); // 四舍五入到最近的整数
        }
      },
      data: [
        {
          value: 150,
          name: '心率'
        }
      ]
    }
  ]
};

heart_rate_option && heart_rate_echarts.setOption(heart_rate_option);