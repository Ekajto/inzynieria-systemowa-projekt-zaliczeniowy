import axios from "axios";
import { defineStore } from "pinia";
import { ref, type Ref } from "vue";

const api = axios.create({
  baseURL: process.env.BACKEND_APP_PORT
    ? `http://localhost:${process.env.BACKEND_APP_PORT}`
    : "http://localhost:8000",
});

type Todo = {
  id: number;
  to_do: string;
  is_done: string;
  create_date: string;
};

export const useTodoStore = defineStore("todo", () => {
  const todos: Ref<Todo[]> = ref([]);

  async function getAllTodos() {
    try {
      const { data } = await api.get("/todos");
      todos.value = data as Todo[];
    } catch (e) {
      todos.value = [];
    }
  }

  async function createTodo(to_do: string) {
    await api.post("/todos", { to_do });
    await getAllTodos();
  }

  async function deleteTodo(id: number) {
    try {
      await api.delete(`/todos/${id}`);
    } catch (e) {
      console.error(e);
    }
    getAllTodos();
  }

  async function doneTodo({ id }: { id: number }) {
    try {
      await api.put(`/todos/${id}/done`);
    } catch (e) {
      console.error(e);
    }
    getAllTodos();
  }

  getAllTodos();
  return {
    todos,
    createTodo,
    deleteTodo,
    doneTodo,
    getAllTodos,
  };
});
