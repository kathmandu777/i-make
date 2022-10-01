import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

createApp(App).use(router).use(require("vue3-shortkey")).mount("#app");
