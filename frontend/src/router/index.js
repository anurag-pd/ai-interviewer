import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/AIInterviewer.vue"),
  },
  {
    path: "/admin",
    name: "AdminPanel",
    component: () => import("../views/AdminPanel.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
