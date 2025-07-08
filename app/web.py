# Web交互入口
from flask import Flask, request, jsonify
from app.nlp.processor import NLPProcessor
from app.data.system_monitor.monitor.collector.all_collectors import AllCollectors
from app.anomaly.detector import AnomalyDetector

app = Flask(__name__)
nlp_processor = NLPProcessor()
system_collector = AllCollectors()
anomaly_detector = AnomalyDetector()


@app.route('/api/ask', methods=['POST'])
def handle_question():
    """处理自然语言请求"""
    data = request.json
    question = data.get('question', '')
    context = data.get('context', {})

    response = nlp_processor.process(question, context)
    return jsonify({
        'response': response,
        'context': context
    })


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """获取系统指标"""
    metrics = system_collector.collect_all_metrics()
    return jsonify(metrics)


@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    """获取异常历史"""
    # 实际需从数据库查询
    return jsonify({
        'anomalies': []
    })


if __name__ == '__main__':
    app.run(debug=True)