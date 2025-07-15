<template>
  <div class="skills">
    <h3>🧠 Detected Skills by Category:</h3>
    <div v-for="(list, cat) in skills" :key="cat">
      <b>{{ cat }}</b
      >: {{ list.join(", ") }}
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
const props = defineProps({ skills: Object });
</script>

<style scoped>
.skills {
  background: #f4f6fb;
  padding: 1.1rem;
  border-radius: 10px;
  font-size: 1.05rem;
  margin-bottom: 1.1rem;
  border: 1px solid #ececff;
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
