<template>
    <div class="message-popup" v-if="message">
        <div :class="['message', type]">
            {{ message }}
            <button v-if="autoClose" @click="closeMessage">OK</button>
        </div>
    </div>
</template>
  
<script lang="ts">
import { ref, onMounted, watchEffect } from 'vue';

export default {
    props: {
        message: String,
        type: String, // Puede ser 'error' o 'success'
        autoClose: Boolean, // Nuevo prop para controlar el cierre automático
    },
    setup(props, { emit }) {
        const visible = ref(false);

        const closeMessage = () => {
            visible.value = false;
            emit('close');
        };

        onMounted(() => {
            visible.value = true;

            if (props.autoClose) {
                setTimeout(closeMessage, 8000); // 8000 milisegundos = 8 segundos (puedes ajustar el tiempo)
            }
        });

        // Cerrar automáticamente cuando el mensaje cambia
        watchEffect(() => {
            if (props.autoClose) {
                setTimeout(closeMessage, 8000); // 8000 milisegundos = 8 segundos (puedes ajustar el tiempo)
            }
        });

        return {
            visible,
            closeMessage,
        };
    },
};
</script>
  
<style scoped>
/* Estilos CSS aquí ... */
</style>
  