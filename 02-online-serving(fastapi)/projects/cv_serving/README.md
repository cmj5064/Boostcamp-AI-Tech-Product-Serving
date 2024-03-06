# CV Serving Example through Web Single Pattern

CV 모델을 Web Single Pattern으로 서빙하는 예제입니다.

## Pre-requisites

- Python >= 3.9
- Poetry >= 1.1.4

## Installation

```bash
poetry install
```

## Run

먼저 `.env` 파일을 생성하고, 아래와 같이 모델 경로를 설정합니다.

```bash
# .env
MODEL_PATH=./model/model.pkl
```

그리고 아래와 같이 실행합니다.

```bash
PYTHONPATH=.
poetry run python main.py
```

## Usage

### Predict

```bash
curl -X POST -F "file=@./example_images/0a101263343a4a60a8dcd94d1fc8e8e253dadf14.jpg" http://localhost:8000/predict
 
{"id":1,"result":4}%
```

### Get all predictions

```bash
curl "http://localhost:8000/predict"

[{"id":1,"result":0},{"id":2,"result":4},{"id":3,"result":3}]
```

### Get a prediction

```bash
curl "http://localhost:8000/predict/1"
{"id":1,"result":0}
```

## Build

```bash
docker build -t web_single_example .
```

## Project Structure

```bash
.
├── .dockerignore    # 도커 이미지 빌드 시 제외할 파일 목록
├── .gitignore       # git에서 제외할 파일 목록
├── Dockerfile       # 도커 이미지 빌드 설정 파일
├── README.md        # 프로젝트 설명 파일
├── __init__.py
├── api.py           # API 엔드포인트 정의 파일
├── config.py        # Config 정의 파일
├── database.py      # 데이터베이스 연결 파일
├── dependencies.py  # 앱 의존성 관련 로직 파일
├── main.py          # 앱 실행 파일
├── model/           # 모델 관련 디렉토리
├── poetry.lock      # Poetry 라이브러리 버전 관리 파일
└── pyproject.toml   # Poetry 프로젝트 설정 파일
```
# 기본과제

## 목표
- 내가 만든 모델을 서빙하는 API 서버를 만들 수 있습니다.

## 요구 사항
- 내가 만든 모델을 서빙하는 API 서버 엔드 포인트를 구현합니다.
- 위 과제 링크에서 TODO를 검색해보시면 구현해야할 함수를 확인할 수 있습니다.

## 고려 사항
- 단순히 모델 출력 결과를 응답하는 것 뿐 아니라, 그 결과를 DB에 저장해야 합니다.

## 더 공부하면 좋을 내용
- FastAPI 공식 문서: https://fastapi.tiangolo.com/
- SQL Model (ORM) 공식 문서: https://sqlmodel.tiangolo.com/

# 심화과제

## 목표
- 기존에 개발했던 ML 서빙 서버에 좀 더 추가된 기능을 넣어봅시다.
- 웹 서버를 지속적으로 운영 하는데 필요한 기본적인 기능을 구현해 봅시다.
  
## 요구 사항
- 모든 엔드포인트에 사용자 인증(Authentication) 로직 추가하기
- 현재 모든 API 엔드포인트에는 별도의 인증 로직이 없으므로, 누구나 요청할 수 있습니다.
- 따라서 우리가 의도하지 않은 사용자가 요청할 수 있고, 이는 정보 유출 및 D-DOS 공격의 근간이 됩니다.
- 따라서 우리가 의도한 사용자만 API를 이용할 수 있도록 인증 로직을 추가해 주세요.
- 예를 들어
  - 요청 헤더 내에 authorization: my_secret_token와 같이 인증 정보를 담아  `POST /predict` 로 요청을 보냅니다. 이 경우, my_secret_token 값이 인증된 값인 경우, 기존처럼 응답에 상태 코드는 200이 되어야 합니다.
  - 만약 my_secret_token 값이 인증된 값이 아니거나, 요청 헤더에 키 값이 존재하지 않는 경우 응답 상태 코드는 401이 되어야 합니다.
- 모든 엔드포인트에 대한 접근 로그를 파일에 쓰기
  - 접근 로그는 운영 중에 누가, 언제 API에 접근했는지 추적하는데 쓰입니다.
  - 현재 모든 API 엔드포인트에 대한 접근 로그 기록은 stdout 으로만 출력되고 있습니다.
  - 따라서 서버가 한 번이라도 종료되면 기존의 모든 로그 기록은 유실되고 맙니다.
  - 서버가 종료 후에도 모든 로그 기록을 볼 수 있도록 로그 파일(output.log)을 저장합니다.
- 부하 테스트(Load Test)를 통해 초당 몇 개의 요청을 처리할 수 있는지 확인하기
  - 내가 만든 API 서버는 초당 몇개의 요청을 처리할 수 있는지(이를 Request Per Second, RPM이라고 부릅니다) 확인해봅시다.
  - 부하테스트 도구로는 Locust를 활용합니다.

## 고려 사항
- 인증 방법은 어떤 것을 구현해도 상관없습니다. 간단한 것부터 구현해보세요. 위 예시 같이 단순히 Header에 Authorization 키와 간단한 값을 - 사용하기를 추천합니다.
- 로거는 기존의 loguru 라이브러리를 활용해보세요.
- 정확한 부하 테스트 성능은, 로컬이 아닌 운영 환경과 동일한 머신 위에서 진행해야 합니다. 정확한 부하 테스트 성능 보다는, 어떻게 부하 테스트 코드를 작성할 수 있는지 이번 기회에 학습해보세요!

## 더 공부하면 좋을 내용
- 인증 방법에 어떤 것들이 있는지 살펴보고, 각 장/단점을 알아봅시다.
- 인증 로직을 확장하여, 일반적인 로그인/로그아웃 기능은 어떻게 구현할 수 있을지 생각해 봅시다.
- 로그를 남기는 방법 역시 파일 외에 어떤 방법이 있나 살펴보고, 어떤 환경에서 어떤 로깅 방식을 채택하면 좋을지 생각해보세요.
- 실제 현업에서는 부하 테스트 말고도, 앱의 시간별 상태를 나타내는 “메트릭" 이라는 개념이 있습니다. ML 서빙 서버에서는 어떤 메트릭을 남기고 활용할 수 있을지 한번 찾아보세요!