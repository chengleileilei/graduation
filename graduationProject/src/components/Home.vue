<template>
  <div class="centered">
    <h1 class="home-first-tit">基于专利数据的人才画像系统</h1>
    <!-- <h2>This is 首页 page!</h2> -->
    <!-- <Card :id="1" score = "100"></Card> -->
    <!-- <p>{{ ipcData }}</p> -->
    <el-row :gutter="20" class="centered">
      <el-col
        :xs="24"
        :sm="12"
        :md="12"
        :lg="12"
        :xl="12"
        v-for="(ipcInfo, index) in ipcData"
        :key="index"
        class="card-wrap"
      >
        <div class="card">
          <!-- <img :src="card.logo_src" alt="" class="card-logo" /> -->
          <p class="card-tit1">{{ ipcInfo.ipc_category }}</p>
          <p class="card-tit2">
            {{ ipcInfo.ipc_category_info }}
          </p>
          <div class="ipc-ivnentor-wrap">
            <div
              v-for="(inventorInfo, index) in ipcInfo.top_inventors"
              :key="index"
              class="ipc-inventor"
              @click="routerTo(inventorInfo.id)"
            >
              <Card :id="inventorInfo.id" :score="inventorInfo.score"></Card>

              <!-- <p>id：{{ inventorInfo.id }}</p> -->
              <!-- <p>评分：{{ inventorInfo.score }}</p> -->
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Card from "./homeSub/IpcCard.vue";
export default {
  name: "home",
  components: {
    Card,
  },
  data() {
    return {
      ipcData: "",
      // data: "this.data",
    };
  },
  created() {},
  mounted() {
    this.$axios
      .get("http://127.0.0.1:5000/ipc_category_info")
      .then((response) => {
        this.ipcData = response.data;
        for (let i = 0; i < this.ipcData.length; i++) {
          var res = JSON.parse(this.ipcData[i].top_inventors);
          var res_dic = [];

          for (let id in res) {
            res_dic.push({ id: id, score: res[id] });
          }

          // 根据评分排序
          this.ipcData[i].top_inventors = res_dic.sort(
            (a, b) => b.score - a.score
          );
        }
      });
  },
  methods: {
    routerTo(id) {
      this.$router.push("/inventor/" + id);
    },
    // async getInventorInfo(inventor_id) {
    //   var res = await this.$axios.get(
    //     "http://127.0.0.1:5000/inventor_info_brief",
    //     {
    //       params: {
    //         id: inventor_id,
    //       },
    //     }
    //   );
    //   // console.log(res.data);
    //   return res.data;
    // },
  },
};
</script>

<style>
.home-first-tit{
  text-align: center;
  margin: 20px;
}
.card {
  max-width: 527px;
  /* width: 527px; */
  /* height: 339px; */
  margin: 0 auto;
  padding: 30px;
  background-color: white;
  box-shadow: 0px 0px 10px 5px rgba(230, 222, 222, 0.4);
  border-radius: 2px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
}
.card-wrap {
  margin-bottom: 40px;
}
.card-logo {
  width: 120px;
  height: 120px;
}
.card-tit1 {
  font-size: 32px;
}
.card-tit2 {
  font-size: 20px;
  /* text-indent: 2em; */
  text-align: left;
}

.ipc-inventor-wrap {
  display: flex;
  flex-direction: column;
}

.ipc-inventor {
  cursor: pointer;
  margin: 10px;
  display: flex;
  flex-direction: row;
}
.ipc-inventor p {
  float: left;
  margin: 5px;
}
</style>