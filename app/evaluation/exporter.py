from fastapi import FastAPI
import os
import sys
from app.evaluation.evaluator import ModelEvaluator

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 app 目录
app_dir = os.path.dirname(current_dir)
# 获取项目根目录
project_root = os.path.dirname(app_dir)
# 添加项目根目录到Python路径
sys.path.insert(0, project_root)

app = FastAPI(title="Evalution")

model_evaluator = ModelEvaluator()

@app.get("/metrics")
async def evaluations():
    return model_evaluator.evaluate()

@app.get("/")
async def root():
    return {"message": "Evaluation is running. Try GET /metrics"}