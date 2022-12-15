# setup.py placed at root directory
import pkg_resources
from setuptools import setup

setup(
    name='ds_helpers_lib',
    version='0.1.0',
    author='',
    description="This is a helper's library for data exploration and ML workflows",
    url='',
    keywords='',
    python_requires='>=3.7, <4',
    install_requires=["matplotlib",
                      "pandas==1.3.5",
                      "pytest==7.2.0",
                      "scikit-learn",
                      "seaborn"]
)