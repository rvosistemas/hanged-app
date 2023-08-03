<template>
    <form @submit.prevent="submitForm" class="form-container">
        <input v-model="username" placeholder="Username" />
        <input v-model="password" type="password" placeholder="Password" />
        <input
               v-model="confirmPassword"
               type="password"
               placeholder="Confirm Password" />
        <button type="submit">Sign up</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    </form>

    <button @click="goToLogin" class="login-button">I already have an account, Start
        session</button>
</template>

<script setup lang="ts">
import { ref, inject } from "vue";
import { useRouter } from "vue-router";

const FLASK_API_BASE_URL = inject<string>("FLASK_API_BASE_URL");

const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const router = useRouter();

function validateData() {
    if (!username.value || !password.value || !confirmPassword.value) {
        errorMessage.value = "Please, Complete all fields.";
        return true;
    }
}

function validatePassword() {
    if (password.value !== confirmPassword.value) {
        errorMessage.value = "Passwords do not match.";
        return true;
    }
}

async function submitForm() {
    errorMessage.value = "";
    successMessage.value = "";

    if (validateData()) return
    if (validatePassword()) return

    const userData = {
        username: username.value,
        password: password.value,
        password_confirm: confirmPassword.value,
    };

    await registration(userData);
}

async function registration(userData: Object) {
    try {
        const response = await fetch(`${FLASK_API_BASE_URL}/api/auth/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });

        if (response.status === 409) {
            errorMessage.value = "User already exists.";
        } else if (response.status === 200) {
            successMessage.value = "Successful registration!";
            router.push({ path: "/login" });
        }
    } catch (error) {
        console.error("Error when making the registration:", error);
        errorMessage.value = "Error when registering. Try it again.";
    }
}

const goToLogin = () => {
    router.push({ path: "/login" });
};
</script>


<style scoped>
.form-container {
    display: flex;
    flex-direction: column;
    max-width: 300px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.form-container input {
    margin-bottom: 10px;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.form-container button {
    padding: 8px 12px;
    background-color: #007bff;
    color: #fff;
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

.login-button {
    margin-top: 10px;
    background-color: #f0f0f0;
    color: #333;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>
