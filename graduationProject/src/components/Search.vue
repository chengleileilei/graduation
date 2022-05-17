<template>
  <div class="centered">
    <h1>人才检索</h1>
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
    <el-row>
      <div v-for="(id, index) in patent_ids" :key="index" class="result-wrap">
        <InventorCard :id="id"></InventorCard>
      </div>
      {{ patent_ids }}
    </el-row>
  </div>
</template>

<script>
export default {
  name: "ipc",
  data() {
    return {
      searchName: "",
      patent_ids: [],
    };
  },
  methods: {
    search() {
      this.patent_ids=[]
      console.log(this.searchName);
      this.$axios
        .get("http://127.0.0.1:5000/search_inventors", {
          params: {
            name: this.searchName,
          },
        })
        .then((response) => {
          this.patent_ids = response.data;
          console.log(this.patent_ids);
        });
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
    //     this.patent_ids = response;
    //     console.log(this.patent_ids);
    //     // console.log(this.inventorInforBrief)

    //     // console.log(this.inventorInforBrief.T_index);
    //   });
  },
};
</script>

<style>
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
.result-wrap{
  border: 2px solid rgb(2, 7, 75);
  border-radius: 20px;
  padding: 20px;
  margin: 20px;
}
</style>