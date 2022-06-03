<template>
  <div class="centered inventor-card-wrap">
    <!-- <div class="info-btn-wrap">
      <p @click="routerTo(id)" class="info-btn">前往主页</p>
    </div> -->
    <div class="avatar">
      <img
        src="@/assets/inventor_card/default_avatar.png"
        alt=""
        @click="routerTo(id)"
      />
    </div>

    <div class="inventor-info">
      <p @click="routerTo(id)" class="inventor-name">
        {{ data.inventor_name }}
      </p>
      <div class="index-wrap">
        <div class="patent-num-wrap">
          <p>专利数量：{{ data.inventor_patents_totalnum }}</p>
        </div>
        <div class="patent-score-wrap">
          <p>专利质量综合评分：{{ data.average_score }}</p>
        </div>
        <div class="inventor-score-wrap">
          <p>发明人综合评分：{{ data.T_index }}</p>
        </div>
      </div>

      <div
        v-for="(item, index) in companyList"
        :key="index"
        class="company-wrap"
      >
        <p>
          <span class="el-icon-s-home"></span>
          {{ item.company_name[0] }}（贡献专利{{ item.num }}篇）{{ item.start_time }}至{{
            item.end_time
          }}
          
        </p>
      </div>

      <!-- <p>合作者</p> -->
      <div class="collaborator-wrap">
        <p><span class="el-icon-user-solid"></span>合作者：</p>
        <p  class="collaborator-text" v-if="collaboratorList.length==0">暂无数据</p>
        <div v-for="(item, index) in collaboratorList.slice(0, 5)" :key="index">
          <p @click="routerTo(item.id)" class="collaborator-text">
            {{ item.name }}({{ item.num }})
          </p>
        </div>
      </div>

      <!-- <div class="research-wrap">
        <p><span class="el-icon-s-opportunity"></span>研究领域：</p>
        <p>{{data.inventor_categories}}</p>
        <p class="research-text" v-if="JSON.stringify(data.inventor_categories)=='{}'">暂无数据</p>
        <div v-for="(item, index) in data.inventor_categories" :key="index">
          <p class="research-text">
            {{ item.category_name }}:{{ item.time.length }}
          </p>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script>
export default {
  name: "Inventor",
  props: ["id"],
  data() {
    return {
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
    routerTo(id) {
      console.log("tettttt");
      this.$router.push("/inventor/" + id);
    },
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
/* .info-btn-wrap {
  display: flex;
  flex-direction: row;
}
.info-btn {
  display: flex;
  flex-direction: row;
  cursor: pointer;
  border: 1px solid black;
  border-radius: 5px;
  margin: 5px;
  padding: 10px;
} */
.inventor-card-wrap {
  margin: 10px;
  outline: 1px solid rgba(173, 173, 173, 0.726);
  padding: 10px;
  border-radius: 10px;
  box-shadow: 3px 3px rgba(231, 230, 230, 0.89);
  display: flex;
  flex-direction: row;
  align-items: center;
}
.inventor-card-wrap:hover {
  outline: 2px solid rgba(197, 197, 197, 0.568);
  box-shadow: 5px 5px rgba(231, 230, 230, 0.89);
}

/* 人物头像 */
.avatar {
  max-width: 130px;
  padding-right: 10px;
}
.avatar img {
  width: 100%;
  cursor: pointer;
  border-radius: 10px;
}
/* 人物信息 */
.inventor-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.inventor-name {
  font-size: 24px;
  cursor: pointer;
  font-weight: 800;
}
.inventor-name:hover {
  color: #3e38a3;
}

/* 发明人评分信息 */
.index-wrap {
  display: flex;
  flex-direction: row;
  margin-top: 5px;
  margin-bottom: 5px;
}
.index-wrap > div {
  margin-right: 10px;
  border-radius: 2px;
  padding: 2px 8px 2px 8px;
}
.index-wrap p {
  font-size: 16px;
  color: #000000d2;
}
.patent-num-wrap {
  border: 1px solid #b7ce9d;
}
.patent-score-wrap {
  border: 1px solid #ddb74e;
}
.inventor-score-wrap {
  border: 1px solid #869ed4;
}
/* 公司信息 */
.company-wrap {
  margin-bottom: 5px;
}
/* 合作者信息 */
.collaborator-wrap {
  display: flex;
  flex-direction: row;
  margin-bottom: 5px;
}
.collaborator-text {
  margin-right: 10px;
  cursor: pointer;
}
.collaborator-text:hover {
  color: #3e38a3;
  text-decoration-line: underline;
}
.research-wrap {
  display: flex;
  flex-direction: row;
  margin-bottom: 5px;
  align-items: center;
}
.research-text {
  margin-right: 15px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.795)
}
</style>