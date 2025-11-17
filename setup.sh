#!/usr/bin/env bash
set -e

echo "Creating virtual environment..."
python -m venv venv
# shellcheck disable=SC1091
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo "Done. To activate the virtualenv run: source venv/bin/activate"
