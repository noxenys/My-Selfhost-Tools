# 🛠️ 我的自建服务工具箱

这里存放我所有自建服务相关的代码和配置。

## ⚙️ 通用环境准备
脚本均基于 **Python 3.8+**。
运行前请确保已安装 `requests` 库：
```bash
pip install requests
```

---
## 📁 项目目录索引

### 🔹 [Sublink Pro 自动化脚本](./Sublink-Pro)
- **[标签管理 (Tags)](./Sublink-Pro/Tags)**: 包含全量/核心标签的导入与清理脚本。
- **[规则管理 (Rule)](./Sublink-Pro/Rule)**: 包含自动化打标规则的部署与清理脚本。

## 🚀 快速开始

### Sublink Pro 自动化管理
1. 克隆仓库并进入项目目录
2. 安装依赖：`pip install requests`
3. 运行标签同步脚本：`python Sublink-Pro/Tags/sync_core_20.py`
4. 运行规则部署脚本：`python Sublink-Pro/Rule/rule_core_10.py`
5. 按照提示输入 Bearer Token（或查看「Token 配置」部分了解本地快速配置方式）

## ⚠️ 重要注意事项

1. **Token 配置**：所有脚本支持两种 Token 获取方式：
   - **本地快速配置**：直接在脚本中赋值（注释状态，适合频繁使用）
   - **运行时输入**：默认方式，运行时提示输入（安全，适合共享环境）
2. **Token 安全**：直接赋值的 Token 严禁提交到 GitHub 等公共平台。
3. **鉴权获取**：通过浏览器 F12 -> 网络面板 -> 抓取任意接口的 `Authorization: Bearer <TOKEN>` 字段。
4. **API 兼容性**：脚本基于 Sublink Pro 特定 API 设计，请确保使用兼容版本。

## 🔜 计划加入
- [ ] n8n 工作流备份
- [ ] Docker 部署脚本

---

**👤 作者：** [noxenys](https://github.com/noxenys)
**📅 最后更新时间：** 2026-01-07
**📄 许可证：** [MIT](./LICENSE)

---