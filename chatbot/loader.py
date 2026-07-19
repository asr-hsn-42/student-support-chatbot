from pathlib import Path
from pypdf import PdfReader 

DATA_FOLDER = "data"


def load_documents():
    documents = []

    pdf_files = Path(DATA_FOLDER).glob("*.pdf")

    for pdf in pdf_files:

        reader = PdfReader(pdf)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        documents.append({
            "source": pdf.name,
            "text": text
        })

    return documents