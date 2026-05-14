### Intégration dans une Interface Web

Pour rendre cette solution accessible via une interface web, vous pouvez utiliser Flask :

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
openai.api_key = 'YOUR_API_KEY'

def analyze_legal_situation(situation):
    prompt = f"Analyze the following legal situation and extract the key requirements for a real estate solution:\n{situation}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def define_search_criteria(legal_requirements):
    criteria = {
        'location': 'France',
        'property_type': 'residential',
        'tax_friendly': True,
        'residency_requirements': 'minimal'
    }
    return criteria

def search_real_estate(criteria):
    search_url = f"https://example-real-estate-site.com/search?location={criteria['location']}&type={criteria['property_type']}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    listings = []
    for listing in soup.find_all('div', class_='listing'):
        data = {
            'title': listing.find('h2').text,
            'price': listing.find('span', class_='price').text,
            'location': listing.find('span', class_='location').text,
            'link': listing.find('a')['href']
        }
        listings.append(data)
    return pd.DataFrame(listings)

def evaluate_properties(properties, criteria):
    evaluated_properties = []
    for _, property in properties.iterrows():
        if criteria['tax_friendly']:
            property['evaluation'] = 'tax friendly'
        else:
            property['evaluation'] = 'standard'
        evaluated_properties.append(property)
    return pd.DataFrame(evaluated_properties)

@app.route('/search_property', methods=['POST'])
def search_property():
    situation = request.json.get('situation')
    requirements = analyze_legal_situation(situation)
    criteria = define_search_criteria(requirements)
    properties = search_real_estate(criteria)
    evaluated_properties = evaluate_properties(properties, criteria)
    return evaluated_properties.to_json()

if __name__ == '__main__':
    app.run(debug=True)
```