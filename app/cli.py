# 命令行交互入口
import cmd
from app.nlp.processor import NLPProcessor
from app.utils.logger import get_logger


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
    cli = AIOpsCLI()
    cli.cmdloop()