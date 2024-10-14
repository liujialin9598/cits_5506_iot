<template>
  <div>
    <div ref="phChartRef" style="width: 100%; height: 400px;"></div>
    
    <div ref="tdsChartRef" style="width: 100%; height: 400px;"></div>

    <div ref="temperatureChartRef" style="width: 100%; height: 400px;"></div> <!-- 添加温度图表 -->
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'EChartsComponent',
  data() {
    return {
      sensorData: {
        timestamps: [],
        ph: [],
        tds: [],
        tmp: [], // 添加温度数据
      },
    };
  },
  mounted() {
    this.fetchSensorData();
  },
  methods: {
    async fetchSensorData() {
      try {
        const response = await fetch('http://192.168.4.26:8000/iot/get-data/');  // 替换为你的 Django API 地址
        const json = await response.json();
        
        if (json.status === 'success') {
          // 处理新数据格式
          json.data.forEach(entry => {
            this.sensorData.timestamps.push(entry.timestamp);
            this.sensorData.ph.push(entry.ph);
            this.sensorData.tds.push(entry.tds);
            this.sensorData.tmp.push(entry.tmp); // 获取温度数据
          });
          
          this.initPHChart();
          this.initTDSChart();
          this.initTemperatureChart(); // 初始化温度图表
        } else {
          console.error('Error fetching data:', json.message);
        }
      } catch (error) {
        console.error('Error fetching sensor data:', error);
      }
    },
    initPHChart() {
      const chart = echarts.init(this.$refs.phChartRef);
      const options = {
        title: {
          text: 'pH change',
        },
        tooltip: {},
        xAxis: {
          type: 'category',
          data: this.sensorData.timestamps,
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: 'pH',
            type: 'line',
            data: this.sensorData.ph,
          },
        ],
      };
      chart.setOption(options);
    },
    initTDSChart() {
      const chart = echarts.init(this.$refs.tdsChartRef);
      const options = {
        title: {
          text: 'TDS change',
        },
        tooltip: {},
        xAxis: {
          type: 'category',
          data: this.sensorData.timestamps,
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: 'TDS',
            type: 'line',
            data: this.sensorData.tds,
          },
        ],
      };
      chart.setOption(options);
    },
    initTemperatureChart() { // 添加温度图表的初始化
      const chart = echarts.init(this.$refs.temperatureChartRef);
      const options = {
        title: {
          text: 'Temperature change',
        },
        tooltip: {},
        xAxis: {
          type: 'category',
          data: this.sensorData.timestamps,
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: 'Temperature',
            type: 'line',
            data: this.sensorData.tmp, // 使用温度数据
          },
        ],
      };
      chart.setOption(options);
    },
  },
};
</script>

<style scoped>
/* 可以添加样式 */
</style>
