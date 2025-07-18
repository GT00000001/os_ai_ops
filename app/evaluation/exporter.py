from fastapi import FastAPI
import os
import sys
from app.evaluation.evaluator import ModelEvaluator
from app.config import Config


# 添加项目根目录到Python路径
sys.path.insert(0, Config.BASE_DIR)

app = FastAPI(title="Evalution")

model_evaluator = ModelEvaluator()

@app.get("/metrics")
async def evaluations():
    return model_evaluator.evaluate()

@app.get("/")
async def root():
    return {"message": "Evaluation is running. Try GET /metrics"}