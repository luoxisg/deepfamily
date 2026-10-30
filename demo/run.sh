#!/bin/sh
# DeepFamily developer demo: tests + CLI acceptance run.
cd "$(dirname "$0")" || exit 1
python3 -m unittest discover -s tests -v
python3 -m demo.cli
