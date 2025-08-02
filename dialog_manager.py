# 人物对话文本管理文件
# 格式: {对话ID: {文本内容, 说话人(可选)}}
DIALOGS = {
    # 储存相关对话
    "empty_storage": {
        "text": "身上没有可以储存的粮食"
    },
    "storage_success": {
        "text": "储存完成！"
    },
    # 可以添加更多对话...
}

def get_dialog_text(dialog_id):
    """获取指定ID的对话文本"""
    if dialog_id in DIALOGS:
        return DIALOGS[dialog_id]["text"]
    return ""