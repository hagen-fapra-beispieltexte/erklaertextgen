<template>
  <div>
    <PromptPage 
      :initialPrompt="initialPrompt"
      :initialLength="initialLength"
      :initialTextType="initialTextType"
      @submit="handlePromptSubmit" 
    />
    <OutputPage 
      v-if="outputVisible" 
      :generatedText="generatedText" 
      :loading="loading" 
      :initialPrompt="initialPrompt"
      :initialLength="initialLength"
      :initialTextType="initialTextType"
      @retry="handleRetry"
    />
  </div>
</template>

<script>
import PromptPage from '../components/PromptPage.vue'
import OutputPage from '../components/OutputPage.vue'
import axios from 'axios'

export default {
  components: {
    PromptPage,
    OutputPage
  },
  data() {
    return {
      outputVisible: false,
      generatedText: '',
      loading: false,
      initialPrompt: '',
      initialLength: 0,
      initialTextType: ''
    }
  },
  methods: {
    async handlePromptSubmit(promptData) {
      this.initialPrompt = promptData.prompt;
      this.initialLength = promptData.length;
      this.initialTextType = promptData.textType;
      this.loading = true;
      this.outputVisible = true;

      try {
        const response = await axios.post('http://localhost:5000/generate_text', promptData);
        this.generatedText = response.data.generated_text;
      } catch (error) {
        this.generatedText = 'Fehler beim Abrufen des Textes';
      } finally {
        this.loading = false;
      }
    },
    handleRetry(data) {
      this.initialPrompt = data.prompt;
      this.initialLength = data.length;
      this.initialTextType = data.textType;
      this.outputVisible = false;
    }
  }
}
</script>


<style>
/* Add your styles here */
</style>