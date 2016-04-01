#!/usr/bin/env python

# Downloads and compiles linenoise.

from __future__ import print_function

import os
import os.path
import platform
import shutil
import subprocess
import sys
from runner import *

LIB_LINENOISE_PATCH = "linenoise.patch"
LIB_LINENOISE_DIR = "deps/linenoise"

def download_linenoise():
  """Clones linenoise into deps/linenoise and checks out the right version."""

  # Delete it if already there so we ensure we get the correct version if the
  # version number in this script changes.
  if os.path.isdir(LIB_LINENOISE_DIR):
    print("Cleaning output directory...")
    remove_dir(LIB_LINENOISE_DIR)

  ensure_dir("deps")

  print("Cloning linenoise...")
  run([
    "git", "clone", "--quiet", "--depth=1",
    "https://github.com/antirez/linenoise.git",
    LIB_LINENOISE_DIR
  ])

  print("Applying patch...")
  run([
    "git", "am", "--quiet",
    "../../util/" + LIB_LINENOISE_PATCH
  ], "deps/linenoise")

def main():
  expect_usage(len(sys.argv) >= 2)

  if sys.argv[1] == "download":
    download_linenoise()
  else:
    expect_usage(false)


def expect_usage(condition):
  if (condition): return

  print("Usage: linenoise.py download")
  sys.exit(1)


main()
