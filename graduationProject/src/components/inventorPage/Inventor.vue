<template>
  <div class="centered">
    {{ inventorData.patents_ipcs }}
    <div ref="ipcRiver" class="river-wrap"></div>

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

    <!-- 合作者 -->
    <h1>合作者</h1>
    <!-- {{ collaboratorGraphData.node }} -->
    <!-- <br /> -->
    <!-- {{ collaboratorGraphData.link }} -->
    <div ref="collaboratorGraphData" class="collaborator-graph-wrap"></div>
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
      collaboratorGraphData: {
        node: [
          // { category: 0,  value: 5, label: "乔布斯" },
          // { category: 1,value: 2, label: "丽萨" },
        ],
        link: [
          // { source: 0, target: 1, value: 1, label: "合作者" },
          // { source: 0, target: 1, value: 5, label: "女儿" }
        ],
      },
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

        // 构建company 专利k线图数据 companyChartData
        for (let k in this.inventorData.inventor_companys) {
          var arr_time = this.inventorData.inventor_companys[k]["times"];
          var res = this.getTimeAndCount(arr_time);
          // console.log(res)
          this.companyChartData[k] = res;
          this.companyChartData[k]["name"] =
            this.inventorData.inventor_companys[k]["company_name"];
        }

        // 构建合作者网络图数据
        this.collaboratorGraphData["node"].push({
          category: 0,
          value: 10,
          label: this.inventorData.inventor_name,
          name: this.inventorData.inventor_name,
        }); // 加入中心节点
        for (var i = 0; i < this.collaboratorList.length; i++) {
          this.collaboratorGraphData["node"].push({
            category: i + 1,
            value: this.collaboratorList[i]["num"],
            label: this.collaboratorList[i]["name"],
            name: this.collaboratorList[i]["name"],
          });
          this.collaboratorGraphData["link"].push({
            source: 0,
            target: i + 1,
            value: this.collaboratorList[i]["num"],
            label: "合作者",
          });
        }
        console.log(this.collaboratorGraphData);

        // 等待v-for渲染完毕后开始绘制图表
        this.$nextTick(() => {
          this.initCompanyK();
          this.initCollaboratorGraph();
          this.initIpcRiver();
        });
      });
  },
  mounted() {
    // this.initMonthWorkOrder();
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
            text:
              this.companyChartData[id]["name"] +
              "（" +
              this.inventorData.inventor_companys[id]["times"].length +
              "篇)",
            textStyle: {
              // 主标题文本样式{"fontSize": 18,"fontWeight": "bolder","color": "#333"}
              color: "#3e38a3",
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

    initCollaboratorGraph() {
      let myChart = this.$echarts.init(this.$refs.collaboratorGraphData);
      let options = {
        title: {
          text: "人际关系网络图", //标题

          top: "top", //相对在y轴上的位置
          left: "center", //相对在x轴上的位置
        },
        tooltip: {
          //提示框，鼠标悬浮交互时的信息提示
          trigger: "item", //数据触发类型
          formatter: function (params) {
            //触发之后返回的参数，这个函数是关键
            if (params.data.category != undefined) {
              //如果触发节点
              return "合作数量:" + params.data.value; //返回标签
            } else {
              //如果触发边
              return "关系:" + params.data.label;
            }
          },
        },
        //工具箱，每个图表最多仅有一个工具箱
        toolbox: {
          show: true,
          feature: {
            //启用功能
            //dataView数据视图，打开数据视图，可设置更多属性,readOnly 默认数据视图为只读(即值为true)，可指定readOnly为false打开编辑功能
            dataView: { show: true, readOnly: true },
            restore: { show: true }, //restore，还原，复位原始图表
            saveAsImage: { show: true }, //saveAsImage，保存图片
          },
        },
        //全局颜色，图例、节点、边的颜色都是从这里取，按照之前划分的种类依序选取
        color: ["rgb(194,53,49)", "rgb(178,144,137)", "rgb(97,160,168)"],
        //图例，每个图表最多仅有一个图例
        // legend: [{
        //   x: 'left',//图例位置
        //   //图例的名称，这里返回短名称，即不包含第一个，当然你也可以包含第一个，这样就可以在图例中选择主干人物
        //   data: graph.categoriesshort.map(function (a) {
        //           return a.name;
        //       })
        // }],
        //sereis的数据: 用于设置图表数据之用
        series: [
          {
            name: "人际关系网络图", //系列名称
            type: "graph", //图表类型
            layout: "force", //echarts3的变化，force是力向图，circular是和弦图
            draggable: true, //指示节点是否可以拖动
            data: this.collaboratorGraphData["node"], //节点数据
            edges: this.collaboratorGraphData["link"], //边、联系数据
            // categories: graph.categories,//节点种类
            focusNodeAdjacency: true, //当鼠标移动到节点上，突出显示节点以及节点的边和邻接节点
            roam: true, //是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            label: {
              //图形上的文本标签，可用于说明图形的一些数据信息
              normal: {
                show: true, //显示
                position: "right", //相对于节点标签的位置
                //回调函数，你期望节点标签上显示什么
                formatter: function (params) {
                  return params.data.label;
                },
              },
            },
            symbolSize: (value, params) => {
              return value;
            },
            //节点的style
            itemStyle: {
              normal: {
                opacity: 0.9, //设置透明度为0.8，为0时不绘制
              },
            },
            // 关系边的公用线条样式
            lineStyle: {
              normal: {
                show: true,
                color: "target", //决定边的颜色是与起点相同还是与终点相同
                curveness: 0.1, //边的曲度，支持从 0 到 1 的值，值越大曲度越大。
              },
            },
            force: {
              edgeLength: [100, 200], //线的长度，这个距离也会受 repulsion，支持设置成数组表达边长的范围
              repulsion: 100, //节点之间的斥力因子。值越大则斥力越大
            },
          },
        ],
      };
      myChart.setOption(options);
    },
    initIpcRiver() {
      let myChart = this.$echarts.init(this.$refs.ipcRiver);
      let options = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "line",
            lineStyle: {
              color: "rgba(0,0,0,0.2)",
              width: 1,
              type: "solid",
            },
          },
        },
        legend: {
          data: ["DQ", "TY", "SS", "QG", "SY", "DD"],
        },
        singleAxis: {
          top: 50,
          bottom: 50,
          axisTick: {},
          axisLabel: {},
          type: "time",
          axisPointer: {
            animation: true,
            label: {
              show: true,
            },
          },
          splitLine: {
            show: true,
            lineStyle: {
              type: "dashed",
              opacity: 0.2,
            },
          },
        },
        series: [
          {
            type: "themeRiver",
            emphasis: {
              itemStyle: {
                shadowBlur: 20,
                shadowColor: "rgba(0, 0, 0, 0.8)",
              },
            },
            data: [
              ["2015/11/08", 10, "DQ"],
              ["2015/11/09", 15, "DQ"],
              ["2015/11/10", 35, "DQ"],
              ["2015/11/11", 38, "DQ"],
              ["2015/11/12", 22, "DQ"],
              ["2015/11/13", 16, "DQ"],
              ["2015/11/14", 7, "DQ"],
              ["2015/11/15", 2, "DQ"],
              ["2015/11/16", 17, "DQ"],
              ["2015/11/17", 33, "DQ"],
              ["2015/11/18", 40, "DQ"],
              ["2015/11/19", 32, "DQ"],
              ["2015/11/20", 26, "DQ"],
              ["2015/11/21", 35, "DQ"],
              ["2015/11/22", 40, "DQ"],
              ["2015/11/23", 32, "DQ"],
              ["2015/11/24", 26, "DQ"],
              ["2015/11/25", 22, "DQ"],
              ["2015/11/26", 16, "DQ"],
              ["2015/11/27", 22, "DQ"],
              ["2015/11/28", 10, "DQ"],
              ["2015/11/08", 35, "TY"],
              ["2015/11/09", 36, "TY"],
              ["2015/11/10", 37, "TY"],
              ["2015/11/11", 22, "TY"],
              ["2015/11/12", 24, "TY"],
              ["2015/11/13", 26, "TY"],
              ["2015/11/14", 34, "TY"],
              ["2015/11/15", 21, "TY"],
              ["2015/11/16", 18, "TY"],
              ["2015/11/17", 45, "TY"],
              ["2015/11/18", 32, "TY"],
              ["2015/11/19", 35, "TY"],
              ["2015/11/20", 30, "TY"],
              ["2015/11/21", 28, "TY"],
              ["2015/11/22", 27, "TY"],
              ["2015/11/23", 26, "TY"],
              ["2015/11/24", 15, "TY"],
              ["2015/11/25", 30, "TY"],
              ["2015/11/26", 35, "TY"],
              ["2015/11/27", 42, "TY"],
              ["2015/11/28", 42, "TY"],
              ["2015/11/08", 21, "SS"],
              ["2015/11/09", 25, "SS"],
              ["2015/11/10", 27, "SS"],
              ["2015/11/11", 23, "SS"],
              ["2015/11/12", 24, "SS"],
              ["2015/11/13", 21, "SS"],
              ["2015/11/14", 35, "SS"],
              ["2015/11/15", 39, "SS"],
              ["2015/11/16", 40, "SS"],
              ["2015/11/17", 36, "SS"],
              ["2015/11/18", 33, "SS"],
              ["2015/11/19", 43, "SS"],
              ["2015/11/20", 40, "SS"],
              ["2015/11/21", 34, "SS"],
              ["2015/11/22", 28, "SS"],
              ["2015/11/23", 26, "SS"],
              ["2015/11/24", 37, "SS"],
              ["2015/11/25", 41, "SS"],
              ["2015/11/26", 46, "SS"],
              ["2015/11/27", 47, "SS"],
              ["2015/11/28", 41, "SS"],
              ["2015/11/08", 10, "QG"],
              ["2015/11/09", 15, "QG"],
              ["2015/11/10", 35, "QG"],
              ["2015/11/11", 38, "QG"],
              ["2015/11/12", 22, "QG"],
              ["2015/11/13", 16, "QG"],
              ["2015/11/14", 7, "QG"],
              ["2015/11/15", 2, "QG"],
              ["2015/11/16", 17, "QG"],
              ["2015/11/17", 33, "QG"],
              ["2015/11/18", 40, "QG"],
              ["2015/11/19", 32, "QG"],
              ["2015/11/20", 26, "QG"],
              ["2015/11/21", 35, "QG"],
              ["2015/11/22", 40, "QG"],
              ["2015/11/23", 32, "QG"],
              ["2015/11/24", 26, "QG"],
              ["2015/11/25", 22, "QG"],
              ["2015/11/26", 16, "QG"],
              ["2015/11/27", 22, "QG"],
              ["2015/11/28", 10, "QG"],
              ["2015/11/08", 10, "SY"],
              ["2015/11/09", 15, "SY"],
              ["2015/11/10", 35, "SY"],
              ["2015/11/11", 38, "SY"],
              ["2015/11/12", 22, "SY"],
              ["2015/11/13", 16, "SY"],
              ["2015/11/14", 7, "SY"],
              ["2015/11/15", 2, "SY"],
              ["2015/11/16", 17, "SY"],
              ["2015/11/17", 33, "SY"],
              ["2015/11/18", 40, "SY"],
              ["2015/11/19", 32, "SY"],
              ["2015/11/20", 26, "SY"],
              ["2015/11/21", 35, "SY"],
              ["2015/11/22", 4, "SY"],
              ["2015/11/23", 32, "SY"],
              ["2015/11/24", 26, "SY"],
              ["2015/11/25", 22, "SY"],
              ["2015/11/26", 16, "SY"],
              ["2015/11/27", 22, "SY"],
              ["2015/11/28", 10, "SY"],
              ["2015/11/08", 10, "DD"],
              ["2015/11/09", 15, "DD"],
              ["2015/11/10", 35, "DD"],
              ["2015/11/11", 38, "DD"],
              ["2015/11/12", 22, "DD"],
              ["2015/11/13", 16, "DD"],
              ["2015/11/14", 7, "DD"],
              ["2015/11/15", 2, "DD"],
              ["2015/11/16", 17, "DD"],
              ["2015/11/17", 33, "DD"],
              ["2015/11/18", 4, "DD"],
              ["2015/11/19", 32, "DD"],
              ["2015/11/20", 26, "DD"],
              ["2015/11/21", 35, "DD"],
              ["2015/11/22", 40, "DD"],
              ["2015/11/23", 32, "DD"],
              ["2015/11/24", 26, "DD"],
              ["2015/11/25", 22, "DD"],
              ["2015/11/26", 16, "DD"],
              ["2015/11/27", 22, "DD"],
              ["2015/11/28", 10, "DD"],
            ],
          },
        ],
      };
      myChart.setOption(options);
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
.collaborator-graph-wrap {
  width: 800px;
  height: 600px;
  border: 1px solid black;
}
.river-wrap {
  width: 800px;
  height: 600px;
  border: 1px solid black;
}
</style>