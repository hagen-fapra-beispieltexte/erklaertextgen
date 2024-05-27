<template>
  <div class="container">
    <h1 class="title">KLUG - Kinder-Lerntext und Unterrichtstext Generator</h1>
    <div class="output-container" v-if="!loading">
      <h2>Hier siehst du deinen Text</h2>
      <div class="output-text">{{ generatedText }}</div>
      <button @click="goBack" class="back-button">Zurück zur Eingabe</button>
    </div>
    <div class="loading-container" v-else>
      <h2>Hier entsteht dein Text...</h2>
    </div>
  </div>
</template>

<script>
export default {
  props: ['generatedText', 'loading'],
  methods: {
    goBack() {
      this.$emit('back');
    }
  }
}
</script>

<style>
.container {
  padding: 20px;
  font-family: Arial, sans-serif;
}
.title {
  font-size: 16pt;
  text-align: left;
  margin-bottom: 20px;
}
.output-container, .loading-container {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  background-color: #f9f9f9;
}
.output-text {
  margin: 20px 0;
  background-color: #81d4fa;
  padding: 20px;
  border-radius: 10px;
}
.back-button {
  background-color: #81d4fa;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  cursor: pointer;
}
</style>