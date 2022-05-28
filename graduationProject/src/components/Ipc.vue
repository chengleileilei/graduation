<template>
  <div>
    <!-- <h2>This is 人才统计 page!</h2> -->
    <el-container>
      <el-aside width="200px" class="ipc-menu">
        <p class="aside-tit">分类</p>
        <!-- <div v-for="(item, index) in ipcData" :key="index">
          <div @click="changeCurrentWord(index)" class="ipc-router-wrap">
            <p>{{ item.ipc_category }} {{ item.ipc_category_info }}</p>
          </div>
        </div> -->

        <div v-for="(item, index) in ipcData" :key="index">
          <!-- {{index}} -->
          <div
            @click="changeCurrentWord(index)"
            :class="{
              'aside-button-wrap': 1,
              'active-aside-button-wrap': currentIndex == index,
            }"
          >
            <p
              :class="{
                'aside-button-text': 1,
                'active-aside-button-text': currentIndex == index,
              }"
            >
              {{ item.ipc_category }} {{ item.ipc_category_info }}
            </p>
          </div>
        </div>
      </el-aside>
      <el-main class="ipc-main">
        <IpcMain
          :topData="ipcData[currentIndex]"
          :key="new Date().getTime()"
        ></IpcMain>
        <!-- 传入一个变化参数作为key，让组件及时进行数据更新 -->
        <!-- <router-view /> -->
      </el-main>
    </el-container>
    <!-- <p>{{ ipcData }}</p> -->
  </div>
</template>

<script>
import IpcMain from "./ipcSub/IpcMain.vue";

export default {
  name: "ipc",
  components: {
    IpcMain,
  },
  data() {
    return {
      ipcData: "",
      currentIndex: 0,
    };
  },
  created() {
    this.$axios
      .get("http://127.0.0.1:5000/ipc_category_info")
      .then((response) => {
        this.ipcData = response.data;
        // console.log(this.ipcData);
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
        console.log(this.ipcData);
      });
  },
  methods: {
    changeCurrentWord(aindex) {
      this.currentIndex = aindex;

      // console.log('cccc')
    },
  },
};
</script>

<style>
.ipc-menu {
  background-color: #f8f8f8;
}
.ipc-main {
  /* border: solid 1px yellowgreen; */
  /* max-height: 1000px; */
}
.aside-tit {
  text-align: center;
  font-size: 26px;
  font-weight: 700;
  color: #3e38a3;
}
.aside-button-wrap > p {
  font-size: 18px;
  /* font-weight: 500; */
}
.aside-button-wrap {
  cursor: pointer;
  /* border: 1px solid black; */
  padding: 10px;
}
.active-aside-button-wrap {
  background-color: #3d38a3e8;
}
.aside-button-wrap:hover {
  background-color: #3d38a3e8;
    transition-duration:0.5s;

}

.aside-button-wrap:hover .aside-button-text {
  color: rgb(255, 255, 255);
  font-weight: 800;
  transition-duration:0.1s;
}
.active-aside-button-text {
  color: rgb(255, 255, 255);
  font-weight: 800;
}

/* .aside-button-wrap > p:hover {
  color: rgb(21, 1, 77);
  font-weight: 800;
} */
</style>