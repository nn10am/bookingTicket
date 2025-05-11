import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import BookingPage from "../views/BookingPage.vue";

const routes = [
    { path: "/", component: HomePage },
    { path: "/booking", component: BookingPage }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;

