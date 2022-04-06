<template>
  <div>
    <h1>example page</h1>
    <div class="inventor">
      <p>发明人id: {{ id }}</p>
      <p>姓名：{{ name }}</p>
      <p>已发表专利号：{{ patents_ids }}</p>
      <p>发表专利数量：{{ patents_num }}</p>
      <p>历史就职公司信息：</p>
      <ul>
        <li v-for="(value, key) in companys" :key="key">{{ key }} : {{ value }}</li>
      </ul>
      <p>ipc分类号信息：</p>
      <ul>
        <li v-for="(value, key) in ipcs" :key="key">{{ key }} : {{ value }}</li>
      </ul>
      <p>共同发明人信息：</p>
      <ul>
        <li v-for="(value, key) in collaboritors" :key="key">{{ key }} : {{ value }}</li>
      </ul>

      <!-- <p>msg:::{{ msg }}</p> -->
    </div>
  </div>
</template>

<script>
export default {
  name: "example",
  data() {
    return {
      msg: null,
      id: null,
      name: null,
      patents_ids: null,
      patents_num: null,
      companys: null,
      ipcs: null,
      collaboritors: null,
    };
  },
  created() {
    this.$axios
      .get("http://127.0.0.1:5000/")
      .then((response) => {
        this.msg = response.data;
        console.log(this.msg);
        this.id = response.data[0];
        this.name = response.data[1];
        this.patents_ids = response.data[2];
        this.patents_num = response.data[3];
        this.companys = JSON.parse(response.data[4]);
        console.log(this.companys, typeof this.companys);
        this.ipcs = JSON.parse(response.data[5]);
        this.collaboritors = JSON.parse(response.data[7]);
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style>
.inventor {
  border: 2px solid rgb(5, 4, 99);
  border-radius: 20px;
  text-align: left;
  padding: 20px;
  width: 80%;
  margin: 0 auto;
}
</style>