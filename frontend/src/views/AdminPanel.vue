<template>
  <div class="admin-panel">
    <h1>Admin Panel</h1>
    <section class="admin-section">
      <h2>All Questions</h2>
      <button @click="fetchQuestions" :disabled="loading">Refresh</button>
      <div v-if="loading" class="admin-loading">Loading...</div>
      <table v-if="questions.length" class="admin-table">
        <thead>
          <tr>
            <th>Question</th>
            <th>Skill</th>
            <th>Difficulty</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="q in questions" :key="q.id">
            <td>{{ q.question }}</td>
            <td>{{ q.skill }}</td>
            <td>{{ q.difficulty }}</td>
            <td>
              <button @click="removeQuestion(q.id)" :disabled="loading">
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else-if="!loading">No questions found.</div>
    </section>
    <section class="admin-section">
      <h2>Add New Question</h2>
      <form @submit.prevent="addQuestion">
        <input v-model="newQuestion.question" placeholder="Question" required />
        <input v-model="newQuestion.skill" placeholder="Skill" required />
        <select v-model="newQuestion.difficulty" required>
          <option value="">Select Difficulty</option>
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>
        <button type="submit" :disabled="loading">Add Question</button>
      </form>
      <div v-if="addMsg" class="admin-msg">{{ addMsg }}</div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
const questions = ref([]);
const loading = ref(false);
const addMsg = ref("");
const newQuestion = ref({
  question: "",
  skill: "",
  difficulty: "Easy",
  category: "",
});

async function fetchQuestions() {
  loading.value = true;
  try {
    const res = await fetch("/api/admin/list_questions");
    const data = await res.json();
    questions.value = data.questions || [];
  } finally {
    loading.value = false;
  }
}

async function removeQuestion(id) {
  if (!confirm("Remove this question?")) return;
  loading.value = true;
  try {
    await fetch("/api/admin/remove_question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id }),
    });
    await fetchQuestions();
  } finally {
    loading.value = false;
  }
}

async function addQuestion() {
  loading.value = true;
  addMsg.value = "";
  try {
    const res = await fetch("/api/admin/add_question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newQuestion.value),
    });
    const data = await res.json();
    addMsg.value = data.message || (data.success ? "Added!" : "Error");
    if (data.success) {
      newQuestion.value = {
        question: "",
        skill: "",
        difficulty: "Easy",
      };
      await fetchQuestions();
    }
  } finally {
    loading.value = false;
  }
}

fetchQuestions();
</script>

<style scoped>
.admin-panel {
  max-width: 700px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 6px 32px 0 #6c63ff22;
  padding: 2.5rem 2rem;
}
h1 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #6c63ff;
}
.admin-section {
  margin-bottom: 2.5rem;
}
.admin-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.admin-table th,
.admin-table td {
  border: 1px solid #ececff;
  padding: 0.7rem 0.5rem;
  text-align: left;
}
.admin-table th {
  background: #f4f6fb;
}
.admin-loading {
  color: #6c63ff;
  margin: 1rem 0;
}
.admin-msg {
  margin-top: 1rem;
  color: #2d2d5a;
}
form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
  margin-top: 1rem;
}
input {
  flex: 1 1 180px;
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  background: #f4f6fb;
  font-size: 1rem;
}
select {
  flex: 1 1 180px;
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  background: #f4f6fb;
  font-size: 1rem;
}
button {
  background: #22c55e;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 1.2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: none;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
