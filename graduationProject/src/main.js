// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'

Vue.prototype.$axios = axios; // 把对象挂载vue中



Vue.config.productionTip = false

// runtime-compiler(Vue1)
// template -> ast -> render -> virtual dom tree -> UI

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: { App },
    template: '<App/>'
})

// axios({
//     url: 'http://127.0.0.1:5000/'
// }).then(res => {
//     console.log(res);
// })


// runtime-only(Vue2)  代码更少，性能更高，
// runder -> virtual dom tree -> UI
// vue-template-compiler 将.vue文件中的template渲染为render函数

// new Vue({
//     el: '#app',
//     router,
//     render: function(h) {
//         return h(App)
//     }
// })