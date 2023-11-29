#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
PROJECT_DIR="$(realpath "${BASEDIR}/..")"
PY_PROJECT_DIR="${PROJECT_DIR}/data-calc"
DATA_PROJECT_DIR="${PROJECT_DIR}/proto"

PYTHON_SCRIPT_TO_RUN=$PY_PROJECT_DIR/scripts/char_exp/char_rank_exp_calc.py

VENV_DIR=$PY_PROJECT_DIR"/venv"
source $VENV_DIR/bin/activate

export PYTHONPATH=$PYTHONPATH:$PY_PROJECT_DIR
export CSV_DIR=$DATA_PROJECT_DIR/csv

cd "${PY_PROJECT_DIR}" || exit
python $PYTHON_SCRIPT_TO_RUN
