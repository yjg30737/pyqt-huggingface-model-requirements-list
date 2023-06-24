# pyqt-huggingface-model-requirements-list

[![](https://img.shields.io/badge/korean-readme-green)](https://github.com/yjg30737/pyqt-huggingface-model-requirements-list/blob/main/README.kr.md)
  
This is another version of <a href="https://github.com/yjg30737/huggingface_gui/edit/main/README.md">huggingface_gui</a>. Instead of displaying all the models on the PC at once, it only shows the user-defined subset of models. The models are located within a table widget.

Each model item has a different interface depending on its installation status. If the model is not installed, it displays an install button, and if the model is installed, it displays a remove button.

It supports the installation of various models such as general text generation and image-to-text conversion models (e.g., Stable Diffusion).

Even if a model is marked as installed, it may not actually be functional. In that case, please remove and reinstall it (you can check the size in the table attributes for hints).

Models can be installed in parallel.

The current installation process (progress bar, etc.) is only displayed in the command prompt.

## Requirements
* PyQt5 >= 5.14
* huggingface_hub
* transformers
* diffusers

## How to Run
1. git clone ~
2. pip intsall -r requirements.txt
3. set desired models to show
```python
# in main.py
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # set desired model to show
    
    # The dictionary should be defined as follows:
    # { "id": "model_name", "type": "type" }
    # The "type" should be written as either "General" or "Stable Diffusion." If the type is not specified, it will be initialized as "General."
    # I couldn't find a definitive way to extract the type based on the model name from HuggingFace, so we had no choice but to do it as follows.
    
    model_subset = [{'id': 'runwayml/stable-diffusion-v1-5', 'type': 'Stable Diffusion'},
     {'id': 'CompVis/stable-diffusion-v1-4', 'type': 'Stable Diffusion'},
     {'id': 'deepset/tinyroberta-squad2'},
     {'id': 'prompthero/openjourney', 'type': 'Stable Diffusion'},
     {'id': 'SG161222/Realistic_Vision_V1.4', 'type': 'Stable Diffusion'},
     {'id': 'stabilityai/stable-diffusion-2-1-base', 'type': 'Stable Diffusion'},
     {'id': 'tuner007/pegasus_paraphrase'}]

    w = HuggingFaceModelRequirementsWidget(model_subset)
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec())
```
4. python main.py

## Preview
![image](https://github.com/yjg30737/pyqt-huggingface-model-requirements-list/assets/55078043/d13bfed5-f921-4f37-9716-bd946649ba58)
