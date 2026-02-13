#!/bin/bash
# Enhanced pipeline runner with multi-species support

set -e

# Default values
SPECIES=""
STAGE="all"
PARALLEL=false
VERBOSE=false
DRY_RUN=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Run the rodent ovarian follicle ML pipeline for one or more species.

OPTIONS:
    -s, --species SPECIES    Species to process (required)
                            Examples: mouse, rat, nmr
                            Multiple: mouse,rat,nmr
    -t, --stage STAGE       Pipeline stage to run (default: all)
                            Options: all, ingest, preprocess, train, infer, postprocess, eval
    -p, --parallel          Run multiple species in parallel
    -v, --verbose           Enable verbose output
    -d, --dry-run           Show commands without executing
    -h, --help              Show this help message

EXAMPLES:
    # Run full pipeline for mouse
    $0 --species mouse

    # Run only training for rat
    $0 --species rat --stage train

    # Process multiple species in parallel
    $0 --species mouse,rat,nmr --parallel

    # Dry run to see what would be executed
    $0 --species mouse --dry-run

SUPPORTED SPECIES:
    mouse       - Mus musculus
    rat         - Rattus norvegicus
    nmr         - Heterocephalus glaber (Naked Mole Rat)
    guinea_pig  - Cavia porcellus
    hamster     - Mesocricetus auratus

EOF
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--species)
            SPECIES="$2"
            shift 2
            ;;
        -t|--stage)
            STAGE="$2"
            shift 2
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}"
            usage
            ;;
    esac
done

# Check required arguments
if [ -z "$SPECIES" ]; then
    echo -e "${RED}Error: Species is required${NC}"
    usage
fi

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "${GREEN}✓ Activated virtual environment${NC}"
fi

# Function to run a stage
run_stage() {
    local species=$1
    local stage=$2
    
    echo -e "${YELLOW}Running $stage for $species...${NC}"
    
    local cmd="bash scripts/run_${stage}.sh --species $species"
    
    if [ "$VERBOSE" = true ]; then
        cmd="$cmd --verbose"
    fi
    
    if [ "$DRY_RUN" = true ]; then
        echo "  Would run: $cmd"
        return 0
    fi
    
    if $cmd; then
        echo -e "${GREEN}✓ $stage completed for $species${NC}"
        return 0
    else
        echo -e "${RED}✗ $stage failed for $species${NC}"
        return 1
    fi
}

# Function to run full pipeline for one species
run_species_pipeline() {
    local species=$1
    
    echo ""
    echo "=========================================="
    echo "Processing Species: $species"
    echo "=========================================="
    
    if [ "$STAGE" = "all" ]; then
        # Run all stages
        run_stage "$species" "ingest" || return 1
        run_stage "$species" "preprocess" || return 1
        run_stage "$species" "train" || return 1
        run_stage "$species" "infer" || return 1
        run_stage "$species" "postprocess_count" || return 1
        run_stage "$species" "eval_report" || return 1
    else
        # Run specific stage
        run_stage "$species" "$STAGE" || return 1
    fi
    
    echo -e "${GREEN}✓ Pipeline completed for $species${NC}"
}

# Main execution
echo "=========================================="
echo "Rodent Ovarian Follicle ML Pipeline"
echo "=========================================="
echo "Species: $SPECIES"
echo "Stage: $STAGE"
echo "Parallel: $PARALLEL"
echo "=========================================="
echo ""

# Split species if comma-separated
IFS=',' read -ra SPECIES_ARRAY <<< "$SPECIES"

if [ ${#SPECIES_ARRAY[@]} -eq 1 ]; then
    # Single species
    run_species_pipeline "$SPECIES"
    exit_code=$?
    
elif [ "$PARALLEL" = true ]; then
    # Multiple species in parallel
    echo "Running ${#SPECIES_ARRAY[@]} species in parallel..."
    
    pids=()
    for species in "${SPECIES_ARRAY[@]}"; do
        run_species_pipeline "$species" &
        pids+=($!)
    done
    
    # Wait for all processes
    exit_code=0
    for pid in "${pids[@]}"; do
        if ! wait $pid; then
            exit_code=1
        fi
    done
    
else
    # Multiple species sequentially
    exit_code=0
    for species in "${SPECIES_ARRAY[@]}"; do
        if ! run_species_pipeline "$species"; then
            exit_code=1
            break
        fi
    done
fi

echo ""
echo "=========================================="
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}✓ All pipelines completed successfully${NC}"
else
    echo -e "${RED}✗ Some pipelines failed${NC}"
fi
echo "=========================================="

exit $exit_code
