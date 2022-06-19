<template>
  <div class="centered">
    {{riverData}}
    <!-- {{ inventorData.inventor_categories }} -->
    {{ riverData }}
    <!-- {{ pieData }} -->

    <!-- {{test}} -->
    <!-- {{ companyChartData }} -->
    <!-- <div
      ref="monthWorkOrder"
      class="echarts-box"
      style="width: 600px; height: 300px; border: 1px solid red"
    ></div> -->
    <!-- {{inventorData.inventor_companys}} -->
    <div class="info-wrap base-box">
      <div class="avatar2">
        <img
          src="@/assets/inventor_card/default_avatar.png"
          alt=""
          @click="routerTo(id)"
        />
      </div>
      <div class="info-right">
        <h1>{{ inventorData.inventor_name }}</h1>
        <div class="base-info">
          <p><span class="el-icon-user-solid"></span>id:{{ this.id }}</p>
          <p><span class="el-icon-info"></span>发明人</p>
        </div>
        <div
          v-for="(item, index) in companyList"
          :key="index"
          class="company-wrap"
        >
          <p>
            <span class="el-icon-office-building"></span>
            {{ item.start_time }} 至 {{ item.end_time }}
            {{ item.company_name[0] }}（贡献专利{{ item.num }}篇）
          </p>
        </div>
        <div class="score-wrap">
          <div class="number-wrap">
            <div class="star-wrap"><img src="@/assets/star.png" alt="" /></div>
            <div class="num-info-wrap">
              <p>
                专利申请数量<span
                  class="el-icon-question small-title"
                  title="系统中专利数据"
                ></span>
              </p>
              <p>
                <span class="number">{{
                  inventorData.inventor_patents_totalnum
                }}</span
                >件
              </p>
            </div>
          </div>
          <div class="number-wrap">
            <div class="star-wrap"><img src="@/assets/star.png" alt="" /></div>
            <div class="num-info-wrap">
              <p>
                发明人评分<span
                  class="el-icon-question small-title"
                  title="模型根据数据生成的人才评分"
                ></span>
              </p>
              <p>
                <span class="number">{{ inventorData.T_index }}</span>
              </p>
            </div>
          </div>
          <div class="number-wrap">
            <div class="star-wrap"><img src="@/assets/star.png" alt="" /></div>
            <div class="num-info-wrap">
              <p>
                专利分数<span
                  class="el-icon-question small-title"
                  title="全部专利平均分"
                ></span>
              </p>
              <p>
                <span class="number">{{ inventorData.average_score }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-row :gutter="0" class="">
      <el-col :xs="16" :sm="16" :md="16" :lg="16" :xl="16">
        <div class="base-box">
          <h2><span class="el-icon-aim"></span> 技术领域</h2>
          <div class="category-wrap">
            <div v-for="(item, index) in pieData" :key="index">
              <p>{{ item.name }}({{ item.value }})</p>
            </div>
          </div>
        </div>
        <div class="base-box">
          <h2><span class="el-icon-data-line"></span> 可视分析</h2>
          <div class="echarts-wrap">
            <div
              ref="ipcRiver"
              class="river-wrap charts-base"
              :style="{
                'background-image': `url(${require('@/assets/chart_bg.png')})`,
              }"
            ></div>
            <div class="radar-and-pie">
              <div
                ref="scoreRadar"
                class="radar-wrap charts-base"
                :style="{
                  'background-image': `url(${require('@/assets/chart_bg.png')})`,
                }"
              ></div>
              <div
                ref="ipcPie"
                class="pie-wrap charts-base"
                :style="{
                  'background-image': `url(${require('@/assets/chart_bg.png')})`,
                }"
              ></div>
            </div>
            <div
              ref="collaboratorGraphData"
              class="collaborator-graph-wrap charts-base"
              :style="{
                'background-image': `url(${require('@/assets/chart_bg.png')})`,
              }"
            ></div>
          </div>
        </div>
        <div class="base-box">
          <h2><span class="el-icon-data-line"></span> 专利k线</h2>
          <div class="echarts-wrap">
            <div v-for="(item, index) in companyList" :key="index">
              <div
                ref="companyK"
                class="company-k-wrap charts-base"
                :style="{
                  'background-image': `url(${require('@/assets/chart_bg.png')})`,
                }"
                :id="String(item.id)"
              ></div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
        <div class="base-box page-right-wrap">
          <h2>合作列表</h2>
          <!-- {{ collaboratorList }} -->
          <p v-if="collaboratorList.length == 0">暂无数据</p>
          <div>
            <div v-for="(item, index2) in collaboratorList" :key="index2">
              <colCard :id="item.id"></colCard>
              <!-- <p>{{ item.name }} : {{ item.num }}</p> -->
            </div>
          </div>
        </div>
        <div class="base-box page-right-wrap">
          <h2>关键词</h2>
          <p v-if="JSON.stringify(inventorData.inventor_categories) == '{}'">
            暂无数据
          </p>
          <div
            v-for="(item, index) in inventorData.inventor_categories"
            :key="index"
          >
            <!-- <p v-if="item.category_name.substr(0,7)!='inside_'">{{ item.category_name }}({{ item.time.length }})</p> -->
            <p>{{ item.category_name }}({{ item.time.length }})</p>
          </div>
        </div>
      </el-col>
    </el-row>
<!-- 
    <p>专利列表</p>
    <div v-for="(item, index) in inventorData.patents_ids" :key="index">
      <p>专利id：{{ item }}</p>
    </div>
    <p>ipc分类信息</p>
    <div v-for="(item, index) in inventorData.patents_ipcs" :key="index">
      <p>ipc号：{{ index }} 发表{{ item.time.length }}次 {{ item.ipc_info }}</p>
    </div> -->
  </div>
</template>

<script>
import colCard from "../inventorPage/colCard.vue";

export default {
  name: "Inventor",
  components: {
    colCard,
  },
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
      riverData: [],
      riverLegend: [],
      ipcInfo: {},
      pieData: [],
    };
  },
  created() {
    this.$axios
      .get("http://127.0.0.1:5000/inventor_info_all", {
        params: {
          id: this.id,
        },
      })
      .then(async (response) => {
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
        for (var key in this.inventorData.inventor_categories) {
          console.log(
            "kkk",
            this.inventorData.inventor_categories[key]["category_name"]
          );
          if (
            this.inventorData.inventor_categories[key]["category_name"].substr(
              0,
              7
            ) == "inside_"
          ) {
            delete this.inventorData.inventor_categories[key];
          }
        }
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

        // 构建合作者网络节点图数据
        this.collaboratorGraphData["node"].push({
          category: 0,
          value: 10,
          label: this.inventorData.inventor_name,
          name: this.inventorData.inventor_id,
        }); // 加入中心节点
        for (var i = 0; i < this.collaboratorList.length; i++) {
          this.collaboratorGraphData["node"].push({
            category: i + 1,
            value: this.collaboratorList[i]["num"],
            label: this.collaboratorList[i]["name"],
            name: this.collaboratorList[i]["id"],
          });
          this.collaboratorGraphData["link"].push({
            source: 0,
            target: i + 1,
            value: this.collaboratorList[i]["num"],
            label: "合作者",
          });
        }
        console.log(this.collaboratorGraphData);

        // 同步请求ipc分类信息数据，进而构造河流图数据
        await this.$axios
          .get("http://127.0.0.1:5000/ipc_category_info")
          .then((response) => {
            // this.ipcInfo = response.data
            for (let i = 0; i < response.data.length; i++) {
              this.riverLegend.push(
                response.data[i].ipc_category +
                  response.data[i].ipc_category_info
              );
              // console.log(this.riverLegend);
              if (!(response.data[i].ip_category in this.ipcInfo)) {
                this.ipcInfo[response.data[i].ipc_category] =
                  response.data[i].ipc_category_info;
              }
            }
            // console.log(this.ipcInfo);

            // 构造河流图数据
            var riverDataDic = {};
            for (let i in this.inventorData.patents_ipcs) {
              var fw = i.slice(0, 1);
              fw += this.ipcInfo[fw];
              if (fw in riverDataDic) {
                riverDataDic[fw] = riverDataDic[fw].concat(
                  this.inventorData.patents_ipcs[i]["time"]
                );
              } else {
                riverDataDic[fw] = this.inventorData.patents_ipcs[i]["time"];
              }
            }
            // this.riverData = riverDataDic
            // console.log(riverDataDic);

            for (var i in riverDataDic) {
              this.pieData.push({ name: i, value: riverDataDic[i].length }); //顺路构造饼图数据
              var currentIpcDic = {};
              for (let n = 0; n < riverDataDic[i].length; n++) {
                if (riverDataDic[i][n].slice(0, 4) in currentIpcDic) {
                  currentIpcDic[riverDataDic[i][n].slice(0, 4)] += 1;
                } else {
                  currentIpcDic[riverDataDic[i][n].slice(0, 4)] = 1;
                }
              }
              for (let k in currentIpcDic) {
                this.riverData.push([k, currentIpcDic[k], i]);
              }
            }
            this.pieData = this.pieData.sort((a, b) => b.value - a.value);

            // console.log(this.pieData);
          });

        // 等待v-for渲染完毕后开始绘制图表
        this.$nextTick(() => {
          this.initCompanyK();
          this.initCollaboratorGraph();
          this.initIpcRiver();
          this.initIpcPie();
          this.initRadar();
        });
      });
  },
  mounted() {
    // this.initMonthWorkOrder();
  },
  methods: {
    getNumScore(n) {
      let score_num = 0;
      if (n == 0) {
        score_num = 0;
      } else if (n <= 2) {
        score_num = 10;
      } else if (n <= 5) {
        score_num = 20;
      } else if (n <= 10) {
        score_num = 30;
      } else if (n <= 20) {
        score_num = 40;
      } else if (n <= 30) {
        score_num = 50;
      } else if (n <= 40) {
        score_num = 60;
      } else if (n <= 50) {
        score_num = 70;
      } else if (n <= 70) {
        score_num = 80;
      } else if (n <= 100) {
        score_num = 90;
      } else {
        score_num = 100;
      }
      return score_num;
    },
    routerTo(id) {
      console.log("tettttt");
      this.$router.push("/inventor/" + id);
    },
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
        // console.log("id", companyCharts[i]["id"]);
        // console.log(this.companyChartData[id]);
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
            trigger: "axis",
            backgroundColor: "rgba(204, 221, 255, 0.6)",
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
        window.addEventListener("resize", () => {
          myChart.resize();
        });
      }
    },

    initCollaboratorGraph() {
      let myChart = this.$echarts.init(this.$refs.collaboratorGraphData);
      let options = {
        title: {
          text: this.inventorData.inventor_name + "合作者网络图",
          // subtext: "Fake Data",
          left: "center",
          textStyle: {
            color: "#3e38a3",
            // fontFamily: "Arial",
            // fontSize: 12,
            fontStyle: "normal",
            fontWeight: "800",
          },
        },
        tooltip: {
          //提示框，鼠标悬浮交互时的信息提示
          trigger: "item", //数据触发类型
          backgroundColor: "rgba(204, 221, 255, 0.6)",
          borderColor: "#CCDDFF",
          textStyle: { color: "#2562DC" },
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
        // color: ["rgb(194,53,49)", "rgb(178,144,137)", "rgb(97,160,168)"],
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
            // focusNodeAdjacency: false, //当鼠标移动到节点上，突出显示节点以及节点的边和邻接节点
            roam: false, //是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
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
      window.addEventListener("resize", () => {
        myChart.resize();
      });
      var that = this;
      myChart.on("click", function (param) {
        if (param.dataType == "node") {
          console.log("点击了节点", param);
          console.log("点击了节点", param.name);
          that.routerTo(param.name);
        } else {
          console.log("点击了边", param);
        }
      });
    },

    initIpcRiver() {
      let myChart = this.$echarts.init(this.$refs.ipcRiver);
      let options = {
        title: {
          text: this.inventorData.inventor_name + "研究领域河流图",
          // subtext: "Fake Data",
          left: "center",
          textStyle: {
            color: "#3e38a3",
            // fontFamily: "Arial",
            // fontSize: 12,
            fontStyle: "normal",
            fontWeight: "800",
          },
        },
        tooltip: {
          trigger: "axis",
          backgroundColor: "rgba(204, 221, 255, 0.9)",
          borderColor: "#CCDDFF",
          textStyle: { color: "#2562DC" },
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
          data: this.riverLegend,
          orient: "vertical",

          // left: "left",
          bottom: "bottom",
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
            data: this.riverData,
          },
        ],
      };
      myChart.setOption(options);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initIpcPie() {
      let myChart = this.$echarts.init(this.$refs.ipcPie);
      let options = {
        title: {
          text: this.inventorData.inventor_name + "研究领域分布",
          // subtext: "Fake Data",
          left: "center",
          textStyle: {
            color: "#3e38a3",
            // fontFamily: "Arial",
            // fontSize: 12,
            fontStyle: "normal",
            fontWeight: "800",
          },
        },
        tooltip: {
          trigger: "item",
          backgroundColor: "rgba(204, 221, 255, 0.9)",
          borderColor: "#CCDDFF",
          textStyle: { color: "#2562DC" },
        },
        legend: {
          type: "scroll",
          // orient: "vertical",
          // left: "left",
          bottom: "bottom",
        },
        series: [
          {
            name: "Access From",
            type: "pie",
            radius: ["0%", "50%"],
            itemStyle: {
              borderRadius: 5,
              borderColor: "#fff",
              borderWidth: 1,
            },
            data: this.pieData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.1)",
              },
            },
          },
        ],
      };

      myChart.setOption(options);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initRadar() {
      let myChart = this.$echarts.init(this.$refs.scoreRadar);
      let options = {
        title: {
          text: this.inventorData.inventor_name + "评分雷达",
          // subtext: "Fake Data",
          left: "center",
          textStyle: {
            color: "#3e38a3",
            // fontFamily: "Arial",
            // fontSize: 12,
            fontStyle: "normal",
            fontWeight: "800",
          },
        },

        // legend: {
        //   data: ["thomas"],
        // },
        radar: {
          // shape: 'circle',
          indicator: [
            { name: "综合评分", max: 100 },
            { name: "专利质量评分", max: 100 },
            { name: "专利数量评分", max: 100 },
          ],
          radius: 100,
          center: ["50%", "60%"],
          axisName: {
            color: "rgb(0, 0, 0)",
          },
        },

        series: [
          {
            name: "Budget vs spending",
            type: "radar",
            data: [
              {
                value: [
                  this.inventorData.T_index,
                  this.inventorData.average_score,
                  this.getNumScore(this.inventorData.inventor_patents_totalnum),
                ],
                name: "thomas",
              },
            ],
          },
        ],
      };
      myChart.setOption(options);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
  },
  watch: {
    $route: {
      handler(val, oldval) {
        // console.log(val);//新路由信息
        // console.log(oldval);//老路由信息
        this.id = this.$route.query.id;
        this.$router.go(0); //页面刷新
      },
      // 深度观察监听
      deep: true,
    },
  },
};
</script>

<style>
/* echarts 容器样式 */
.charts-base {
  /* margin: 20px 0; */
  background-color: #e4f1ff;
  background-repeat: no-repeat;
  background-size: 100% 100%;
  -webkit-box-shadow: 0 1px 0 0 rgb(69 70 73 / 50%),
    0 1px 4px 0 hsl(0deg 0% 77% / 50%);
  box-shadow: 0 1px 0 0 rgb(69 70 73 / 50%), 0 1px 4px 0 hsl(0deg 0% 77% / 50%);
  border-radius: 4px;
}
.radar-wrap {
  width: 49%;
  height: 300px;
}
.pie-wrap {
  width: 49%;
  height: 300px;
}
.company-k-wrap {
  margin: 20px 0;
  width: 100%;
  height: 300px;
  /* border: 1px solid black; */
}
.collaborator-graph-wrap {
  width: 100%;
  height: 550px;
  /* border: 1px solid black; */
}
.river-wrap {
  width: 100%;
  height: 300px;
  /* background-image:url("../assets/chart_bg.png"); */
  /* border: 1px solid black; */
}

/* 页面布局样式 */
.info-wrap {
  display: flex;
}
.base-box {
  border: 1px solid #dadada;
  /* background-color: rgba(253, 252, 241, 0.719); */
  margin: 10px;
  padding: 15px;
  border-radius: 2px;
  box-shadow: 0px 0px 5px 3px rgba(224, 224, 224, 0.4);
}

/* 人物头像 */
.avatar2 {
  max-width: 100px;
  padding-right: 10px;
}
.avatar2 img {
  width: 100%;
  cursor: pointer;
  border-radius: 2px;
}

.info-right {
  display: flex;
  flex-direction: column;
}

/* .company-wrap {
  margin-bottom: 5px;
} */

.base-info {
  display: flex;
  flex-direction: row;
  margin: 5px 0;
}
.base-info > p {
  margin-right: 20px;
}

.score-wrap {
  display: flex;
  flex-direction: row;
}
.number-wrap {
  margin: 5px 10px;
  display: flex;
  padding: 10px 30px;
  flex-direction: row;
  border-radius: 5px;
  background-color: rgb(255, 238, 205);
  border: 1px solid rgb(253, 227, 212);
  box-shadow: 0px 0px 5px 3px rgb(224, 224, 224);
}
.num-info-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.star-wrap {
  max-width: 50px;
  margin-right: 8px;
  /* margin: 10px; */
}
.star-wrap img {
  width: 50px;
}
.number {
  font-size: 20px;
  font-weight: 700;
  color: rgb(255, 110, 25);
}
.small-title {
  cursor: pointer;
}
.category-wrap {
  margin: 20px 0;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  /* width: 80%; */
}
.category-wrap > div {
  margin: 10px 10px;
  padding: 5px 20px;
  border-radius: 20px;
  background-color: rgba(196, 200, 255, 0.349);
}
.page-right-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  /* justify-content: center; */
  max-height: 1470px;
  overflow: auto;
}
.page-right-wrap > h2 {
  padding: 10px 30%;
  margin: 10px;
  border-bottom: 1px solid rgb(160, 160, 160);
}
.echarts-wrap {
  margin: 20px;
}
.radar-and-pie {
  margin: 20px 0;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  /* color: rgb(0, 0, 0); */
}
</style>