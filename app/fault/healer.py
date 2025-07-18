# 故障修复逻辑
# 功能：诊断故障并执行修复
# 核心组件：
# FaultHealer 类：故障自愈主类
# diagnose()：诊断故障根因
# generate_fix_script()：生成修复脚本
# execute_fix()：执行修复操作
# verify_fix()：验证修复效果
# 自愈流程：诊断 → 生成脚本 → 执行 → 验证
from app.fault.script_generator import ScriptGenerator
from app.utils.helpers import run_command
from app.data.collector.all_collectors import AllCollectors


import time
from app.fault.script_generator import ScriptGenerator
from app.utils.helpers import run_command
from app.data.collector.all_collectors import AllCollectors

class FaultHealer:
    def __init__(self):
        self.script_generator = ScriptGenerator()
        self.system_collector = AllCollectors()

    def diagnose(self, anomaly):
        """诊断故障原因"""
        # 根据异常类型推断根因
        root_cause = "unknown"
        if "cpu_usage" in anomaly and anomaly["cpu_usage"] > 90:
            root_cause = "high_cpu"
        elif "memory_usage" in anomaly and anomaly["memory_usage"] > 90:
            root_cause = "high_memory"
        return root_cause

    def generate_fix_script(self, root_cause):
        """生成修复脚本"""
        return self.script_generator.generate(root_cause)

    def execute_fix(self, script):
        """执行修复脚本"""
        start_time = time.time()
        result = run_command(script)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time

    def verify_fix(self):
        """验证修复效果"""
        metrics = self.system_collector.collect_all_metrics()
        # 检查关键指标是否恢复正常
        return (metrics["cpu_usage"] < 80 and
                metrics["memory_usage"] < 80 and
                metrics["disk_usage"] < 90)

    def heal(self, anomaly):
        """完整的自愈流程"""
        start_time = time.time()
        root_cause = self.diagnose(anomaly)
        script = self.generate_fix_script(root_cause)
        result, execution_time = self.execute_fix(script)
        is_fixed = self.verify_fix()
        end_time = time.time()
        analysis_time = end_time - start_time - execution_time
        return is_fixed, execution_time, analysis_time