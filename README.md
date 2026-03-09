# 📄 Document Processor AI - Portfolio Project

Un'applicazione Python che estrae e analizza dati da documenti utilizzando intelligenza artificiale (OpenAI/Anthropic).

## 🎯 Caratteristiche

✅ **Caricamento Documenti**
- Supporta file .txt e .pdf
- Estrae automaticamente metadati

✅ **Estrazione Intelligente**
- Estrae tema principale, punti chiave, entità nominate
- Analizza tono del documento

✅ **Riassunto Automatico**
- Genera riassunti di diverse lunghezze (short/medium/long)
- Mantiene i concetti chiave

✅ **Analisi Sentiment**
- Classifica il sentimento (positivo/negativo/neutrale)
- Fornisce confidence score e reasoning

✅ **Q&A Personalizzate**
- Rispondi a domande specifiche sul documento
- Supporta domande multiple

✅ **Multi-Provider**
- Integrazione con OpenAI (GPT-4)
- Integrazione con Anthropic (Claude)

## 📋 Struttura Progetto

```
ai-consultant/
├── src/
│   ├── document_processor.py    # Caricamento e processing documenti
│   └── ai_analyzer.py           # Analisi AI
├── documents/                   # Cartella per i documenti da analizzare
├── output/                      # Risultati in JSON
├── main.py                      # Pipeline principale
├── requirements.txt             # Dipendenze Python
├── .env.example                 # Template variabili d'ambiente
└── README.md                    # Questo file
```

## 🚀 Quick Start

### 1. Setup Ambiente

```bash
# Attiva virtual environment
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
```

### 2. Configura API Keys

```bash
# Copia il template
cp .env.example .env

# Modifica .env con le tue chiavi
nano .env
```

Aggiungi le tue API keys:
```
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
AI_PROVIDER=anthropic  # openai o anthropic
```

### 3. Testa il Progetto

**Analisi Base:**
```bash
python main.py
```

**Output Esempio:**
```
🚀 Document Processor AI - Demo

📄 Elaborazione documento: documents/sample.txt
✓ Documento caricato (1187 caratteri)
✓ Metadati estratti
🤖 Avvio analisi AI...
✓ Informazioni estratte
✓ Riassunto generato
✓ Sentiment analizzato
✓ Risultati salvati in: output/analysis_20260309_150302.json

📊 RISULTATI ANALISI
📝 Metadati: sample.txt (.txt, 1193 bytes, 1187 caratteri)
📌 Informazioni Estratte: Tema IA, punti chiave, entità nominate
📋 Riassunto: L'AI sta rivoluzionando lavoro e vita...
😊 Sentiment: positivo (85% confidence)
```

## 📊 Output

I risultati vengono salvati in `output/` in formato JSON:

```json
{
  "timestamp": "2024-03-09T10:30:00",
  "metadata": {
    "file_name": "document.txt",
    "file_type": ".txt",
    "file_size": 1024,
    "content_length": 5000
  },
  "extraction": "...",
  "summary": "...",
  "sentiment": {
    "sentiment": "positivo",
    "confidence": 85,
    "reasoning": "..."
  },
  "ai_provider": "openai"
}
```

## 🔧 Configurazione Avanzata

### Supporto PDF

I file PDF vengono elaborati automaticamente con PyPDF2:

```python
pipeline.process_document("documents/report.pdf")
```

### Chunking Documenti

Per documenti molto lunghi, il sistema divide automaticamente il contenuto:

```python
chunks = processor.split_into_chunks(chunk_size=2000)
```

### Cambio Provider AI

```python
# Usa Anthropic invece di OpenAI
pipeline = DocumentProcessingPipeline(ai_provider="anthropic")
```

## 📚 API Reference

### DocumentProcessor

```python
processor = DocumentProcessor("path/to/document.txt")

# Carica documento
content = processor.load_document()

# Estrai metadati
metadata = processor.extract_metadata()

# Dividi in chunks
chunks = processor.split_into_chunks(chunk_size=1000)
```

### AIAnalyzer

```python
analyzer = AIAnalyzer(provider="openai")

# Estrai informazioni
info = analyzer.extract_info(text)

# Riassumi
summary = analyzer.summarize(text, summary_length="medium")

# Analizza sentiment
sentiment = analyzer.analyze_sentiment(text)

# Rispondi a domande
answers = analyzer.answer_questions(text, questions)
```

## 🌟 Casi d'Uso

1. **Analisi Report e Documenti Business**
2. **Estrazione Automatica di Informazioni**
3. **Classificazione e Categorizzazione**
4. **Q&A su Documenti**
5. **Sintesi di Letteratura Accademica**
6. **Content Analysis**

## ⚠️ Note Importanti

- Richiede API keys valide da OpenAI o Anthropic
- Attenzione ai costi API in case di elaborazione massiccia
- I documenti lunghi vengono elaborati per chunks
- Rate limiting dipende dal provider AI

## 📝 Miglioramenti Futuri

- [ ] Support per più formati (DOCX, XLSX)
- [ ] Cache risultati per documenti identici
- [ ] Batch processing
- [ ] API REST endpoint
- [ ] Web Interface
- [ ] Database per archiviare risultati

## 🤝 Contributi

Segnala bug e suggerimenti tramite GitHub Issues!

## 📄 Licenza

MIT License - Vedi LICENSE per dettagli

## 👨‍💼 Author

**Danilo Roscini**  
AI Consultant - Portfolio Project  
[GitHub](https://github.com/Danilorv98/ai-consultant)

---

**Versione:** 1.0.0  
**Ultimo Aggiornamento:** Marzo 2026
