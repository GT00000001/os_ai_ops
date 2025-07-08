# 修复脚本生成
# 功能：生成修复脚本
# 核心方法：
# generate()：根据根因生成脚本
# 技术实现：
# 使用 Jinja2 模板引擎
# 模板示例：重启服务、清理缓存、释放资源

from jinja2 import Environment, FileSystemLoader
from app.config import config
from app.utils.logger import get_logger


class ScriptGenerator:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.env = Environment(
            loader=FileSystemLoader("app/fault/script_templates"),
            autoescape=False  # 脚本不需要HTML转义
        )

    def generate(self, root_cause, context=None):
        """根据根因生成修复脚本"""
        if not context:
            context = {}

        try:
            template = self.env.get_template(f"{root_cause}.j2")
            return template.render(context)
        except Exception as e:
            self.logger.error(f"Failed to generate script: {e}")
            return None