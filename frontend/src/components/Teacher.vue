<template>
  <div class="outer-container">
    <div class="container">
      <h1 class="title">
        LUSTiG - Lehrer Unterrichts- und Schultext Generator
      </h1>
      <div class="instructions">
        Wählen Sie die Art des Textes aus und geben Sie ein Thema ein.
      </div>
      <div class="form-container">
        <div class="form-row">
          <div class="label-cell">
            <div class="label">Maximale Textlänge in Wörtern</div>
          </div>
          <div class="input-cell">
            <input 
              type="number" 
              v-model="maxWords" 
              @input="updateMaxTokens" 
              class="input-field" 
              placeholder="Maximale Wortanzahl" 
            />
          </div>
        </div>
        <div class="form-row">
          <div class="label-cell"></div>
          <div class="input-cell">
            <input type="range" min="0" max="250" v-model="maxWords" class="slider" @input="updateMaxTokens" />
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
            <div class="label">{{ textType === 'Geschichte' ? 'Titel einer Geschichte' : textType === 'Erklärtext' ? 'Thema des Erklärtextes' : 'Erst Art des Textes wählen' }}</div>
          </div>
          <div class="input-cell">
            <input 
              type="text" 
              v-model="prompt" 
              @keyup.enter="submitPrompt" 
              :disabled="textType === ''"
              :placeholder="textType === '' ? 'Erst Art des Textes wählen' : ''" 
              :class="{'disabled': textType === ''}"
              class="input-field" 
            />
          </div>
        </div>
        <div class="form-row">
          <div class="label-cell"></div>
          <div class="input-cell">
            <button @click="submitPrompt" class="submit-button full-width-button">{{ generatedText ? 'Text neu generieren' : 'Text generieren' }}</button>
          </div>
        </div>
      </div>
      <div class="output-container" v-if="generatedText">
        <textarea v-model="editableText" class="editable-output" ref="textarea"></textarea>
        <vue-markdown-it :source="editableText"></vue-markdown-it>
        <div class="button-container">
          <button @click="downloadTextWithVocabList" class="download-button">Text mit Vokabelliste herunterladen</button>
          <button @click="copyToClipboard" class="copy-button">Text mit Vokabelliste in den Zwischenspeicher laden</button>
        </div>
      </div>
      <div class="vocab-list">
        <h3 class="vocab-title">Vokabelliste</h3>
        <table>
          <tbody>
            <tr v-for="(synonymEntry, index) in synonymList" :key="index">
              <td><input v-model="synonymEntry.word" /></td>
              <td><input v-model="synonymEntry.synonyms" /></td>
              <td><button @click="removeSynonym(index)">Wort löschen</button></td>
            </tr>
          </tbody>
        </table>
        <button @click="addSynonym" class="add-synonym-button">+</button>
      </div>
    </div>
  </div>
</template>

<script>
import { VueMarkdownIt } from 'vue3-markdown-it';

export default {
  components: {
    VueMarkdownIt
  },
  data() {
    return {
      maxWords: 0,
      maxTokens: 0,
      textType: '',
      prompt: '',
      generatedText: '',
      editableText: '',
      synonymList: []
    };
  },
  methods: {
    updateMaxTokens() {
      this.maxTokens = Math.round(this.maxWords * 1.33);
    },
    selectTextType(type) {
      this.textType = type;
    },
    submitPrompt() {
      if (this.textType && this.prompt && this.maxTokens > 0) {
        const promptData = { length: this.maxTokens, textType: this.textType, prompt: this.prompt };
        fetch('http://localhost:5000/generate_text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(promptData)
        })
        .then(response => response.json())
        .then(data => {
          this.generatedText = data.generated_text;
          this.editableText = data.generated_text;
        });
      } else {
        this.errorMessage = 'Bitte füllen Sie alle Felder aus.';
      }
    },
    addSynonym() {
      this.synonymList.push({ word: '', synonyms: '' });
    },
    removeSynonym(index) {
      this.synonymList.splice(index, 1);
    },
    downloadTextWithVocabList() {
      let vocabString = 'Vokabeln: ';
      this.synonymList.forEach(entry => {
        vocabString += `${entry.word}: ${entry.synonyms}; `;
      });
      const fullText = `${this.editableText}\n\n${vocabString}`;
      const blob = new Blob([fullText], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'text_with_vocab.txt';
      a.click();
      URL.revokeObjectURL(url);
    },
    copyToClipboard() {
      let vocabString = 'Vokabeln: ';
      this.synonymList.forEach(entry => {
        vocabString += `${entry.word}: ${entry.synonyms}; `;
      });
      const fullText = `${this.editableText}\n\n${vocabString}`;
      navigator.clipboard.writeText(fullText).then(() => {
        alert('Text mit Vokabelliste wurde in den Zwischenspeicher geladen.');
      });
    }
  }
}
</script>

<style scoped>
body, html {
  height: 100%;
  width: 100%;
  margin: 0;
}

.outer-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 98vw;
  height: auto;
  aspect-ratio: 2 / 1;
  padding: 0.5vw;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 1vw rgba(0, 0, 0, 0.1);
  background-color: white;
  border-radius: 1vw;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: auto;
}

.container {
  width: 95vw;
  height: 95vh;
  padding: 0vw;
  font-family: Arial, sans-serif;
  box-shadow: 0 0 1vw rgba(0, 0, 0, 0.1);
  background-color: white;
  border-radius: 1vw;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: auto;
}

.title {
  font-size: 3vw;
  text-align: center;
  margin-bottom: 0.5vw;
  color: #303f9f;
}

.instructions {
  text-align: center;
  font-size: 2vw;
  color: #303f9f;
  margin-bottom: 0vw;
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
  margin-bottom: .8vw;
}

.label-cell, .input-cell {
  flex: 1;
}

.label-cell {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0;
  margin: 0;
}

.input-cell {
  display: flex;
  justify-content: center;
  align-items: center;
}

.label {
  background-color: #303f9f;
  color: white;
  border-radius: 1vw;
  padding: 1vw;
  text-align: center;
  width: 100%;
  font-size: 2vw;
}

.input-field {
  width: 98%;
  padding: 1vw;
  border: 0.25vw solid #ccc;
  border-radius: 1vw;
  font-size: 2vw;
}

.input-field.disabled {
  background-color: #e0e0e0;
  cursor: not-allowed;
}

.slider-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 98%;
}

.slider {
  width: 97%;
  margin-top: 0vw;
  margin-bottom: 1vw;
  -webkit-appearance: none;
  appearance: none;
  height: 1vw;
  border-radius: 1vw;
  background: #81d4fa;
  outline: none;
  opacity: 0.7;
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 3vw;
  height: 3vw;
  border-radius: 50%;
  background: #0288d1;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 3vw;
  height: 3vw;
  border-radius: 50%;
  background: #0288d1;
  cursor: pointer;
}

.submit-button {
  background-color: #0288d1;
  color: white;
  border: none;
  border-radius: 1vw;
  padding: 1vw 2vw;
  cursor: pointer;
  width: 100%;
  text-align: center;
  font-size: 2vw;
}

.full-width-button {
  width: 98%;
}

.error-message {
  color: red;
  margin-top: 1vw;
  font-size: 2vw;
}

.centered-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.editable-output {
  width: 100%;
  height: 20vh;
  margin-top: 2vw;
  padding: 1vw;
  border: 0.25vw solid #ccc;
  border-radius: 1vw;
  font-size: 2vw;
}

.button-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 1.5vw;
}

.download-button {
  background-color: #0288d1; /* farbe herunterladen button */
  color: white;
  border: none; 
  border-radius: 1vw; 
  padding: 0vw 0vw;
  cursor: pointer; 
  flex: 1; 
  margin: 0 0.5vw; 
  font-size: 2vw;
}

.copy-button {
  background-color: #0288d1; /* farbe zwischenspeicher button */
  color: white;
  border: none; 
  border-radius: 1vw; 
  padding: 0vw 0vw;
  cursor: pointer; 
  flex: 1; 
  margin: 0 0.5vw; 
  font-size: 2vw;
}

.vocab-list {
  margin-top: 2vw;
  width: 100%;
  padding: 0vw;
  border: 0.25vw solid #ccc;
  border-radius: 1vw;
  background-color: #f9f9f9;
}

.vocab-list table {
  width: 100%;
  border-collapse: collapse;
}

.vocab-list td {
  border: 1px solid #000;
  padding: 0.5vw;
  font-size: 1.5vw;
}

.vocab-list input {
  width: 100%;
  padding: 0.5vw;
  font-size: 1.5vw;
}

.vocab-title {
  color: #000000;
  font-size: 2.5vw;
  margin-bottom: 1vw;
}

.add-synonym-button {
  background-color: #0288d1;
  color: white;
  border: none;
  border-radius: 5vw;
  padding: 0.5vw 1vw;
  cursor: pointer;
  font-size: 2vw;
  margin-top: 0vw;
}

.text-type-buttons {
  display: flex; 
  justify-content: space-between; 
  width: 100%;
}

.text-type-buttons button {
  background-color: #81d4fa; /* farbe erklärtext button */
  border: none; 
  border-radius: 1vw; 
  padding: 1vw; 
  cursor: pointer; 
  flex: 1; 
  margin: 0 0.5vw; 
  font-size: 2vw;
}

.text-type-buttons button.selected {
  background-color: #303f9f; /* farbe ausgewählter geschichte button */
  color: white;
}

@media (max-width: 800px) {
  .container {
    padding: 5vw;
  }

  .title {
    font-size: 3vw;
    margin-bottom: 2vw;
  }

  .label {
    font-size: 2.5vw;
  }

  .text-type-buttons button {
    font-size: 3vw;
    padding: 1.5vw;
  }

  .submit-button,
  .add-synonym-button {
    font-size: 3vw;
    padding: 1.5vw 1.5vw;
  }

  .editable-output {
    font-size: 3vw;
    padding: 1.5vw;
  }

  .vocab-list td {
    font-size: 3vw;
    padding: 1vw;
  }

  .vocab-list input {
    font-size: 3vw;
    padding: 1vw;
  }
}
</style>
