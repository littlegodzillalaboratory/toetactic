#!/usr/bin/bash
set -o nounset

cd ../
. ./.venv/bin/activate
cd examples/

printf "\n\n========================================\n"
printf "Show help guide:\n"
toetactic --help

printf "\n\n========================================\n"
printf "Show version info: toetactic --version\n"
toetactic --version

printf "\n\n========================================\n"
printf "Run command with default config file and default issues file:\n"
toetactic
