# 导入所需的库
import requests  # 用于发送HTTP请求
import json      # 用于处理JSON数据
import time      # 用于处理时间相关功能
import urllib3   # 用于处理URL相关功能

# 禁用urllib3的警告信息
urllib3.disable_warnings()

# ==================== ✅ 核心暗号 (锁定会报 403 的正确路径) ====================
# API接口地址，用于添加规则
API_URL = "https://prosub.zeabur.app/api/v1/tags/rules/add" 
# 两种Token获取方式，根据需要选择其中一种：
# 方式1: 直接赋值（适合本地频繁使用，注意不要提交到GitHub）
# TOKEN = "your_token_here"  # 取消注释并替换为你的Token

# 方式2: 运行时输入（安全，推荐用于可能共享的环境）
TOKEN = input("请输入 Bearer Token: ")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}", 
    "Content-Type": "application/json", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

# 20 条规则全量对齐
CORE_RULES = [
    {"n": "速-超快", "tag": "🔥超快", "f": "speed", "o": "greater_than", "v": "100"},
    {"n": "速-极速", "tag": "⚡极速", "f": "speed", "o": "greater_than", "v": "50"},
    {"n": "速-正常", "tag": "✅正常", "f": "speed", "o": "greater_than", "v": "20"},
    {"n": "速-较慢", "tag": "🐌较慢", "f": "speed", "o": "less_than", "v": "20"},
    {"n": "延-低延迟", "tag": "🚀低延迟", "f": "latency", "o": "less_than", "v": "50"},
    {"n": "延-中等", "tag": "📊中等延迟", "f": "latency", "o": "less_than", "v": "150"},
    {"n": "延-高延迟", "tag": "🌐高延迟", "f": "latency", "o": "greater_than", "v": "150"},
    {"n": "地-香港", "tag": "🇭🇰香港", "f": "country_code", "o": "equal", "v": "HK"},
    {"n": "地-日本", "tag": "🇯🇵日本", "f": "country_code", "o": "equal", "v": "JP"},
    {"n": "地-美国", "tag": "🇺🇸美国", "f": "country_code", "o": "equal", "v": "US"},
    {"n": "地-新加坡", "tag": "🇸🇬新加坡", "f": "country_code", "o": "equal", "v": "SG"},
    {"n": "地-德国", "tag": "🇩🇪德国", "f": "country_code", "o": "equal", "v": "DE"},
    {"n": "地-韩国", "tag": "🇰🇷韩国", "f": "country_code", "o": "equal", "v": "KR"},
    {"n": "流-Netflix", "tag": "🎬Netflix", "f": "name", "o": "regex_match", "v": ".*(Netflix|NF).*"},
    {"n": "流-游戏加速", "tag": "🎮游戏加速", "f": "name", "o": "regex_match", "v": ".*(Game|游戏|电竞).*"},
    {"n": "流-音乐解锁", "tag": "🎵音乐解锁", "f": "name", "o": "regex_match", "v": ".*(Music|Spotify|音乐).*"},
    {"n": "流-YouTube", "tag": "📺YouTube 4K", "f": "name", "o": "regex_match", "v": ".*(YouTube|4K|YT).*"},
    {"n": "稳-线路CN2", "tag": "🟢CN2 GIA", "f": "name", "o": "regex_match", "v": ".*(CN2|GIA).*"},
    {"n": "稳-极其稳定", "tag": "📈极其稳定", "f": "name", "o": "regex_match", "v": ".*(Static|Premium).*"},
    {"n": "稳-波动较大", "tag": "📉波动较大", "f": "latency", "o": "greater_than", "v": "300"}
]

def sync():
    print(f"📡 正在向最终确认接口同步规则: {API_URL}")
    success = 0
    for r in CORE_RULES:
        # 封装双重序列化 JSON
        payload = {
            "name": r["n"],
            "tagName": r["tag"],
            "enabled": True,
            "triggerType": "subscription_update",
            "conditions": json.dumps({
                "logic": "and",
                "conditions": [{"field": r["f"], "operator": r["o"], "value": r["v"]}]
            })
        }
        try:
            res = requests.post(API_URL, headers=HEADERS, json=payload, verify=False, timeout=10)
            if res.status_code in [200, 201]:
                print(f"  ✅ {r['n']} -> 成功")
                success += 1
            else:
                print(f"  ❌ {r['n']} 失败 | 代码: {res.status_code} | 原因: {res.text}")
        except Exception as e:
            print(f"  ❌ 网络异常: {e}")
        time.sleep(0.1)
    print(f"\n✨ 同步结束！成功创建 {success} 条规则。")

if __name__ == "__main__": sync()