# **MP4 to Text 웹사이트**

Whisper AI 모델을 활용해 MP4 파일을 텍스트로 변환하는 웹사이트를 제작하였습니다.

## **시작하기 전에**

## **1. 설치 및 환경 설정**

### **1.1. FFmpeg 설치**
- **FFmpeg**: 비디오, 오디오, 이미지 인코딩/디코딩 및 멀티플렉싱/디멀티플렉싱을 지원하는 멀티미디어 프레임워크입니다.
    ```bash
    # 리눅스
    sudo apt update && sudo apt install ffmpeg
    
    # MacOS
    brew install ffmpeg
    
    # 윈도우
    choco install ffmpeg
    ```

### **1.2. Pytorch 설치**
- **참고**: 설치 명령어는 사용하고 있는 운영체제 및 환경에 따라 달라질 수 있습니다. 공식 웹사이트를 참고하세요.
- https://pytorch.kr/get-started/locally/
    ```bash
    # 이 명령어는 Linux의 PoPOS 및 Ubuntu 22.10에서 수행되었습니다.
    conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidi 
    ```

### **1.3. Whisper AI 설치**
    
    pip install git+https://github.com/openai/whisper.git 
    

### **1.4. 기타 필요한 파이썬 패키지들 설치**

    pip install -r requirements.txt
    
    # 패키지들 설명
    - `pip`: 파이썬 패키지를 설치, 업그레이드, 제거 도구.
    - `PySocks`: SOCKS 프로토콜 라이브러리.
    - `setuptools`: 패키지 설치 및 배포 라이브러리.
    - `streamlit`: 웹 애플리케이션 개발 도구.
    - `torchaudio`: 오디오 처리 라이브러리.
    - `torchvision`: 컴퓨터 비전 라이브러리.
    - `wheel`: 패키지 배포 형식.
    - `python-docx`: Microsoft Word 문서 작업 라이브러리.

3. **의존성 목록**
    - `subprocess`: 외부 명령 실행.
    - `streamlit`: 웹 앱 생성.
    - `whisper`: 오디오 전사.
    - `os`: 파일 및 디렉토리 작업.
    - `docx`: Microsoft Word 문서 생성.

## **어플리케이션 기능**

### **상수**

- `MODEL_CHOICES`: 사용 가능한 Whisper 모델 크기 (Base < small < medium < large).
- Base < small < medium < large 모델 순으로 더 정확한 결과를 나타내나, 더 많은 시간과 성능을 필요로 합니다

### **함수**

- `create_vtt_file`: 전사된 텍스트를 VTT 파일로 변환.
- `create_docx_file`: 전사된 텍스트를 DOCX 파일로 변환.
- `save_uploaded_file`: 업로드된 파일 저장.
- `format_text`: 텍스트 파일을 읽기 쉽게 변환.
- `convert_video_to_mp3`: 비디오를 MP3 오디오로 변환.
- `transcribe_audio`: Whisper 모델로 오디오 전사.
- `create_text_file`: 비디오 파일로부터 전사된 텍스트 파일 생성.

## **어플리케이션 실행**

1. 터미널에서 해당 폴더 경로로 이동 후 다음 명령어 실행.
    ```bash
    streamlit run streamlit_whisper.py
    ```
    ![웹사이트캡처](https://github.com/ShinYeachan/mp4_to_text_internship/assets/147697028/6274d740-3db2-4b70-9a14-dded45ff6b8a)
2. 원하는 모델 선택.
3. `Browse files` 버튼으로 파일 선택.
4. 400MB의 용량 부족 시, streamlit_whisper 폴더 안에 `.streamlit` 폴더 생성 후 그 안에 `config.toml` 파일 생성. 그리고 해당 내용 입력
    ```bash
    [server]
    maxUploadSize = 원하는 용량(숫자로)
    ```
5. 파일 선택 후 `Transcribe` 클릭하여 전사 시작.
6. 전사 완료 시 텍스트 출력 및 원하는 확장자로 다운로드 가능.
![웹사이트캡처2](https://github.com/ShinYeachan/mp4_to_text_internship/assets/147697028/d95cdfa5-c4b3-4449-b503-7b7b7fa4567a)


## **참조 링크**
[YouTube 참조 동영상](https://www.youtube.com/watch?v=cNLXzXyuzUs&t=1023s)
