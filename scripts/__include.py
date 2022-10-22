import os
import sys


def __include():
    PROJECT_PATH = os.getcwd()
    SOURCE_PATH = os.path.join(PROJECT_PATH, "src")
    sys.path.append(SOURCE_PATH)

    print("imported src")


__include()
