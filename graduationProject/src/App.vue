<template>
  <div id="app">
    <el-row class="nav-wrap">
      <div class="nav centered">
        <p>基于异构专利数据的人才画像系统</p>
        <div>
          <router-link class="link-a" active-class="active" to="/home">首页</router-link>
          <router-link class="link-a" active-class="active" to="/ipc">人才统计</router-link>
          <router-link class="link-a" active-class="active" to="/search">人才检索</router-link>
        </div>
      </div>
    </el-row>
    <keep-alive>

    <router-view />
    </keep-alive>

    <el-row>
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="footer-wrap">
        <el-row class="centered footer">
          <el-col :xs="24" :sm="24" :md="16" :lg="14" :xl="14" class="footer-l">
            <p class="with-logo-left">
              <img
                class="footer-logo"
                src="@/assets/icon/arcoDesign-location.svg"
                alt=""
              />
              地址：江苏省徐州市铜山区大学路1号中国矿业大学南湖校区
              计算机科学与技术学院
            </p>
            <p class="with-logo-left">
              <img
                class="footer-logo"
                src="@/assets/icon/fas-fa-phone.svg"
                alt=""
              />
              电话：19851693573
            </p>
            <p class="with-logo-left">
              <img
                class="footer-logo"
                src="@/assets/icon/arcoDesign-email.svg"
                alt=""
              />
              邮箱：08182994@cumt.edu.cn
            </p>
            <br />
            <a href="http://cs.cumt.edu.cn/"
              ><p class="small-p">
                友情链接：中国矿业大学计算机科学与技术学院
              </p></a
            >
          </el-col>

          <el-col :xs="24" :sm="24" :md="8" :lg="10" :xl="10" class="footer-r">
            <img src="@/assets/wechat.jpg" alt="" />

            <p>
              <a href="https://github.com/chengleileilei/graduation"
                >项目仓库：<br />https://github.com/chengleileilei/graduation</a
              >
            </p>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="footer-b">
            <p class="with-logo-center">
              <img
                class="footer-logo"
                src="@/assets/icon/fas-fa-copyright.svg"
                alt=""
              />
              China University Of Mining And Technology
            </p>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
* {
  margin: 0;
}
    a{
        text-decoration: none; /* 去除默认的下划线 */
        color: #000;    /* 去除默认的颜色和点击后变化的颜色 */ 
    }
.centered {
  max-width: 1420px;
  margin: 0 auto;
}
/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
.nav-wrap {
  background-color: #f8f8f8;
  border-bottom: 1px solid #e7e7e7;
  /* display: flex;
  flex-direction: row;
  justify-content: center; */
}
.nav {
  height: 70px;
  margin-left: 20px;
  margin-right: 20px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.nav > p {
  font-size: 24px;
  color: #333333;
  font-weight: 600;
  font-family: Times New Roman-bold;
}
.link-a {
  color: #777;
  font-size: 16px;
  font-family: Arial;
  font-weight: bold;
  margin-left: 10px;
  margin-right: 10px;
}
.active{
  font-size: 20px;
      color: #3E38A3;
}

.footer-wrap {
  margin-top: 10px;

  background-color: rgba(45, 45, 45, 1);
}
.footer-wrap p {
  color: rgba(255, 255, 255, 1);
  font-size: 18px;
}
.footer {
  min-height: 257px;
  padding: 10px 20px 0px 20px;
}

.footer-l {
  margin-top: 40px;

  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}
.footer-l .small-p {
  font-size: 18px;
}

.footer-l .with-logo-left {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.footer-r {
  margin-top: 40px;

  display: flex;
  align-items: center;
}
.footer-r img {
  width: 150px;
  margin-right: 35px;
}
.footer-r p {
  text-align: left;
}
.footer-r a {
  color: white;
}

.footer-b {
  margin-top: 30px;
  padding-bottom: 10px;
}
.footer-b p {
  color: rgba(189, 192, 193, 1);
  font-size: 16px;
  font-family: SourceHanSansSC-regular;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.footer-logo {
  margin-right: 10px;
  width: 20px;
  height: 20px;
}
</style>
