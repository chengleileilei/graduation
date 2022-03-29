<template>
    <div>
        <h2> This is about page!</h2>
        <p>Hello, it is practice of router! about page</p>
        <p>{{ msg }}</p>
    </div>
</template>

<script>
export default {
  name: 'about',
  data () {
    return {
      msg: 'about.p'
    }
  }
}
</script>

<style>
h2{
    color: rgb(255, 0, 0);
}
</style>