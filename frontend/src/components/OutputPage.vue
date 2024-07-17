<template>
  <div class="outer-container" @click="hideSynonyms">
    <div class="container">
      <h1 class="title">KLUG - Kinder-Lerntext und Unterrichtstext Generator</h1>
      <div class="instructions">
          
      </div>
      <div class="output-container" v-if="!loading">
        <div class="output-text" @click.stop="showSynonym($event)">
          <h2 class="result-title">{{ textType === 'Geschichte' ? 'Deine Geschichte über ' : 'Dein Erklärtext über ' }} "{{ prompt }}":</h2>
          <div v-html="highlightedText"></div>
        </div>
        <div class="synonym-box" v-if="synonyms" :style="{ top: synonymBoxPosition.top, left: synonymBoxPosition.left }">
          <p class="synonym-word">{{ currentWord }}:</p>
          <p class="synonym-item">{{ synonyms.join(', ') }}</p>
        </div>
        <div class="button-container">
          <button @click="retry" class="retry-button">Erneut versuchen</button>
          <button @click="downloadText" class="download-button">Text herunterladen</button>
        </div>
        <div class="synonym-list" v-if="synonymList.length">
          <h3 class="synonym-title">Wörter mit der selben Bedeutung ("Synonyme"):</h3>
          <table class="synonym-table">
            <tbody>
              <tr v-for="(synonymEntry, index) in synonymList" :key="index">
                <td class="synonym-word">{{ synonymEntry.word }}: </td>
                <td class="synonym-item">{{ synonymEntry.synonyms.join(', ') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="loading-container" v-else>
        <h2>Hier entsteht dein Text...</h2>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['generatedText', 'loading', 'initialPrompt', 'initialLength', 'initialTextType'],
  data() {
    return {
      synonyms: null,
      currentWord: '',
      synonymBoxPosition: { top: '0px', left: '0px' },
      synonymList: [],
      prompt: this.initialPrompt,
      textType: this.initialTextType
    };
  },
  computed: {
    highlightedText() {
      return this.generatedText.split(' ').map(word => `<span class="highlight-word">${word}</span>`).join(' ');
    }
  },
  methods: {
    retry() {
      this.$emit('retry', { 
        prompt: this.initialPrompt, 
        length: this.initialLength, 
        textType: this.initialTextType 
      });
    },
    downloadText() {
      const blob = new Blob([this.generatedText], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'text.txt';
      a.click();
      URL.revokeObjectURL(url);
    },
    showSynonym(event) {
      if (event.target.classList.contains('highlight-word')) {
        const word = event.target.innerText;
        fetch(`http://127.0.0.1:5000/get_synonyms?word=${word}`)
          .then(response => response.json())
          .then(data => {
            this.synonyms = data.synonyms;
            this.currentWord = word;
            this.synonymBoxPosition = { top: `${event.clientY + 10}px`, left: `${event.clientX + 10}px` };
            this.synonymList.push({ word: this.currentWord, synonyms: this.synonyms });
            this.synonyms = null;
            this.currentWord = '';
          });
      }
    },
    hideSynonyms() {
      this.synonyms = null;
      this.currentWord = '';
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
  width: 95vw;
  height: auto;
  aspect-ratio: 2 / 1;
  padding: 2.5vw;
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
  width: 90vw;
  height: 80vh;
  padding: 1vw;
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
  margin-bottom: 1vw;
  color: #303f9f;
}

.result-title {
  font-size: 2.5vw;
  text-align: center;
  color: white; /* Weißer Text für den blauen Container */
  margin-bottom: 1vw;
}

.instructions {
  text-align: center;
  font-size: 2vw;
  color: #303f9f;
  margin-bottom: 0vw;
}

.output-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.loading-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 2vw;
  border: 0.25vw solid #ccc;
  border-radius: 1vw;
  color: #000000;
  background-color: #f9f9f9;
}

.output-text {
  margin: 0.5vw 0;
  background-color: #81d4fa;
  padding: 0.5vw;
  color: #000000;
  border-radius: 1vw;
  width: 100%;
  text-align: center;
  font-size: 2vw;
  position: relative;
}

.output-text h2 {
  margin-top: 0;
  margin-bottom: 0.0vw;
}

.button-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 0.0vw;
  margin-bottom: 0.5vw;
}

.retry-button, .download-button {
  color: #ffffff;
  background-color: #0288d1;
  border: none;
  border-radius: 1vw;
  padding: 1vw 2vw;
  cursor: pointer;
  font-size: 2vw;
}

.retry-button.selected, .download-button.selected {
  background-color: #b3e5fc;
}

.synonym-box {
  position: absolute;
  background-color: #ffffff;
  color: #000000;
  border: 1px solid #000000;
  padding: 1vw;
  border-radius: 1vw;
  box-shadow: 0 0 1vw rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.synonym-list {
  margin-top: 0vw;
  width: 100%;
  max-height: 60vh;
  overflow-y: auto;
}

.synonym-list table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #000000;
}

.synonym-list td {
  border: 1px solid #000000;
  padding: 0.5vw;
  font-size: 1.5vw;
}

.synonym-word {
  color: #000000;
}

.synonym-item {
  background-color: #ffffff;
  color: #000000;
  border-radius: 0.5vw;
  padding: 0.5vw;
}

.synonym-title {
  color: #000000;
  font-size: 2vw;
}

@media (max-width: 800px) {
  .container {
    padding: 5vw;
  }

  .title {
    font-size: 3vw;
    margin-bottom: 1vw;
  }

  .result-title {
    font-size: 2.5vw;
    margin-bottom: 0.5vw;
  }

  .instructions {
    font-size: 2.5vw;
    margin-bottom: 2vw;
  }

  .output-container, .loading-container {
    padding: 2vw;
  }

  .output-text {
    font-size: 3vw;
    padding: 2.5vw;
    margin: 2vw 0;
  }

  .retry-button, .download-button {
    font-size: 3vw;
    padding: 1.5vw 2.5vw;
  }

  .synonym-list td {
    font-size: 3vw;
    padding: 1vw;
  }

  .translated-text {
    font-size: 3vw;
    padding: 2.5vw;
    margin-top: 1vw;
  }
}
</style>
