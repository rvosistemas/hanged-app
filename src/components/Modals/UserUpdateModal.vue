<template>
    <div v-if="isOpen" class="modal-overlay">
        <div class="modal">
            <h2>Update User</h2>
            <form @submit.prevent="submitUpdateUser">
                <input v-model="props.selectedUser.username" placeholder="Username" />

                <!-- Select for Role -->
                <h3>Role</h3>
                <select v-model="props.selectedUser.role">
                    <option v-for="role in Object.values(RoleEnum)" :key="role">{{ role }}</option>
                </select>

                <!-- Select for Status -->
                <h3>Status</h3>
                <select v-model="props.selectedUser.status">
                    <option v-for="status in Object.values(StatusEnum)" :key="status">{{ status }}</option>
                </select>

                <!-- Password input -->
                <h3>Password</h3>
                <input v-model="props.selectedUser.password" type="password" placeholder="Password" />

                <!-- Confirm password input -->
                <h3>Confirm Password</h3>
                <input v-model="confirmPassword" type="password" placeholder="Confirm Password" />

                <button type="submit">Update</button>
                <button type="button" @click="closeUpdateModal">Cancel</button>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, ref, watchEffect } from 'vue';
import axios from 'axios';

interface User {
    id: number;
    username: string;
    role: string;
    status: string;
    password: string;
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
const isUpdateModalOpen = ref(false);
const users = ref<User[]>([]);
const token = localStorage.getItem('token');

const emits = defineEmits();

const props = defineProps({
    isOpen: Boolean,
    selectedUser: {
        type: Object as () => User,
        required: true,
    },
});



watchEffect(() => {
    if (props.selectedUser) {
        onOpenUpdateModal(props.selectedUser);
    }
});

const onOpenUpdateModal = (user: User) => {
    Object.assign(props.selectedUser, user); // Update properties of selectedUser
    isUpdateModalOpen.value = true; // Open the modal
};

const closeUpdateModal = () => {
    emits('close');
    isUpdateModalOpen.value = false;
    // Reset properties of selectedUser when closing modal
    Object.assign(props.selectedUser, {
        id: 0,
        username: "",
        password: "",
        role: "",
        status: "",
    });
    confirmPassword.value = "";
};

const submitUpdateUser = async () => {

    if (!props.selectedUser) {
        return; // Handle the case when selectedUser is undefined
    }

    // Validación de contraseña y confirmación
    if (props.selectedUser.password !== confirmPassword.value) {
        console.error("Password and Confirm Password do not match");
        return;
    }

    // validar campos vacíos
    if (!props.selectedUser.username || !props.selectedUser.password || !props.selectedUser.role || !props.selectedUser.status) {
        console.error("Please, Complete all fields.");
        return;
    }

    try {
        const response = await axios.put( // Use axios.put for updating user
            `${FLASK_API_BASE_URL}/api/users/users/${props.selectedUser.id}`,
            props.selectedUser,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        // Update the user in the users array
        const updatedUserIndex = users.value.findIndex(u => u.id === props.selectedUser.id);
        if (updatedUserIndex !== -1) {
            users.value[updatedUserIndex] = response.data;
        }
        closeUpdateModal(); // Close the modal after updating
    } catch (error) {
        console.error('Error updating user:', error);
    }
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