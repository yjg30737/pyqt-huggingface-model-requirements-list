# pyqt-huggingface-model-requirements-list
이것은 <a href="https://github.com/yjg30737/huggingface_gui/edit/main/README.md">huggingface_gui</a>의 또 다른 버전입니다. 이것은 pc에 있는 모델을 한꺼번에 보여주는 것이 아니라, 사용자가 정의한 일부 모델만 보여줍니다. 모델은 테이블 위젯 내에 위치해 있습니다. 

각 모델 아이템은 설치 여부에 따라 인터페이스가 다릅니다. 모델이 설치되어 있지 않을 시 설치 버튼을 표시하며, 모델이 설치되어 있을 시 제거 버튼을 표시합니다.

일반적인 모델(text generation)과 이미지 텍스트 변환 모델(image2text such as Stable Diffusion) 등 다양한 모델 설치를 지원합니다.

모델이 설치되어 있음으로 표시된다고 해도, 실제 구동이 되지 않을 수 있습니다. 이 때는 제거 후 다시 설치해 주세요. (테이블 속성에서 사이즈를 보고 힌트를 얻을 수도 있습니다)

모델은 병렬 설치가 가능합니다.

현재 설치 과정(프로그레스바 등)은 명령 프롬프트에서만 표시됩니다.

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
