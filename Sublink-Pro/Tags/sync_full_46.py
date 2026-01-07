# ==========================================================
# 💡 维护笔记：
# 1. 字段名：必须使用 "groupName" 字段，否则标签无法入组
# 2. 删除逻辑：接口只接受 DELETE 方法，且名字要挂在 URL 后面
# 3. 运行前置：请按 F12 抓取最新的 Bearer Token
# ==========================================================

import requests  # 导入requests库，用于发送HTTP请求
import time  # 导入time库，用于处理时间相关功能
import urllib3  # 导入urllib3库，用于处理HTTP请求

# 禁用安全警告，避免在请求时出现SSL证书验证的警告信息
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== ✅ 模块化配置 ====================
# 定义API接口的基础URL
API_URL = "https://xxxxxx.zeabur.app/api/v1/tags/add"

# 💡 安全建议：运行脚本时手动粘贴 Token，保护隐私
# 两种Token获取方式，根据需要选择其中一种：
# 方式1: 直接赋值（适合本地频繁使用，注意不要提交到GitHub）
# TOKEN = "your_token_here"  # 取消注释并替换为你的Token

# 方式2: 运行时输入（安全，推荐用于可能共享的环境）
TOKEN = input("请输入 Bearer Token: ")

# 设置请求头信息，包括认证令牌、内容类型和用户代理
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",  # 认证信息，使用Bearer Token
    "Content-Type": "application/json",  # 指定请求内容类型为JSON
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"  # 模拟浏览器用户代理
}

# 15 组全量定义
TAG_GROUPS = [
    {"name": "速度评级", "tags": [
        {"name": "🔥超快", "color": "#FF4444", "description": "> 100MB/s"},
        {"name": "⚡极速", "color": "#00DD00", "description": "50-100MB/s"},
        {"name": "✅正常", "color": "#0099FF", "description": "20-50MB/s"},
        {"name": "🐌较慢", "color": "#FF9900", "description": "< 20MB/s"},
    ]},
    {"name": "延迟评级", "tags": [
        {"name": "🚀低延迟", "color": "#00FF00", "description": "< 50ms"},
        {"name": "📊中等延迟", "color": "#FFFF00", "description": "50-150ms"},
        {"name": "🌐高延迟", "color": "#FF0000", "description": "> 150ms"},
    ]},
    {"name": "速度状态", "tags": [
        {"name": "✨速度稳定", "color": "#00FF00", "description": "无明显限速"},
        {"name": "⚠️偶尔限速", "color": "#FF0000", "description": "高峰期波动"},
    ]},
    {"name": "地区分类", "tags": [
        {"name": "🇭🇰香港", "color": "#DD0066", "description": "HK"},
        {"name": "🇯🇵日本", "color": "#FF0000", "description": "JP"},
        {"name": "🇺🇸美国", "color": "#0000FF", "description": "US"},
        {"name": "🇸🇬新加坡", "color": "#FF3333", "description": "SG"},
        {"name": "🇩🇪德国", "color": "#000000", "description": "DE"},
        {"name": "🇰🇷韩国", "color": "#3399FF", "description": "KR"},
    ]},
    {"name": "洲别分类", "tags": [
        {"name": "🌏亚洲节点", "color": "#FF0000", "description": "Asia"},
        {"name": "🌍美洲节点", "color": "#0000FF", "description": "America"},
        {"name": "🌎欧洲节点", "color": "#000000", "description": "Europe"},
    ]},
    {"name": "运营商线路", "tags": [
        {"name": "🟢CN2 GIA", "color": "#00FF00", "description": "优质线路"},
        {"name": "🟡BGP直连", "color": "#FFFF00", "description": "主流线路"},
        {"name": "🔴普通线路", "color": "#FF0000", "description": "国际直连"},
    ]},
    {"name": "专线类型", "tags": [
        {"name": "💎IEPL", "color": "#FFD700", "description": "端到端专线"},
        {"name": "📌内网专线", "color": "#FF69B4", "description": "中转专线"},
    ]},
    {"name": "协议类型", "tags": [
        {"name": "🔴Shadowsocks", "color": "#FF0000", "description": "SS"},
        {"name": "🟢Trojan", "color": "#00FF00", "description": "Trojan"},
        {"name": "🔵Vless", "color": "#0000FF", "description": "Vless"},
        {"name": "🟡Vmess", "color": "#FFFF00", "description": "Vmess"},
    ]},
    {"name": "加密方式", "tags": [
        {"name": "🔐强加密", "color": "#0000FF", "description": "AES-256"},
        {"name": "⚡轻加密", "color": "#00FF00", "description": "ChaCha20"},
    ]},
    {"name": "TLS版本", "tags": [
        {"name": "🔒带TLS", "color": "#00FF00", "description": "加密传输"},
        {"name": "❌无TLS", "color": "#FF0000", "description": "明文/其他"},
    ]},
    {"name": "延迟稳定性", "tags": [
        {"name": "📈极其稳定", "color": "#00FF00", "description": "波动小"},
        {"name": "📉波动较大", "color": "#FF0000", "description": "波动大"},
    ]},
    {"name": "负载状态", "tags": [
        {"name": "✅轻载", "color": "#00FF00", "description": "用户少"},
        {"name": "⚠️中载", "color": "#FFFF00", "description": "用户适中"},
        {"name": "🔴重载", "color": "#FF0000", "description": "建议更换"},
    ]},
    {"name": "有效期", "tags": [
        {"name": "✅长期有效", "color": "#00FF00", "description": "资源稳定"},
        {"name": "⚠️即将过期", "color": "#FF0000", "description": "请留意"},
    ]},
    {"name": "流媒体支持", "tags": [
        {"name": "🎬Netflix", "color": "#E50914", "description": "支持奈飞"},
        {"name": "🎮游戏加速", "color": "#FF00FF", "description": "支持电竞"},
        {"name": "🎵音乐解锁", "color": "#1DB954", "description": "支持Spotify"},
        {"name": "📺YouTube 4K", "color": "#FF0000", "description": "支持高清"},
    ]},
    {"name": "使用场景", "tags": [
        {"name": "💼工作办公", "color": "#0066CC", "description": "稳定性优先"},
        {"name": "🎮电竞游戏", "color": "#FF00FF", "description": "低延迟优先"},
        {"name": "🎬休闲娱乐", "color": "#FF6600", "description": "速度优先"},
        {"name": "🔒隐私上网", "color": "#000000", "description": "安全性优先"},
    ]},
]

def sync_full():
    print("🚀 正在同步 Sublink Pro 全量标签模块 (使用 groupName 字段)...")
    success_count = 0
    for group in TAG_GROUPS:
        for tag in group["tags"]:
            # ✅ 确认使用 groupName 字段，确保标签入组
            payload = {
                "name": tag["name"],
                "groupName": group["name"], 
                "color": tag["color"],
                "description": tag["description"]
            }
            try:
                r = requests.post(API_URL, headers=HEADERS, json=payload, verify=False, timeout=10)
                if r.status_code == 200:
                    print(f"  ✅ {group['name']} -> {tag['name']}")
                    success_count += 1
            except Exception:
                print(f"  ❌ {tag['name']} 网络异常")
            time.sleep(0.1)
    print(f"\n✨ 同步完成！共新增 {success_count} 个标签。")

if __name__ == "__main__":
    sync_full()