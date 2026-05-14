### Extraction de Texte à partir de Fichiers EPUB et PDF

#### Extraction de Texte à partir de Fichiers PDF

Pour les fichiers PDF, vous pouvez utiliser des bibliothèques comme `PyPDF2`, `pdfminer.six` ou `PyMuPDF`.

**Exemple avec PyMuPDF** :
```python
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

pdf_text = extract_text_from_pdf("sample.pdf")
print(pdf_text)
```

#### Extraction de Texte à partir de Fichiers EPUB

Pour les fichiers EPUB, vous pouvez utiliser des bibliothèques comme `ebooklib` et `BeautifulSoup`.

**Exemple avec EbookLib et BeautifulSoup** :
```python
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    text = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text += soup.get_text()
    return text

epub_text = extract_text_from_epub("sample.epub")
print(epub_text)
```