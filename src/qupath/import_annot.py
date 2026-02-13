"""
Import annotations from QuPath for ML training.

This module handles importing annotations from QuPath (GeoJSON format)
and mapping them to image tiles for training.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from shapely.geometry import shape, Point, Polygon
from shapely.ops import unary_union

logger = logging.getLogger(__name__)


def load_geojson(geojson_path: Path) -> Dict:
    """
    Load a GeoJSON file from QuPath.
    
    Args:
        geojson_path: Path to GeoJSON file
        
    Returns:
        Dictionary with GeoJSON data
    """
    with open(geojson_path, 'r') as f:
        data = json.load(f)
    
    logger.info(f"Loaded GeoJSON from {geojson_path}")
    logger.info(f"Features: {len(data.get('features', []))}")
    
    return data


def parse_qupath_classification(properties: Dict) -> str:
    """
    Parse classification from QuPath properties.
    
    Args:
        properties: Feature properties dictionary
        
    Returns:
        Classification string (e.g., 'Primordial', 'Primary')
    """
    # QuPath stores classification in different ways
    classification = properties.get('classification', {})
    
    if isinstance(classification, dict):
        return classification.get('name', 'Unknown')
    elif isinstance(classification, str):
        return classification
    
    # Check for object type
    object_type = properties.get('objectType', 'Unknown')
    if object_type == 'annotation':
        return properties.get('name', 'Unknown')
    
    return 'Unknown'


def geojson_to_dataframe(geojson_data: Dict, coordinate_scale: float = 1.0) -> pd.DataFrame:
    """
    Convert GeoJSON features to pandas DataFrame.
    
    Args:
        geojson_data: GeoJSON dictionary
        coordinate_scale: Scale factor for coordinates (microns per pixel)
        
    Returns:
        DataFrame with annotation information
    """
    features = geojson_data.get('features', [])
    
    annotations = []
    for feature in features:
        geometry = feature.get('geometry', {})
        properties = feature.get('properties', {})
        
        # Parse classification
        classification = parse_qupath_classification(properties)
        
        # Get geometry info
        geom = shape(geometry)
        bounds = geom.bounds  # (minx, miny, maxx, maxy)
        centroid = geom.centroid
        area = geom.area * (coordinate_scale ** 2)
        
        annotation_dict = {
            'classification': classification,
            'geometry_type': geometry.get('type'),
            'x_min': bounds[0],
            'y_min': bounds[1],
            'x_max': bounds[2],
            'y_max': bounds[3],
            'centroid_x': centroid.x,
            'centroid_y': centroid.y,
            'area_um2': area,
            'geometry': geom
        }
        
        # Add any custom properties
        for key, value in properties.items():
            if key not in ['classification', 'objectType', 'name']:
                annotation_dict[f'property_{key}'] = value
        
        annotations.append(annotation_dict)
    
    df = pd.DataFrame(annotations)
    logger.info(f"Parsed {len(df)} annotations")
    
    if not df.empty:
        logger.info(f"Classifications: {df['classification'].value_counts().to_dict()}")
    
    return df


def map_annotations_to_tiles(
    annotations_df: pd.DataFrame,
    tiles_manifest: pd.DataFrame,
    overlap_threshold: float = 0.5
) -> pd.DataFrame:
    """
    Map annotations to image tiles based on spatial overlap.
    
    Args:
        annotations_df: DataFrame with annotation geometries
        tiles_manifest: DataFrame with tile information (x, y, width, height)
        overlap_threshold: Minimum overlap ratio to assign label (0-1)
        
    Returns:
        Updated tiles_manifest with label column
    """
    logger.info(f"Mapping {len(annotations_df)} annotations to {len(tiles_manifest)} tiles")
    
    # Initialize label column
    tiles_manifest['label'] = 'background'
    tiles_manifest['label_confidence'] = 0.0
    
    for tile_idx, tile_row in tiles_manifest.iterrows():
        # Create tile polygon
        tile_poly = Polygon([
            (tile_row['x'], tile_row['y']),
            (tile_row['x'] + tile_row['width'], tile_row['y']),
            (tile_row['x'] + tile_row['width'], tile_row['y'] + tile_row['height']),
            (tile_row['x'], tile_row['y'] + tile_row['height'])
        ])
        
        tile_area = tile_poly.area
        best_overlap = 0.0
        best_classification = 'background'
        
        # Find annotation with highest overlap
        for _, annot in annotations_df.iterrows():
            annot_geom = annot['geometry']
            
            # Calculate overlap
            try:
                intersection = tile_poly.intersection(annot_geom)
                overlap_ratio = intersection.area / tile_area
                
                if overlap_ratio > best_overlap:
                    best_overlap = overlap_ratio
                    best_classification = annot['classification']
            except Exception as e:
                logger.debug(f"Error calculating overlap: {e}")
                continue
        
        # Assign label if overlap exceeds threshold
        if best_overlap >= overlap_threshold:
            tiles_manifest.at[tile_idx, 'label'] = best_classification
            tiles_manifest.at[tile_idx, 'label_confidence'] = best_overlap
    
    # Log label distribution
    label_counts = tiles_manifest['label'].value_counts()
    logger.info(f"Tile label distribution:")
    for label, count in label_counts.items():
        logger.info(f"  {label}: {count} ({count/len(tiles_manifest)*100:.1f}%)")
    
    return tiles_manifest


def import_qupath_annotations(
    geojson_path: Path,
    tiles_manifest_path: Path,
    species: str,
    coordinate_scale: float = 1.0,
    overlap_threshold: float = 0.5
) -> pd.DataFrame:
    """
    Complete workflow to import QuPath annotations and map to tiles.
    
    Args:
        geojson_path: Path to QuPath GeoJSON export
        tiles_manifest_path: Path to tiles manifest CSV
        species: Species code (for validation)
        coordinate_scale: Microns per pixel
        overlap_threshold: Minimum overlap to assign label
        
    Returns:
        Updated tiles manifest with labels
    """
    logger.info(f"Importing QuPath annotations for {species}")
    
    # Load GeoJSON
    geojson_data = load_geojson(geojson_path)
    
    # Parse to DataFrame
    annotations_df = geojson_to_dataframe(geojson_data, coordinate_scale)
    
    # Load tiles manifest
    tiles_manifest = pd.read_csv(tiles_manifest_path)
    logger.info(f"Loaded {len(tiles_manifest)} tiles from manifest")
    
    # Map annotations to tiles
    labeled_tiles = map_annotations_to_tiles(
        annotations_df,
        tiles_manifest,
        overlap_threshold
    )
    
    # Validate classifications for species
    from species.registry import get_species_info
    species_info = get_species_info(species)
    
    if species_info:
        valid_types = species_info.typical_follicle_types + ['background']
        invalid_labels = set(labeled_tiles['label'].unique()) - set(valid_types)
        
        if invalid_labels:
            logger.warning(f"Found invalid labels for {species}: {invalid_labels}")
            logger.warning(f"Valid labels: {valid_types}")
    
    return labeled_tiles


def validate_geojson(geojson_path: Path) -> bool:
    """
    Validate QuPath GeoJSON format.
    
    Args:
        geojson_path: Path to GeoJSON file
        
    Returns:
        True if valid, False otherwise
    """
    try:
        data = load_geojson(geojson_path)
        
        # Check required fields
        if 'type' not in data:
            logger.error("Missing 'type' field")
            return False
        
        if data['type'] != 'FeatureCollection':
            logger.error(f"Expected FeatureCollection, got {data['type']}")
            return False
        
        if 'features' not in data:
            logger.error("Missing 'features' field")
            return False
        
        # Check feature structure
        for i, feature in enumerate(data['features'][:5]):  # Check first 5
            if 'geometry' not in feature:
                logger.error(f"Feature {i} missing geometry")
                return False
            
            if 'properties' not in feature:
                logger.warning(f"Feature {i} missing properties")
        
        logger.info("✓ GeoJSON validation passed")
        return True
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return False


def export_tile_labels_for_review(
    labeled_tiles: pd.DataFrame,
    output_path: Path,
    sample_size: int = 100
):
    """
    Export sample of labeled tiles for manual review.
    
    Args:
        labeled_tiles: DataFrame with tile labels
        output_path: Path to save review file
        sample_size: Number of tiles to sample
    """
    # Sample tiles
    if len(labeled_tiles) > sample_size:
        sample = labeled_tiles.sample(n=sample_size, random_state=42)
    else:
        sample = labeled_tiles
    
    # Select relevant columns
    review_cols = ['tile_id', 'tile_path', 'label', 'label_confidence', 
                   'x', 'y', 'tissue_ratio']
    review_df = sample[review_cols].copy()
    
    # Sort by confidence (lowest first for review)
    review_df = review_df.sort_values('label_confidence')
    
    # Save
    review_df.to_csv(output_path, index=False)
    logger.info(f"Exported {len(review_df)} tiles for review to {output_path}")
