<template>
  <div id="app">
    <PromptPage ref="promptPage" v-if="!outputVisible" @submit="handlePromptSubmit" />
    <OutputPage v-else :generatedText="generatedText" :loading="loading" @back="reset" />
  </div>
</template>

<script>
import PromptPage from './PromptPage.vue'
import OutputPage from './OutputPage.vue'
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
      loading: false
    }
  },
  methods: {
    async handlePromptSubmit(promptData) {
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
    reset() {
      this.outputVisible = false;
      this.generatedText = '';
      this.loading = false;
      // Clear error message on reset
      if (this.$refs.promptPage) {
        this.$refs.promptPage.errorMessage = '';
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 50px;
}
</style>
