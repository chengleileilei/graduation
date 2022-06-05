<template>
  <div class="page-card" @click="routerTo(id)">
    <div class="page-card-avatar">
      <!-- <img src="@/assets/inventor_card/default_avatar.png" alt="" /> -->
      <img src="@/assets/man.png" alt="" />
    </div>
    <div>
      <h3>{{ inventorInforBrief.inventor_name }}</h3>
      <div class="name-and-num">
        <p class="num">
          T指数：<span>{{ inventorInforBrief.T_index }}</span>
        </p>
        <p class="num">
          专利申请量：<span>{{
            inventorInforBrief.inventor_patents_totalnum
          }}</span>
        </p>
      </div>

      <div
        v-for="(item, index) in inventorInforBrief.inventor_companys"
        :key="index"
        class="company-wrap"
      >
        <!-- {{item}} -->
        <p>
          <span class="el-icon-office-building"></span>
          {{ item.company_name[0] }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Card",
  props: ["id"],
  data() {
    return {
      inventorInforBrief: {},
      company: {},
    };
  },
  methods:{
        routerTo(id) {
      console.log("tettttt");
      this.$router.push("/inventor/" + id);
    },
  },

  created() {
    this.$axios
      .get("http://127.0.0.1:5000/inventor_info_brief", {
        params: {
          id: this.id,
        },
      })
      .then((response) => {
        // console.log(response)
        this.inventorInforBrief = response.data;
        // console.log(this.inventorInforBrief)
        this.inventorInforBrief.T_index = parseFloat(
          this.inventorInforBrief.T_index
        ).toFixed(2);
        // console.log(this.inventorInforBrief.T_index);
        this.inventorInforBrief.inventor_companys = JSON.parse(
          this.inventorInforBrief.inventor_companys
        );
      });
  },
};
</script>

<style>
.page-card {
  cursor: pointer;
  margin:10px 0px;
  padding:10px 0;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  border-bottom: 1px solid rgb(160, 160, 160);
}
.page-card:hover{
  border-bottom: 1px solid #3E38A3;;
  /* box-shadow: 5px 5px rgba(231, 230, 230, 0.89); */
}
.page-card-avatar {
  width: 80px;
  min-width: 30px;
  margin-right: 15px;
}
.page-card-avatar img {
  width: 100%;
  border-radius: 50%;
}
.name-and-num {
  margin: 3px 0;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
      flex-wrap: wrap;
}
.num {
  margin-right: 6%;
  font-size: 14px;
  font-weight: 400;
  color: #595959;
}
.num span {
  display: inline-block;
  padding: 4px 6px;
  font-weight: 600;
  font-size: 12px;
  color: #ff9e41;
  background: #fff;
  border-radius: 12px;
  -webkit-box-shadow: 0 1px 3px 0 hsl(0deg 0% 63% / 50%);
  box-shadow: 0 1px 3px 0 hsl(0deg 0% 63% / 50%);
}
</style>