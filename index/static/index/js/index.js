// 设置echarts图的方法
function set_echarts(id) {
  let chartDom = document.getElementById(id);
  let mycharts = echarts.init(chartDom);
  let option;

  // 获取数据
  let name = chartDom.dataset.name;
  let min = chartDom.dataset.min;
  let max = chartDom.dataset.max;
  let unit = chartDom.dataset.unit;
  let currentValue = chartDom.dataset.currentValue;
  let isInt = chartDom.dataset.isInt === 'true';
  let axisLabel;

  // 判断该指标整型/浮点型
  if (isInt) {
    axisLabel = {
      formatter: function(value) {
        return Math.round(value); // 四舍五入到最近的整数
      }
    };
  } else {
    axisLabel = {
      formatter: function(value) {
        return value.toFixed(1); // 保留一位小数
      }
    };
  }

  option = {
    tooltip: {
      formatter: '{a} <br/>{b} : {c}bpm'
    },
    series: [
      {
        name: name,
        type: 'gauge',
        min: min,
        max: max,
        progress: {
          show: true,
        },
        detail: {
          valueAnimation: true,
          formatter: '{value}' + unit,
        },
        axisLabel: axisLabel,
        data: [
          {
            value: currentValue,
            name: name
          }
        ]
      }
    ]
  };
  option && mycharts.setOption(option);
}

// 心率
set_echarts("heart_rate");
// 血压
set_echarts("blood_pressure");
// 体温
set_echarts("temperature");
// 血氧
set_echarts("blood_oxygen");