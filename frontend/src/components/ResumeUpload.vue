<template>
  <div>
    <h1><span class="emoji">📄</span> Upload Resume</h1>
    <div class="desc">
      Upload your resume to extract skills and start your interview.
    </div>
    <form @submit.prevent="onUpload">
      <div class="inputs">
        <input
          type="file"
          name="resume"
          accept=".pdf,.doc,.docx,.txt"
          required
        />
        <input
          type="text"
          name="job_title"
          placeholder="Target Job Title (optional)"
        />
      </div>
      <button type="submit" :disabled="loading">Upload Resume</button>
    </form>
  </div>
</template>

<script setup>
const props = defineProps({ loading: Boolean });
const emit = defineEmits(["upload"]);

function onUpload(e) {
  emit("upload", e);
}
</script>

<style scoped>
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
h1 {
  font-size: 2.2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.5rem 0;
  font-weight: 700;
  letter-spacing: -1px;
}
.emoji {
  font-size: 2.2rem;
  margin-right: 0.2rem;
}
.desc {
  margin-bottom: 0.7rem;
  color: #444;
  font-size: 1.08rem;
  text-align: center;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  width: 100%;
  align-items: center;
}
.inputs {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  width: 100%;
  justify-content: center;
}
input[type="file"],
input[type="text"] {
  background: #f4f6fb;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.6rem;
  font-size: 1.05rem;
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
@media (max-width: 600px) {
  .card {
    max-width: 98vw;
    padding: 1.3rem 0.7rem;
  }
}
</style>
