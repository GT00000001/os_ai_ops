# 命令行交互入口
import cmd
from app.nlp.processor import NLPProcessor
from app.utils.logger import get_logger
import uvicorn

class AIOpsCLI(cmd.Cmd):
    prompt = "运维管家> "

    def __init__(self):
        super().__init__()
        self.nlp_processor = NLPProcessor()
        self.logger = get_logger(__name__)
        self.context = {}  # 对话上下文

    def do_ask(self, question):
        """通过自然语言提问"""
        response = self.nlp_processor.process(question, self.context)
        print(response)

    def do_exit(self, _):
        """退出系统"""
        print("再见！")
        return True


if __name__ == "__main__":
    uvicorn.run(
        "app.evaluation.exporter:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式，生产环境建议移除
        log_level="info"
    )
    cli = AIOpsCLI()
    cli.cmdloop()