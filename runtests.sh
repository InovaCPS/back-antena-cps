#!/usr/bin/env python3
import sys, subprocess

subprocess.call([sys.executable, '-m', 'unittest', 'discover', 'src/main/tests/'])