### Revised Radar Chart Code

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Données des comptes classifiées (sans FBS_broker et HeroWarsWeb)
data = {
    'Compte': [
        "bencryptomike", "getbased_ai", "CryptoKrum", "Kingnmjhy5",
        "paragon0", "VikulyadrRu", "smileofus", "misun1786"
    ],
    'Crypto/AI': [1, 1, 1, 0, 0, 0, 0, 0],
    'Promotion': [0, 0, 0, 0, 0, 1, 1, 1],
    'Diversité': [0, 0, 0, 1, 0, 0, 0, 0],
    'Automatisation': [1, 1, 1, 0, 0, 0, 0, 0],
    'Spam': [0, 0, 0, 1, 0, 0, 1, 1],
    'Engagement': [0, 0, 0, 1, 0, 0, 1, 1]
}

# Conversion en DataFrame
df = pd.DataFrame(data)

# Configuration du graphique
labels = df.columns[1:]
num_vars = len(labels)

# Angles pour le radar chart
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# Complète le cercle
angles += angles[:1]

# Initialisation du plot
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

# Dessiner chaque ligne de données
for i in range(len(df)):
    values = df.iloc[i].drop('Compte').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, label=df.iloc[i]['Compte'])
    ax.fill(angles, values, alpha=0.25)

# Ajouter les labels
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

# Légende
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.show()
```