from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)

class PdfService:
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Extracts text from a given PDF file."""
        text = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            raise
        return text
