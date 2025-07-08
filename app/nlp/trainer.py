# os_ai_ops/app/nlp/trainer.py
import os
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TrainingArguments, Trainer
from transformers.trainer_utils import get_last_checkpoint
from app.config import config
from app.utils.logger import get_logger


class NLPTrainer:
    def __init__(self, model_name=config.NLP_MODEL_NAME, data_path=config.NLP_TRAINING_DATA_PATH):
        """
        初始化 NLPTrainer 类
        :param model_name: 预训练模型名称
        :param data_path: 训练数据文件路径
        """
        self.logger = get_logger(__name__)
        self.model_name = model_name
        self.data_path = data_path
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.data = self._load_data()

    def _load_data(self):
        """
        加载训练数据
        :return: 训练数据列表，每个元素为字典，包含 'text' 和 'label'
        """
        try:
            # 假设数据文件是一个文本文件，每行格式为 "text\tlabel"
            with open(self.data_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            data = []
            for line in lines:
                text, label = line.strip().split('\t')
                data.append({'text': text, 'label': int(label)})
            return data
        except Exception as e:
            self.logger.error(f"Failed to load data: {e}")
            return []

    def prepare_data(self):
        """
        准备训练数据，包括分词和划分训练集、验证集
        :return: 训练集和验证集的输入和标签
        """
        texts = [d['text'] for d in self.data]
        labels = [d['label'] for d in self.data]
        inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        inputs["labels"] = np.array(labels)
        train_inputs, val_inputs, train_labels, val_labels = train_test_split(
            inputs["input_ids"], inputs["labels"], test_size=0.2, random_state=42
        )
        return train_inputs, val_inputs, train_labels, val_labels

    def train_model(self):
        """
        训练 NLP 模型
        :return: 训练好的 Trainer 对象
        """
        train_inputs, val_inputs, train_labels, val_labels = self.prepare_data()

        # 配置训练参数
        training_args = TrainingArguments(
            output_dir=config.NLP_TRAINING_OUTPUT_DIR,
            num_train_epochs=config.NLP_NUM_TRAIN_EPOCHS,
            per_device_train_batch_size=config.NLP_PER_DEVICE_TRAIN_BATCH_SIZE,
            per_device_eval_batch_size=config.NLP_PER_DEVICE_EVAL_BATCH_SIZE,
            warmup_steps=config.NLP_WARMUP_STEPS,
            weight_decay=config.NLP_WEIGHT_DECAY,
            logging_dir=config.NLP_LOGGING_DIR,
            logging_steps=config.NLP_LOGGING_STEPS,
            evaluation_strategy="steps",
            eval_steps=config.NLP_EVAL_STEPS,
            save_strategy="steps",
            save_steps=config.NLP_SAVE_STEPS,
            load_best_model_at_end=True,
            metric_for_best_model="f1",
        )

        # 创建 Trainer 对象
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_inputs,
            eval_dataset=val_inputs,
            compute_metrics=self._compute_metrics,
        )

        # 检查是否有之前的训练断点
        last_checkpoint = get_last_checkpoint(config.NLP_TRAINING_OUTPUT_DIR)
        if last_checkpoint is not None:
            self.logger.info(f"Resuming training from checkpoint: {last_checkpoint}")
            trainer.train(resume_from_checkpoint=last_checkpoint)
        else:
            self.logger.info("Starting training from scratch")
            trainer.train()

        # 保存最终模型
        trainer.save_model(os.path.join(config.NLP_TRAINING_OUTPUT_DIR, "final_model"))
        self.logger.info("Model saved successfully")

        return trainer

    def _compute_metrics(self, eval_pred):
        """
        计算评估指标，如准确率、精确率、召回率、F1 分数
        :param eval_pred: 评估预测结果
        :return: 评估指标字典
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        accuracy = accuracy_score(labels, predictions)
        precision = precision_score(labels, predictions, average='weighted')
        recall = recall_score(labels, predictions, average='weighted')
        f1 = f1_score(labels, predictions, average='weighted')
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }


