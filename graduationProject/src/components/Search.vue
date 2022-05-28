<template>
  <div class="centered">
    <h1 class="first-tit">人才检索</h1>
    <el-row class="search-wrap">
      <input
        type="text"
        name=""
        id=""
        class="search-inpur"
        v-model="searchName"
        @keyup.enter="search"
      />
      <i
        class="el-icon-search s-icon"
        style="margin: 0 10px; font-size: 35px; color: black"
        @click="search"
      ></i>
    </el-row>
    <!-- <el-row>
      <div v-for="(id, index) in allInventors" :key="index" class="result-wrap">
        <InventorCard :id="id"></InventorCard>
      </div>
      {{ allInventors }}
    </el-row> -->

    <div
      v-infinite-scroll="load"
      style="overflow: auto"
      class="search-result-wrap"
    >
      <p>{{ searchState }}</p>
      <div
        v-for="(id, index) in currInventors"
        :key="index"

      >
        {{ id }}
        <InventorCard :id="id"></InventorCard>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ipc",
  data() {
    return {
      searchName: "",
      allInventors: [],
      searchState: "当前无检索结果",
      currInventors: [],
      currCount: 0,
    };
  },
  methods: {
    search() {
      console.log(typeof this.searchName);
      console.log(this.searchName);

      if (this.searchName == "") {
        this.searchState = "请输入检索关键词";
        console.log("kongle");
        return;
      }
      this.allInventors = [];
      this.currInventors = [];
      (this.currCount = 0), (this.searchState = "正在检索，请稍后...");

      // console.log(this.searchName);
      this.$axios
        .get("http://127.0.0.1:5000/search_inventors", {
          params: {
            name: this.searchName,
          },
        })
        .then((response) => {
          this.allInventors = response.data;
          // console.log(this.allInventors);
          this.searchState =
            "共检索到" + String(this.allInventors.length) + "条结果。";

          var n = 0;
          for (let i = n; i < n + 5; i++) {
            if (i >= this.allInventors.length) {
              break;
            }
            this.currInventors.push(this.allInventors[i]);
            this.currCount += 1;
          }
        });
    },
    load() {
      var n = this.currCount;
      for (let i = n; i < n + 2; i++) {
        if (i >= this.allInventors.length) {
          break;
        }
        this.currInventors.push(this.allInventors[i]);
        this.currCount += 1;
      }
    },
  },

  created() {
    // this.$axios
    //   .get("http://127.0.0.1:5000/search_inventors", {
    //     params: {
    //       name: this.searchName,
    //     },
    //   })
    //   .then((response) => {
    //     // console.log(response)
    //     this.allInventors = response;
    //     console.log(this.allInventors);
    //     // console.log(this.inventorInforBrief)
    //     // console.log(this.inventorInforBrief.T_index);
    //   });
  },
};
</script>

<style>
.first-tit {
  text-align: center;
  margin: 20px;
}
.search-wrap {
  /* width: 70%; */
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
.search-inpur {
  height: 40px;
  width: 50%;
  border-radius: 20px;
  font-size: 20px;
  padding-left: 20px;
}
.s-icon {
  cursor: pointer;
}
.result-wrap {
  border: 2px solid rgb(2, 7, 75);
  border-radius: 20px;
  padding: 20px;
  margin: 20px;
}
.search-result-wrap {
  max-height: 800px;
  min-height: 400px;
}
</style>