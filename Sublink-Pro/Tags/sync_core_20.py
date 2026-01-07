# ==========================================================
# 💡 维护笔记：
# 1. 字段名：必须使用 "groupName" 字段，否则标签无法入组
# 2. 删除逻辑：接口只接受 DELETE 方法，且名字要挂在 URL 后面
# 3. 运行前置：请按 F12 抓取最新的 Bearer Token
# ==========================================================

import requests  # 导入requests库，用于发送HTTP请求
import time  # 导入time库，用于处理时间相关的功能
import urllib3  # 导入urllib3库，用于处理HTTP请求

# 禁用安全警告，避免在请求HTTPS时出现证书验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== ✅ 模块化配置 ====================
# 定义API接口的URL地址
API_URL = "https://xxxxxx.zeabur.app/api/v1/tags/add"

# 💡 维护建议：运行脚本时再粘贴 Token。
# 这样即便代码上传到 GitHub Public 仓库，你的账号也是安全的
# 两种Token获取方式，根据需要选择其中一种：
# 方式1: 直接赋值（适合本地频繁使用，注意不要提交到GitHub）
# TOKEN = "your_token_here"  # 取消注释并替换为你的Token

# 方式2: 运行时输入（安全，推荐用于可能共享的环境）
TOKEN = input("请输入 Bearer Token: ")

# 设置请求头信息，包含认证信息和内容类型等
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",  # Bearer Token认证
    "Content-Type": "application/json",  # JSON格式数据
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"  # 模拟浏览器请求
}

# ==================== 🏷️ 20 个核心标签数据 ====================
# 定义标签组数据，包含速度评级、延迟评级、地区分类等
TAG_GROUPS = [
    {"name": "速度评级", "tags": [  # 速度评级标签组
        {"name": "🔥超快", "color": "#FF4444", "description": "> 100MB/s"},  # 超快速度标签
        {"name": "⚡极速", "color": "#00DD00", "description": "50-100MB/s"},  # 极速标签
        {"name": "✅正常", "color": "#0099FF", "description": "20-50MB/s"},  # 正常速度标签
        {"name": "🐌较慢", "color": "#FF9900", "description": "< 20MB/s"},  # 较慢速度标签
    ]},
    {"name": "延迟评级", "tags": [  # 延迟评级标签组
        {"name": "🚀低延迟", "color": "#00FF00", "description": "< 50ms"},  # 低延迟标签
        {"name": "📊中等延迟", "color": "#FFFF00", "description": "50-150ms"},  # 中等延迟标签
        {"name": "🌐高延迟", "color": "#FF0000", "description": "> 150ms"},  # 高延迟标签
    ]},
    {"name": "地区分类", "tags": [  # 地区分类标签组
        {"name": "🇭🇰香港", "color": "#DD0066", "description": "HK"},  # 香港地区标签
        {"name": "🇯🇵日本", "color": "#FF0000", "description": "JP"},  # 日本地区标签
        {"name": "🇺🇸美国", "color": "#0000FF", "description": "US"},  # 美国地区标签
        {"name": "🇸🇬新加坡", "color": "#FF3333", "description": "SG"},  # 新加坡地区标签
        {"name": "🇩🇪德国", "color": "#000000", "description": "DE"},  # 德国地区标签
        {"name": "🇰🇷韩国", "color": "#3399FF", "description": "KR"},  # 韩国地区标签
    ]},
    {"name": "流媒体支持", "tags": [  # 流媒体支持标签组
        {"name": "🎬Netflix", "color": "#E50914", "description": "支持奈飞"},
        {"name": "🎮游戏加速", "color": "#FF00FF", "description": "支持电竞"},  # 游戏加速标签
        {"name": "🎵音乐解锁", "color": "#1DB954", "description": "支持Spotify"},
        {"name": "📺YouTube 4K", "color": "#FF0000", "description": "支持高清"},  # YouTube 4K支持标签
    ]},
    {"name": "稳定性", "tags": [  # 稳定性标签组
        {"name": "📈极其稳定", "color": "#00FF00", "description": "SLA 99.9%"},
        {"name": "📉波动较大", "color": "#FF0000", "description": "偶有抖动"},  # 波动较大标签
        {"name": "🟢CN2 GIA", "color": "#00FF00", "description": "优质线路"},  # CN2 GIA线路标签
    ]},
]

def sync_core():  # 定义同步核心标签的函数

    """
    同步 Sublink-Pro Tags 模块的核心函数
    该函数会遍历所有标签组，并将每个标签发送到服务器进行同步
    """
    print(f"📡 正在同步 Sublink-Pro Tags 模块...")  # 打印同步开始提示
    session = requests.Session()
    success, skipped = 0, 0

    for group in TAG_GROUPS:
        for tag in group["tags"]:
            # ✅ 确认使用 groupName 字段，确保标签正确入组
            payload = {
                "name": tag["name"],
                "groupName": group["name"],
                "color": tag["color"],
                "description": tag["description"]
            }
            try:
                r = session.post(API_URL, headers=HEADERS, json=payload, verify=False, timeout=10)
                if r.status_code == 200:
                    print(f"  ✅ {group['name']} -> {tag['name']}")
                    success += 1
                elif r.status_code == 409:
                    print(f"  ⚠️ {tag['name']} - 已存在")
                    skipped += 1
                else:
                    print(f"  ❌ {tag['name']} - 失败: {r.status_code}")
            except Exception:
                print(f"  ❌ {tag['name']} - 网络异常")
            time.sleep(0.1)

    print(f"\n✨ 同步完成！新增: {success} | 跳过: {skipped}")

if __name__ == "__main__":
    sync_core()