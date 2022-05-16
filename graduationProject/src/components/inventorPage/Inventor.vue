<template>
  <div class="centered">
    <p>{{ this.id }}</p>

    <p>姓名：{{ data.inventor_name }}</p>
    <!-- <p>公司：{{ data.inventor_companys }}</p> -->
    <p>公司</p>
    <div v-for="(item, index) in companyList" :key="index">
      <p>
        {{ item.company_name[0] }} {{ item.start_time }}-{{
          item.end_time
        }}
        贡献专利{{ item.num }}篇
      </p>
    </div>
    <p>专利数量：{{ data.inventor_patents_totalnum }}</p>
    <p>专利质量综合评分：{{ data.average_score }}</p>
    <p>发明家质量综合评分：{{ data.T_index }}</p>
    <!-- <p>合作者：{{data.collaborators}}</p> -->
    <div v-for="(item, index) in collaboratorList" :key="index">
      <p>{{ item.name }} : {{ item.num }}</p>
    </div>
    <p>研究领域</p>
    <div v-for="(item, index) in data.inventor_categories" :key="index">
      <p>{{ item.category_name }}:{{ item.time.length }}</p>
    </div>
    <p>专利列表</p>
    <div v-for="(item, index) in data.patents_ids" :key="index">
      <p>专利id：{{ item }}</p>
    </div>
    <p>ipc分类信息</p>
    <div v-for="(item, num) in data.patents_ipcs" :key="num">
      <p>ipc号：{{ num }} 发表{{ item.time.length }}次 {{ item.ipc_info }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Inventor",
  data() {
    return {
      id: this.$route.params.id,
      data: {},
      companyList: [],
      collaboratorList: [],
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
        this.data = response.data;
        // console.log(this.data)
        this.data.T_index = parseFloat(this.data.T_index).toFixed(2);
        this.data.average_score = parseFloat(this.data.average_score).toFixed(
          2
        );
        this.data.inventor_companys = JSON.parse(this.data.inventor_companys);
        for (var key in this.data.inventor_companys) {
          this.companyList.push({
            id: key,
            company_name: this.data.inventor_companys[key]["company_name"],
            time: this.data.inventor_companys[key]["times"],
            end_time: this.arrayMax(this.data.inventor_companys[key]["times"]),
            start_time: this.arrayMin(
              this.data.inventor_companys[key]["times"]
            ),
            num: this.data.inventor_companys[key]["patents_num"],
          });
        }
        // console.log(this.companyList);
        this.data.collaborators = JSON.parse(this.data.collaborators);
        for (var key in this.data.collaborators) {
          this.collaboratorList.push({
            id: key,
            name: this.data.collaborators[key]["name"],
            num: this.data.collaborators[key]["times"].length,
            patents: this.data.collaborators[key]["patent_ids"],
          });
        }
        // console.log(this.collaboratorList);

        this.collaboratorList = this.collaboratorList.sort(
          (a, b) => b.num - a.num
        );
        this.companyList = this.companyList.sort((a, b) => b.num - a.num);
        this.data.inventor_categories = JSON.parse(
          this.data.inventor_categories
        );
        this.data.patents_ids = JSON.parse(this.data.patents_ids);
        this.data.patents_ipcs = JSON.parse(this.data.patents_ipcs);
        // console.log(this.data.inventor_categories)
      });
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
  },
};
</script>

<style>
</style>