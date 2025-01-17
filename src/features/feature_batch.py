"""
Feature batch runner
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import fire

from src.features.registry.feature_registry import FeatureRegistry
from src.features.registry.feature_store import LocalFeatureStore

def runner():
    fire.Fire(FeatureRegistry(LocalFeatureStore(FeatureRegistry.registry_dir)))

if __name__ == "__main__":
    runner()
