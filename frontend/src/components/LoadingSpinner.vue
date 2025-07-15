<template>
  <div
    style="
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 200px;
    "
  >
    <div class="spinner"></div>
    <div class="loading-text">Loading...</div>
  </div>
</template>

<script setup>
// No logic needed
</script>

<style scoped>
.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #6c63ff;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}
.loading-text {
  text-align: center;
  color: #444;
  font-size: 1.08rem;
  margin-top: 0.5rem;
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
