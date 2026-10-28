"""Test-collection fix only: make the repo root importable so `pytest`
collects without PYTHONPATH=. This file changes no pipeline behaviour;
it only puts the directory containing the `analyst` package on sys.path,
the same layout the scanner repo already uses inside each test file."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
