import Menu from "@/views/Menu.vue";
import Mode from "@/views/Mode.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/menu",
    name: "Menu",
    component: Menu,
  },
  {
    path: "/mode",
    name: "Mode",
    component: Mode,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
