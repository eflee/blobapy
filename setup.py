""" Setup file """
from setuptools import setup, find_packages

def get_version():
    with open("blobapy/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])

REQUIREMENTS = [
    "bloop",
    "flask"
]

TEST_REQUIREMENTS = [
    "coverage",
    "flake8",
    "pytest",
    "tox",
]

if __name__ == "__main__":
    setup(
        name="blobapy",
        version=get_version(),
        url="https://github.com/eflee/blobapy",
        packages=find_packages(exclude=("tests")),
        install_requires=REQUIREMENTS,
        tests_require=REQUIREMENTS + TEST_REQUIREMENTS,
    )
