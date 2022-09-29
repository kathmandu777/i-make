import Menu from "@/views/Menu.vue";
// import Mode from "@/views/Mode.vue";
import Event from "@/views/mode/Event.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    // モード選択ページ（トップページ）
    path: "/menu",
    name: "Menu",
    component: Menu,
  },
  {
    // 各モードのページ
    path: "/mode",
    name: "Mode",
    // component: Mode,
    children: [
      {
        // EventMode
        path: "EVENT", /* Enum をそのまま使っている関係で大文字 */
        name: "Event",
        component: Event,
      }
    ]
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
