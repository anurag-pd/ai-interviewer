<template>
  <div class="chat">
    <div
      v-for="(msg, idx) in store.chatHistory"
      :key="idx"
      :class="msg.role === 'ai' ? 'msg-ai' : 'msg-user'"
    >
      {{ msg.text }}
    </div>
    <form @submit.prevent="onSend">
      <input
        type="text"
        v-model="inputValue"
        :disabled="store.loading"
        placeholder="Type your answer..."
      />
      <button type="submit" :disabled="store.loading || !inputValue.trim()">
        Send
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useInterviewStore } from "../stores/interviewStore";
const store = useInterviewStore();
const inputValue = ref(store.userInput);

watch(
  () => store.userInput,
  (val) => {
    inputValue.value = val;
  }
);

function onSend() {
  store.sendUserInput(inputValue.value);
}
</script>

<style scoped>
.chat {
  background: #f9f9ff;
  padding: 1.1rem;
  border-radius: 10px;
  min-height: 180px;
  max-height: 320px;
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
</style>
