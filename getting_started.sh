#!/bin/bash
# Comprehensive setup script for Rodent Ovarian Follicle ML Pipeline

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "================================================================"
echo "  Rodent Ovarian Follicle ML Pipeline - Setup"
echo "================================================================"
echo -e "${NC}"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.10+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo -e "${YELLOW}  Virtual environment already exists, recreating...${NC}"
    rm -rf .venv
fi

python3 -m venv .venv
echo -e "${GREEN}✓ Virtual environment created${NC}"

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --quiet --upgrade pip setuptools wheel
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
echo -e "  This may take a few minutes..."

if [ -f "environment/requirements.txt" ]; then
    pip install --quiet -r environment/requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    exit 1
fi

# Create directory structure
echo -e "${YELLOW}Creating directory structure...${NC}"

# Data directories
mkdir -p data/raw/{mouse,rat,nmr,guinea_pig,hamster}
mkdir -p data/interim/tiles
mkdir -p data/processed

# Output directories
mkdir -p outputs/{logs,models,predictions,metrics,figures,reports}

# Annotation directories
mkdir -p annotations/{gold_set,qupath_scripts,species_notes}

# Create .gitkeep files
find data outputs annotations -type d -exec touch {}/.gitkeep \;

echo -e "${GREEN}✓ Directory structure created${NC}"

# Make scripts executable
echo -e "${YELLOW}Making scripts executable...${NC}"
chmod +x scripts/*.sh
chmod +x run/*.py
echo -e "${GREEN}✓ Scripts are executable${NC}"

# Verify installation
echo -e "${YELLOW}Verifying installation...${NC}"

python3 -c "
import sys
import importlib

required = [
    'torch', 'torchvision', 'numpy', 'pandas', 'sklearn',
    'PIL', 'yaml', 'tqdm', 'matplotlib', 'seaborn'
]

missing = []
for package in required:
    try:
        if package == 'sklearn':
            importlib.import_module('sklearn')
        elif package == 'PIL':
            importlib.import_module('PIL')
        else:
            importlib.import_module(package)
    except ImportError:
        missing.append(package)

if missing:
    print(f'Missing packages: {missing}')
    sys.exit(1)
else:
    print('✓ All required packages installed')
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Installation verified${NC}"
else
    echo -e "${RED}✗ Some packages failed to install${NC}"
    exit 1
fi

# Create sample config if doesn't exist
if [ ! -f "configs/dataset.yaml" ]; then
    echo -e "${YELLOW}Creating sample configuration...${NC}"
    cat > configs/dataset.yaml << 'EOF'
# Global dataset configuration

# MOTHER database settings
mother_database:
  base_url: "https://mother-db.org/downloads/"
  download_xml: true
  verify_checksums: false

# Data paths
paths:
  raw_data: "data/raw"
  interim_data: "data/interim"
  processed_data: "data/processed"
  annotations: "annotations"

# Train/validation/test split
split_ratios:
  train: 0.7
  val: 0.15
  test: 0.15

# Random seed for reproducibility
seed: 42

# Processing options
processing:
  num_workers: 4
  batch_processing: true
EOF
    echo -e "${GREEN}✓ Sample configuration created${NC}"
fi

# Print success message
echo ""
echo -e "${GREEN}"
echo "================================================================"
echo "  ✓ Setup Complete!"
echo "================================================================"
echo -e "${NC}"

echo -e "Next steps:"
echo ""
echo -e "1. ${YELLOW}Activate the environment:${NC}"
echo -e "   ${BLUE}source .venv/bin/activate${NC}"
echo ""
echo -e "2. ${YELLOW}Check system health:${NC}"
echo -e "   ${BLUE}bash scripts/doctor.sh${NC}"
echo ""
echo -e "3. ${YELLOW}Run pipeline for a species:${NC}"
echo -e "   ${BLUE}bash scripts/run_pipeline.sh --species mouse${NC}"
echo ""
echo -e "4. ${YELLOW}Or run individual stages:${NC}"
echo -e "   ${BLUE}bash scripts/run_ingest.sh --species mouse${NC}"
echo -e "   ${BLUE}bash scripts/run_preprocess.sh --species mouse${NC}"
echo -e "   ${BLUE}bash scripts/run_train.sh --species mouse${NC}"
echo ""
echo -e "5. ${YELLOW}For multi-species analysis:${NC}"
echo -e "   ${BLUE}bash scripts/run_pipeline.sh --species mouse,rat,nmr --parallel${NC}"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo -e "  • README.md - Overview and quick start"
echo -e "  • IMPLEMENTATION_GUIDE.md - Detailed usage guide"
echo -e "  • docs/ - Additional documentation"
echo ""
echo -e "${YELLOW}Supported species:${NC} mouse, rat, nmr, guinea_pig, hamster"
echo ""
echo -e "${GREEN}Happy follicle counting! 🔬${NC}"
echo ""
