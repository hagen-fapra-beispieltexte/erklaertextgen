<template>
  <div class="outer-container">
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
            <div class="label">{{ textType === 'Geschichte' ? 'Thema der Geschichte?' : 'Was soll erklärt werden?' }}</div>
          </div>
          <div class="input-cell">
            <input type="text" v-model="prompt" @keyup.enter="submitPrompt" placeholder="Gib hier ein Wort ein..." class="input-field" />
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      length: 0,
      textType: '',
      prompt: '',
      errorMessage: ''
    }
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
.outer-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
}

.container {
  padding: 20px;
  font-family: Arial, sans-serif;
  width: 800px;  /* Feste Breite */
  height: 400px; /* Feste Höhe */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: white;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.title {
  font-size: 16pt;
  text-align: center;
  margin-bottom: 20px;
  color: #303f9f;
}

.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.form-row {
  display: flex;
  flex-direction: row;
  width: 100%;
  margin-bottom: 20px;
}

.label-cell, .input-cell {
  flex: 1;
}

.label-cell {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.input-cell {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 5px;
  padding: 5px;
}

.label {
  background-color: #303f9f;
  color: white;
  border-radius: 10px;
  padding: 10px;
  text-align: center;
  width: 80%;
}

.slider-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.slider {
  width: 98%;
  margin-bottom: 10px;
  -webkit-appearance: none;
  height: 10px;
  border-radius: 5px;
  background: #81d4fa;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #0288d1;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #0288d1;
  cursor: pointer;
}

.slider-buttons {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.slider-buttons button {
  background-color: #81d4fa;
  border: none;
  border-radius: 10px;
  padding: 10px;
  cursor: pointer;
  flex: 1;
  margin: 0 5px;
}

.slider-buttons button.selected {
  background-color: #0288d1;
  color: white;
}

.text-type-buttons {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.text-type-buttons button {
  background-color: #81d4fa;
  border: none;
  border-radius: 10px;
  padding: 10px;
  cursor: pointer;
  flex: 1;
  margin: 0 5px;
}

.text-type-buttons button.selected {
  background-color: #0288d1;
  color: white;
}

button {
  background-color: #81d4fa;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  cursor: pointer;
}

button.selected {
  background-color: #0288d1;
  color: white;
}

.input-field {
  width: 98%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.submit-button {
  background-color: #0288d1;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  cursor: pointer;
  width: 100%;
  text-align: center;
}

.full-width-button {
  width: calc(100% - 40px);
  margin: 0 20px;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.centered-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

/* Slider color changes based on length value */
.slider-length-1 {
  background: #0288d1;
}

.slider-length-2 {
  background: #0277bd;
}

.slider-length-3 {
  background: #01579b;
}

/* Media queries to handle responsiveness */
@media (max-width: 800px) {
  .form-row {
    flex-direction: column;
  }

  .label-cell, .input-cell {
    width: 100%;
    justify-content: center;
  }

  .label {
    width: 100%;
    text-align: center;
  }
}
</style>