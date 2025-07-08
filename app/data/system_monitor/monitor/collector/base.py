from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Collector(ABC):
    @abstractmethod
    def collect(self) -> dict:
        """返回本采集器的监控数据"""
        pass

    @abstractmethod
    def top(self, n: int = 5) -> List[Dict[str, Any]]:
        """返回最近 n 条数据"""
        pass

    @abstractmethod
    def recent(self, n: int = 5) -> List[Dict[str, Any]]:
        """返回最近 n 条数据"""
        pass
