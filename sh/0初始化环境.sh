#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
PROJECT_DIR="$(realpath "${BASEDIR}/..")"
PY_PROJECT_DIR="${PROJECT_DIR}/data-calc"
DATA_PROJECT_DIR="${PROJECT_DIR}/proto"

echo "初始化 python 环境"
cd "${PY_PROJECT_DIR}" || exit
sh ./use_venv.sh

echo "初始化 node 环境"
cd "${DATA_PROJECT_DIR}" || exit
yarn install

echo "初始化完成"
