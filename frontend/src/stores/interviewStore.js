import { defineStore } from "pinia";
import { ref } from "vue";

export const useInterviewStore = defineStore("interview", () => {
  const chatHistory = ref([]);
  const loading = ref(false);
  const userInput = ref("");
  const stage = ref("upload");
  const jobTitle = ref("");
  const skills = ref(null);
  const resumeText = ref("");
  const currentSkillIndex = ref(0);
  const currentDifficultyIndex = ref(0);
  const userDifficulty = ref(["easy", "medium", "difficult"]);
  const selectedTopics = ref([]);
  const phase = ref("intro");

  async function handleResumeUpload(formData) {
    loading.value = true;
    try {
      const res = await fetch("/api/upload_resume", {
        method: "POST",
        credentials: "include",
        body: formData,
      });
      const data = await res.json();
      resumeText.value = data.resume_text;
      skills.value = data.extracted_skills;
      jobTitle.value = data.job_title;
      userDifficulty.value = data.user_difficulty || userDifficulty.value;
      selectedTopics.value = data.selected_topics || [];
      stage.value = "skills";
    } catch (err) {
      alert("Error uploading resume.");
    }
    loading.value = false;
  }

  async function startInterview() {
    loading.value = true;
    const res = await fetch("/api/start_interview", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });
    const data = await res.json();
    chatHistory.value = [
      { role: "ai", text: data.greeting },
      { role: "ai", text: data.first_question },
    ];
    phase.value = "rag";
    stage.value = "interview";
    loading.value = false;
  }

  async function loadRagQuestion() {
    loading.value = true;
    try {
      const res = await fetch("/api/rag_question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ current_skill_index: currentSkillIndex.value }),
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json();
      if (data.end) {
        chatHistory.value.push({
          role: "ai",
          text: data.message || "✅ Interview complete.",
        });
        stage.value = "done";
      } else if (data.rag_question) {
        chatHistory.value.push({ role: "ai", text: data.rag_question });
        phase.value = "followup";
        currentDifficultyIndex.value = 0;
        currentSkillIndex.value = data.next_skill_index;
      } else {
        chatHistory.value.push({
          role: "ai",
          text: data.message || "❓ No question generated.",
        });
      }
    } catch (err) {
      chatHistory.value.push({
        role: "ai",
        text: "⚠️ Failed to load question.",
      });
    } finally {
      loading.value = false;
    }
  }

  async function sendUserInput(input) {
    if (!input.trim()) return;
    loading.value = true;
    chatHistory.value.push({ role: "user", text: input });
    try {
      if (phase.value === "rag") {
        await loadRagQuestion();
        phase.value = "followup";
      } else if (phase.value === "followup") {
        const res = await fetch("/api/followup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({
            user_input: input,
            current_skill_index: currentSkillIndex.value,
            current_difficulty_index: currentDifficultyIndex.value,
          }),
        });
        if (!res.ok) throw new Error("Follow-up fetch failed");
        const data = await res.json();
        if (data.message) {
          chatHistory.value.push({ role: "ai", text: data.message });
        }
        if (data.followup) {
          chatHistory.value.push({
            role: "ai",
            text: `(${data.followup.difficulty}) ${data.followup.question}`,
          });
          currentDifficultyIndex.value = data.next_difficulty_index;
        }
        if (
          data.next_skill_index !== undefined &&
          data.next_skill_index !== currentSkillIndex.value
        ) {
          currentSkillIndex.value = data.next_skill_index;
          currentDifficultyIndex.value = 0;
          await loadRagQuestion();
        }
        if (data.end) {
          stage.value = "done";
        }
      }
    } catch (err) {
      chatHistory.value.push({
        role: "ai",
        text: "⚠️ Failed to process your input.",
      });
    } finally {
      userInput.value = "";
      loading.value = false;
    }
  }

  return {
    chatHistory,
    loading,
    userInput,
    stage,
    jobTitle,
    skills,
    resumeText,
    currentSkillIndex,
    currentDifficultyIndex,
    userDifficulty,
    selectedTopics,
    phase,
    handleResumeUpload,
    startInterview,
    loadRagQuestion,
    sendUserInput,
  };
});
