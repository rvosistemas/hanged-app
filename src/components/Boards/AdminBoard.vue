<template>
    <div class="admin-board-container">
        <h1>Admin Panel</h1>
        <table>
            <caption class="table-title">All Users</caption>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.role }}</td>
                    <td>{{ user.status }}</td>
                    <td>
                        <button @click="editUser(user)"
                                class="editButton">Edit</button>
                        <button @click="deleteUser(user)"
                                class="deleteButton">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <button @click="openCreateModal" class="createButton">Create User</button>
        <!-- MODALS -->
        <UserCreateUpdateModal :isOpen="isCreateModalOpen" @close="closeCreateModal" />
    </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted } from 'vue';
import axios from 'axios';
import UserCreateUpdateModal from '../Modals/UserCreateUpdateModal.vue';

// ------------ interfaces ------------
interface User {
    id: number;
    username: string;
    role: string;
    status: string;
}

const FLASK_API_BASE_URL = inject<string>("FLASK_API_BASE_URL");

const users = ref<User[]>([]);
const token = localStorage.getItem('token'); // Obtén el token de localStorage

// Realiza la solicitud HTTP cuando el componente se monta
onMounted(async () => {
    try {
        const response = await axios.get(`${FLASK_API_BASE_URL}/api/users/users`, {
            headers: {
                Authorization: `Bearer ${token}`, // Incluye el token en el encabezado
            },
        });
        users.value = response.data;
    } catch (error) {
        console.error('Error al obtener la lista de usuarios:', error);
    }
});

const editUser = (user: User) => {
    console.log(user);
};

const deleteUser = (user: User) => {
    console.log(user);
};

const openCreateModal = () => {
    isCreateModalOpen.value = true;
};

const closeCreateModal = () => {
    isCreateModalOpen.value = false;
};

const isCreateModalOpen = ref(false);

</script>

<style scoped lang="scss">
.admin-board-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    h1 {
        font-size: 24px;
        margin-bottom: 20px;
        color: white;
    }

    table {
        align-self: center;
        width: 80%;
        border-collapse: collapse;
        border: 1px solid #ccc;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        background-color: white;

        .table-title {
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            color: white;
            background-color: #007bff;
        }

        th,
        td {
            padding: 12px;
            text-align: left;

            button {
                border: none;
                color: white;
                padding: 5px 10px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                margin: 2px 2px;
                cursor: pointer;
            }

            .editButton {
                background-color: #00ff08;

                &:hover {
                    background-color: #008604;
                }
            }

            .deleteButton {
                background-color: #ff0400;

                &:hover {
                    background-color: #890000;
                }
            }

        }

        th {
            background-color: #f2f2f2;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        tr:hover {
            background-color: #f5f5f5;
        }
    }

    .createButton {
        margin-top: 20px;
        padding: 8px 12px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }


}
</style>
