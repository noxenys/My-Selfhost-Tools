import requests  # 导入requests库，用于发送HTTP请求
import time  # 导入time库，用于处理时间相关操作
import urllib3  # 导入urllib3库，用于处理HTTP连接

urllib3.disable_warnings()  # 禁用urllib3的警告信息

# ==================== ✅ 锁定配置 ====================
LIST_URL = "https://prosub.zeabur.app/api/v1/tags/rules"  # API接口的基础URL
# 两种Token获取方式，根据需要选择其中一种：
# 方式1: 直接赋值（适合本地频繁使用，注意不要提交到GitHub）
# TOKEN = "your_token_here"  # 取消注释并替换为你的Token

# 方式2: 运行时输入（安全，推荐用于可能共享的环境）
TOKEN = input("请输入 Bearer Token: ")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}  # 设置请求头，包含认证信息
TARGET_PREFIXES = ["速-", "延-", "地-", "流-", "稳-"]  # 需要处理的规则名称前缀列表

# 探测队列：[ (URL后缀, 请求方法) ]
PROBE_LIST = [
    ("/del", "POST"),     # 缩写 del - 使用/del后缀和POST方法进行探测
    ("/remove", "POST"),  # 动词 remove - 使用/remove后缀和POST方法进行探测
    ("/delete", "DELETE"),# 标准 DELETE 方法配合 /delete 路径 - 使用标准RESTful风格的删除方法
    ("", "DELETE")        # 纯复数路径配合 DELETE 方法 - 使用复数路径和DELETE方法
]

def cleanup():  # 定义清理函数，用于删除符合条件的规则
    print("🔍 正在检索现有自动化规则...")  # 打印开始检索的提示信息
    try:
        response = requests.get(LIST_URL, headers=HEADERS, verify=False)  # 发送GET请求获取规则列表
        rules = response.json().get("data", [])  # 解析响应数据，获取规则列表
        to_delete = [r for r in rules if any(r["name"].startswith(p) for p in TARGET_PREFIXES)]  # 筛选出符合条件的规则
        
        if not to_delete:  # 如果没有找到符合条件的规则
            print("📭 未发现符合 Core 20 前缀的规则。")  # 打印提示信息
            return

        print(f"🗑️ 发现 {len(to_delete)} 条规则，启动接口探测模式...")  # 打印发现的规则数量和开始探测的提示
        
        working_path = None  # 初始化工作路径为None
        working_method = None  # 初始化工作方法为None

        for r in to_delete:  # 遍历所有需要删除的规则
            rid = r["id"]  # 获取规则ID
            rname = r["name"]  # 获取规则名称

            # 如果还没找到可用路径，开始探测
            if not working_path:  # 如果还没有找到可用的删除路径
                for suffix, method in PROBE_LIST:  # 遍历所有探测方案
                    # 探测方案 A: ?id=xxx 参数形式
                    test_url = f"{LIST_URL}{suffix}?id={rid}"  # 构建测试URL
                    try:
                        res = requests.request(method, test_url, headers=HEADERS, verify=False, timeout=5)  # 发送请求
                        if res.status_code in [200, 204]:  # 如果响应状态码成功
                            working_path = suffix  # 保存成功的路径
                            working_method = method  # 保存成功的方法
                            print(f"🎯 探测成功！正确暗号: {method} {suffix}")  # 打印成功信息
                            print(f"  ✅ 已删除: {rname}")  # 打印删除成功的规则名称
                            break
                    except: continue  # 如果请求失败，继续下一个探测方案
                
                if not working_path:  # 如果所有探测方案都失败
                    print("❌ 所有常规删除接口均失效。请手动删除一条并抓包查看 URL。")  # 打印错误信息
                    return
            else:
                # 已经找到路径，全速清理
                final_url = f"{LIST_URL}{working_path}?id={rid}"  # 构建最终的删除URL
                res = requests.request(working_method, final_url, headers=HEADERS, verify=False)  # 发送删除请求
                if res.status_code in [200, 204]:  # 如果删除成功
                    print(f"  ✅ 已删除: {rname}")  # 打印删除成功的规则名称
                else:  # 如果删除失败
                    print(f"  ❌ 删除失败: {rname}")  # 打印删除失败的规则名称
            
            time.sleep(0.05)

        print(f"\n✨ 清理完毕！共成功删除规则。")

    except Exception as e:
        print(f"❌ 运行异常: {e}")

if __name__ == "__main__": cleanup()