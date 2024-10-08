<template>
  <div class="container">
    <h1 class="title">KLUG - Kinder-Lerntext und Unterrichtstext Generator</h1>
    <div class="form-container">
      <div class="form-row">
        <div class="label-cell">
          <div class="label">Wie lang soll dein Text sein?</div>
        </div>
        <div class="input-cell">
          <div class="slider-container">
            <input type="range" min="1" max="3" v-model="length" class="slider" @input="updateButtonsAndSlider" />
            <div class="slider-buttons">
              <button @click="setLength(1)" :class="{'selected': length === 1}">kurz</button>
              <button @click="setLength(2)" :class="{'selected': length === 2}">mittel</button>
              <button @click="setLength(3)" :class="{'selected': length === 3}">lang</button>
            </div>
          </div>
        </div>
      </div>
      <div class="form-row">
        <div class="label-cell">
          <div class="label">Welche Art von Text?</div>
        </div>
        <div class="input-cell">
          <div class="text-type-buttons">
            <button @click="selectTextType('Geschichte')" :class="{'selected': textType === 'Geschichte'}">Geschichte</button>
            <button @click="selectTextType('Erklärtext')" :class="{'selected': textType === 'Erklärtext'}">Erklärtext</button>
          </div>
        </div>
      </div>
      <div class="form-row">
        <div class="label-cell">
          <div class="label">{{ textType === '' ? 'Wähle Erklärtext, oder Geschichte aus!' : (textType === 'Geschichte' ? 'Titel einer Geschichte eingeben!' : 'Formuliere deine Frage!') }}</div>
        </div>
        <div class="input-cell">
          <input 
            type="text" 
            v-model="prompt" 
            @keyup.enter="submitPrompt" 
            :disabled="textType === ''"
            :placeholder="textType === '' ? 'Wähle Erklärtext, oder Geschichte aus!' : (textType === 'Geschichte' ? 'Titel einer Geschichte eingeben!' : 'Formuliere deine Frage!')" 
            :class="{'disabled': textType === ''}"
            class="input-field" 
          />
        </div>
      </div>
      <div class="form-row">
        <div class="label-cell"></div>
        <div class="input-cell">
          <button @click="submitPrompt" class="submit-button full-width-button">Drücke hier, um die Eingabe abzusenden!</button>
        </div>
      </div>
    </div>
    <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  props: ['initialPrompt', 'initialLength', 'initialTextType'],
  data() {
    return {
      length: this.initialLength || 0,
      textType: this.initialTextType || '',
      prompt: this.initialPrompt || '',
      errorMessage: ''
    };
  },
  methods: {
    setLength(value) {
      this.length = value;
      this.updateButtonsAndSlider();
    },
    selectTextType(type) {
      this.textType = type;
    },
    submitPrompt() {
      if (this.textType && this.prompt) {
        this.errorMessage = '';
        this.$emit('submit', { length: this.length, textType: this.textType, prompt: this.prompt });
      } else {
        this.errorMessage = 'Bitte füllen Sie alle Felder aus.';
      }
    },
    updateButtonsAndSlider() {
      this.updateButtons();
      this.updateSliderColor();
    },
    updateButtons() {
      const buttons = document.querySelectorAll('.slider-buttons button');
      buttons.forEach((button, index) => {
        if (index + 1 === this.length) {
          button.classList.add('selected');
        } else {
          button.classList.remove('selected');
        }
      });
    },
    updateSliderColor() {
      const slider = document.querySelector('.slider');
      slider.classList.remove('slider-length-1', 'slider-length-2', 'slider-length-3');
      slider.classList.add(`slider-length-${this.length}`);
    }
  },
  watch: {
    length() {
      this.updateSliderColor();
    }
  },
  mounted() {
    this.updateButtonsAndSlider();
  }
}
</script>

<style scoped>
/* Dynamischer Container, der sich an die Fenstergröße anpasst */
.container {
  position: absolute; /* Absolut positioniert relativ zum Viewport */
  top: 50%; /* Vertikal zentriert */
  left: 50%; /* Horizontal zentriert */
  transform: translate(-50%, -50%); /* Verschiebt um die Hälfte der eigenen Größe, um exakte Zentrierung zu erreichen */
  width: 100vw; /* % der Fensterbreite */
  max-width: 1600px; /* Maximale Breite 1600px */
  height: auto; /* Höhe wird durch Seitenverhältnis bestimmt */
  aspect-ratio: 2 / 1; /* Seitenverhältnis 2:1 */
  padding: 2.5vw; /* Padding relativ zur Fensterbreite */
  font-family: Arial, sans-serif; /* Schriftart */
  box-shadow: 0 0 1vw rgba(0, 0, 0, 0.1); /* Schatten relativ zur Fensterbreite */
  background-color: white; /* Hintergrundfarbe */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  display: flex; /* Flexbox-Modell */
  flex-direction: column;
  justify-content: space-between;
  margin: auto; /* Zentriert den Container horizontal */
}

.title {
  font-size: 3vw; 
  text-align: center; 
  margin-bottom: 2vw; 
  color: #303f9f; /* Schriftfarbe Überschrift */
}

.form-container {
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  width: 100%; /* Breite 100% */
}

.form-row {
  display: flex; 
  flex-direction: row; 
  width: 100%; /* Breite 100% */
  margin-bottom: 2vw; /* Margin unten 2% der Fensterbreite */
}

.label-cell, .input-cell {
  flex: 1; /* Flex-Grow 1 */
}

.label-cell {
  display: flex; 
  justify-content: flex-end; /* Inhalt rechtsbündig */
  align-items: center; /* Inhalt zentriert */
  padding: 0; 
  margin: 0; 
}

.input-cell {
  display: flex; 
  justify-content: center; /* Inhalt zentriert */
  align-items: center; /* Inhalt zentriert */
}

.label {
  background-color: #303f9f; /* Hintergrundfarbe */
  color: white; /* Schriftfarbe */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  padding: 1vw; 
  text-align: center; 
  width: 100%; /* Breite der dunkelblauen Anweisungstexte */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}

.slider-container {
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  width: 100%; 
}

.slider {
  width: 98%; 
  margin-bottom: 1vw; /* Margin unten 1% der Fensterbreite */
  -webkit-appearance: none; /* Entfernt Standardstil in Webkit */
  height: 1vw; /* Höhe 1% der Fensterbreite */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  background: #81d4fa; /* Hintergrundfarbe */
  outline: none; /* Kein Umriss */
  opacity: 0.7; /* Opazität */
  -webkit-transition: .2s; /* Transition in Webkit */
  transition: opacity .2s; /* Transition für Opazität */
}

.slider:hover {
  opacity: 1; /* Opazität bei Hover */
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none; /* Entfernt Standardstil in Webkit */
  appearance: none; /* Entfernt Standardstil */
  width: 3vw; /* Breite 3% der Fensterbreite */
  height: 3vw; /* Höhe 3% der Fensterbreite */
  border-radius: 50%; /* Radius der Ecken 50% */
  background: #0288d1; /* Hintergrundfarbe */
  cursor: pointer; /* Cursor wird Zeiger */
}

.slider::-moz-range-thumb {
  width: 3vw; /* Breite 3% der Fensterbreite */
  height: 3vw; /* Höhe 3% der Fensterbreite */
  border-radius: 50%; /* Radius der Ecken 50% */
  background: #0288d1; /* Hintergrundfarbe */
  cursor: pointer; /* Cursor wird Zeiger */
}

.slider-buttons {
  display: flex; 
  justify-content: space-between; 
  width: 100%; 
}

.slider-buttons button {
  background-color: #b3e5fc; /* Hintergrundfarbe kurz button */
  border: none; /* Kein Rahmen */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  padding: 1vw; /* Padding relativ zur Fensterbreite */
  cursor: pointer; /* Cursor wird Zeiger */
  flex: 1; /* Flex-Grow 1 */
  margin: 0 0.5vw; /* Margin horizontal 0.5% der Fensterbreite */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}

.slider-buttons button:nth-child(2) {
  background-color: #4fc3f7; /* Hintergrundfarbe mittel button */
}

.slider-buttons button:nth-child(3) {
  background-color: #03a9f4; /* Hintergrundfarbe lang button */
}

.slider-buttons button.selected {
  background-color: #303f9f; /* Farbe für gedrückte Buttons am SLIDER */
  color: white; /* Schriftfarbe gedrückte Buttons */
}

.text-type-buttons {
  display: flex; /* Flexbox-Modell */
  justify-content: space-between; /* Verteilung der Kinder */
  width: 100%; /* Breite 100% */
}

.text-type-buttons button {
  background-color: #b3e5fc; /* Hintergrundfarbe geschichte button */
  border: none; /* Kein Rahmen */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  padding: 1vw; /* Padding relativ zur Fensterbreite */
  cursor: pointer; /* Cursor wird Zeiger */
  flex: 1; /* Flex-Grow 1 */
  margin: 0 0.5vw; /* Margin horizontal 0.5% der Fensterbreite */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}

.text-type-buttons button:nth-child(2) {
  background-color: #4fc3f7; /* Hintergrundfarbe erklärtext button */
}

.text-type-buttons button.selected {
  background-color: #303f9f; /* Farbe für gedrückte Buttons TEXTART */
  color: white; /* Schriftfarbe */
}

button {
  background-color: #81d4fa; /* Hintergrundfarbe */
  border: none; /* Kein Rahmen */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  padding: 1vw 2vw; /* Padding vertikal 1vw, horizontal 2vw */
  cursor: pointer; /* Cursor wird Zeiger */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}

button.selected {
  background-color: #0288d1; /* Hintergrundfarbe */
  color: white; /* Schriftfarbe */
}

.input-field {
  width: 98%; /* Breite 100% */
  padding: 1vw; /* Padding relativ zur Fensterbreite */
  border: 0.25vw solid #ccc; /* Rahmen relativ zur Fensterbreite */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}

.input-field.disabled {
  background-color: #e0e0e0;
  cursor: not-allowed;
}

.submit-button {
  background-color: #0288d1; /* Hintergrundfarbe */
  color: white; /* Schriftfarbe */
  border: none; /* Kein Rahmen */
  border-radius: 1vw; /* Radius der Ecken relativ zur Fensterbreite */
  padding: 1vw 2vw; /* Padding vertikal 1vw, horizontal 2vw */
  cursor: pointer; /* Cursor wird Zeiger */
  width: 100%; /* Breite 100% */
  text-align: center; /* Textzentrierung */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}

.full-width-button {
  width: 98%; /* Breite 100% */
}

.error-message {
  color: red; /* Schriftfarbe */
  margin-top: 1vw; /* Margin oben relativ zur Fensterbreite */
  font-size: 2vw; /* Schriftgröße 2% der Fensterbreite */
}

.centered-button {
  display: flex; /* Flexbox-Modell */
  justify-content: center; /* Inhalt zentriert */
  align-items: center; /* Inhalt zentriert */
  width: 100%; /* Breite 100% */
}

/* Slider color changes based on length value */
.slider-length-1 {
  background: #0288d1; /* Hintergrundfarbe */
}

.slider-length-2 {
  background: #0277bd; /* Hintergrundfarbe */
}

.slider-length-3 {
  background: #01579b; /* Hintergrundfarbe */
}

/* Media queries to handle responsiveness */
@media (max-width: 800px) {
  .container {
    padding: 5vw; /* Padding 5% der Fensterbreite */
  }

  .form-row {
    flex-direction: column; /* Anordnung in Spalte */
  }

  .label-cell, .input-cell {
    width: 100%; /* Breite 100% */
    justify-content: center; /* Inhalt zentriert */
  }

  .label {
    width: 100%; /* Breite 100% */
    text-align: center; /* Textzentrierung */
  }
}
</style>
