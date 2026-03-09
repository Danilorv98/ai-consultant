import json
import os
from datetime import datetime
from src.document_processor import DocumentProcessor
from src.ai_analyzer import AIAnalyzer


class DocumentProcessingPipeline:
    """Pipeline completa per processare e analizzare documenti."""
    
    def __init__(self, ai_provider: str = "openai"):
        self.processor = None
        self.analyzer = AIAnalyzer(provider=ai_provider)
        self.results = {}
    
    def process_document(self, document_path: str, output_path: str = "output/") -> dict:
        """Processa un documento completo."""
        print(f"📄 Elaborazione documento: {document_path}")
        
        # Carica il documento
        self.processor = DocumentProcessor(document_path)
        content = self.processor.load_document()
        print(f"✓ Documento caricato ({len(content)} caratteri)")
        
        # Estrai metadati
        metadata = self.processor.extract_metadata()
        print(f"✓ Metadati estratti")
        
        # Analisi AI
        print("🤖 Avvio analisi AI...")
        
        # Estrazione informazioni
        extraction = self.analyzer.extract_info(content)
        print("✓ Informazioni estratte")
        
        # Riassunto
        summary = self.analyzer.summarize(content, "medium")
        print("✓ Riassunto generato")
        
        # Analisi sentiment
        sentiment = self.analyzer.analyze_sentiment(content)
        print("✓ Sentiment analizzato")
        
        # Compila risultati
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata,
            "extraction": extraction,
            "summary": summary,
            "sentiment": sentiment,
            "ai_provider": self.analyzer.provider
        }
        
        # Salva risultati
        output_file = self._save_results(output_path)
        print(f"✓ Risultati salvati in: {output_file}")
        
        return self.results
    
    def process_with_custom_questions(self, document_path: str, questions: list, output_path: str = "output/") -> dict:
        """Processa un documento con domande personalizzate."""
        print(f"📄 Elaborazione documento: {document_path}")
        
        # Carica il documento
        self.processor = DocumentProcessor(document_path)
        content = self.processor.load_document()
        print(f"✓ Documento caricato ({len(content)} caratteri)")
        
        # Estrai metadati
        metadata = self.processor.extract_metadata()
        
        # Rispondi alle domande personalizzate
        print("🤖 Risposta alle domande...")
        answers = self.analyzer.answer_questions(content, questions)
        print("✓ Domande risposte")
        
        # Riassunto generale
        summary = self.analyzer.summarize(content, "medium")
        
        # Compila risultati
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata,
            "questions": questions,
            "answers": answers,
            "summary": summary,
            "ai_provider": self.analyzer.provider
        }
        
        # Salva risultati
        output_file = self._save_results(output_path)
        print(f"✓ Risultati salvati in: {output_file}")
        
        return self.results
    
    def _save_results(self, output_path: str) -> str:
        """Salva i risultati in un file JSON."""
        os.makedirs(output_path, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.json"
        filepath = os.path.join(output_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def display_results(self):
        """Visualizza i risultati nel terminale."""
        if not self.results:
            print("❌ Nessun risultato disponibile. Processa un documento prima.")
            return
        
        print("\n" + "="*60)
        print("📊 RISULTATI ANALISI")
        print("="*60)
        
        print(f"\n📝 Metadati:")
        for key, value in self.results.get("metadata", {}).items():
            print(f"  {key}: {value}")
        
        if "extraction" in self.results:
            print(f"\n📌 Informazioni Estratte:")
            print(f"  {self.results['extraction'][:500]}...")
        
        if "summary" in self.results:
            print(f"\n📋 Riassunto:")
            print(f"  {self.results['summary']}")
        
        if "sentiment" in self.results:
            print(f"\n😊 Sentiment:")
            sentiment_data = self.results['sentiment']
            if isinstance(sentiment_data, dict) and "sentiment" in sentiment_data:
                print(f"  Sentiment: {sentiment_data.get('sentiment')}")
                print(f"  Confidence: {sentiment_data.get('confidence')}%")
        
        if "answers" in self.results:
            print(f"\n❓ Risposte alle Domande:")
            for q, a in self.results['answers'].items():
                print(f"  {q}: {a}")
        
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # Esempio di utilizzo
    print("🚀 Document Processor AI - Demo\n")
    
    # Crea un documento di esempio
    sample_doc = "documents/sample.txt"
    if not os.path.exists(sample_doc):
        os.makedirs("documents", exist_ok=True)
        with open(sample_doc, 'w', encoding='utf-8') as f:
            f.write("""Intelligenza Artificiale: Il Futuro della Tecnologia

L'intelligenza artificiale sta rivoluzionando il modo in cui lavoriamo e viviamo.
Le aziende utilizzano AI per migliorare l'efficienza, ridurre i costi e offrire migliori servizi ai clienti.
Tuttavia, è importante affrontare le sfide etiche e di sicurezza che l'IA presenta.
Il futuro della tecnologia sarà modellato da come affrontiamo questi problemi.
""")
    
    # Processa il documento
    pipeline = DocumentProcessingPipeline(ai_provider="openai")
    results = pipeline.process_document(sample_doc)
    
    # Visualizza risultati
    pipeline.display_results()
