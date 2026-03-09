import os
import json
from typing import Optional, Literal
from openai import OpenAI
from anthropic import Anthropic


class AIAnalyzer:
    """Analizza documenti usando AI (OpenAI o Anthropic)."""
    
    def __init__(self, provider: Literal["openai", "anthropic"] = "openai"):
        self.provider = provider
        self._init_client()
    
    def _init_client(self):
        """Inizializza il client AI."""
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY non configurata in .env")
            self.client = OpenAI(api_key=api_key)
        elif self.provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY non configurata in .env")
            self.client = Anthropic(api_key=api_key)
    
    def extract_info(self, text: str, extraction_prompt: Optional[str] = None) -> str:
        """Estrae informazioni dal testo usando AI."""
        if extraction_prompt is None:
            extraction_prompt = """Estrai le seguenti informazioni dal testo:
1. Tema principale
2. Punti chiave (max 5)
3. Entità nominate (persone, organizzazioni, luoghi)
4. Tono del documento
Rispondi in JSON."""
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sei un esperto analista di documenti."},
                    {"role": "user", "content": f"{extraction_prompt}\n\nTesto:\n{text}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        
        elif self.provider == "anthropic":
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": f"{extraction_prompt}\n\nTesto:\n{text}"}
                ]
            )
            return message.content[0].text
    
    def summarize(self, text: str, summary_length: str = "medium") -> str:
        """Riassumi il documento."""
        length_map = {
            "short": "circa 50 parole",
            "medium": "circa 150 parole",
            "long": "circa 300 parole"
        }
        
        prompt = f"Riassumi il seguente testo in {length_map.get(summary_length, '150 parole')}:\n\n{text}"
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sei un esperto di sintesi di testi."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        
        elif self.provider == "anthropic":
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
    
    def analyze_sentiment(self, text: str) -> dict:
        """Analizza il sentiment del documento."""
        prompt = f"""Analizza il sentiment del seguente testo e rispondi in JSON:
{{
    "sentiment": "positivo/negativo/neutrale",
    "confidence": 0-100,
    "reasoning": "spiegazione"
}}

Testo: {text}"""
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sei un esperto di analisi del sentiment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            result = response.choices[0].message.content
        
        elif self.provider == "anthropic":
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result = message.content[0].text
        
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": "Errore nella risposta AI", "raw_response": result}
    
    def answer_questions(self, text: str, questions: list) -> dict:
        """Risponde a domande specifiche sul documento."""
        questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
        prompt = f"""Basandoti sul seguente testo, rispondi alle seguenti domande:

{questions_text}

Testo:
{text}

Rispondi in JSON con il formato: {{"question_1": "risposta", "question_2": "risposta"}}"""
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sei un esperto nell'estrazione di informazioni."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            result = response.choices[0].message.content
        
        elif self.provider == "anthropic":
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result = message.content[0].text
        
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": "Errore nella risposta AI", "raw_response": result}
