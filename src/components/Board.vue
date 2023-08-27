<template>
    <Navbar />
    <div class="board-container">
        <h1>Board</h1>
        <button @click="goToLogin" class="login-btn">close session</button>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import Navbar from "./Navbar/Navbar.vue";

const router = useRouter();

const goToLogin = () => {
    router.push({ path: "/login" });
};

</script>

<style scoped>
.board-container {
    display: block;
    text-align: center;
    padding: 10px;
}

.login-btn {
    margin-top: 10px;
    background-color: #d95050;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>