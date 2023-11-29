#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
PY_PROJECT_DIR="$(realpath "${BASEDIR}")"

cd $PY_PROJECT_DIR || exit

GLOBAL_PYTHON=$(which python3.10)
if [ -z "$GLOBAL_PYTHON" ]; then
    GLOBAL_PYTHON=$(which python3)
fi
if [ -z "$GLOBAL_PYTHON" ]; then
    GLOBAL_PYTHON=$(which python)
fi

echo "Using global python: $GLOBAL_PYTHON"

VENV_DIR=$PY_PROJECT_DIR"/venv"
ACTIVATE=$VENV_DIR"/bin/activate"

if [ ! -d $VENV_DIR ]; then
    # Take action if $VENV_DIR exists. #
    mkdir $VENV_DIR
    $GLOBAL_PYTHON -m venv $VENV_DIR
else
    echo "Virtual environment folder already exists"
fi

if grep -Faq "$VENV_DIR" $ACTIVATE; then
    # code if found
    echo "Virtual environment is ready to use"
else
    # code if not found
    echo "Virtual environment is incorrect, recreating..."

    rm -rf $VENV_DIR

    # Take action if $VENV_DIR exists. #
    mkdir $VENV_DIR
    $GLOBAL_PYTHON -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "To activate the virtual environment, Please run the following command:"
echo "      source $VENV_DIR/bin/activate"
echo
