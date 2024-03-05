model = None

def load_model(model_path: str):
    import joblib
    
    global model
    model = joblib.load(model_path)

def get_model():
    global model    # 앱이 실행될 때 load_model에서 만들어진 global 변수 model을 가져옴
    return model