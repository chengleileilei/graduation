import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home.vue'
import Example from '@/components/Example.vue'
import Ipc from '@/components/Ipc.vue'
import Search from '@/components/Search.vue'
import Inventor from '@/components/inventorPage/Inventor.vue'
// import IpcMain from '@/components/ipcSub/IpcMain.vue'

Vue.use(Router)

export default new Router({
    routes: [{
            path: '/',
            redirect: '/home'
        },
        {
            path: '/home',
            name: 'home',
            component: Home
        }, {
            path: '/ipc',
            name: 'ipc',
            component: Ipc,
            // children: [{
            //     path: 'category/:firstword',
            //     component: IpcMain
            // }]
        }, {
            path: '/search',
            name: 'search',
            component: Search
        }, , {
            path: '/inventor/:id/',
            name: 'inventor',
            component: Inventor
        },
        {
            path: '/example',
            name: 'example',
            component: Example
        }

    ]
})