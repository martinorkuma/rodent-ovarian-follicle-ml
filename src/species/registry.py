"""
Species registry for managing multi-species rodent follicle analysis.

This module provides a centralized registry of supported rodent species
with their morphological characteristics and analysis parameters.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class SpeciesInfo:
    """Information about a rodent species."""
    
    # Identifiers
    common_name: str
    scientific_name: str
    species_code: str  # Short code for filenames (e.g., 'mouse', 'rat', 'nmr')
    mother_id: str  # MOTHER database identifier
    
    # Morphology
    typical_follicle_types: List[str]
    follicle_size_ranges: Dict[str, tuple]  # {follicle_type: (min_um, max_um)}
    ovary_size_mm: tuple  # (min, max) typical ovary size
    
    # Analysis parameters
    recommended_tile_size: int = 256
    recommended_magnification: str = "20x"
    stain_normalization: str = "standardize"  # or "reinhard", "macenko"
    
    # Dataset info
    available_samples: int = 0
    age_groups: List[str] = None
    
    # Notes
    notes: str = ""


# Species Registry
SPECIES_REGISTRY = {
    "mouse": SpeciesInfo(
        common_name="Mouse",
        scientific_name="Mus musculus",
        species_code="mouse",
        mother_id="M-musculus",
        typical_follicle_types=[
            "primordial", "primary", "secondary", "antral"
        ],
        follicle_size_ranges={
            "primordial": (15, 25),
            "primary": (25, 40),
            "secondary": (40, 150),
            "antral": (150, 400)
        },
        ovary_size_mm=(2, 4),
        recommended_tile_size=256,
        recommended_magnification="20x",
        age_groups=["juvenile", "young_adult", "adult", "aged"],
        notes="Most common laboratory model. Extensive literature available."
    ),
    
    "rat": SpeciesInfo(
        common_name="Rat",
        scientific_name="Rattus norvegicus",
        species_code="rat",
        mother_id="R-norvegicus",
        typical_follicle_types=[
            "primordial", "primary", "secondary", "antral", "preovulatory"
        ],
        follicle_size_ranges={
            "primordial": (20, 30),
            "primary": (30, 50),
            "secondary": (50, 200),
            "antral": (200, 600),
            "preovulatory": (600, 1000)
        },
        ovary_size_mm=(4, 7),
        recommended_tile_size=512,
        recommended_magnification="10x",
        age_groups=["juvenile", "young_adult", "adult", "aged"],
        notes="Larger follicles than mouse. May need larger tiles."
    ),
    
    "nmr": SpeciesInfo(
        common_name="Naked Mole Rat",
        scientific_name="Heterocephalus glaber",
        species_code="nmr",
        mother_id="H-glaber",
        typical_follicle_types=[
            "primordial", "transitional_primordial", "primary", 
            "transitional_primary", "secondary", "multilayer"
        ],
        follicle_size_ranges={
            "primordial": (15, 25),
            "transitional_primordial": (20, 30),
            "primary": (25, 40),
            "transitional_primary": (35, 50),
            "secondary": (45, 80),
            "multilayer": (80, 150)
        },
        ovary_size_mm=(1, 3),
        recommended_tile_size=256,
        recommended_magnification="20x",
        age_groups=["juvenile", "adult"],
        notes="Unique reproductive biology. Limited antral development."
    ),
    
    "guinea_pig": SpeciesInfo(
        common_name="Guinea Pig",
        scientific_name="Cavia porcellus",
        species_code="guinea_pig",
        mother_id="C-porcellus",
        typical_follicle_types=[
            "primordial", "primary", "secondary", "antral"
        ],
        follicle_size_ranges={
            "primordial": (20, 35),
            "primary": (35, 60),
            "secondary": (60, 250),
            "antral": (250, 800)
        },
        ovary_size_mm=(5, 10),
        recommended_tile_size=512,
        recommended_magnification="10x",
        age_groups=["juvenile", "adult"],
        notes="Large ovaries with prominent antral follicles."
    ),
    
    "hamster": SpeciesInfo(
        common_name="Syrian Hamster",
        scientific_name="Mesocricetus auratus",
        species_code="hamster",
        mother_id="M-auratus",
        typical_follicle_types=[
            "primordial", "primary", "secondary", "antral"
        ],
        follicle_size_ranges={
            "primordial": (15, 25),
            "primary": (25, 45),
            "secondary": (45, 180),
            "antral": (180, 500)
        },
        ovary_size_mm=(3, 5),
        recommended_tile_size=256,
        recommended_magnification="20x",
        age_groups=["juvenile", "adult"],
        notes="Regular estrous cycles. Good model for reproductive studies."
    ),
}


def get_species_info(species_code: str) -> Optional[SpeciesInfo]:
    """
    Get information about a species.
    
    Args:
        species_code: Short species code (e.g., 'mouse', 'rat')
        
    Returns:
        SpeciesInfo object or None if not found
    """
    species_info = SPECIES_REGISTRY.get(species_code.lower())
    
    if species_info is None:
        logger.warning(f"Species '{species_code}' not found in registry")
        logger.info(f"Available species: {list(SPECIES_REGISTRY.keys())}")
    
    return species_info


def list_species() -> List[str]:
    """
    Get list of all supported species codes.
    
    Returns:
        List of species codes
    """
    return list(SPECIES_REGISTRY.keys())


def validate_species(species_code: str) -> bool:
    """
    Check if a species is supported.
    
    Args:
        species_code: Species code to validate
        
    Returns:
        True if supported, False otherwise
    """
    return species_code.lower() in SPECIES_REGISTRY


def get_follicle_types(species_code: str) -> List[str]:
    """
    Get typical follicle types for a species.
    
    Args:
        species_code: Species code
        
    Returns:
        List of follicle type names
    """
    info = get_species_info(species_code)
    if info:
        return info.typical_follicle_types
    return []


def get_recommended_tile_size(species_code: str) -> int:
    """
    Get recommended tile size for a species.
    
    Args:
        species_code: Species code
        
    Returns:
        Recommended tile size in pixels
    """
    info = get_species_info(species_code)
    if info:
        return info.recommended_tile_size
    return 256  # Default


def get_species_labelmap(species_code: str) -> Dict[int, str]:
    """
    Generate labelmap for a species.
    
    Args:
        species_code: Species code
        
    Returns:
        Dictionary mapping class IDs to follicle type names
    """
    info = get_species_info(species_code)
    if not info:
        return {}
    
    labelmap = {0: "background"}
    for idx, follicle_type in enumerate(info.typical_follicle_types, start=1):
        labelmap[idx] = follicle_type
    
    return labelmap


def compare_species(species_codes: List[str]) -> Dict:
    """
    Compare multiple species characteristics.
    
    Args:
        species_codes: List of species codes to compare
        
    Returns:
        Dictionary with comparison data
    """
    comparison = {
        "species": [],
        "follicle_types": [],
        "ovary_size": [],
        "tile_size": []
    }
    
    for code in species_codes:
        info = get_species_info(code)
        if info:
            comparison["species"].append(info.common_name)
            comparison["follicle_types"].append(len(info.typical_follicle_types))
            comparison["ovary_size"].append(info.ovary_size_mm)
            comparison["tile_size"].append(info.recommended_tile_size)
    
    return comparison


def register_custom_species(species_code: str, species_info: SpeciesInfo):
    """
    Register a custom species (for research use).
    
    Args:
        species_code: Unique code for the species
        species_info: SpeciesInfo object with species details
    """
    if species_code in SPECIES_REGISTRY:
        logger.warning(f"Overwriting existing species: {species_code}")
    
    SPECIES_REGISTRY[species_code] = species_info
    logger.info(f"Registered custom species: {species_code}")


# Alias mapping for common alternative names
SPECIES_ALIASES = {
    "mus_musculus": "mouse",
    "m_musculus": "mouse",
    "rattus_norvegicus": "rat",
    "r_norvegicus": "rat",
    "heterocephalus_glaber": "nmr",
    "h_glaber": "nmr",
    "naked_mole_rat": "nmr",
    "cavia_porcellus": "guinea_pig",
    "c_porcellus": "guinea_pig",
    "mesocricetus_auratus": "hamster",
    "m_auratus": "hamster",
    "syrian_hamster": "hamster"
}


def resolve_species_code(name: str) -> Optional[str]:
    """
    Resolve various species name formats to standard code.
    
    Args:
        name: Species name (common, scientific, or code)
        
    Returns:
        Standardized species code or None
    """
    name_lower = name.lower().replace(" ", "_").replace("-", "_")
    
    # Check if it's already a valid code
    if name_lower in SPECIES_REGISTRY:
        return name_lower
    
    # Check aliases
    if name_lower in SPECIES_ALIASES:
        return SPECIES_ALIASES[name_lower]
    
    # Check scientific names
    for code, info in SPECIES_REGISTRY.items():
        if info.scientific_name.lower().replace(" ", "_") == name_lower:
            return code
        if info.common_name.lower().replace(" ", "_") == name_lower:
            return code
    
    return None
