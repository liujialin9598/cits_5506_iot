<template>
  <div>
    <el-button type="primary" @click="refreshWater">Refresh Water</el-button> <!-- 按钮点击事件 -->
    
    <div ref="phChartRef" style="width: 100%; height: 400px;"></div>
    
    <div ref="tdsChartRef" style="width: 100%; height: 400px;"></div>

    <div ref="temperatureChartRef" style="width: 100%; height: 400px;"></div> <!-- 温度图表 -->
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
        temperature: [],
      },
    };
  },
  mounted() {
    this.fetchSensorData();
  },
  methods: {
    async fetchSensorData() {
      try {
        const response = await fetch('http://3.90.228.112:8000/iot/get-data/');
        const json = await response.json();
        
        if (json.status === 'success') {
          json.data.forEach(entry => {
            this.sensorData.timestamps.push(entry.timestamp);
            this.sensorData.ph.push(entry.ph);
            this.sensorData.tds.push(entry.tds);
            this.sensorData.temperature.push(entry.temperature);
          });
          
          this.initPHChart();
          this.initTDSChart();
          this.initTemperatureChart();
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
    initTemperatureChart() {
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
            data: this.sensorData.temperature,
          },
        ],
      };
      chart.setOption(options);
    },
    async refreshWater() {
      try {
        const response = await fetch('http://3.90.228.112:8000/fresh', {
          method: 'POST', // 使用 POST 请求
          headers: {
            'Content-Type': 'application/json', // 设置请求头
          },
          body: JSON.stringify({ signal: 'fresh' }), // 发送的信号数据
        });

        const result = await response.json();
        console.log('Response from server:', result); // 处理响应
      } catch (error) {
        console.error('Error sending refresh signal:', error);
      }
    },
  },
};
</script>

<style scoped>
/* 可以添加样式 */
</style>
