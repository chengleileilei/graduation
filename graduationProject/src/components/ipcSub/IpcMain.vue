<template>
  <div>
    <h1>{{ topData.ipc_category }} {{ topData.ipc_category_info }}</h1>
    <!-- {{ topData }} -->
    <p>高权重发明家</p>
    <div
      v-for="(item, index_ipc_main) in topData.top_inventors"
      :key="index_ipc_main"
      class="ipc-top-wrap"
    >
      {{ item.id }}
      <InventorCard :id="item.id"></InventorCard>
    </div>
    <p>全部发明家</p>
    <p>{{ this.allInventors }}</p>
    <p>currInventors发明家</p>
    <button @click="load">加2</button>
    <p>{{ currInventors }}</p>

    <!-- <ul v-infinite-scroll="load" style="overflow: auto">
      <div
        v-for="(id, index) in currInventors"
        :key="index"
        class="ipc-top-wrap"
      >
      lalalal
        {{ item.id }}
        <InventorCard :id="id"></InventorCard>
      </div>
    </ul> -->

    <!-- <div v-for="(id, index) in allInventors" :key="index" class="ipc-top-wrap">
      {{ item.id }}
      <InventorCard :id="id"></InventorCard>
    </div> -->
    <div v-infinite-scroll="load" style="overflow: auto" class="scoll-wrap">
      <div v-for="(id, index) in currInventors" :key="index" class="ipc-top-wrap">
        {{ id }}
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
      for (let i = n; i < n + 2; i++) {
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
.scoll-wrap{
  max-height: 500px;
}
</style>