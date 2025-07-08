# 实体提取
# 功能：从文本中提取关键实体（如指标类型、应用名称）
# 核心方法：
# extract()：提取实体（如 "CPU"、"MySQL"）
# 技术实现：
# 简单实现：基于正则表达式
# 高级实现：使用命名实体识别（NER）模型

import re
from typing import List, Dict, Any
from app.config import config
from app.utils.logger import get_logger


class EntityExtractor:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.entity_patterns = self._load_entity_patterns()
        self.stopwords = self._load_stopwords()

    def _load_entity_patterns(self) -> Dict[str, List[str]]:
        """加载实体识别模式"""
        return {
            "metric": [
                r"\b(cpu|memory|disk|network|load|uptime)\b",
                r"\b(cpu usage|memory usage|disk space|network traffic)\b"
            ],
            "duration": [
                r"\b(\d+)\s*(seconds?|sec|minutes?|min|hours?|hrs?|days?|d)\b",
                r"\b(last|past)\s+(\d+)\s*(seconds?|sec|minutes?|min|hours?|hrs?|days?|d)\b"
            ],
            "application": [
                r"\b(nginx|apache|mysql|postgres|redis|kafka|zookeeper)\b",
                r"\b(docker|kubernetes|jenkins|gitlab)\b"
            ],
            "severity": [
                r"\b(critical|high|medium|low|warning|error)\b"
            ]
        }

    def _load_stopwords(self) -> List[str]:
        """加载停用词列表"""
        return [
            "the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
            "for", "to", "from", "with", "without", "by", "of", "about"
        ]

    def extract(self, text: str) -> Dict[str, Any]:
        """从文本中提取实体"""
        entities = {}

        # 预处理文本
        cleaned_text = self._preprocess_text(text)

        # 提取各类实体
        for entity_type, patterns in self.entity_patterns.items():
            extracted_entities = self._extract_by_patterns(cleaned_text, patterns)
            if extracted_entities:
                entities[entity_type] = extracted_entities

        # 提取数值
        numbers = self._extract_numbers(cleaned_text)
        if numbers:
            entities["numbers"] = numbers

        return entities

    def _preprocess_text(self, text: str) -> str:
        """预处理文本（小写、去除停用词）"""
        text = text.lower()

        # 去除停用词
        words = text.split()
        filtered_words = [word for word in words if word not in self.stopwords]

        return " ".join(filtered_words)

    def _extract_by_patterns(self, text: str, patterns: List[str]) -> List[str]:
        """使用正则表达式模式提取实体"""
        entities = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # 处理匹配结果（可能是元组或字符串）
                if isinstance(match, tuple):
                    # 取最后一个非空元素（针对带量词的模式）
                    entity = next((m for m in match if m.strip()), "")
                else:
                    entity = match

                if entity and entity not in entities:
                    entities.append(entity.strip())

        return entities

    def _extract_numbers(self, text: str) -> List[float]:
        """提取文本中的数值"""
        numbers = []
        number_pattern = r"[-+]?\d*\.\d+|\d+"

        for match in re.finditer(number_pattern, text):
            try:
                numbers.append(float(match.group(0)))
            except ValueError:
                continue

        return numbers

    def extract_relations(self, entities: Dict[str, Any], text: str) -> Dict[str, Any]:
        """提取实体间的关系"""
        relations = {}

        # 示例：提取"metric"与"duration"的关系
        if "metric" in entities and "duration" in entities:
            for metric in entities["metric"]:
                for duration in entities["duration"]:
                    if metric in text and duration in text:
                        if "metric_duration" not in relations:
                            relations["metric_duration"] = []
                        relations["metric_duration"].append({
                            "metric": metric,
                            "duration": duration
                        })

        return relations