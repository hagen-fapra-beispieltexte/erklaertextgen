<template>
  <div class="outer-container">
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
.outer-container {
  display: flex;
  justify-content: center; /* Zentriert den Container horizontal */
  align-items: center; /* Zentriert den Container vertikal */
  height: 100vh; /* Macht den outer-container so hoch wie das Viewport */
  background-color: #f0f0f0; /* Hintergrundfarbe des outer-container */
}

.container {
  padding: 20px;
  font-family: Arial, sans-serif;
  width: 800px;  /* Feste Breite */
  height: 400px; /* Feste Höhe */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Ein wenig Schatten für ein besseres visuelles Ergebnis */
  background-color: white; /* Hintergrundfarbe des Containers */
  border-radius: 10px; /* Abrundung der Ecken */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
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
  flex: 1; /* Flex-Wachstum, damit die Container den verfügbaren Platz nutzen */
  display: flex;
  flex-direction: column;
  justify-content: center; /* Zentriert den Inhalt vertikal */
  align-items: center; /* Zentriert den Inhalt horizontal */
}
.output-text {
  margin: 20px 0;
  background-color: #81d4fa;
  padding: 20px;
  border-radius: 10px;
  width: 100%; /* Text nimmt die gesamte Breite des Containers ein */
  text-align: center; /* Text wird zentriert angezeigt */
}
.back-button {
  background-color: #81d4fa;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  cursor: pointer;
}
</style>