<template>
  <div class="ipc-card">
    <p>{{ inventorInforBrief.inventor_name }}</p>
    <p>id: {{ inventorInforBrief.inventor_id }}</p>
    <p>指数：{{ formattScore }}</p>
    <p>专利数量：{{ inventorInforBrief.inventor_patents_totalnum }}</p>
    <p>T指数：{{ inventorInforBrief.T_index }}</p>
    <!-- {{inventorInforBrief}} -->
  </div>
</template>

<script>
export default {
  name: "Card",
  props: ["id", "score"],
  data() {
    return {
      inventorInforBrief: {},
      formattScore : 0
    };
  },

  created() {
    this.formattScore = parseFloat(
      this.score
    ).toFixed(2);

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
      });
  },
};
</script>

<style>
.ipc-card {
  display: flex;
  flex-direction: row;
}
</style>