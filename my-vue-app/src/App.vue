<template>
  <div class="all">
    <div
      class="jumbotron text-center"
      style="
        margin-bottom: 0;
        background-color: lightblue;
        background-size: cover;
        background-position: center;
      "
    >
      <h1>Smart Fish Tank</h1>
      <p>Health monitoring and cleaning system</p>
    </div>

    <nav class="navbar navbar-inverse">
      <div class="container-fluid">
        <div class="navbar-header">
          <button
            type="button"
            class="navbar-toggle"
            data-toggle="collapse"
            data-target="#myNavbar"
          >
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
          <ul class="nav navbar-nav">
            <li class="active"><a href="index1.html">Home</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="button">
      <el-button :plain="true" @click="open2">Refresh</el-button>
      <el-button :plain="true" @click="stop">Stop</el-button>
    </div>

    <div class="container">
      <div class="row">
        <div class="col-sm-8">
          <h3>Water Quality</h3>
          <div ref="tdsChartRef" style="width: 100%; height: 400px"></div>
          <p>
            These are a measure of all dissolved solids in water and can be used
            to measure salt. This is great for checking purity of water for
            breeding and for monitoring salt levels when it has been added to
            aquariums. TDS and Conductivity are interchangeable. TDS to
            conductivity: TDS/.53 or Conductivity to TDS: Conductivity/1.88.
          </p>
          <hr class="hidden-sm hidden-md hidden-lg" />
        </div>
      </div>

      <div class="row">
        <div class="col-sm-8">
          <h3>Ph Value</h3>
          <div ref="phChartRef" style="width: 100%; height: 400px"></div>
          <p>
            Measure of the acid/alkali nature of the water. The pH is the
            concentration of hydrogen ions and is logarithmic. This means that a
            shift of 1 pH unit is actually a ten-fold change: therefore a change
            of 1 pH unit is a significant change. pH 7.0 is neutral, below 7 is
            acid, above 7 is alkaline.
          </p>
        </div>
      </div>

      <div class="row">
        <div class="col-sm-8">
          <h3>Temperature</h3>
          <div
            ref="temperatureChartRef"
            style="width: 100%; height: 400px"
          ></div>
          <!-- 温度图表 -->
          <p>
            Fish are cold-blooded and need adequate temperatures to function
            properly. Temperatures outside their normal range make them more
            susceptible to disease. Check temperature regularly with a
            thermometer.
          </p>
        </div>
      </div>

      <div class="row">
        <div class="col-sm-8">
          <p>
            You can have more information about the quality of water and about
            fish from here
          </p>
          <ul class="nav nav-pills nav-stacked">
            <li class="active">
              <a href="https://www.serenityusa.com/blog/office-fish-tanks/"
                >Serenity Aquarium and Services</a
              >
            </li>
            <li>
              <a
                href="https://cafishvet.com/fish-tanks/how-to-clean-a-fish-tank/"
                >How to keep your fish tank clean</a
              >
            </li>
            <li>
              <a
                href="https://www.rspca.org.uk/adviceandwelfare/pets/fish/diet"
              >
                What to Feed your pet Fish
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="jumbotron text-center footer" style="margin-bottom: 0">
      <h2 style="font-style: italic">Having any trouble???</h2>
      <h2 style="font-style: italic">Contact Us on : 0425701761</h2>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "EChartsComponent",
  data() {
    return {
      sensorData: {
        timestamps: [],
        ph: [],
        tds: [],
        tmp: [],
      },
      refreshing: true,
    };
  },
  mounted() {
    this.timer = setInterval(() => {
      this.fetchSensorData();
    }, 2000);
  },
  methods: {
    async fetchSensorData() {
      try {
        const response = await fetch("http://3.90.228.112:8000/iot/get-data/");
        const json = await response.json();
        this.sensorData = {
          timestamps: [],
          ph: [],
          tds: [],
          tmp: [],
        };
        if (json.status === "success") {
          json.data.forEach((entry) => {
            this.sensorData.timestamps.push(entry.timestamp);
            this.sensorData.ph.push(entry.ph);
            this.sensorData.tds.push(entry.tds);
            this.sensorData.tmp.push(entry.tmp);
          });

          this.initPHChart();
          this.initTDSChart();
          this.initTemperatureChart();
        } else {
          console.error("Error fetching data:", json.message);
        }
      } catch (error) {
        console.error("Error fetching sensor data:", error);
      }
    },
    initPHChart() {
      const chart = echarts.init(this.$refs.phChartRef);
      const options = {
        tooltip: {},
        xAxis: {
          type: "category",
          data: this.sensorData.timestamps,
        },
        yAxis: {
          type: "value",
          axisLabel: {
            textStyle: {
              color: "#FFFFFF", // x 轴标签字体颜色
            },
          },
        },
        series: [
          {
            name: "pH",
            lebel: { show: true },
            type: "line",
            data: this.sensorData.ph,
            // 设置线条颜色和样式
            itemStyle: {
              color: "#FF5733", // 线条颜色
            },
            lineStyle: {
              width: 2, // 线条宽度
            },
            areaStyle: {
              color: "rgba(255, 87, 51, 0.3)", // 填充颜色
            },
          },
        ],
        color: ["#FF5733"], // 也可以设置整体颜色数组
      };
      chart.setOption(options);
    },
    initTDSChart() {
      const chart = echarts.init(this.$refs.tdsChartRef);
      const options = {
        tooltip: {},
        xAxis: {
          type: "category",
          data: this.sensorData.timestamps,
        },
        yAxis: {
          type: "value",
          axisLabel: {
            textStyle: {
              color: "#FFFFFF", // x 轴标签字体颜色
            },
          },
        },
        series: [
          {
            name: "TDS",
            type: "line",
            data: this.sensorData.tds,
            itemStyle: {
              color: "#1E90FF", // 更改为 DodgerBlue 线条颜色
            },
            lineStyle: {
              width: 2, // 线条宽度
            },
            areaStyle: {
              color: "rgba(30, 144, 255, 0.3)", // 填充颜色为半透明 DodgerBlue
            },
          },
        ],
      };
      chart.setOption(options);
    },
    initTemperatureChart() {
      const chart = echarts.init(this.$refs.temperatureChartRef);
      const options = {
        tooltip: {},
        xAxis: {
          type: "category",
          data: this.sensorData.timestamps,
        },
        yAxis: {
          type: "value",
          axisLabel: {
            textStyle: {
              color: "#FFFFFF", // x 轴标签字体颜色
            },
          },
        },
        series: [
          {
            name: "Temperature",
            type: "line",
            data: this.sensorData.tmp,
            itemStyle: {
              color: "#32CD32", // 更改为 LimeGreen 线条颜色
            },
            lineStyle: {
              width: 2, // 线条宽度
            },
            areaStyle: {
              color: "rgba(50, 205, 50, 0.3)", // 填充颜色为半透明 LimeGreen
            },
          },
        ],
      };
      chart.setOption(options);
    },
    async refreshWater() {
      try {
        const response = await fetch("http://3.90.228.112:8000/iot/fresh/", {
          method: "POST", // 使用 POST 请求
          headers: {
            "Content-Type": "application/json", // 设置请求头
          },
          body: JSON.stringify({ signal: "fresh" }), // 发送的信号数据
        });

        const result = await response.json();
        console.log("Response from server:", result); // 处理响应
      } catch (error) {
        console.error("Error sending refresh signal:", error);
      }
    },
    async refreshWater_stop() {
      try {
        const response = await fetch(
          "http://3.90.228.112:8000/iot/fresh_stop/",
          {
            method: "POST", // 使用 POST 请求
            headers: {
              "Content-Type": "application/json", // 设置请求头
            },
            body: JSON.stringify({ signal: "fresh" }), // 发送的信号数据
          }
        );

        const result = await response.json();
        console.log("Response from server:", result); // 处理响应
      } catch (error) {
        console.error("Error sending refresh signal:", error);
      }
    },
    open2() {
      this.$message({
        message: "Refresh has beed scheduled.",
        type: "success",
      });
      this.refreshWater();
    },
    stop() {
      this.$message({
        message: "Stopping...",
        type: "warning",
      });
      this.refreshWater_stop();
    },
  },
  beforeDestroy() {
    // 组件销毁时清除定时器
    clearInterval(this.timer);
  },
};
</script>

<style scoped>
.all {
  background-image: url("https://cdn.pixabay.com/photo/2023/05/15/09/42/fish-7994570_1280.jpg");
  background-size: cover;
  background-position: center;
}

body {
  position: relative; /* To position pseudo-element */
  background-image: url("https://cdn.pixabay.com/photo/2023/05/15/09/42/fish-7994570_1280.jpg");
  background-size: cover;
  background-position: center;
}

/* Pseudo-element for blurred background */
body::before {
  content: ""; /* Required for pseudo-elements */
  position: fixed; /* Fix it to the viewport */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  /* background-image: url("https://cdn.pixabay.com/photo/2023/05/15/09/42/fish-7994570_1280.jpg"); */
  background-size: cover;
  background-position: center;
  filter: blur(5px); /* Apply the blur effect */
  z-index: -1; /* Send it behind other content */
}

.fakeimg {
  height: 150px;
  width: 250px;
  background: #aaa;
}

.button {
  padding: 1px;
  text-align: center;
}

/* Set font color to white for all text except the footer */
.content,
h1,
h3,
p {
  color: white; /* Set font color to white */
}

/* Style for the footer */
.footer {
  background-color: lightblue; /* Light blue background for footer */
  padding: 20px; /* Add some padding */
}
</style>
