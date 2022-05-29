<template>
  <div class="centered">
    <!-- {{inventorData.inventor_companys}} -->
    <!-- {{test}} -->
    <!-- {{ companyChartData }} -->
    <!-- <div
      ref="monthWorkOrder"
      class="echarts-box"
      style="width: 600px; height: 300px; border: 1px solid red"
    ></div> -->
    <!-- {{inventorData.inventor_companys}} -->
    <p>{{ this.id }}</p>

    <p>姓名：{{ inventorData.inventor_name }}</p>
    <!-- <p>公司：{{ inventorData.inventor_companys }}</p> -->
    <p>公司</p>
    <div v-for="(item, index) in companyList" :key="index">
      <p>
        {{ item.company_name[0] }} {{ item.start_time }}-{{
          item.end_time
        }}
        贡献专利{{ item.num }}篇
      </p>
      <!-- {{item.id}} -->
      <div ref="companyK" class="company-k-wrap" :id="String(item.id)"></div>
    </div>

    <p>专利数量：{{ inventorData.inventor_patents_totalnum }}</p>
    <p>专利质量综合评分：{{ inventorData.average_score }}</p>
    <p>发明家质量综合评分：{{ inventorData.T_index }}</p>
    <div v-for="(item, index2) in collaboratorList" :key="index2">
      <p>{{ item.name }} : {{ item.num }}</p>
    </div>
    <p>研究领域</p>
    <div v-for="(item, index) in inventorData.inventor_categories" :key="index">
      <p>{{ item.category_name }}:{{ item.time.length }}</p>
    </div>
    <p>专利列表</p>
    <div v-for="(item, index) in inventorData.patents_ids" :key="index">
      <p>专利id：{{ item }}</p>
    </div>
    <p>ipc分类信息</p>
    <div v-for="(item, index) in inventorData.patents_ipcs" :key="index">
      <p>ipc号：{{ index }} 发表{{ item.time.length }}次 {{ item.ipc_info }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Inventor",
  data() {
    return {
      id: this.$route.params.id,
      inventorData: {},
      companyList: [],
      collaboratorList: [],
      test: "",
      companyChartData: {},
    };
  },
  created() {
    this.$axios
      .get("http://127.0.0.1:5000/inventor_info_all", {
        params: {
          id: this.id,
        },
      })
      .then((response) => {
        // console.log(response)
        this.inventorData = response.data;
        // console.log(this.inventorData)
        this.inventorData.T_index = parseFloat(
          this.inventorData.T_index
        ).toFixed(2);
        this.inventorData.average_score = parseFloat(
          this.inventorData.average_score
        ).toFixed(2);
        this.inventorData.inventor_companys = JSON.parse(
          this.inventorData.inventor_companys
        );
        for (var key in this.inventorData.inventor_companys) {
          this.companyList.push({
            id: key,
            company_name:
              this.inventorData.inventor_companys[key]["company_name"],
            time: this.inventorData.inventor_companys[key]["times"],
            end_time: this.arrayMax(
              this.inventorData.inventor_companys[key]["times"]
            ),
            start_time: this.arrayMin(
              this.inventorData.inventor_companys[key]["times"]
            ),
            num: this.inventorData.inventor_companys[key]["patents_num"],
          });
        }
        // console.log(this.companyList);
        this.inventorData.collaborators = JSON.parse(
          this.inventorData.collaborators
        );
        for (var key in this.inventorData.collaborators) {
          this.collaboratorList.push({
            id: key,
            name: this.inventorData.collaborators[key]["name"],
            num: this.inventorData.collaborators[key]["times"].length,
            patents: this.inventorData.collaborators[key]["patent_ids"],
          });
        }
        // console.log(this.collaboratorList);

        this.collaboratorList = this.collaboratorList.sort(
          (a, b) => b.num - a.num
        );
        this.companyList = this.companyList.sort((a, b) => b.num - a.num);
        this.inventorData.inventor_categories = JSON.parse(
          this.inventorData.inventor_categories
        );
        this.inventorData.patents_ids = JSON.parse(
          this.inventorData.patents_ids
        );
        this.inventorData.patents_ipcs = JSON.parse(
          this.inventorData.patents_ipcs
        );
        // console.log(this.inventorData.inventor_categories)

        // console.log(this.inventorData.inventor_companys, "0000000000000000");
        for (let k in this.inventorData.inventor_companys) {
          var arr_time = this.inventorData.inventor_companys[k]["times"];
          var res = this.getTimeAndCount(arr_time);
          // console.log(res)
          this.companyChartData[k] = res;
          this.companyChartData[k]["name"] =
            this.inventorData.inventor_companys[k]["company_name"];
        }
        // 等待v-for渲染完毕后开始绘制图表
        this.$nextTick(() => {
          this.initCompanyK();
        });
      });
  },
  mounted() {
    this.initMonthWorkOrder();
  },
  methods: {
    arrayMax(arrs) {
      var max = arrs[0];
      for (var i = 1, ilen = arrs.length; i < ilen; i++) {
        if (arrs[i] > max) {
          max = arrs[i];
        }
      }
      return max;
    },
    arrayMin(arrs) {
      var min = arrs[0];
      for (var i = 1, ilen = arrs.length; i < ilen; i++) {
        if (arrs[i] < min) {
          min = arrs[i];
        }
      }
      return min;
    },
    getTimeAndCount(arr) {
      var res = {};
      for (let i = 0; i < arr.length; i++) {
        var year = arr[i].split("-")[0];
        if (year in res) {
          res[year]++;
        } else {
          res[year] = 1;
        }
      }
      var res_arr = {};
      res_arr["time"] = [];
      res_arr["count"] = [];
      for (let k in res) {
        res_arr["time"].push(k);
        res_arr["count"].push(res[k]);
      }
      return res_arr;
    },

    initCompanyK() {
      var companyCharts = this.$refs.companyK;

      // console.log(companyCharts, companyCharts.length);
      for (var i = 0; i < companyCharts.length; i++) {
        console.log("id", companyCharts[i]["id"]);
        console.log(this.companyChartData[id]);
        var id = companyCharts[i]["id"];
        let myChart = this.$echarts.init(companyCharts[i]);
        let options = {
          title: {
            show: true,
            x: "center",
            text: this.companyChartData[id]["name"]+"（"+this.inventorData.inventor_companys[id]["times"].length+"篇)",
            textStyle: {
              // 主标题文本样式{"fontSize": 18,"fontWeight": "bolder","color": "#333"}
              color:"#3e38a3",
              // fontFamily: "Arial",
              // fontSize: 12,
              fontStyle: "normal",
              fontWeight: "800",
            },
          },
          tooltip: {
            backgroundColor: "rgba(204, 221, 255, 0.6)",
            trigger: "axis",
            borderColor: "#CCDDFF",
            textStyle: { color: "#2562DC" },
          },
          color: ["#635df7", "#f15d5d"],
          grid: {
            left: "3%",
            right: "4%",
            bottom: "3%",
            containLabel: true,
          },
          xAxis: [
            {
              type: "category",
              data: this.companyChartData[id]["time"],
              axisTick: {
                alignWithLabel: true,
              },
            },
          ],
          yAxis: [
            {
              type: "value",
              splitLine: {
                show: true,
                lineStyle: {
                  type: "dashed",
                  color: "#D3D8DD",
                },
              },
            },
          ],
          series: [
            {
              name: "专利",
              type: "line",
              barWidth: 10,
              data: this.companyChartData[id]["count"],
              smooth: true,
            },
          ],
        };
        myChart.setOption(options);
      }
    },
  },
  watch: {
    id_public_goods_type: {
      handler(val) {
        // 检测到数据变化
        if (val && val != this.$route.params.id) {
          this.id = val;
          // 刷新页面
          this.$nextTick(this.refresh);
        }
      },
      immediate: true,
    },
  },
};
</script>

<style>
.company-k-wrap {
  width: 600px;
  height: 300px;
  border: 1px solid black;
}
</style>