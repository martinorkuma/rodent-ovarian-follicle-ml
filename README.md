# Rodent Ovarian Follicle ML Pipeline

A **multi-species, production-ready machine learning pipeline** for automated identification, segmentation, and quantification of ovarian follicles in rodent histological images from the MOTHER database.

Note: This is a sub-project of an ongoing team project done by Julian Coles, Martin Orkuma, Pamela Styborski, and Silvia Tenempaguay-Nunez

## Overview

This pipeline supports analysis across multiple rodent species, including:

- **Naked Mole Rat** (Heterocephalus glaber)
- **Mouse** (Mus musculus)
- **Rat** (Rattus norvegicus)
- **Hamster** (Mesocricetus auratus)
- **And other rodent species in the MOTHER database**

### Key Features

- **Multi-species support** with species-specific configurations
- **QuPath integration** for annotation and quality control
- **Flexible ML models** (ResNet, EfficientNet, custom architectures)
- **Transfer learning** across species
- **Comprehensive evaluation** and cross-species comparison
- **Interactive exploration tools** for data analysis
- **Docker support** for reproducibility

## Quick Start

### Prerequisites

- Python 3.10+
- WSL/Linux/macOS

### One-Time Setup

```bash
# Clone or download this repository
git clone git@github.com:martinorkuma/rodent-ovarian-follicle-ml.git
cd rodent-ovarian-follicle-ml

# Run setup (creates venv, installs dependencies, verifies environment)
bash getting_started.sh

# Check environment health
bash scripts/doctor.sh
```

### Run Pipeline

```bash
# Full pipeline for a single species
bash scripts/run_pipeline.sh --species mouse

# Or run individual stages
bash scripts/run_ingest.sh --species rat
bash scripts/run_preprocess.sh --species rat
bash scripts/run_train.sh --species rat
bash scripts/run_infer.sh --species rat
bash scripts/run_postprocess_count.sh --species rat
bash scripts/run_eval_report.sh --species rat

# Multi-species comparison
bash scripts/run_multi_species.sh --species mouse,rat,nmr
```

## Project Structure

```text
rodent-ovarian-follicle-ml/
├── README.md                     # This file
├── CONTRIBUTING.md               # Contribution guidelines
├── getting_started.sh            # One-command setup
├── .gitignore                    
│
├── configs/                     # Configuration files
│   ├── species/                 # Species-specific configs
│   │   ├── mouse.yaml           # M. musculus settings
│   │   ├── rat.yaml             # R. norvegicus settings
│   │   └── nmr.yaml             # H. glaber settings
│   ├── dataset.yaml             # Global dataset settings
│   ├── preprocess.yaml          # Tiling and normalization
│   ├── train.yaml               # Model and training config
│   ├── infer.yaml               # Inference settings
│   ├── eval.yaml                # Evaluation metrics
│   └── qupath.yaml              # QuPath integration settings
│
├── data/                         # Data directory (gitignored)
│   ├── raw/                     # Raw MOTHER downloads
│   │   ├── mouse/               # Species subdirectories
│   │   ├── rat/
│   │   └── nmr/
│   ├── interim/                 # Processed tiles
│   └── processed/               # ML-ready data
│
├── annotations/                  # Annotation resources
│   ├── protocol.md              # Standard annotation protocol
│   ├── species_notes/           # Species-specific notes
│   │   ├── mouse.md
│   │   ├── rat.md
│   │   └── nmr.md
│   ├── labelmap.json            # Universal follicle classes
│   ├── gold_set/                # Ground truth annotations
│   └── qupath_scripts/          # QuPath groovy scripts
│       ├── export_annotations.groovy
│       └── import_predictions.groovy
│
├── outputs/                      # Generated outputs (gitignored)
│   ├── logs/                    # Execution logs
│   ├── models/                  # Trained models
│   ├── predictions/             # Inference results
│   ├── metrics/                 # Performance metrics
│   ├── figures/                 # Plots and visualizations
│   └── reports/                 # HTML/PDF reports
│
├── src/                         # Source code library
│   ├── ingest/                  # Data acquisition
│   │   ├── ingest.py            # MOTHER database download
│   │   └── mother_api.py        # MOTHER API wrapper
│   ├── preprocess/              # Preprocessing
│   │   ├── preprocess.py        # Tiling and normalization
│   │   ├── stain_norm.py        # Advanced stain normalization
│   │   └── augmentation.py      # Data augmentation
│   ├── train/                   # Training
│   │   ├── train.py             # Training loop
│   │   ├── models.py            # Model architectures
│   │   ├── losses.py            # Loss functions
│   │   └── callbacks.py         # Training callbacks
│   ├── infer/                   # Inference
│   │   ├── infer.py             # Batch inference
│   │   └── ensemble.py          # Model ensembling
│   ├── postprocess/             # Post-processing
│   │   ├── count.py             # Follicle counting
│   │   ├── spatial.py           # Spatial analysis
│   │   └── statistics.py        # Statistical summaries
│   ├── eval/                    # Evaluation
│   │   ├── evaluate.py          # Metrics computation
│   │   ├── visualize.py         # Visualization
│   │   └── compare.py           # Cross-species comparison
│   ├── qupath/                  # QuPath integration
│   │   ├── export.py            # Export to QuPath
│   │   ├── import_annot.py      # Import annotations
│   │   └── groovy_bridge.py     # Python-Groovy bridge
│   ├── species/                 # Species-specific utilities
│   │   ├── registry.py          # Species registry
│   │   ├── morphology.py        # Species morphology
│   │   └── validators.py        # Species validators
│   └── utils/                   # Utilities
│       ├── config.py            # Configuration management
│       ├── paths.py             # Path resolution
│       ├── logging.py           # Logging utilities
│       ├── seed.py              # Reproducibility
│       ├── io.py                # I/O operations
│       └── validation.py        # Data validation
│
├── run/                         # Execution entry points
│   ├── ingest.py
│   ├── preprocess.py
│   ├── train.py
│   ├── infer.py
│   ├── postprocess_count.py
│   ├── eval_report.py
│   └── multi_species_compare.py
│
├── explore/                      # Exploration scripts
│   ├── 00_dataset_stats.py
│   ├── 01_species_comparison.py
│   ├── 02_view_tiles.py
│   ├── 03_annotation_quality.py
│   ├── 04_model_predictions.py
│   └── 05_cross_species_analysis.py
│
├── scripts/                      # Shell scripts
│   ├── env.sh                   # Environment helpers
│   ├── doctor.sh                # System check
│   ├── run_stage.sh             # Stage runner template
│   ├── run_ingest.sh
│   ├── run_preprocess.sh
│   ├── run_train.sh
│   ├── run_infer.sh
│   ├── run_postprocess_count.sh
│   ├── run_eval_report.sh
│   ├── run_pipeline.sh          # Full pipeline
│   └── run_multi_species.sh     # Multi-species analysis
│
├── tests/                        # Unit tests
│   ├── test_config.py
│   ├── test_ingest.py
│   ├── test_preprocess.py
│   ├── test_species.py
│   └── test_integration.py
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md          # System architecture
│   ├── SPECIES_GUIDE.md         # Species-specific info
│   ├── QUPATH_INTEGRATION.md    # QuPath workflow
│   └── API.md                   # Code API documentation
│
└── environment/
    ├── requirements.txt         # Python dependencies
    ├── requirements-dev.txt     # Development dependencies
    └── Dockerfile              # Docker container

```

## Pipeline Stages

### 1. Ingest

Downloads slides from the MOTHER database for the specified species.

```bash
bash scripts/run_ingest.sh --species mouse
```

### 2. Preprocess

Tiles slides, normalizes staining, and detects tissue regions.

```bash
bash scripts/run_preprocess.sh --species mouse
```

### 3. Train

Trains ML model on annotated tiles.

```bash
bash scripts/run_train.sh --species mouse
```

### 4. Infer

Runs predictions on new slides.

```bash
bash scripts/run_infer.sh --species mouse
```

### 5. Postprocess

Aggregates predictions, counts follicles by type.

```bash
bash scripts/run_postprocess_count.sh --species mouse
```

### 6. Evaluate

Computes metrics, generates reports, and visualizations.

```bash
bash scripts/run_eval_report.sh --species mouse
```

## QuPath Integration

This pipeline integrates tightly with QuPath for annotation and visualization:

1. **Export annotations from QuPath** → Import to pipeline
2. **Train model** using QuPath annotations
3. **Export predictions** → Visualize in QuPath

See [QuPath Integration Guide](docs/QUPATH_INTEGRATION.md) for details.

## Configuration

All pipeline behavior is controlled via YAML files in `configs/`:

- **Species-specific** (`configs/species/*.yaml`): Morphology, expected follicle types
- **Dataset** (`configs/dataset.yaml`): Paths, splits, MOTHER settings
- **Preprocessing** (`configs/preprocess.yaml`): Tile size, normalization
- **Training** (`configs/train.yaml`): Model, hyperparameters, augmentation
- **Inference** (`configs/infer.yaml`): Batch size, thresholds
- **Evaluation** (`configs/eval.yaml`): Metrics, visualizations

## Multi-Species Analysis

Compare follicle characteristics across species:

```bash
# Run pipeline for multiple species
bash scripts/run_multi_species.sh --species mouse,rat,nmr

# Generate comparative report
python explore/01_species_comparison.py --species mouse,rat,nmr
```

## Transfer Learning

Train on one species, fine-tune on another:

```bash
# Train base model on mouse
bash scripts/run_train.sh --species mouse

# Fine-tune on rat
bash scripts/run_train.sh --species rat --pretrained outputs/models/mouse/best_model.pth
```

## Adding New Species

1. Create species config: `configs/species/new_species.yaml`
2. Add morphology notes: `annotations/species_notes/new_species.md`
3. Run pipeline: `bash scripts/run_pipeline.sh --species new_species`

See [Species Guide](docs/SPECIES_GUIDE.md) for details.

## Development

```bash
# Install dev dependencies
pip install -r environment/requirements-dev.txt

# Run tests
pytest tests/

# Run specific test
pytest tests/test_species.py -v

# Format code
black src/ run/ tests/
flake8 src/ run/ tests/
```

## Docker

```bash
# Build image
docker build -t rodent-follicle-ml .

# Run container
docker run -v $(pwd)/data:/app/data rodent-follicle-ml \
  bash scripts/run_pipeline.sh --species mouse
```

## Citation

If you use this pipeline, please cite:

```bibtex
@software{rodent_follicle_ml,
  title = {Rodent Ovarian Follicle ML Pipeline},
  author = {Julian Coles, Martin Orkuma, Pamela Styborski, and Silvia Tenempaguay-Nunez},
  year = {2026},
  url = {https://github.com/martinorkuma/rodent-ovarian-follicle-ml}
}
```

And the MOTHER database:

```bibtex
@article{watanabe2024mother,
  title={Overview of the Multispecies Ovary Tissue Histology Electronic Repository (MOTHER)},
  author={Watanabe, Kelley H and others},
  journal={Biology of Reproduction},
  year={2024}
}
```

## License

MIT License - see LICENSE file

## Support

- **Issues**: Open a GitHub issue
- **Discussions**: GitHub Discussions
- **Email**: <martin.t.orkuma@gmail.com>

## Acknowledgments

- MOTHER Database team
- Arizona State University
- Julian Coles, Martin Orkuma, Pamela Styborski, and Silvia Tenempaguay-Nunez

---
