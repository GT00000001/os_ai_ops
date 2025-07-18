def generate_test_data():
    # 正常场景
    normal_data = [
        {"cpu_usage": 20, "memory_usage": 30, "disk_usage": 40},
        {"cpu_usage": 15, "memory_usage": 25, "disk_usage": 35}
    ]
    normal_labels = [0] * len(normal_data)

    # 异常场景
    anomaly_data = [
        {"cpu_usage": 95, "memory_usage": 92, "disk_usage": 90},
        {"cpu_usage": 98, "memory_usage": 96, "disk_usage": 94}
    ]
    anomaly_labels = [1] * len(anomaly_data)

    # 边缘场景
    edge_data = [
        {},  # 空输入
        {"cpu_usage": -1, "memory_usage": -1, "disk_usage": -1}  # 错误命令
    ]
    edge_labels = [0] * len(edge_data)

    test_data = normal_data + anomaly_data + edge_data
    true_labels = normal_labels + anomaly_labels + edge_labels

    return test_data, true_labels

