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

<style scoped>
/* Der Container passt sich dynamisch an die Breite an, mit einer maximalen Breite von 1600px und einem festen Seitenverhältnis von 2:1 */
.container {
  position: absolute; /* Absolut positioniert relativ zum Viewport */
  top: 50%; /* Vertikal zentriert */
  left: 50%; /* Horizontal zentriert */
  transform: translate(-50%, -50%); /* Verschiebt um die Hälfte der eigenen Größe, um exakte Zentrierung zu erreichen */
  width: 80vw; /* 80% der Fensterbreite */
  max-width: 1600px; /* Maximale Breite 1600px */
  height: auto; /* Höhe wird durch Seitenverhältnis bestimmt */
  aspect-ratio: 2 / 1; /* Seitenverhältnis 2:1 */
  padding: 2.5vw; /* Padding relativ zur Fensterbreite */
  font-family: Arial, sans-serif; /* Schriftart */
  box-shadow: 0 0 1vw rgba(0, 0, 0, 0.1); /* Schatten relativ zur Fensterbreite */
  background-color: white; /* Hintergrundfarbe */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  display: flex; /* Flexbox-Modell */
  flex-direction: column; /* Anordnung der Kinder in Spalte */
  justify-content: space-between; /* Verteilung der Kinder */
}

.title {
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
  text-align: center; /* Textzentrierung */
  margin-bottom: 2vw; /* Margin unten 2% der Fensterbreite */
  color: #303f9f; /* Schriftfarbe */
}

.output-container, .loading-container {
  border: 0.25vw solid #ccc; /* Rahmen relativ zur Fensterbreite */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  padding: 2.5vw; /* Padding relativ zur Fensterbreite */
  background-color: #f9f9f9; /* Hintergrundfarbe */
  flex: 1; /* Flex-Wachstum, damit die Container den verfügbaren Platz nutzen */
  display: flex; /* Flexbox-Modell */
  flex-direction: column; /* Anordnung in Spalte */
  color: #29b6f6; /* Textfarbe */
  justify-content: center; /* Zentriert den Inhalt vertikal */
  align-items: center; /* Zentriert den Inhalt horizontal */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}

.output-text {
  margin: 2.5vw 0; /* Margin vertikal relativ zur Fensterbreite */
  background-color: #81d4fa; /* Hintergrundfarbe */
  padding: 2.5vw; /* Padding relativ zur Fensterbreite */
  color: #000000; /* Textfarbe */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  width: 100%; /* Text nimmt die gesamte Breite des Containers ein */
  text-align: center; /* Text wird zentriert angezeigt */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}

.back-button {
  color: #ffffff; /* Schriftfarbe */
  background-color: #0288d1; /* Hintergrundfarbe */
  border: none; /* Kein Rahmen */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  padding: 1vw 2vw; /* Padding vertikal 1vw, horizontal 2vw */
  cursor: pointer; /* Cursor wird Zeiger */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}
</style>
