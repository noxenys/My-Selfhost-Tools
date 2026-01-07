import requests  # 导入requests库，用于发送HTTP请求
import json  # 导入json库，用于处理JSON数据
import time  # 导入time库，用于时间相关操作
import urllib3  # 导入urllib3库，用于处理HTTP请求

# 禁用urllib3的警告信息
urllib3.disable_warnings()

# ==================== ✅ 精简版配置 ====================
# API端点URL，用于添加规则
ADD_URL = "https://prosub.zeabur.app/api/v1/tags/rules/add"
# 两种Token获取方式，根据需要选择其中一种：
# 方式1: 直接赋值（适合本地频繁使用，注意不要提交到GitHub）
# TOKEN = "your_token_here"  # 取消注释并替换为你的Token

# 方式2: 运行时输入（安全，推荐用于可能共享的环境）
TOKEN = input("请输入 Bearer Token: ")
# 请求头信息，包含认证令牌和内容类型
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# 精选 10 条规则 (逻辑更实用)
LITE_RULES = [
    # 性能类 (2条)
    {"n": "速-极速4K", "tag": "🚀高速", "f": "speed", "o": "greater_than", "v": "50"},
    {"n": "延-低延迟", "tag": "🎮竞技", "f": "latency", "o": "less_than", "v": "50"},
    
    # 地区类 (4条)
    {"n": "地-香港", "tag": "🇭🇰HK", "f": "country_code", "o": "equal", "v": "HK"},
    {"n": "地-日本", "tag": "🇯🇵JP", "f": "country_code", "o": "equal", "v": "JP"},
    {"n": "地-美国", "tag": "🇺🇸US", "f": "country_code", "o": "equal", "v": "US"},
    {"n": "地-新加坡", "tag": "🇸🇬SG", "f": "country_code", "o": "equal", "v": "SG"},
    
    # 解锁类 (2条)
    {"n": "流-Netflix", "tag": "🎬NF", "f": "name", "o": "regex_match", "v": ".*(Netflix|NF).*"},
    {"n": "流-ChatGPT", "tag": "🤖AI", "f": "name", "o": "regex_match", "v": ".*(GPT|OpenAI|AI).*"},
    
    # 稳定类 (2条)
    {"n": "稳-静态独享", "tag": "🟢静态", "f": "name", "o": "regex_match", "v": ".*(Static|Premium|专线).*"},
    {"n": "稳-波动大", "tag": "⚠️波动", "f": "latency", "o": "greater_than", "v": "300"}
]

def deploy_lite():
    print("📡 正在部署 精英 10 条自动化规则...")
    success = 0
    for r in LITE_RULES:
        payload = {
            "name": r["n"], "tagName": r["tag"], "enabled": True, "triggerType": "subscription_update",
            "conditions": json.dumps({"logic": "and", "conditions": [{"field": r["f"], "operator": r["o"], "value": r["v"]}]})
        }
        res = requests.post(ADD_URL, headers=HEADERS, json=payload, verify=False)
        if res.status_code == 200:
            print(f"  ✅ {r['n']}")
            success += 1
        time.sleep(0.1)
    print(f"\n✨ 部署完成！共 {success} 条规则，SLP 界面现在会清爽很多。")

if __name__ == "__main__": deploy_lite()