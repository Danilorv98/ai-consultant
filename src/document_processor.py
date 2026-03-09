import os
import json
from typing import Optional


class DocumentProcessor:
    """Processa e estrae testo da diversi formati di documenti."""
    
    def __init__(self, document_path: str):
        self.document_path = document_path
        self.content = None
        self.file_type = self._detect_file_type()
    
    def _detect_file_type(self) -> str:
        """Rileva il tipo di file dal percorso."""
        _, ext = os.path.splitext(self.document_path)
        return ext.lower()
    
    def load_document(self) -> str:
        """Carica il contenuto del documento."""
        if not os.path.exists(self.document_path):
            raise FileNotFoundError(f"Documento non trovato: {self.document_path}")
        
        if self.file_type == '.txt':
            self.content = self._load_txt()
        elif self.file_type == '.pdf':
            self.content = self._load_pdf()
        else:
            raise ValueError(f"Tipo di file non supportato: {self.file_type}")
        
        return self.content
    
    def _load_txt(self) -> str:
        """Carica un file di testo."""
        with open(self.document_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_pdf(self) -> str:
        """Carica un file PDF (richiede PyPDF2)."""
        try:
            import PyPDF2
        except ImportError:
            raise ImportError("PyPDF2 non installato. Usa: pip install PyPDF2")
        
        text = ""
        with open(self.document_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def get_content(self) -> Optional[str]:
        """Ritorna il contenuto caricato."""
        if self.content is None:
            self.load_document()
        return self.content
    
    def split_into_chunks(self, chunk_size: int = 1000) -> list:
        """Divide il documento in chunks per l'elaborazione."""
        content = self.get_content()
        chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
        return chunks
    
    def extract_metadata(self) -> dict:
        """Estrae metadati del documento."""
        return {
            "file_name": os.path.basename(self.document_path),
            "file_type": self.file_type,
            "file_size": os.path.getsize(self.document_path),
            "content_length": len(self.get_content()) if self.content else 0
        }
