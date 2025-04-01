from datetime import datetime

def format_timestamps(data):
    """
    格式化数据中的 created_at 和 updated_at 时间戳为人类可读格式。
    支持单个字典或字典列表。
    """
    def format_item(item):
        if "created_at" in item and item["created_at"]:
            timestamp = item["created_at"]
            if len(str(timestamp)) > 10:  # 毫秒级时间戳长度大于10
                timestamp = timestamp / 1000
            item["created_at"] = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        
        if "updated_at" in item and item["updated_at"]:
            timestamp = item["updated_at"]
            if len(str(timestamp)) > 10:  # 毫秒级时间戳长度大于10
                timestamp = timestamp / 1000
            item["updated_at"] = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return item

    # 如果是列表，逐项处理
    if isinstance(data, list):
        return [format_item(item) for item in data]
    # 如果是单个字典，直接处理
    elif isinstance(data, dict):
        return format_item(data)
    return data