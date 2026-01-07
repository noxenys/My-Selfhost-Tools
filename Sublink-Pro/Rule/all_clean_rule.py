# 导入所需的库
import requests  # 用于发送HTTP请求
import time      # 用于处理时间延迟
import urllib3   # 用于处理URL相关功能

# 禁用urllib3的警告信息
urllib3.disable_warnings()

# ==================== ✅ 锁定抓包确认的正确接口 ====================
# 规则列表的API地址
LIST_URL = "https://prosub.zeabur.app/api/v1/tags/rules"
DELETE_URL_BASE = "https://prosub.zeabur.app/api/v1/tags/rules/delete" # 确认后缀为 /delete
# 两种Token获取方式，根据需要选择其中一种：
# 方式1: 直接赋值（适合本地频繁使用，注意不要提交到GitHub）
# TOKEN = "your_token_here"  # 取消注释并替换为你的Token

# 方式2: 运行时输入（安全，推荐用于可能共享的环境）
TOKEN = input("请输入 Bearer Token: ")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def nuclear_wipe():
    print("🔍 正在检索后台所有规则...")
    try:
        # 1. 获取当前所有规则列表
        res = requests.get(LIST_URL, headers=HEADERS, verify=False)
        if res.status_code != 200:
            print(f"❌ 无法获取列表: {res.text}")
            return
            
        rules = res.json().get("data", [])
        if not rules:
            print("📭 后台已经是空的，无需操作。")
            return

        print(f"⚠️ 警告：发现 {len(rules)} 条规则，准备全量清空！")
        confirm = input("输入 'y' 确认清空所有规则，输入其他退出: ")
        if confirm.lower() != 'y':
            print("❌ 操作已取消。")
            return

        # 2. 执行删除逻辑
        success_count = 0
        for r in rules:
            rid = r["id"]
            rname = r["name"]
            
            # 构造抓包确认的完整 URL
            final_del_url = f"{DELETE_URL_BASE}?id={rid}"
            
            try:
                # 必须使用 DELETE 方法
                response = requests.delete(final_del_url, headers=HEADERS, verify=False, timeout=10)
                
                if response.status_code == 200:
                    print(f"  ✅ 已清理: {rname} (ID: {rid})")
                    success_count += 1
                else:
                    print(f"  ❌ 清理失败: {rname} | 代码: {response.status_code} | 原因: {response.text}")
            except Exception as e:
                print(f"  ❌ 网络异常: {e}")
            
            # 适当延迟，防止请求过快
            time.sleep(0.1)

        print(f"\n✨ 后台清理完毕！共成功删除 {success_count} 条规则。")

    except Exception as e:
        print(f"❌ 运行异常: {e}")

if __name__ == "__main__":
    nuclear_wipe()