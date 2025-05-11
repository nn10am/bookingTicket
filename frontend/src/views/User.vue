<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const users = ref([]);

onMounted(async () => {
    try {
        const response = await axios.get("");
        users.value = response.data;
    } catch (error) {
        console.error("API error: ", error)
    }
});
</script>

<template>
    <div>
        <h1> List of users</h1>
        <ul>
            <li v-for="user in users" :key="user.id">
                {{  user.name }} - {{ user.email }}
            </li>
        </ul>
    </div>
</template>