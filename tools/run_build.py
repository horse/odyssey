#!/usr/bin/env python3

from tools import build_source
from tools.source_repairs import apply_source_patches


build_source.apply_source_patches = apply_source_patches
build_source.main()
