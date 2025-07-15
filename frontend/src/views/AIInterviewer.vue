<template>
  <div class="page-bg">
    <div :class="['card', { 'card-interview': store.stage === 'interview' }]">
      <LoadingSpinner v-if="store.loading" />
      <ResumeUpload
        v-else-if="store.stage === 'upload'"
        :loading="store.loading"
        @upload="onResumeUpload"
      />
      <div v-else-if="store.stage === 'skills'" class="section">
        <h2 style="font-size: 1.3rem">
          🎯 Target Job Title:
          <span style="font-weight: 500; color: #6c63ff">
            {{ store.jobTitle || "Not specified" }}
          </span>
        </h2>
        <SkillsList :skills="store.skills" />
        <button @click="store.startInterview" :disabled="store.loading">
          Start Interview
        </button>
      </div>
      <div v-else-if="store.stage === 'interview'" class="section">
        <h2 style="font-size: 1.3rem">🎤 Interview in Progress</h2>
        <InterviewChat />
      </div>
      <div
        v-else-if="store.stage === 'done'"
        class="section"
        style="text-align: center"
      >
        <h2 style="font-size: 1.3rem">🎉 Interview Complete</h2>
        <div style="margin-top: 1.2rem; font-size: 1.1rem; color: #2d2d5a">
          {{
            store.chatHistory.length > 0
              ? store.chatHistory[store.chatHistory.length - 1].text
              : "Thank you!"
          }}
        </div>
        <div v-if="store.chatHistory.length > 0" class="qa-summary">
          <h3 style="margin-top: 2rem; color: #22c55e">
            Questions & Answers Recap
          </h3>
          <table class="qa-table">
            <thead>
              <tr>
                <th>Question</th>
                <th>Your Answer</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="i in qaPairs.length" :key="i - 1">
                <td>{{ qaPairs[i - 1].question }}</td>
                <td>{{ qaPairs[i - 1].answer }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useInterviewStore } from "../stores/interviewStore";
import ResumeUpload from "../components/ResumeUpload.vue";
import SkillsList from "../components/SkillsList.vue";
import InterviewChat from "../components/InterviewChat.vue";
import LoadingSpinner from "../components/LoadingSpinner.vue";
import { computed } from "vue";
const store = useInterviewStore();

function onResumeUpload(e) {
  const form = e.target;
  const formData = new FormData(form);
  store.handleResumeUpload(formData);
}

// Build Q&A pairs for summary table
const qaPairs = computed(() => {
  const pairs = [];
  const history = store.chatHistory;
  for (let i = 0; i < history.length - 1; i++) {
    // Pair every AI message with the next user message
    if (
      history[i] &&
      history[i].role === "ai" &&
      history[i + 1] &&
      history[i + 1].role === "user"
    ) {
      pairs.push({ question: history[i].text, answer: history[i + 1].text });
    }
  }
  return pairs;
});
</script>

<style scoped>
.page-bg {
  min-height: 100vh;
  width: 100vw;
  background: #f7f8fc;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
body {
  background: linear-gradient(120deg, #f4f6fb 60%, #e3e3ff 100%);
  min-height: 100vh;
  font-family: "Segoe UI", "Roboto", Arial, sans-serif;
}
.center-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(120deg, #f4f6fb 60%, #e3e3ff 100%);
}
.card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 6px 32px 0 #6c63ff22;
  padding: 2.8rem 2.2rem 2.2rem 2.2rem;
  max-width: 480px;
  width: 100%;
  margin: 2rem 0;
  display: flex;
  flex-direction: column;
  gap: 1.7rem;
  border: 1px solid #ececff;
}
.card-interview {
  width: 100%;
  min-height: 60vh;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 6px 32px 0 #6c63ff22;
  padding: 2.8rem 2.2rem 2.2rem 2.2rem;
  max-width: 480px;
  width: 100%;
  margin: 2rem 0;
  display: flex;
  flex-direction: column;
  gap: 1.7rem;
  border: 1px solid #ececff;
}
h1,
h2,
h3 {
  margin: 0 0 0.5rem 0;
  font-weight: 700;
  letter-spacing: -1px;
}
h1 {
  font-size: 2.2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.section {
  margin-bottom: 1.7rem;
}
.skills {
  background: #f4f6fb;
  padding: 1.1rem;
  border-radius: 10px;
  font-size: 1.05rem;
  margin-bottom: 1.1rem;
  border: 1px solid #ececff;
}
.chat {
  background: #f9f9ff;
  padding: 1.1rem;
  border-radius: 10px;
  overflow-y: auto;
  font-size: 1.05rem;
  border: 1px solid #ececff;
}
.msg-ai {
  color: #2d2d5a;
  background: #e3e3ff;
  padding: 0.7rem 1rem;
  border-radius: 10px 10px 10px 3px;
  margin-bottom: 0.6rem;
  max-width: 85%;
  word-break: break-word;
}
.msg-user {
  color: #1a3a1a;
  background: #d1ffd1;
  padding: 0.7rem 1rem;
  border-radius: 10px 10px 3px 10px;
  margin-bottom: 0.6rem;
  text-align: right;
  align-self: flex-end;
  max-width: 85%;
  word-break: break-word;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
input[type="file"] {
  background: #f4f6fb;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.6rem;
  font-size: 1.05rem;
}
input[type="text"] {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.7rem;
  font-size: 1.05rem;
  background: #f9f9ff;
  transition: border 0.2s;
}
input[type="text"]:focus {
  border: 2px solid #6c63ff;
  outline: none;
}
button {
  background: #22c55e;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.8rem 1.3rem;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: none;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.emoji {
  font-size: 2.2rem;
  margin-right: 0.2rem;
}
.qa-summary {
  margin-top: 2.5rem;
  text-align: left;
}
.qa-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background: #f9f9ff;
  border-radius: 10px;
  overflow: hidden;
}
.qa-table th,
.qa-table td {
  border: 1px solid #ececff;
  padding: 0.7rem 0.5rem;
  text-align: left;
}
.qa-table th {
  background: #e3ffe3;
  color: #1a3a1a;
}
.qa-table td {
  background: #fff;
}
@media (max-width: 600px) {
  .card {
    max-width: 98vw;
    padding: 1.3rem 0.7rem;
  }
}
</style>
