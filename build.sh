#!/bin/bash

echo "Generate Python file for GUI layout."
pyuic4 -xo tcxgen_gui_layout.py tcxgen_gui_layout.ui

echo "Generate binary from Python."
python ~/pyinstaller-2.0/pyinstaller.py tcxgen.spec