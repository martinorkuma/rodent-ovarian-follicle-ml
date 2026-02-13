#!/bin/bash
# System health check script

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "System Health Check"
echo "=========================================="
echo ""

# Check Python
echo -n "Python 3: "
if command -v python3 &> /dev/null; then
    VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $VERSION${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
fi

# Check pip
echo -n "pip: "
if command -v pip &> /dev/null; then
    VERSION=$(pip --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ version $VERSION${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
fi

# Check virtual environment
echo -n "Virtual environment: "
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${YELLOW}! Not found - run getting_started.sh${NC}"
fi

# Check if venv is activated
echo -n "Environment activated: "
if [ -n "$VIRTUAL_ENV" ]; then
    echo -e "${GREEN}✓ Yes${NC}"
else
    echo -e "${YELLOW}! No - run: source .venv/bin/activate${NC}"
fi

echo ""
echo "Required Directories:"
for dir in configs data outputs scripts run src; do
    echo -n "  $dir/: "
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
    fi
done

echo ""
echo "Configuration Files:"
for file in configs/dataset.yaml configs/train.yaml configs/preprocess.yaml; do
    echo -n "  $file: "
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}! Missing${NC}"
    fi
done

echo ""
echo "Python Packages:"
if [ -n "$VIRTUAL_ENV" ]; then
    python3 -c "
import sys
packages = {
    'torch': 'PyTorch',
    'torchvision': 'TorchVision',
    'numpy': 'NumPy',
    'pandas': 'Pandas',
    'sklearn': 'scikit-learn',
    'PIL': 'Pillow',
    'yaml': 'PyYAML',
    'shapely': 'Shapely'
}

for module, name in packages.items():
    try:
        if module == 'sklearn':
            __import__('sklearn')
        elif module == 'PIL':
            __import__('PIL')
        else:
            __import__(module)
        print(f'  {name}: \033[0;32m✓\033[0m')
    except ImportError:
        print(f'  {name}: \033[0;31m✗\033[0m')
"
else
    echo -e "${YELLOW}  Activate venv to check packages${NC}"
fi

echo ""
echo "=========================================="
echo "Health Check Complete"
echo "=========================================="
