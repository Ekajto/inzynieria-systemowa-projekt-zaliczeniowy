<template>
  <div>
    <form @submit.prevent="addTodo">
      <input v-model="to_do" type="text" />
      <button :disabled="!to_do.length" type="submit">Add todo</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { defineEmits, ref } from "vue";
const to_do = ref("");
const emits = defineEmits(["todo-added"]);
function addTodo() {
  emits("todo-added", to_do.value);
  to_do.value = "";
}
</script>

<style scoped></style>
