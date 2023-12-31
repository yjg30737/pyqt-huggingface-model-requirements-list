from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name='pyqt-huggingface-model-requirements-list',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'src': ['hf-logo.svg']},
    description='Python desktop app implementation of "installation screen" of required HuggingFace model list',
    url='https://github.com/yjg30737/pyqt-huggingface-model-requirements-list.git',
    long_description_content_type='text/markdown',
    long_description=long_description,
    install_requires=[
        'PyQt5>=5.14',
        'huggingface_hub',
        'transformers',
        'diffusers'
    ]
)