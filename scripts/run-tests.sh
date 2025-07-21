#bin/bash
# This project uses the "coverage" module to run tests and measure code coverage. Read more at https://coverage.readthedocs.io/en/7.9.2/

set -eu

PROJECT_DIR=$PWD
VENV_DIR="python3-virtualenv"


echo "=== setting up testing environment==="

if [ ! -d "$VENV_DIR" ]; then
    python -m venv "$VENV_DIR"
fi
source $VENV_DIR/bin/activate && pip install -r requirements.txt


echo "=== running unittest tests==="

coverage run -m unittest discover -v tests/
echo "~~ unittest coverage ~~"
unittest_coverage=$(coverage report)
echo "$unittest_coverage"


echo "=== running pytest tests==="

coverage run -m pytest
echo "~~ pytest coverage ~~"
pytest_coverage=$(coverage report)
echo "$pytest_coverage"


echo "=== coverage recap ==="

echo "unittest coverage:"
echo "$unittest_coverage" | awk 'END{print $4}'

echo "pytest coverage:"
echo "$pytest_coverage" | awk 'END{print $4}'
