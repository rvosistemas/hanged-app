<template>
    <p class="login-title">LOGIN</p>
    <form @submit.prevent="submitForm" class="form-container">
        <input v-model="username" placeholder="Username" />
        <input v-model="password" type="password" placeholder="Password" />
        <button type="submit" class="submit-btn">Login</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
        <button @click="goToRegister" class="register-btn">I don't have an
            account,
            Sign up</button>
    </form>
</template>

<script setup lang="ts">
import { ref, inject } from "vue";
import { useRouter } from "vue-router";

const FLASK_API_BASE_URL = inject<string>("FLASK_API_BASE_URL");

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const router = useRouter();

function validateData() {
    if (!username.value || !password.value) {
        errorMessage.value = "Please, Complete all fields.";
        return true;
    }
}
async function submitForm() {
    errorMessage.value = "";
    successMessage.value = "";

    if (validateData()) return

    const userData = {
        username: username.value,
        password: password.value,
    };


    await login(userData);
}

async function login(userData: Object) {
    try {
        const response = await fetch(`${FLASK_API_BASE_URL}/api/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });

        const data = await response.json();

        if (data.error) {
            errorMessage.value = data.message;
        } else {
            successMessage.value = data.message;
            localStorage.setItem('token', data.access_token);

            // Wait for 2 seconds (2000 milliseconds) before navigating to 'board'
            setTimeout(() => {
                router.push({ path: "/board" });
            }, 2000);
        }
    } catch (error) {
        console.error("Error when making the login:", error);
        errorMessage.value = "Error when logging. Try it again.";
    }
}

const goToRegister = () => {
    router.push({ path: "/register" });
};

</script>

<style scoped lang="scss">
.form-container {
    display: flex;
    flex-direction: column;
    max-width: 300px;
    max-height: 600px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;

    input {
        margin-bottom: 10px;
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    .submit-btn {
        padding: 8px 12px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    .register-btn {
        margin-top: 10px;
        background-color: #d95050;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    .error-message {
        color: #ff0000;
        margin-top: 5px;
    }

    .success-message {
        color: #00ff00;
        margin-top: 5px;
    }
}
</style>