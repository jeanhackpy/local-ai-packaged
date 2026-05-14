### Example Script

Here's a basic example of a script that scrapes property listings from `fazwaz.fr`.

```python
import requests
from bs4 import BeautifulSoup

# Define the URL of the site
url = 'https://www.fazwaz.fr/'

# Make a GET request to fetch the raw HTML content
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the container with the property listings
# Note: Adjust the selector to match the structure of the website
properties = soup.find_all('div', class_='property-listing')

# Loop through each property and extract details
for property in properties:
    title = property.find('h2', class_='title').text.strip()
    price = property.find('span', class_='price').text.strip()
    location = property.find('span', class_='location').text.strip()
    
    # Print or store the extracted information
    print(f'Title: {title}')
    print(f'Price: {price}')
    print(f'Location: {location}')
    print('-' * 20)

# Further processing, such as saving to a database or file, can be done here
```