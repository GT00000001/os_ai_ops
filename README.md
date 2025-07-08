```text  
os_ai_ops/
├── app/
│   ├── cli.py              # 命令行交互入口
│   ├── web.py              # Web交互入口（Flask）
│   ├── config.py           # os_ai_ops 全局配置
│   ├── utils/              # 通用工具（项目级）
│   │   ├── __init__.py
│   │   ├── helpers.py      # 通用工具函数（命令执行、文件操作等）
│   │   └── logger.py       # 日志配置
│   ├── nlp/                # 自然语言处理模块
│   │   ├── __init__.py
│   │   ├── processor.py    # 意图识别与处理
│   │   ├── entity_extractor.py  # 实体提取
│   │   ├── response_generator.py  # 回复生成
│   │   └── trainer.py      # 模型训练
│   ├── data/               # 数据采集模块
│   │   ├── __init__.py
│   │   └── system_monitor/ # 系统监控子模块（原独立项目）
│   │       ├── __init__.py 
│   │       ├── app.py      
│   │       ├── create.py   
│   │       ├── pyproject.toml 
│   │       ├── config.py   # system_monitor 自身配置（与项目全局配置区分）
│   │       └── monitor/    # 核心监控逻辑包
│   │           ├── __init__.py
│   │           ├── collector/  # 数据采集器
│   │           │   ├── __init__.py
│   │           │   ├── all_collectors.py  # 采集器聚合
│   │           │   ├── base.py            
│   │           │   ├── cpu.py             # CPU/内存采集
│   │           │   ├── disk.py            # 磁盘采集
│   │           │   ├── gpu_domestic.py    
│   │           │   ├── log_reader.py      # 操作系统日志采集
│   │           │   ├── network.py         # 网络IO采集
│   │           │   └── system_command.py  # 系统命令执行工具
│   │           ├── exporter/  # 数据导出（如REST API）
│   │           │   └── rest_api.py        # FastAPI 接口
│   │           └── utils/     # 监控工具包
│   │               └── os_info.py         
│   ├── anomaly/            # 异常检测模块
│   │   ├── __init__.py
│   │   ├── detector.py      # 异常检测模型
│   │   ├── trainer.py       # 模型训练
│   │   └── rules_engine.py  # 规则引擎检测
│   ├── fault/              # 故障自愈模块
│   │   ├── __init__.py
│   │   ├── healer.py        # 故障修复逻辑
│   │   ├── script_generator.py  # 修复脚本生成
│   │   └── script_templates/  # 修复脚本模板
│   ├── app_defect/         # 应用缺陷检测模块
│   │   ├── __init__.py
│   │   ├── detector.py      # 应用缺陷检测
│   │   ├── cve_scanner.py   # CVE漏洞扫描
│   │   └── config_analyzer.py  # 配置分析
│   └── evaluation/         # 模型评价模块
│       ├── __init__.py
│       ├── evaluator.py     # 评估指标
│       └── test_cases.py    # 测试用例
├── tests/                  # 单元测试
│   ├── test_nlp.py
│   ├── test_anomaly.py
│   ├── test_fault.py
│   ├── test_app_defect.py
│   └── test_system_monitor.py  # system_monitor 模块测试（可选）
├── models/                 # 训练好的模型存储
├── logs/                   # 日志输出
├── requirements.txt        # 项目依赖清单（建议合并 system_monitor 的依赖）
└── README.md               # 项目文档
```