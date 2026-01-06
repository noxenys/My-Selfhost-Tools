# ==========================================================
# 💡 Clean 模块维护笔记：
# 1. 接口方法：删除必须使用 DELETE 方法
# 2. 参数传递：标签名字必须进行 URL 编码并挂在 ?name= 后面
# 3. 运行前置：必须先通过 F12 抓取最新的 Authorization Bearer Token
# ==========================================================

import requests  # 处理URL相关功能  # 用于发送HTTP请求
import urllib3  # 用于处理URL和HTTP请求
import time  # 用于处理时间相关功能
from urllib.parse import quote  # 用于URL编码

# 禁用不安全请求的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 定义删除标签的基础URL
BASE_DELETE_URL = "https://xxxxx.zeabur.app/api/v1/tags/delete"
# ✅ 维护建议：改为手动输入，保护隐私
TOKEN = input("请输入最新的 Bearer Token: ")

# 设置请求头信息，包含认证信息和用户代理
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

TAG_NAMES = ["🔥超快", "⚡极速", "✅正常", "🐌较慢", "🚀低延迟", "📊中等延迟", "🌐高延迟", "✨速度稳定", "⚠️偶尔限速", "🇭🇰香港", "🇯🇵日本", "🇺🇸美国", "🇸🇬新加坡", "🇩🇪德国", "🇰🇷韩国", "🌏亚洲节点", "🌍美洲节点", "🌎欧洲节点", "🟢CN2 GIA", "🟡BGP直连", "🔴普通线路", "💎IEPL", "📌内网专线", "🔴Shadowsocks", "🟢Trojan", "🔵Vless", "🟡Vmess", "🔐强加密", "⚡轻加密", "🔒带TLS", "❌无TLS", "📈极其稳定", "📉波动较大", "✅轻载", "⚠️中载", "🔴重载", "✅长期有效", "⚠️即将过期", "🎬Netflix", "🎮游戏加速", "🎵音乐解锁", "📺YouTube 4K", "💼工作办公", "🎮电竞游戏", "🎬休闲娱乐", "🔒隐私上网"]

def clean_all():
    print(f"🗑️ 正在清理 Tags 模块...")
    for name in TAG_NAMES:
        # ✅ 确认为 DELETE 方法且参数拼接在 URL 后
        url = f"{BASE_DELETE_URL}?name={quote(name)}"
        try:
            r = requests.delete(url, headers=HEADERS, verify=False, timeout=10)
            if r.status_code == 200: print(f"  ✅ 已清理: {name}")
        except: pass
        time.sleep(0.1)
    print("\n✨ 清理结束！")

if __name__ == "__main__": clean_all()