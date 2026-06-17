#!/usr/bin/env python3
"""
Entity Resolution & Data Normalization avec PydanticAI
=======================================================

Pipeline hybride:
1. Règles Python pour cas simples (rapide, 0 coût)
2. PydanticAI pour cas ambigus (LLM, robuste)

Auteur: Léon 🏝️
"""

import json
import hashlib
import re
from decimal import Decimal
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from dataclasses import dataclass

# Import PydanticAI (avec fallback si non installé)
try:
    from pydantic_ai import Agent, RunContext
    PYDANTIC_AI_AVAILABLE = True
except ImportError:
    PYDANTIC_AI_AVAILABLE = False
    print("⚠️ PydanticAI non installé. Mode règles uniquement.")


# ============================================================================
# SCHÉMAS PYDANTIC - Validation stricte
# ============================================================================

class ThaiAddress(BaseModel):
    """Adresse thaïlandaise normalisée avec validation"""
    raw: str = Field(description="Adresse brute originale")
    normalized: str = Field(default="", description="Adresse normalisée")
    province: str = Field(default="Bangkok", description="Province")
    district: Optional[str] = Field(default=None, description="District/Amphoe")
    zone: Optional[str] = Field(default=None, description="Zone (Sukhumvit, Sathorn, etc.)")
    microzone: Optional[str] = Field(default=None, description="Micro-zone (Soi, etc.)")
    postal_code: Optional[str] = Field(default=None, pattern=r"^\d{5}$")

    @field_validator('province', mode='before')
    @classmethod
    def normalize_province(cls, v):
        """Normalise les noms de provinces"""
        if not v:
            return "Bangkok"
        aliases = {
            'bkk': 'Bangkok',
            'กรุงเทพ': 'Bangkok',
            'กรุงเทพมหานคร': 'Bangkok',
            'phuket': 'Phuket',
            'ภูเก็ต': 'Phuket',
            'samui': 'Surat Thani',
            'koh samui': 'Surat Thani',
        }
        return aliases.get(v.lower(), v)


class PropertySpecs(BaseModel):
    """Caractéristiques immobilières avec validation"""
    property_type: str = Field(default="condo", description="Type: condo, villa, townhouse, land")
    bedrooms: Optional[Decimal] = Field(default=None, ge=0, le=20)
    bathrooms: Optional[Decimal] = Field(default=None, ge=0, le=20)
    floor_area_sqm: Optional[Decimal] = Field(default=None, gt=0, description="Surface habitable m²")
    land_area_sqm: Optional[Decimal] = Field(default=None, gt=0, description="Surface terrain m²")
    floor_number: Optional[int] = Field(default=None, ge=0, le=200)
    orientation: Optional[str] = Field(default=None)
    view_types: List[str] = Field(default_factory=list)

    @field_validator('property_type', mode='before')
    @classmethod
    def normalize_type(cls, v):
        """Normalise le type de bien"""
        if not v:
            return "condo"
        aliases = {
            'condominium': 'condo',
            'apartment': 'condo',
            'house': 'villa',
            'home': 'villa',
            'townhome': 'townhouse',
        }
        return aliases.get(v.lower(), v.lower())

    @model_validator(mode='after')
    def compute_land_area(self):
        """Si land_area non spécifié et villa, utiliser floor_area"""
        if self.property_type == 'land' and not self.floor_area_sqm:
            raise ValueError("Land property requires land_area_sqm")
        return self


class Price(BaseModel):
    """Prix avec validation et conversion automatique"""
    thb: Decimal = Field(gt=0, description="Prix en THB")
    original: Decimal = Field(gt=0, description="Prix original")
    currency: str = Field(default="THB")
    per_sqm: Optional[Decimal] = Field(default=None, description="Prix au m²")

    @model_validator(mode='after')
    def compute_per_sqm(self):
        """Calcule prix/m² si surface disponible"""
        # Sera calculé plus tard avec la surface
        return self


class Project(BaseModel):
    """Projet immobilier avec matching intelligent"""
    name: str = Field(min_length=2, max_length=200)
    name_normalized: str = Field(default="")
    developer: Optional[str] = Field(default=None)
    standing: Optional[str] = Field(default=None, pattern="^(budget|mid_range|premium|luxury)$")

    @field_validator('name_normalized', mode='before')
    @classmethod
    def normalize_name(cls, v, info):
        """Normalise le nom pour matching"""
        name = info.data.get('name', v or '')
        if not name:
            return ""
        # Lowercase, remove punctuation, normalize spaces
        normalized = re.sub(r'[^\w\s]', ' ', name.lower())
        return re.sub(r'\s+', ' ', normalized).strip()


class CanonicalProperty(BaseModel):
    """Propriété canonique pour déduplication"""
    project: Project
    specs: PropertySpecs
    canonical_hash: str = Field(default="")

    def compute_hash(self) -> str:
        """Génère hash pour matching"""
        components = [
            self.project.name_normalized,
            str(self.specs.bedrooms or ''),
            str(self.specs.floor_area_sqm or ''),
            str(self.specs.floor_number or ''),
        ]
        data = '|'.join(components).lower()
        return hashlib.md5(data.encode()).hexdigest()

    @model_validator(mode='after')
    def set_hash(self):
        self.canonical_hash = self.compute_hash()
        return self


class PropertyListing(BaseModel):
    """Listing complet normalisé avec validation"""
    # Identification
    source: str = Field(min_length=1)
    external_id: str = Field(min_length=1)
    external_url: str

    # Titre et description
    title: str = Field(min_length=5, max_length=500)
    description: Optional[str] = Field(default="")

    # Projet
    project: Project

    # Localisation
    address: ThaiAddress

    # Specs
    specs: PropertySpecs

    # Prix
    price: Price

    # Métadonnées
    images: List[str] = Field(default_factory=list)
    agent_name: Optional[str] = Field(default=None)
    agent_phone: Optional[str] = Field(default=None)
    agency: Optional[str] = Field(default=None)

    # Matching
    canonical_hash: str = Field(default="")
    match_confidence: Decimal = Field(default=Decimal("0"), ge=0, le=1)

    # Timestamps
    first_seen: datetime = Field(default_factory=datetime.utcnow)
    raw_data: Dict[str, Any] = Field(default_factory=dict, exclude=True)

    @model_validator(mode='after')
    def compute_hash_and_price(self):
        """Calcule hash et prix/m²"""
        # Hash
        canonical = CanonicalProperty(project=self.project, specs=self.specs)
        self.canonical_hash = canonical.canonical_hash

        # Prix/m²
        if self.specs.floor_area_sqm and self.price.thb:
            self.price.per_sqm = self.price.thb / self.specs.floor_area_sqm

        return self


# ============================================================================
# AGENT PYDANTIC AI - Pour cas complexes
# ============================================================================

# Prompt système pour l'agent
NORMALIZATION_INSTRUCTIONS = """
Tu es un expert en normalisation de données immobilières thaïlandaises.

Ta tâche: Convertir un texte d'annonce brut en données structurées valides.

Règles importantes:
1. **Projets**: Normalise les noms (lowercase, sans ponctuation)
   - "The Davis Bangkok" → "the davis bangkok"
   - "RHYTHM Charoenkrung Pavillion" → "rhythm charoenkrung pavillion"

2. **Prix**: Convertis tout en THB
   - 1 USD ≈ 35 THB
   - 1 EUR ≈ 38 THB
   - "THB 12,500,000" → 12500000

3. **Zones Bangkok**: Détecte et assigne
   - Sukhumvit 1-21 → zone: "Sukhumvit", district: "Khlong Toei Nuea"
   - Sukhumvit 22-63 → zone: "Sukhumvit", district: "Khlong Tan Nuea"
   - Sathorn/Silom → zone: "Sathorn/Silom", district: "Sathon/Bang Rak"

4. **Types de bien**:
   - Studio → 0 bedrooms, property_type: "condo"
   - Penthouse → property_type: "condo" (marquer dans description)
   - Villa → property_type: "villa"

5. **Champs manquants**:
   - Si pas de bedrooms spécifié → null (pas 0)
   - Si pas de surface → null

Retourne TOUJOURS un PropertyListing valide.
"""


def create_normalizer_agent():
    """Crée l'agent PydanticAI si disponible"""
    if not PYDANTIC_AI_AVAILABLE:
        return None

    agent = Agent(
        'ollama:llama3.3',
        output_type=PropertyListing,
        instructions=NORMALIZATION_INSTRUCTIONS,
    )

    return agent


# ============================================================================
# PIPELINE HYBRIDE
# ============================================================================

class HybridNormalizer:
    """
    Normaliseur hybride:
    - Règles rapides pour cas simples (90%)
    - PydanticAI pour cas ambigus (10%)
    """

    def __init__(self):
        self.agent = create_normalizer_agent()
        self._init_rules()

    def _init_rules(self):
        """Initialise les règles de normalisation"""
        # Mapping zones Bangkok
        self.zone_district_map = {
            'sukhumvit': {
                'default': 'Khlong Toei Nuea',
                'soi_range': {
                    (1, 21): 'Khlong Toei Nuea',
                    (22, 63): 'Khlong Tan Nuea',
                }
            },
            'sathorn': {'default': 'Sathon'},
            'silom': {'default': 'Bang Rak'},
            'riverside': {'default': 'Bang Rak'},
            'ratchada': {'default': 'Din Daeng'},
            'ladprao': {'default': 'Lat Phrao'},
            'ari': {'default': 'Phaya Thai'},
            'siam': {'default': 'Pathum Wan'},
        }

        # Conversion devises
        self.currency_rates = {
            'THB': Decimal('1'),
            'USD': Decimal('35'),
            'EUR': Decimal('38'),
            'GBP': Decimal('44'),
            'CNY': Decimal('5'),
            'JPY': Decimal('0.24'),
        }

    def normalize_address(self, raw: str) -> ThaiAddress:
        """Normalise une adresse avec règles"""
        if not raw:
            return ThaiAddress(raw="")

        addr_lower = raw.lower()

        # Détecter province
        province = "Bangkok"
        for alias, prov in [('phuket', 'Phuket'), ('samui', 'Surat Thani')]:
            if alias in addr_lower:
                province = prov
                break

        # Détecter zone et district
        zone = None
        district = None

        for zone_name, mapping in self.zone_district_map.items():
            if zone_name in addr_lower:
                zone = zone_name.capitalize()

                # Chercher soi number pour Bangkok
                soi_match = re.search(rf'{zone_name}\s*(?:soi)?\s*(\d+)', addr_lower)
                if soi_match and 'soi_range' in mapping:
                    soi_num = int(soi_match.group(1))
                    for (low, high), dist in mapping['soi_range'].items():
                        if low <= soi_num <= high:
                            district = dist
                            zone = f"{zone_name} {soi_num}"
                            break
                else:
                    district = mapping['default']
                break

        return ThaiAddress(
            raw=raw,
            normalized=re.sub(r'\s+', ' ', addr_lower).strip(),
            province=province,
            district=district,
            zone=zone,
        )

    def normalize_price(self, price_str: str, currency: str = 'THB') -> Optional[Price]:
        """Extrait et normalise un prix"""
        if not price_str:
            return None

        # Nettoyer
        clean = price_str.replace(',', '').replace(' ', '')

        # Extraire nombre
        numbers = re.findall(r'\d+(?:\.\d+)?', clean)
        if not numbers:
            return None

        value = Decimal(numbers[0])

        # Convertir en THB
        rate = self.currency_rates.get(currency.upper(), Decimal('1'))
        thb = value * rate

        return Price(thb=thb, original=value, currency=currency.upper())

    def normalize_specs(self, data: Dict[str, Any]) -> PropertySpecs:
        """Normalise les caractéristiques avec règles"""
        # Extraction par règles
        property_type = data.get('type', 'condo')

        # Bedrooms
        bedrooms = None
        bed_str = str(data.get('bedrooms', ''))
        if 'studio' in bed_str.lower():
            bedrooms = Decimal('0')
        else:
            bed_match = re.search(r'(\d+(?:\.\d+)?)', bed_str)
            if bed_match:
                bedrooms = Decimal(bed_match.group(1))

        # Surface
        area = None
        area_str = str(data.get('size', ''))
        area_match = re.search(r'(\d+(?:\.\d+)?)', area_str)
        if area_match:
            area = Decimal(area_match.group(1))

        return PropertySpecs(
            property_type=property_type,
            bedrooms=bedrooms,
            floor_area_sqm=area,
        )

    def is_ambiguous(self, raw_data: Dict[str, Any]) -> bool:
        """Détecte si les données sont ambigües et nécessitent LLM"""
        ambiguous_patterns = [
            # Prix sans devise claire
            lambda d: 'price' in d and not any(c in str(d['price']).upper() for c in ['THB', 'USD', 'EUR', '$', '฿']),
            # Titre sans projet clair
            lambda d: 'title' in d and ' at ' not in d.get('title', '').lower(),
            # Surface ambiguë
            lambda d: 'size' in d and not re.search(r'\d+\s*(?:sqm|m²|m2)', str(d['size']), re.I),
        ]

        return any(pattern(raw_data) for pattern in ambiguous_patterns)

    async def normalize(self, raw_data: Dict[str, Any], source: str) -> Optional[PropertyListing]:
        """
        Normalise un listing avec stratégie hybride:
        1. Essayer règles rapides
        2. Si ambigu, utiliser PydanticAI
        """
        try:
            # === ÉTAPE 1: Règles rapides ===

            # Titre et ID
            title = raw_data.get('title', '')
            external_id = raw_data.get('id') or raw_data.get('listing_id') or ''
            external_url = raw_data.get('url', '')

            if not title or not external_id:
                return None

            # Projet
            project_name = raw_data.get('project_name') or raw_data.get('building') or self._extract_project_from_title(title)

            project = Project(
                name=project_name,
                name_normalized="",  # Auto-computed
            )

            # Adresse
            address_raw = raw_data.get('address') or raw_data.get('location') or ''
            address = self.normalize_address(address_raw)

            # Specs
            specs = self.normalize_specs(raw_data)

            # Prix
            price_str = raw_data.get('price', '')
            currency = self._detect_currency(price_str)
            price = self.normalize_price(price_str, currency)

            if not price:
                # Essayer extraction avancée si prix non détecté
                if self.agent and self.is_ambiguous(raw_data):
                    return await self._normalize_with_llm(raw_data, source)
                return None

            # Créer le listing
            listing = PropertyListing(
                source=source,
                external_id=str(external_id),
                external_url=external_url,
                title=title,
                description=raw_data.get('description', ''),
                project=project,
                address=address,
                specs=specs,
                price=price,
                images=raw_data.get('images', []),
                agent_name=raw_data.get('agent_name'),
                agent_phone=raw_data.get('agent_phone'),
                agency=raw_data.get('agency'),
                raw_data=raw_data,
            )

            return listing

        except Exception as e:
            print(f"Erreur normalisation: {e}")

            # === ÉTAPE 2: Fallback LLM si ambigu ===
            if self.agent and self.is_ambiguous(raw_data):
                return await self._normalize_with_llm(raw_data, source)

            return None

    async def _normalize_with_llm(self, raw_data: Dict[str, Any], source: str) -> Optional[PropertyListing]:
        """Utilise PydanticAI pour les cas complexes"""
        if not self.agent:
            return None

        try:
            # Préparer le prompt
            prompt = f"""
            Normalise cette annonce immobilière:
            {json.dumps(raw_data, ensure_ascii=False, indent=2)}

            Source: {source}
            """

            # Appeler l'agent
            result = await self.agent.run(prompt)
            listing = result.output

            # Ajouter métadonnées
            listing.source = source
            listing.raw_data = raw_data

            return listing

        except Exception as e:
            print(f"Erreur LLM normalisation: {e}")
            return None

    def _extract_project_from_title(self, title: str) -> str:
        """Extrait le nom du projet depuis le titre"""
        # Pattern: "2 Bed Condo at Project Name"
        match = re.search(r'\bat\s+(.+?)(?:\s*,|\s+in|\s+near|\s*$)', title, re.I)
        if match:
            return match.group(1).strip()
        return "Unknown"

    def _detect_currency(self, text: str) -> str:
        """Détecte la devise dans un texte"""
        text_upper = text.upper()
        if 'THB' in text_upper or '฿' in text:
            return 'THB'
        if 'USD' in text_upper or '$' in text:
            return 'USD'
        if 'EUR' in text_upper or '€' in text:
            return 'EUR'
        return 'THB'  # Défaut


# ============================================================================
# TEST
# ============================================================================

async def test_normalizer():
    """Test le normaliseur hybride"""
    normalizer = HybridNormalizer()

    # Test 1: Cas simple (règles)
    simple_data = {
        'id': 'TP123',
        'url': 'https://thailand-property.com/condo/123',
        'title': '2 Bedroom Condo for Sale at The Davis Bangkok Sukhumvit 24',
        'project_name': 'The Davis Bangkok',
        'address': 'Sukhumvit 24, Bangkok',
        'price': 'THB 12,500,000',
        'size': '85 sqm',
        'bedrooms': '2',
        'bathrooms': '2',
    }

    listing = await normalizer.normalize(simple_data, 'thailand-property')

    if listing:
        print("=== LISTING NORMALISÉ (Règles) ===")
        print(f"Titre: {listing.title}")
        print(f"Projet: {listing.project.name_normalized}")
        print(f"Zone: {listing.address.zone}")
        print(f"District: {listing.address.district}")
        print(f"Chambres: {listing.specs.bedrooms}")
        print(f"Prix: {listing.price.thb:,.0f} THB")
        print(f"Prix/m²: {listing.price.per_sqm:,.0f} THB")
        print(f"Hash: {listing.canonical_hash}")
    else:
        print("Erreur normalisation")


if __name__ == '__main__':
    import asyncio
    asyncio.run(test_normalizer())
