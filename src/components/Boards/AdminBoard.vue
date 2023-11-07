<template>
    <Navbar />
    <div class="admin-board-container">
        <h1>Admin Panel</h1>
        <div class="search-container">
            <h2>Search</h2>
            <input v-model="searchText" placeholder="Search Users ..." />
        </div>
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
            <span>{{ currentPage }} / {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage >= totalPages">Siguiente</button>
        </div>


        <button @click="openCreateModal" class="createButton">Create User</button>

        <!-- errors messages -->
        <MessagePopup :message="errorMessage" type="error" :autoClose="true" @close="errorMessage = ''" />
        <MessagePopup :message="successMessage" type="success" :autoClose="true" @close="successMessage = ''" />


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
import { ref, inject, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import { useRouter } from "vue-router";

import Navbar from "../Navbar/Navbar.vue";

import UserCreateModal from '../Modals/UserCreateModal.vue';
import UserUpdateModal from '../Modals/UserUpdateModal.vue';
import UserDeleteModal from '../Modals/UserDeleteModal.vue';
import MessagePopup from '../MessagePopup.vue';

// ------------ interfaces ------------
interface User {
    id: number;
    username: string;
    role: string;
    status: string;
}

const router = useRouter();

const FLASK_API_BASE_URL = inject<string>("FLASK_API_BASE_URL");
const token = localStorage.getItem('token'); // Obtén el token de localStorage

const users = ref<User[]>([]);
const paginatedUsers = ref<User[]>([]);
const selectedUser = ref();
const userToDelete = ref();

const searchText = ref('');

const isCreateModalOpen = ref(false);
const isUpdateModalOpen = ref(false);
const isDeleteModalOpen = ref(false);

const errorMessage = ref("");
const successMessage = ref("");

const currentPage = ref(1); // Página actual
const itemsPerPage = 5; // Cantidad de elementos por página

const filteredUsers = computed(() => {
    const filtered = users.value.filter((user: { username: string; }) =>
        user.username.toLowerCase().includes(searchText.value.toLowerCase())
    );
    return filtered;
});

const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage);

const endIndex = computed(() => startIndex.value + itemsPerPage);

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / itemsPerPage));

const previousPage = () => {
    if (currentPage.value > 1) {
        currentPage.value -= 1;
        updatePaginatedUsers();
    }
};

const nextPage = () => {
    if (endIndex.value < filteredUsers.value.length) {
        currentPage.value += 1;
        updatePaginatedUsers();
    }
};

// Agrega esta función para actualizar paginatedUsers
const updatePaginatedUsers = () => {
    const startIndex = (currentPage.value - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    paginatedUsers.value = filteredUsers.value.slice(startIndex, endIndex);
};

watch(searchText, () => {
    if (searchText.value) {
        // Filtra y muestra los usuarios coincidentes con la búsqueda
        paginatedUsers.value = filteredUsers.value.slice(startIndex.value, endIndex.value);
    } else {
        // Si no hay término de búsqueda, muestra los usuarios paginados normales
        paginatedUsers.value = users.value.slice(startIndex.value, endIndex.value);
    }
    currentPage.value = 1; // Reinicia la página al cambiar la búsqueda
});

// Realiza la solicitud HTTP cuando el componente se monta
onMounted(async () => {
    try {
        const response = await axios.get(`${FLASK_API_BASE_URL}/api/users/all`, {
            headers: {
                Authorization: `Bearer ${token}`, // Incluye el token en el encabezado
            },
        });
        users.value = response.data;
        paginatedUsers.value = users.value.slice(startIndex.value, endIndex.value);
    } catch (error) {
        console.error('Error obtaining the list of users.', error);
    }
});

const handleUserCreated = (newUser: User) => {
    users.value.push(newUser);
    successMessage.value = "User created successfully.";
};

const handleUserDeleted = (userId: number) => {
    users.value = users.value.filter((user: { id: number; }) => user.id !== userId);
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
        console.log('Eliminating user.', userToDelete.value);
        successMessage.value = "User deleted successfully.";
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

    .search-container {
        margin-top: 20px;
        display: flex;
        align-items: center;

        h2 {
            font-size: 18px;
            margin-right: 10px;
            color: white;

        }

        input {
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 14px;
            outline: none;
        }
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

    .pagination {
        margin-top: 20px;
        display: flex;
        align-items: center;
        justify-content: center;

        button {
            padding: 8px 12px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin: 0 5px;

            &:disabled {
                background-color: #ccc;
                cursor: not-allowed;
            }
        }

        span {
            font-size: 16px;
            margin: 0 10px;
            font-weight: bold;
            color: white;
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

    .error-message,
    .success-message {
        position: fixed;
        top: 50px;
        left: 50%;
        transform: translateX(-50%);
        padding: 10px 20px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
    }

    .error-message {
        background-color: #ff0000;
    }

    .success-message {
        background-color: #00ff00;
    }

}
</style>
