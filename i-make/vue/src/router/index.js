import Menu from "@/views/Menu.vue";
import Settings from "@/views/Settings.vue";
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
    // 設定
    path: "/settings",
    name: "Settings",
    component: Settings,
  },
  {
    // 各モードのページ
    path: "/mode",
    name: "Mode",
    // component: Mode,
    children: [
      {
        // EventMode
        path: "EVENT" /* Enum をそのまま使っている関係で大文字 */,
        name: "Event",
        component: Event,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
