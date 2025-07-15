<template>
  <div class="chat">
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(msg, idx) in store.chatHistory"
        :key="idx"
        :class="msg.role === 'ai' ? 'msg-ai' : 'msg-user'"
      >
        {{ msg.text }}
      </div>
    </div>
    <form class="chat-input" @submit.prevent="onSend">
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
import { ref, watch, onMounted, nextTick } from "vue";
import { useInterviewStore } from "../stores/interviewStore";

const store = useInterviewStore();
const inputValue = ref(store.userInput);
const messagesContainer = ref(null);

watch(
  () => store.userInput,
  (val) => {
    inputValue.value = val;
  }
);

// Auto-scroll to bottom when chatHistory changes
watch(
  () => store.chatHistory.length,
  async () => {
    await nextTick();
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
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
  display: flex;
  flex-direction: column;
  font-size: 1.05rem;
  border: 1px solid #ececff;
}
.chat-messages {
  flex: 1 1 auto;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.chat-input {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: auto;
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
/* form styles now in .chat-input */
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
