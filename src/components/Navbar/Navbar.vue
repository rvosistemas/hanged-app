<template>
    <nav class="navbar">
        <router-link to="/board" class="nav-link">Game</router-link>
        <router-link v-if="isAdmin" to="/admin" class="nav-link">Admin</router-link>
        <button @click="goToLogin" class="nav-link logout-btn">Logout</button>
    </nav>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const isAdmin = ref(false);
const router = useRouter();

const goToLogin = () => {
    router.push({ path: "/login" });
};

// Recuperar el rol del usuario del localStorage y verificar si es admin
const userRole = localStorage.getItem("userRole");
if (userRole === "admin") {
    isAdmin.value = true;
}
</script>

<style scoped>
.navbar {
    display: flex;
    justify-content: center;
    padding: 10px;
    background-color: #333;
}

.nav-link {
    color: white;
    margin-right: 20px;
    text-decoration: none;
}

.logout-btn {
    background-color: #d95050;
    border: none;
    border-radius: 5px;
    color: white;
    cursor: pointer;
}
</style>
