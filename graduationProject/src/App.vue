<template>
  <div id="app">
    <router-link to="/">hello</router-link>
    <router-link to="/home">home</router-link>
    <router-link to="/about">about</router-link>
        <router-link to="/example">example</router-link>

    <!-- <img src="./assets/logo.png"> -->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
