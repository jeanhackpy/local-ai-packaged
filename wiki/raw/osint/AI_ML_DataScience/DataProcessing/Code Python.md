### Code Python

```python
import cv2
import pytesseract
import sqlite3

# Configuration de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Chemin vers l'exécutable Tesseract

# Fonction pour extraire le texte de l'image
def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    return text

# Fonction pour parser le texte et extraire les informations
def parse_book_info(text):
    # Cette fonction devra être améliorée pour mieux extraire les titres, auteurs, etc.
    lines = text.split('\n')
    books = []
    for line in lines:
        if line.strip():
            parts = line.split(',')
            if len(parts) >= 3:
                title = parts[0].strip()
                author = parts[1].strip()
                year = parts[2].strip()
                description = ','.join(parts[3:]).strip() if len(parts) > 3 else ''
                books.append((title, author, year, description))
    return books

# Fonction pour créer la base de données et insérer les données
def create_database():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books
                      (title TEXT, author TEXT, year TEXT, description TEXT)''')
    conn.commit()
    conn.close()

def insert_books_into_database(books):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO books (title, author, year, description) VALUES (?, ?, ?, ?)', books)
    conn.commit()
    conn.close()

# Fonction principale pour traiter une image
def process_image(image_path):
    text = extract_text_from_image(image_path)
    books = parse_book_info(text)
    create_database()
    insert_books_into_database(books)

# Exemple d'utilisation
image_path = 'path_to_your_image.jpg'
process_image(image_path)
```