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
                <tr v-for="user in paginatedUsers" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.role }}</td>
                    <td>{{ user.status }}</td>
                    <td>
                        <button @click="openUpdateModal(user)"
                                class="editButton">Edit</button>
                        <button @click="deleteUser(user)"
                                class="deleteButton">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="pagination">
            <button @click="previousPage" :disabled="currentPage === 1">Anterior</button>
            <button @click="nextPage" :disabled="endIndex >= users.length">Siguiente</button>
        </div>

        <button @click="openCreateModal" class="createButton">Create User</button>
        <!-- MODALS -->
        <UserCreateModal :isOpen="isCreateModalOpen" @close="closeCreateModal" @userCreated="handleUserCreated" />
        <UserUpdateModal :isOpen="isUpdateModalOpen" :selectedUser="selectedUser" @close="closeUpdateModal" />
        <UserDeleteModal
                         v-if="isDeleteModalOpen"
                         :isOpen="isDeleteModalOpen"
                         :selectedUser="userToDelete"
                         @cancel="closeDeleteModal"
                         @confirm="confirmDeleteUser"
                         @userDeleted="handleUserDeleted" />
    </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, computed } from 'vue';
import axios from 'axios';

import UserCreateModal from '../Modals/UserCreateModal.vue';
import UserUpdateModal from '../Modals/UserUpdateModal.vue';
import UserDeleteModal from '../Modals/UserDeleteModal.vue';

// ------------ interfaces ------------
interface User {
    id: number;
    username: string;
    role: string;
    status: string;
}

const FLASK_API_BASE_URL = inject<string>("FLASK_API_BASE_URL");
const token = localStorage.getItem('token'); // Obtén el token de localStorage

const users = ref<User[]>([]);
const selectedUser = ref();
const userToDelete = ref();

const isCreateModalOpen = ref(false);
const isUpdateModalOpen = ref(false);
const isDeleteModalOpen = ref(false);

const currentPage = ref(1); // Página actual
const itemsPerPage = 5; // Cantidad de elementos por página

const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage);
const endIndex = computed(() => currentPage.value * itemsPerPage);

const paginatedUsers = computed(() => users.value.slice(startIndex.value, endIndex.value));

const previousPage = () => {
    if (currentPage.value > 1) {
        currentPage.value -= 1;
    }
};

const nextPage = () => {
    if (endIndex.value < users.value.length) {
        currentPage.value += 1;
    }
};
// TODO:CREAR PAGINACION Y MOSTRAR ALERTAS Y MENSAJES DE ERROR

// Realiza la solicitud HTTP cuando el componente se monta
onMounted(async () => {
    try {
        const response = await axios.get(`${FLASK_API_BASE_URL}/api/users/all`, {
            headers: {
                Authorization: `Bearer ${token}`, // Incluye el token en el encabezado
            },
        });
        users.value = response.data;
    } catch (error) {
        console.error('Error al obtener la lista de usuarios:', error);
    }
});

const handleUserCreated = (newUser: User) => {
    users.value.push(newUser);
};

const handleUserDeleted = (userId: number) => {
    users.value = users.value.filter((user) => user.id !== userId);
};

const deleteUser = (user: User) => {
    userToDelete.value = user;
    isDeleteModalOpen.value = true;
};

const openCreateModal = () => {
    isCreateModalOpen.value = true;
};

const openUpdateModal = (user: User) => {
    selectedUser.value = { ...user };
    isUpdateModalOpen.value = true;
};

const closeCreateModal = () => {
    isCreateModalOpen.value = false;
};

const closeUpdateModal = () => {
    isUpdateModalOpen.value = false;
};

const closeDeleteModal = () => {
    userToDelete.value = null;
    isDeleteModalOpen.value = false;
};

const confirmDeleteUser = () => {
    if (userToDelete.value) {
        // Realiza la lógica para eliminar el usuario aquí
        console.log('Eliminando usuario:', userToDelete.value);
        closeDeleteModal();
    }
};

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
