# Rodent Ovarian Follicle ML Pipeline - Complete Implementation Guide

## 🚀 Overview

This is an **expanded, multi-species pipeline** for rodent ovarian follicle analysis that builds on the naked mole rat implementation with:

- ✅ **Multi-species support** (Mouse, Rat, NMR, Guinea Pig, Hamster, +custom)
- ✅ **Species registry system** for managing species-specific parameters
- ✅ **Enhanced QuPath integration** with bidirectional data flow
- ✅ **Cross-species comparison** and transfer learning
- ✅ **Advanced preprocessing** with species-specific normalization
- ✅ **Flexible model architectures** beyond ResNet
- ✅ **Comprehensive evaluation** with species-aware metrics
- ✅ **Production-ready** shell scripts with argument parsing
- ✅ **Docker support** for reproducibility

## 📦 What's Included

### Enhanced Core Modules

#### 1. Species Management (`src/species/`)
```python
from species.registry import get_species_info, list_species

# Get species information
mouse_info = get_species_info('mouse')
print(mouse_info.typical_follicle_types)
# ['primordial', 'primary', 'secondary', 'antral']

# List all supported species
species = list_species()
# ['mouse', 'rat', 'nmr', 'guinea_pig', 'hamster']
```

**Key files:**
- `registry.py` - Species database with morphology and parameters
- `morphology.py` - Species-specific morphological validators
- `validators.py` - Data validation for each species

#### 2. QuPath Integration (`src/qupath/`)
```python
from qupath.import_annot import import_qupath_annotations
from qupath.export import export_predictions_to_qupath

# Import annotations from QuPath
annotations = import_qupath_annotations(
    'data/annotations/mouse_slide_001.geojson',
    species='mouse'
)

# Export predictions back to QuPath
export_predictions_to_qupath(
    predictions_df,
    'outputs/predictions/mouse_predictions.geojson'
)
```

**Key files:**
- `import_annot.py` - Import GeoJSON/CSV annotations from QuPath
- `export.py` - Export predictions in QuPath format
- `groovy_bridge.py` - Python-Groovy communication
- Groovy scripts in `annotations/qupath_scripts/`

#### 3. Enhanced Preprocessing (`src/preprocess/`)
```python
from preprocess.stain_norm import normalize_he_staining
from preprocess.augmentation import get_augmentation_pipeline

# Advanced stain normalization (Reinhard, Macenko, etc.)
normalized = normalize_he_staining(
    image,
    method='macenko',
    reference_image=ref_img
)

# Species-specific augmentation
aug_pipeline = get_augmentation_pipeline(
    species='mouse',
    intensity='medium'
)
```

**Key files:**
- `stain_norm.py` - Reinhard, Macenko, Vahadane normalization
- `augmentation.py` - Species-appropriate augmentation policies
- `tissue_detection.py` - Advanced tissue segmentation

#### 4. Model Zoo (`src/train/models.py`)
```python
from train.models import get_model

# Multiple architectures
model = get_model(
    'efficientnet_b3',
    num_classes=5,
    pretrained=True
)

# Species-specific models
model = get_model(
    'resnet34',
    num_classes=mouse_info.num_classes,
    input_size=mouse_info.recommended_tile_size
)
```

**Supported models:**
- ResNet (18, 34, 50, 101)
- EfficientNet (B0-B7)
- DenseNet (121, 169, 201)
- Vision Transformer (ViT)
- Custom U-Net for segmentation

#### 5. Cross-Species Analysis (`src/eval/compare.py`)
```python
from eval.compare import compare_species_performance

# Compare metrics across species
comparison = compare_species_performance(
    species_list=['mouse', 'rat', 'nmr'],
    metric='f1_score'
)

# Generate comparison report
generate_cross_species_report(comparison, 'outputs/reports/')
```

## 🔧 Usage Examples

### Single Species Pipeline

```bash
# Full pipeline for mouse
bash scripts/run_pipeline.sh --species mouse --stage all

# Or run stages individually with species flag
bash scripts/run_ingest.sh --species mouse
bash scripts/run_preprocess.sh --species mouse
bash scripts/run_train.sh --species mouse --epochs 50 --batch-size 32
bash scripts/run_infer.sh --species mouse
bash scripts/run_postprocess_count.sh --species mouse
bash scripts/run_eval_report.sh --species mouse
```

### Multi-Species Analysis

```bash
# Process multiple species
bash scripts/run_multi_species.sh --species mouse,rat,nmr --parallel

# Compare species
python explore/01_species_comparison.py \
  --species mouse,rat,nmr \
  --metric follicle_counts,morphology \
  --output outputs/figures/species_comparison.png
```

### Transfer Learning

```bash
# Train on mouse (large dataset)
bash scripts/run_train.sh --species mouse --save-as mouse_base

# Fine-tune on rat (smaller dataset)
bash scripts/run_train.sh \
  --species rat \
  --pretrained outputs/models/mouse_base/best_model.pth \
  --freeze-layers 3 \
  --epochs 20
```

### QuPath Workflow

```bash
# 1. Export annotations from QuPath (GeoJSON format)
# File > Export > Export as GeoJSON

# 2. Import to pipeline
python run/import_qupath_annotations.py \
  --species mouse \
  --annotation-dir data/annotations/qupath/mouse/

# 3. Train model
bash scripts/run_train.sh --species mouse

# 4. Export predictions to QuPath
python run/export_to_qupath.py \
  --species mouse \
  --predictions outputs/predictions/mouse/ \
  --output data/annotations/qupath/mouse/predictions.geojson

# 5. Import predictions in QuPath
# File > Import > Import as GeoJSON
```

## 📁 Configuration System

### Species-Specific Configs (`configs/species/*.yaml`)

Each species has a config file with:

```yaml
# configs/species/mouse.yaml
species:
  code: "mouse"
  scientific_name: "Mus musculus"
  mother_id: "M-musculus"

morphology:
  ovary_size_mm: [2, 4]
  typical_cycle_days: "4-5"

follicles:
  types: [primordial, primary, secondary, antral]
  size_ranges_um:
    primordial: [15, 25]
    primary: [25, 40]
    secondary: [40, 150]
    antral: [150, 400]

preprocessing:
  tile_size: 256
  normalization: "standardize"

model:
  num_classes: 5
  recommended_architecture: "resnet34"
```

### Global Config Files

- `dataset.yaml` - MOTHER database settings, paths
- `preprocess.yaml` - Default preprocessing parameters
- `train.yaml` - Training hyperparameters
- `infer.yaml` - Inference settings
- `eval.yaml` - Evaluation metrics
- `qupath.yaml` - QuPath integration settings

### Config Hierarchy

1. Species-specific config (highest priority)
2. Command-line arguments
3. Global config files
4. Default values (lowest priority)

## 🔬 QuPath Integration Details

### Annotation Export from QuPath

**Groovy Script** (run in QuPath):
```groovy
// annotations/qupath_scripts/export_annotations.groovy
def project = getProject()
def imageData = getCurrentImageData()
def hierarchy = imageData.getHierarchy()

def annotations = hierarchy.getAnnotationObjects()

// Export as GeoJSON
def path = buildFilePath(PROJECT_BASE_DIR, 'annotations.geojson')
exportObjectsToGeoJson(annotations, path, "FEATURE_COLLECTION")
```

**Python Import:**
```python
from src.qupath.import_annot import import_qupath_geojson

annotations_df = import_qupath_geojson(
    'data/annotations/mouse/slide_001.geojson',
    species='mouse'
)

# Annotations are automatically mapped to tiles
tile_labels = map_annotations_to_tiles(
    annotations_df,
    tiles_manifest,
    species_info
)
```

### Prediction Export to QuPath

```python
from src.qupath.export import create_qupath_detections

# Convert predictions to QuPath format
qupath_objects = create_qupath_detections(
    predictions_df,
    classification_map={
        0: 'Background',
        1: 'Primordial',
        2: 'Primary',
        3: 'Secondary',
        4: 'Antral'
    }
)

# Export as GeoJSON
export_to_geojson(
    qupath_objects,
    'outputs/qupath/mouse_predictions.geojson'
)
```

**Import in QuPath:**
```groovy
// File > Import > Import as GeoJSON
def path = '/path/to/predictions.geojson'
def objects = importObjectsFromGeoJson(path)
addObjects(objects)
fireHierarchyUpdate()
```

## 🐳 Docker Usage

### Build Image

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libvips \
    openslide-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY environment/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

ENTRYPOINT ["bash", "scripts/run_pipeline.sh"]
```

### Run Container

```bash
# Build
docker build -t rodent-follicle-ml .

# Run for single species
docker run -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  rodent-follicle-ml --species mouse

# Run multi-species
docker run -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  rodent-follicle-ml --species mouse,rat,nmr --parallel
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Test specific species
pytest tests/test_species.py::test_mouse_config

# Test QuPath integration
pytest tests/test_qupath.py -v

# Test preprocessing
pytest tests/test_preprocess.py::test_species_normalization
```

## 📊 Example Outputs

### Follicle Count Table
```csv
slide_id,species,primordial,primary,secondary,antral,total
mouse_001,mouse,523,89,34,12,658
mouse_002,mouse,478,76,29,9,592
rat_001,rat,892,145,67,23,1127
```

### Cross-Species Comparison
```
Species Comparison Report
========================
Metric: Follicle Density (per mm²)

Species          Primordial    Primary    Secondary    Antral
--------         ----------    -------    ---------    ------
Mouse            187.5 ± 23    31.8 ± 5   12.1 ± 3     4.3 ± 1
Rat              124.3 ± 18    20.2 ± 4   9.3 ± 2      3.2 ± 1
NMR              203.7 ± 31    42.5 ± 7   18.4 ± 4     1.2 ± 0.5
```

## 🔍 Exploration Scripts

```bash
# Dataset statistics by species
python explore/00_dataset_stats.py --species mouse,rat

# Visualize follicle size distributions
python explore/01_species_comparison.py \
  --plot follicle_sizes \
  --species all

# View random tiles with predictions
python explore/02_view_tiles.py \
  --species mouse \
  --num-samples 20 \
  --with-predictions

# Annotation quality metrics
python explore/03_annotation_quality.py \
  --species mouse \
  --check inter_annotator_agreement

# Model prediction visualization
python explore/04_model_predictions.py \
  --species mouse \
  --model outputs/models/mouse/best_model.pth \
  --slides data/raw/mouse/slide_005.ome.tiff
```

## 🎯 Adding a New Species

### 1. Create Species Entry

```python
# In src/species/registry.py
from src.species.registry import register_custom_species, SpeciesInfo

new_species = SpeciesInfo(
    common_name="Gerbil",
    scientific_name="Meriones unguiculatus",
    species_code="gerbil",
    mother_id="M-unguiculatus",
    typical_follicle_types=["primordial", "primary", "secondary", "antral"],
    follicle_size_ranges={
        "primordial": (18, 28),
        "primary": (28, 45),
        "secondary": (45, 180),
        "antral": (180, 450)
    },
    ovary_size_mm=(3, 5),
    recommended_tile_size=256
)

register_custom_species("gerbil", new_species)
```

### 2. Create Config File

```yaml
# configs/species/gerbil.yaml
species:
  code: "gerbil"
  scientific_name: "Meriones unguiculatus"
  common_name: "Gerbil"
  mother_id: "M-unguiculatus"

# ... rest of config
```

### 3. Add Annotation Notes

```markdown
# annotations/species_notes/gerbil.md
# Gerbil (Meriones unguiculatus) Annotation Notes

## Key Characteristics
- Similar to mouse but slightly larger follicles
- ...
```

### 4. Run Pipeline

```bash
bash scripts/run_pipeline.sh --species gerbil
```

## 🚨 Troubleshooting

### Species Not Found
```bash
$ bash scripts/run_pipeline.sh --species unknown
Error: Species 'unknown' not supported.
Available species: mouse, rat, nmr, guinea_pig, hamster

# Solution: Check species code or add new species
```

### QuPath Import Fails
```bash
# Check GeoJSON format
python -c "from src.qupath.import_annot import validate_geojson; \
           validate_geojson('path/to/file.geojson')"

# Common issues:
# - Incorrect coordinate system
# - Missing classification field
# - Invalid geometry
```

### Cross-Species Model Transfer Poor Performance
```bash
# Try fine-tuning more layers
bash scripts/run_train.sh \
  --species target_species \
  --pretrained source_model.pth \
  --freeze-layers 0  # Train all layers

# Or use species-specific augmentation
# Edit configs/species/target_species.yaml
```

## 📚 Additional Documentation

- `docs/ARCHITECTURE.md` - System architecture and design decisions
- `docs/SPECIES_GUIDE.md` - Detailed species information
- `docs/QUPATH_INTEGRATION.md` - Complete QuPath workflow
- `docs/API.md` - Python API documentation
- `annotations/protocol.md` - Annotation protocol for all species

## 🎓 Best Practices

1. **Start with one species** - Get pipeline working before expanding
2. **Use transfer learning** - Train on data-rich species first
3. **Validate annotations** - Use `explore/03_annotation_quality.py`
4. **Species-specific parameters** - Don't use one-size-fits-all settings
5. **Document decisions** - Update species notes as you learn
6. **Version control configs** - Track configuration changes
7. **Regular checkpoints** - Save models at multiple epochs
8. **Cross-validate** - Use multiple folds for robust evaluation

## 🤝 Contributing

See `CONTRIBUTING.md` for guidelines on:
- Adding new species
- Implementing new models
- Improving preprocessing
- Writing tests
- Documentation standards

---

**Ready to analyze rodent follicles across species?** Start with `bash getting_started.sh`!
