import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  root: ".",
  plugins: [vue()],
  server: {
    port: 3000,
    open: true,
    proxy: {
      "/api/upload_resume": "http://127.0.0.1:8000",
      "/api/start_interview": "http://127.0.0.1:8000",
      "/api/followup": "http://127.0.0.1:8000",
      "/api/rag_question": "http://127.0.0.1:8000", // if using separate RAG endpoint
      "/api/admin/list_questions": "http://127.0.0.1:8000",
      "/api/admin/add_question": "http://127.0.0.1:8000",
      "/api/admin/remove_question": "http://127.0.0.1:8000",
    },
  },
});
