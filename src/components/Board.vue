<template>
    <div class="board-container">
        board
        <!-- <button @click="goToLogin" class="login-btn">close session</button> -->
        <button @click="goToLogin" class="login-btn">close session</button>
    </div>
</template>

<script setup lang="ts">
// import { ref, inject } from "vue";
import { useRouter } from "vue-router";

// const FLASK_API_BASE_URL = inject<string>("FLASK_API_BASE_URL");

const router = useRouter();

const goToLogin = () => {
    router.push({ path: "/login" });
};

</script>

<style scoped>
.board-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    /* height: 100vh; */
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