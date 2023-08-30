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
        <button @click="createUser()" class="createButton">Create User</button>
        <!-- Modal para crear usuario -->
        <div v-if="isCreateModalOpen" class="modal-overlay">
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

                    <button type="submit">Create</button>
                    <button type="button" @click="closeCreateModal">Cancel</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// TODO: CREAR EL MODAL POR APARTE Y VER SI SE PUEDE REUTILIZAR
import { ref, inject, onMounted } from 'vue';
import axios from 'axios';

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

interface User {
    id: number;
    username: string;
    role: string;
    status: string;
}

interface UserWithPassword extends User {
    password: string;
}

const FLASK_API_BASE_URL = inject<string>("FLASK_API_BASE_URL");

const users = ref<User[]>([]);
const token = localStorage.getItem('token'); // Obtén el token de localStorage
const confirmPassword = ref("");

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

const createUser = () => {
    console.log('createUser');
    isCreateModalOpen.value = true;

};

const isCreateModalOpen = ref(false);
const newUser = ref<UserWithPassword>({
    id: 0,
    username: "",
    password: "",
    role: "",
    status: "",
});

const closeCreateModal = () => {
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

const submitCreateUser = async () => {
    // Validación de contraseña y confirmación
    if (newUser.value.password !== confirmPassword.value) {
        console.error("Password and Confirm Password do not match");
        return;
    }

    try {
        const response = await axios.post(
            `${FLASK_API_BASE_URL}/api/users/users`,
            newUser.value,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        users.value.push(response.data);
        closeCreateModal();
    } catch (error) {
        console.error('Error creating user:', error);
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
}
</style>
