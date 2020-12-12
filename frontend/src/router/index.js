import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import PreSession from "../views/PreSession.vue";
import TrendingWatchables from "../views/TrendingWatchables.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/session",
    name: "PreSession",
    component: PreSession,
  },
  {
    path: "/trending",
    name: "Trending",
    component: TrendingWatchables,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
