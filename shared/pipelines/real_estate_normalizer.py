#!/usr/bin/env python3
"""
Pipeline de Normalisation Immobilière - Palantir Thaïlande
===========================================================

Capacité: Déduplication + Normalisation multi-sources

Pipeline:
1. Extraction → Parsing → Normalisation
2. Matching (hash + fuzzy) → Résolution entités
3. Enrichissement géographique
4. Calcul hash canonique
5. Insertion Supabase

Auteur: Léon 🏝️
"""

import re
import hashlib
import json
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field, asdict
import logging

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# DATA CLASSES - Structures de données
# ============================================================================

@dataclass
class Location:
    """Localisation normalisée"""
    address_raw: str
    address_normalized: str = ""
    province: str = ""
    district: str = ""
    zone: str = ""
    microzone: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geo_point: Optional[str] = None  # PostGIS format


@dataclass
class PropertySpecs:
    """Caractéristiques physiques normalisées"""
    property_type: str = ""  # condo, villa, townhouse, land
    bedrooms: Optional[Decimal] = None
    bathrooms: Optional[Decimal] = None
    floor_area_sqm: Optional[Decimal] = None
    land_area_sqm: Optional[Decimal] = None
    floor_number: Optional[int] = None
    orientation: str = ""
    view_types: List[str] = field(default_factory=list)


@dataclass
class Price:
    """Prix normalisé"""
    price_thb: Decimal = Decimal("0")
    price_original: Decimal = Decimal("0")
    currency_original: str = "THB"
    price_per_sqm: Optional[Decimal] = None


@dataclass
class Listing:
    """Listing complet normalisé"""
    # Identification (obligatoires en premier)
    source: str
    external_id: str
    external_url: str
    title: str

    # Localisation et Specs (obligatoires)
    location: Location = None
    specs: PropertySpecs = None
    price: Price = None

    # Optionnels
    description: str = ""
    project_name: str = ""
    project_name_normalized: str = ""
    developer_name: str = ""
    images: List[str] = field(default_factory=list)
    agent_name: str = ""
    agent_phone: str = ""
    agency_name: str = ""
    canonical_hash: str = ""
    match_confidence: Decimal = Decimal("0")
    raw_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.location is None:
            self.location = Location(address_raw="")
        if self.specs is None:
            self.specs = PropertySpecs()
        if self.price is None:
            self.price = Price(price_thb=Decimal("0"), price_original=Decimal("0"))


# ============================================================================
# NORMALISATEURS
# ============================================================================

class ThaiAddressNormalizer:
    """Normalisation des adresses thaïlandaises"""

    # Mapping districts Bangkok
    BANGKOK_DISTRICTS = {
        'sukhumvit': 'Watthana',
        'sathorn': 'Sathon',
        'silom': 'Bang Rak',
        'sukhumvit 1-21': 'Khlong Toei Nuea',
        'sukhumvit 22-63': 'Khlong Tan Nuea',
        'asoke': 'Khlong Toei Nuea',
        'thonglor': 'Khlong Tan Nuea',
        'ekkamai': 'Khlong Tan Nuea',
        'phrom phong': 'Khlong Tan Nuea',
        'riverside': 'Bang Rak',
        'ratchada': 'Din Daeng',
        'ladprao': 'Lat Phrao',
        'ari': 'Phaya Thai',
        'phahonyothin': 'Phaya Thai',
        'siam': 'Pathum Wan',
        'chit lom': 'Pathum Wan',
        'ploenchit': 'Pathum Wan',
        'wireless road': 'Pathum Wan',
    }

    PROVINCE_ALIASES = {
        'bangkok': 'Bangkok',
        'bkk': 'Bangkok',
        'กรุงเทพ': 'Bangkok',
        'phuket': 'Phuket',
        'ภูเก็ต': 'Phuket',
        'koh samui': 'Surat Thani',
        'samui': 'Surat Thani',
        'เกาะสมุย': 'Surat Thani',
    }

    def normalize(self, address: str) -> Location:
        """Normalise une adresse thaïlandaise"""
        loc = Location(address_raw=address)

        if not address:
            return loc

        # Nettoyage
        addr_lower = address.lower().strip()
        addr_normalized = re.sub(r'\s+', ' ', addr_lower)

        # Détection province
        for alias, province in self.PROVINCE_ALIASES.items():
            if alias in addr_normalized:
                loc.province = province
                break

        # Détection district Bangkok
        if loc.province == 'Bangkok':
            for area, district in self.BANGKOK_DISTRICTS.items():
                if area in addr_normalized:
                    loc.district = district
                    break

        # Extraction zone (Sukhumvit 23, etc.)
        zone_match = re.search(r'(sukhumvit|sathorn|silom|ratchada|ladprao)\s*(soi)?\s*(\d+)?', addr_normalized)
        if zone_match:
            zone_name = zone_match.group(1).capitalize()
            if zone_match.group(3):
                zone_name += f" {zone_match.group(3)}"
            loc.zone = zone_name

        loc.address_normalized = addr_normalized
        return loc


class PropertySpecsNormalizer:
    """Normalisation des caractéristiques immobilières"""

    BEDROOM_ALIASES = {
        'studio': Decimal('0'),
        '0 bedroom': Decimal('0'),
        '1 bedroom': Decimal('1'),
        '1 bed': Decimal('1'),
        '1br': Decimal('1'),
        '2 bedroom': Decimal('2'),
        '2 bed': Decimal('2'),
        '2br': Decimal('2'),
        '3 bedroom': Decimal('3'),
        '3 bed': Decimal('3'),
        '3br': Decimal('3'),
    }

    PROPERTY_TYPE_ALIASES = {
        'condo': 'condo',
        'condominium': 'condo',
        'apartment': 'condo',
        'villa': 'villa',
        'house': 'villa',
        'townhouse': 'townhouse',
        'townhome': 'townhouse',
        'land': 'land',
    }

    VIEW_TYPE_ALIASES = {
        'sea view': 'sea',
        'ocean view': 'sea',
        'city view': 'city',
        'city skyline': 'city',
        'pool view': 'pool',
        'garden view': 'garden',
        'mountain view': 'mountain',
        'river view': 'river',
    }

    def normalize_bedrooms(self, text: str) -> Optional[Decimal]:
        """Extrait et normalise le nombre de chambres"""
        if not text:
            return None

        text_lower = text.lower()

        # Alias directs
        for alias, value in self.BEDROOM_ALIASES.items():
            if alias in text_lower:
                return value

        # Pattern numérique
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:bed|bedroom|br)', text_lower)
        if match:
            return Decimal(match.group(1))

        return None

    def normalize_area(self, text: str) -> Optional[Decimal]:
        """Extrait et normalise une surface en m²"""
        if not text:
            return None

        # Pattern: "45 sqm", "45 m²", "45 sq.m."
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:sqm|sq\.?m\.?|m²|m2)', text.lower())
        if match:
            return Decimal(match.group(1))

        return None

    def normalize_property_type(self, text: str) -> str:
        """Normalise le type de bien"""
        if not text:
            return ""

        text_lower = text.lower()
        for alias, ptype in self.PROPERTY_TYPE_ALIASES.items():
            if alias in text_lower:
                return ptype

        return ""

    def extract_views(self, text: str) -> List[str]:
        """Extrait les types de vue"""
        if not text:
            return []

        text_lower = text.lower()
        views = []

        for alias, view_type in self.VIEW_TYPE_ALIASES.items():
            if alias in text_lower:
                views.append(view_type)

        return list(set(views))


class PriceNormalizer:
    """Normalisation des prix"""

    CURRENCY_RATES = {
        'THB': Decimal('1'),
        'USD': Decimal('35'),  # Approximatif
        'EUR': Decimal('38'),  # Approximatif
        'GBP': Decimal('44'),  # Approximatif
    }

    def normalize(self, price_str: str, currency: str = 'THB') -> Optional[Price]:
        """Normalise un prix"""
        if not price_str:
            return None

        # Extraction numérique
        numbers = re.findall(r'[\d,]+(?:\.\d+)?', price_str.replace(',', ''))
        if not numbers:
            return None

        price_value = Decimal(numbers[0].replace(',', ''))

        # Conversion en THB
        currency_upper = currency.upper()
        rate = self.CURRENCY_RATES.get(currency_upper, Decimal('1'))
        price_thb = price_value * rate

        return Price(
            price_thb=price_thb,
            price_original=price_value,
            currency_original=currency_upper
        )


# ============================================================================
# DÉDUPLICATEUR
# ============================================================================

class ListingDeduplicator:
    """Déduplication des listings multi-sources"""

    def compute_canonical_hash(self, listing: Listing) -> str:
        """
        Calcule un hash canonique pour identifier un bien unique

        Basé sur:
        - Nom projet normalisé
        - Bedrooms
        - Surface
        - Étage (optionnel)
        """
        components = [
            listing.project_name_normalized,
            str(listing.specs.bedrooms or ''),
            str(listing.specs.floor_area_sqm or ''),
            str(listing.specs.floor_number or ''),
        ]

        hash_input = '|'.join(components).lower()
        return hashlib.md5(hash_input.encode()).hexdigest()

    def compute_similarity_score(self, listing1: Listing, listing2: Listing) -> Decimal:
        """
        Calcule un score de similarité entre deux listings

        Retourne un score 0-1
        """
        score = Decimal('0')

        # Même projet? (poids 0.4)
        if listing1.project_name_normalized and listing2.project_name_normalized:
            if listing1.project_name_normalized == listing2.project_name_normalized:
                score += Decimal('0.4')

        # Même localisation? (poids 0.2)
        if listing1.location.zone and listing2.location.zone:
            if listing1.location.zone == listing2.location.zone:
                score += Decimal('0.2')

        # Mêmes specs? (poids 0.4)
        specs_match = 0
        if listing1.specs.bedrooms == listing2.specs.bedrooms:
            specs_match += 1
        if listing1.specs.floor_area_sqm and listing2.specs.floor_area_sqm:
            diff = abs(listing1.specs.floor_area_sqm - listing2.specs.floor_area_sqm)
            if diff < Decimal('5'):  # ±5 m²
                specs_match += 1

        score += Decimal(str(specs_match * 0.2))

        return min(score, Decimal('1'))


# ============================================================================
# PIPELINE PRINCIPAL
# ============================================================================

class RealEstatePipeline:
    """Pipeline complet de normalisation immobilière"""

    def __init__(self):
        self.address_normalizer = ThaiAddressNormalizer()
        self.specs_normalizer = PropertySpecsNormalizer()
        self.price_normalizer = PriceNormalizer()
        self.deduplicator = ListingDeduplicator()

    def process_raw_listing(self, raw_data: Dict[str, Any], source: str) -> Optional[Listing]:
        """
        Traite un listing brut et retourne un listing normalisé

        Input: données brutes depuis scraping
        Output: Listing normalisé avec hash canonique
        """
        try:
            # Extraction données de base
            external_id = raw_data.get('id', '') or raw_data.get('listing_id', '')
            external_url = raw_data.get('url', '')
            title = raw_data.get('title', '')

            if not external_id or not title:
                logger.warning(f"Listing incomplet: {raw_data}")
                return None

            # Normalisation projet
            project_name = raw_data.get('project_name', '') or raw_data.get('building', '')
            project_name_normalized = self._normalize_text(project_name)

            # Normalisation localisation
            address = raw_data.get('address', '') or raw_data.get('location', '')
            location = self.address_normalizer.normalize(address)

            # Normalisation specs
            specs = PropertySpecs(
                property_type=self.specs_normalizer.normalize_property_type(title + ' ' + raw_data.get('type', '')),
                bedrooms=self.specs_normalizer.normalize_bedrooms(title + ' ' + raw_data.get('bedrooms', '')),
                bathrooms=Decimal(str(raw_data.get('bathrooms', 0))) if raw_data.get('bathrooms') else None,
                floor_area_sqm=self.specs_normalizer.normalize_area(raw_data.get('size', '')),
                view_types=self.specs_normalizer.extract_views(title + ' ' + raw_data.get('description', '')),
            )

            # Normalisation prix
            price_str = raw_data.get('price', '')
            price = self.price_normalizer.normalize(price_str)

            if not price:
                logger.warning(f"Prix invalide pour {external_id}")
                return None

            # Calcul prix au m²
            if specs.floor_area_sqm and specs.floor_area_sqm > 0:
                price.price_per_sqm = price.price_thb / specs.floor_area_sqm

            # Création listing
            listing = Listing(
                source=source,
                external_id=str(external_id),
                external_url=external_url,
                title=title,
                description=raw_data.get('description', ''),
                project_name=project_name,
                project_name_normalized=project_name_normalized,
                developer_name=raw_data.get('developer', ''),
                location=location,
                specs=specs,
                price=price,
                images=raw_data.get('images', []),
                agent_name=raw_data.get('agent_name', ''),
                agent_phone=raw_data.get('agent_phone', ''),
                agency_name=raw_data.get('agency', ''),
                raw_data=raw_data,
            )

            # Hash canonique
            listing.canonical_hash = self.deduplicator.compute_canonical_hash(listing)

            logger.info(f"Listing normalisé: {title[:50]}... | Hash: {listing.canonical_hash[:8]}")
            return listing

        except Exception as e:
            logger.error(f"Erreur traitement listing: {e}")
            return None

    def _normalize_text(self, text: str) -> str:
        """Normalise un texte pour matching"""
        if not text:
            return ""

        # Minuscules
        text = text.lower()

        # Suppression ponctuation
        text = re.sub(r'[^\w\s]', ' ', text)

        # Espaces multiples
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def to_supabase_dict(self, listing: Listing) -> Dict[str, Any]:
        """Convertit un listing en dict pour insertion Supabase"""
        return {
            # Listings table
            'source_id': listing.source,  # Sera résolu par FK
            'external_id': listing.external_id,
            'external_url': listing.external_url,
            'price_thb': float(listing.price.price_thb),
            'price_original': float(listing.price.price_original),
            'currency_original': listing.price.currency_original,
            'price_per_sqm': float(listing.price.price_per_sqm) if listing.price.price_per_sqm else None,
            'title': listing.title,
            'description': listing.description,
            'raw_specs': {
                'bedrooms': str(listing.specs.bedrooms) if listing.specs.bedrooms else None,
                'bathrooms': str(listing.specs.bathrooms) if listing.specs.bathrooms else None,
                'floor_area_sqm': str(listing.specs.floor_area_sqm) if listing.specs.floor_area_sqm else None,
                'property_type': listing.specs.property_type,
                'view_types': listing.specs.view_types,
            },
            'images': listing.images,
            'agent_name': listing.agent_name,
            'agent_phone': listing.agent_phone,
            'agency_name': listing.agency_name,
            'canonical_hash': listing.canonical_hash,

            # Projects/Residences (pour création si n'existe pas)
            'project_name': listing.project_name,
            'project_name_normalized': listing.project_name_normalized,

            # Géographie
            'address_raw': listing.location.address_raw,
            'address_normalized': listing.location.address_normalized,
            'province': listing.location.province,
            'district': listing.location.district,
            'zone': listing.location.zone,
        }


# ============================================================================
# TEST
# ============================================================================

if __name__ == '__main__':
    # Exemple de test
    pipeline = RealEstatePipeline()

    # Données brutes simulées
    raw_listing = {
        'id': 'TP123456',
        'url': 'https://www.thailand-property.com/condo/123456',
        'title': '2 Bedroom Condo for Sale at The Davis Bangkok Sukhumvit 24',
        'description': 'Luxury 2 bedroom condo with city view, 85 sqm, high floor',
        'project_name': 'The Davis Bangkok',
        'address': 'Sukhumvit 24, Bangkok',
        'price': 'THB 12,500,000',
        'size': '85 sqm',
        'bedrooms': '2',
        'bathrooms': '2',
        'type': 'Condominium',
        'images': ['https://example.com/image1.jpg'],
        'agent_name': 'John Smith',
    }

    # Traitement
    normalized = pipeline.process_raw_listing(raw_listing, 'thailand-property')

    if normalized:
        print("\n=== LISTING NORMALISÉ ===")
        print(f"Titre: {normalized.title}")
        print(f"Projet: {normalized.project_name_normalized}")
        print(f"Type: {normalized.specs.property_type}")
        print(f"Chambres: {normalized.specs.bedrooms}")
        print(f"Surface: {normalized.specs.floor_area_sqm} m²")
        print(f"Prix: {normalized.price.price_thb:,.0f} THB")
        print(f"Prix/m²: {normalized.price.price_per_sqm:,.0f} THB/m²")
        print(f"Zone: {normalized.location.zone}")
        print(f"District: {normalized.location.district}")
        print(f"Province: {normalized.location.province}")
        print(f"Hash canonique: {normalized.canonical_hash}")

        print("\n=== SUPABASE DICT ===")
        print(json.dumps(pipeline.to_supabase_dict(normalized), indent=2))
