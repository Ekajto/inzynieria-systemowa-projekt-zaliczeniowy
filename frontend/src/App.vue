<script setup lang="ts">
import { storeToRefs } from "pinia";
import TodoInput from "./components/AddToDoForm.vue";
import TodoItem from "./components/ToDoItem.vue";
import { useTodoStore } from "./stores/todo";
const store = useTodoStore();
const { todos } = storeToRefs(store);
const { createTodo, doneTodo, deleteTodo } = store;
</script>

<template>
  <main>
    <todo-input @todo-added="createTodo" />
    <ul>
      <todo-item
        v-for="todo in todos"
        :key="todo.id"
        :todo="todo"
        @todo-toggled="doneTodo"
        @todo-removed="deleteTodo"
      />
    </ul>
  </main>
</template>

<style scoped></style>
