<template>
  <div>
    <h1 class="ipc-first-tit">
      {{ topData.ipc_category }} {{ topData.ipc_category_info }}领域高权重发明家
    </h1>
    <!-- {{ topData }} -->
    <p class="ipc-second-tit"></p>
    <div
      v-for="(item, index_ipc_main) in topData.top_inventors"
      :key="index_ipc_main"
    >
      <!-- {{ item.id }} -->
      <InventorCard :id="item.id"></InventorCard>
    </div>
    <h1 class="ipc-first-tit">
      {{ topData.ipc_category }} {{ topData.ipc_category_info }}领域人才概览
    </h1>
    <p class="ipc-second-tit">总计{{ this.allInventors.length }}人</p>
    <!-- <p>{{ this.allInventors }}</p>
    <p>currInventors发明家</p>
    <button @click="load">加2</button>
    <p>{{ currInventors }}</p> -->

    <!-- <div v-for="(id, index) in allInventors" :key="index" class="ipc-top-wrap">
      {{ item.id }}
      <InventorCard :id="id"></InventorCard>
    </div> -->
    <div v-infinite-scroll="load" style="overflow: auto" class="scoll-wrap">
      <div v-for="(id, index) in currInventors" :key="index">
        <!-- {{ id }} -->
        <InventorCard :id="id"></InventorCard>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "IpcMain",
  props: {
    //test:null,
    topData: {
      //   type: Object, //可以注明设置类型，
      default: () => [], //默认值,
      required: false, //是否必须
    },
  },
  //   props: ["topData"],
  data() {
    return {
      allInventors: [],
      //   firstWord: this.$route.params.firstword,
      currInventors: [],
      currCount: 0,
    };
  },
  created() {
    this.$axios
      .get("http://127.0.0.1:5000/ipc_category_all_inventors", {
        params: { ipc_category: this.topData.ipc_category },
      })
      .then((response) => {
        this.allInventors = response.data;
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
  methods: {
    load() {
      var n = this.currCount;
      for (let i = n; i < n + 3; i++) {
        if (i >= this.allInventors.length) {
          break;
        }
        this.currInventors.push(this.allInventors[i]);
        this.currCount += 1;
      }
    },
  },

  updated() {
    //   this.mydata = this.topData
    //   console.log('mydata:',mydata)
  },
  //   watch: {
  //     topData: {
  //       handler(newValue, oldValue) {
  //         this.init(); //父组件updateTime对象改变会触发此函数
  //         console.log('init')
  //       },
  //       deep: true,
  //     },
  //   },
  //   watch:{
  //   '$route'(newVal,oldVal){
  //     if(newVal.name != this.firstWord) {
  //       this.$destroy();
  //     } else {}
  //   },
  // },
};
</script>

<style>
.ipc-top-wrap {
  border: 2px solid rgb(12, 7, 88);
  border-radius: 10px;
  padding: 10px;
  margin: 10px;
}
.scoll-wrap {
  max-height: 700px;
}
.ipc-first-tit {
  text-align: center;
}
.ipc-second-tit {
  text-align: center;
}
</style>