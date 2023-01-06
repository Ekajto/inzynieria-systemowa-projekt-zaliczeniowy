<template>
  <div>
    <h3>{{ todo.to_do }}</h3>
    <input type="checkbox" v-model="checked" :v-on:checked="toggle" />
    <button @click="remove()">Remove</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
const checked = computed({
  get() {
    return props.todo.completed;
  },
  set(value) {
    toggle(value);
  },
});
const props = defineProps({
  todo: {
    type: Object,
    required: true,
  },
});
const emits = defineEmits(["todo-removed", "todo-toggled"]);
const toggle = (completed: boolean) => {
  emits("todo-toggled", { id: props.todo.id, completed });
};
const remove = () => emits("todo-removed", props.todo.id);
</script>

<style scoped></style>
