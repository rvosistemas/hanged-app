<template>
    <div class="modal-overlay">
        <div class="modal">
            <p>Are you sure you want to delete this record?</p>
            <div class="button-container">
                <button class="confirm" @click="submitDeleteUser">Confirm</button>
                <button class="cancel" @click="cancelDelete">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject } from 'vue';
import axios from 'axios';

interface User {
    id: number;
    username: string;
    role: string;
    status: string;
    password: string;
}

const props = defineProps({
    isOpen: Boolean,
    selectedUser: {
        type: Object as () => User,
        required: true,
    },
});

const FLASK_API_BASE_URL = inject<string>("FLASK_API_BASE_URL");
const token = localStorage.getItem('token');

const emits = defineEmits();

const cancelDelete = () => {
    emits('cancel');
};

const submitDeleteUser = async () => {
    try {
        await axios.delete(
            `${FLASK_API_BASE_URL}/api/users/delete/${props.selectedUser.id}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        // Emitir evento para informar al componente padre
        emits('confirm');
        emits('userDeleted', props.selectedUser.id);
    } catch (error) {
        console.error('Error deleting user:', error);
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

        .button-container {
            display: flex;
            justify-content: space-between;

            .confirm {
                padding: 8px 12px;
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
            }

            .cancel {
                padding: 8px 12px;
                background-color: #ff2a00;
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
