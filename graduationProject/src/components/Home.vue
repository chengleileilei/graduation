<template>
    <div>
        <h2> This is Home page!</h2>
        <p>Hello, it is practice of router! home page</p>
        <p>{{ msg }}</p>
    </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      msg: 'home.p'
    }
  }
}
</script>

<style>
h2{
    color: rgb(255, 0, 0);
}
</style>