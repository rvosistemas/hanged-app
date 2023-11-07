<template>
    <!-- Modal para crear usuario -->
    <div v-if="isOpen" class="modal-overlay">
        <div class="modal">
            <h2>Create New User</h2>
            <form @submit.prevent="submitCreateUser">
                <input v-model="newUser.username" placeholder="Username" />

                <!-- Select for Role -->
                <h3>Role</h3>
                <select v-model="newUser.role">
                    <option v-for="role in Object.values(RoleEnum)" :key="role">{{ role }}</option>
                </select>

                <!-- Select for Status -->
                <h3>Status</h3>
                <select v-model="newUser.status">
                    <option v-for="status in Object.values(StatusEnum)" :key="status">{{ status }}</option>
                </select>

                <!-- Password input -->
                <h3>Password</h3>
                <input v-model="newUser.password" type="password" placeholder="Password" />

                <!-- Confirm password input -->
                <h3>Confirm Password</h3>
                <input v-model="confirmPassword" type="password" placeholder="Confirm Password" />

                <div v-if="errorMessage" class="error-message">
                    {{ errorMessage }}
                </div>
                <div v-if="successMessage" class="success-message">
                    {{ successMessage }}
                </div>

                <button type="submit">Create</button>
                <button type="button" @click="closeCreateModal">Cancel</button>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, ref } from 'vue';
import axios from 'axios';

interface User {
    id: number;
    username: string;
    role: string;
    status: string;
    password: string;
    [key: string]: string | number; // Firma de índice
}

enum RoleEnum {
    FINAL_USER = "final_user",
    ADMIN = "admin",
    OWNER = "owner",
    GUEST = "guest",
    MODERATOR = "moderator"
}

enum StatusEnum {
    ACTIVE = "active",
    INACTIVE = "inactive"
}


const FLASK_API_BASE_URL = inject<string>("FLASK_API_BASE_URL");
const confirmPassword = ref("");
const isCreateModalOpen = ref(false);
const users = ref<User[]>([]);
const token = localStorage.getItem('token');

const errorMessage = ref<string | null>(null);
const successMessage = ref<string | null>(null);

const { isOpen } = defineProps(['isOpen']);
const emits = defineEmits();

const newUser = ref<User>({
    id: 0,
    username: "",
    role: "",
    status: "",
    password: "",
});

const closeCreateModal = () => {
    emits('close');

    isCreateModalOpen.value = false;
    // Limpiar los campos del formulario cuando se cierra el modal
    newUser.value = {
        id: 0,
        username: "",
        password: "",
        role: "",
        status: "",
    };
    confirmPassword.value = "";
};


function validateData() {
    const requiredFields = ['username', 'password', 'role', 'status'];
    const emptyField = requiredFields.find(field => !newUser.value[field]);

    if (emptyField) {
        errorMessage.value = "Please, Complete all fields.";
        return true;
    }

    return false;
}

function validatePassword() {
    if (newUser.value.password !== confirmPassword.value) {
        errorMessage.value = "Passwords do not match.";
        return true;
    }
    return false;
}

async function requestCreate() {
    try {
        const response = await axios.post(
            `${FLASK_API_BASE_URL}/api/users/create`,
            newUser.value,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        users.value.push(response.data);
        const newCreatedUser = response.data;
        emits('userCreated', newCreatedUser);
        successMessage.value = "User created successfully.";
        closeCreateModal();
    } catch (error) {
        errorMessage.value = "Error when creating the user.";
        console.error('Error creating user:', error);
    }
}

const submitCreateUser = async () => {

    if (validateData()) return
    if (validatePassword()) return

    await requestCreate();

};
</script>

<style scoped lang="scss">
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;

    .modal {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

        h2 {
            font-size: 18px;
            margin-bottom: 10px;
        }

        form {
            display: flex;
            flex-direction: column;

            input {
                margin-bottom: 10px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }

            button {
                padding: 8px 12px;
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
            }
        }
    }
}
</style>