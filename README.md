# OpenClaw更新监控与小红书发布系统

## 📋 项目概述

这是一个完整的自动化系统，用于：
1. 监控OpenClaw官方Twitter账号的版本更新
2. 获取GitHub最新发布内容
3. 将内容翻译成中文并格式化为小红书风格
4. 生成可直接发布的小红书笔记

## 🚀 功能特性

### Twitter监控
- 通过推文ID获取@openclaw官方更新内容
- 自动识别版本更新推文
- 提取关键更新要点和统计数据
- 完整中文翻译

### GitHub更新处理
- 自动获取最新发布信息
- 解析Changes/Breaking/Fixes分类
- 全量中文翻译（支持分批次处理）
- 内容摘要和要点提取

### 小红书内容生成
- 小红书风格内容转换
- 平台规范格式优化
- 热门标签自动生成
- 多格式输出（JSON/TXT/MD）

### 自动化流水线
- 一键式处理脚本
- 完整日志记录
- 文件管理和版本控制
- 发布准备指南

## 📁 项目结构

```
openclaw-update-monitor/
├── README.md                    # 项目说明文档
├── LICENSE                      # 开源许可证
├── requirements.txt             # Python依赖
├── config/
│   ├── config.example.yaml      # 配置文件示例
│   └── twitter_ids.txt          # 推文ID数据库
├── scripts/
│   ├── twitter_monitor.py       # Twitter监控脚本
│   ├── github_monitor.py        # GitHub监控脚本
│   ├── xiaohongshu_generator.py # 小红书内容生成器
│   ├── pipeline.py              # 完整处理流水线
│   └── utils.py                 # 工具函数
├── skills/
│   └── xiaohongshu-poster/
│       ├── SKILL.md             # 技能说明文档
│       └── scripts/
│           ├── post_note.py     # 小红书发布脚本
│           └── format_content.py # 内容格式化
├── examples/
│   ├── twitter_example.json     # Twitter数据示例
│   ├── github_example.json      # GitHub数据示例
│   └── xiaohongshu_example.md   # 小红书笔记示例
├── docs/
│   ├── setup_guide.md           # 安装配置指南
│   ├── usage_guide.md           # 使用指南
│   └── troubleshooting.md       # 故障排除
└── output/
    ├── twitter/                 # Twitter数据输出
    ├── github/                  # GitHub数据输出
    └── xiaohongshu/             # 小红书内容输出
```

## 🛠️ 安装配置

### 环境要求
- Python 3.8+
- OpenClaw运行环境
- 网络访问权限（api.fxtwitter.com, api.github.com）

### 快速开始
```bash
# 克隆项目
git clone https://github.com/huazhoufang789-gif/openclaw-.git
cd openclaw-update-monitor

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp config/config.example.yaml config/config.yaml

# 编辑配置文件
vim config/config.yaml
```

### 配置文件说明
```yaml
# config/config.yaml
twitter:
  api_base: "https://api.fxtwitter.com"
  known_tweets: "config/twitter_ids.txt"
  check_interval: 3600  # 检查间隔（秒）

github:
  api_base: "https://api.github.com"
  repo: "openclaw/openclaw"
  check_interval: 3600

xiaohongshu:
  output_dir: "output/xiaohongshu"
  tags: ["OpenClaw", "AIGC", "技术更新", "AI工具"]
  max_content_length: 2000

monitor:
  enable_twitter: true
  enable_github: true
  auto_generate: true
  log_level: "INFO"
```

## 📖 使用方法

### 基本使用
```bash
# 运行完整流水线
python scripts/pipeline.py --all

# 只监控Twitter
python scripts/twitter_monitor.py --tweet-id 2026503611514069173

# 只监控GitHub
python scripts/github_monitor.py --latest

# 生成小红书内容
python scripts/xiaohongshu_generator.py --twitter output/twitter/latest.json --github output/github/latest.json
```

### 定时任务
```bash
# 使用cron定时运行
0 */6 * * * cd /path/to/openclaw-update-monitor && python scripts/pipeline.py --all >> logs/pipeline.log 2>&1
```

### OpenClaw技能使用
```bash
# 安装技能
openclaw skills install ./skills/xiaohongshu-poster

# 使用技能
openclaw run --prompt "使用小红书发布助手生成OpenClaw更新内容"
```

## 🔧 核心脚本说明

### 1. Twitter监控脚本 (`twitter_monitor.py`)
```python
# 功能：获取Twitter更新内容
# 输入：推文ID或用户名
# 输出：JSON格式的推文数据
python twitter_monitor.py --tweet-id 2026503611514069173 --output twitter_data.json
```

### 2. GitHub监控脚本 (`github_monitor.py`)
```python
# 功能：获取GitHub发布内容
# 输入：仓库名称
# 输出：JSON格式的发布数据
python github_monitor.py --repo openclaw/openclaw --latest --output github_data.json
```

### 3. 小红书内容生成器 (`xiaohongshu_generator.py`)
```python
# 功能：生成小红书格式内容
# 输入：Twitter和GitHub数据
# 输出：小红书笔记文件
python xiaohongshu_generator.py --twitter twitter_data.json --github github_data.json --output xiaohongshu_note.md
```

### 4. 完整流水线 (`pipeline.py`)
```python
# 功能：自动化处理流程
# 输入：配置文件
# 输出：完整的处理结果
python pipeline.py --config config/config.yaml --all --output-dir output/
```

## 🎯 输出示例

### Twitter数据示例
```json
{
  "tweet_id": "2026503611514069173",
  "username": "openclaw",
  "text": "OpenClaw 2026.2.24 🦞\n🌍 Stop phrases in 10+ languages...",
  "created_at": "Wed Feb 25 03:44:46 +0000 2026",
  "likes": 1250,
  "retweets": 91,
  "views": 87144,
  "translated_text": "OpenClaw 2026.2.24 🦞\n🌍 支持10+种语言的停止短语..."
}
```

### GitHub数据示例
```json
{
  "version": "v2026.2.24",
  "name": "openclaw 2026.2.24",
  "published_at": "2026-02-25T03:31:17Z",
  "changes": ["Auto-reply/Abort shortcuts: expand standalone stop phrases..."],
  "breaking_changes": ["Heartbeat delivery now blocks direct/DM targets..."],
  "fixes": ["Routing/Session isolation: harden followup routing..."],
  "translated_changes": ["自动回复/中止快捷方式：扩展独立的停止短语..."]
}
```

### 小红书笔记示例
```
OpenClaw 2026年2月25日 🦞 上新啦上新啦！
全是硬货不玩虚的，AI能力、安全防护、多端体验直接拉满✅

🔥 官方Twitter更新速览：
@openclaw: OpenClaw 2026.2.24 🦞
🌍 支持10+种语言的停止短语...
#OpenClaw #AIGC #技术更新
```

## 🔍 监控数据库

### 推文ID数据库 (`config/twitter_ids.txt`)
```
# OpenClaw官方推文ID记录
# 格式：tweet_id|checked_date|version|title
2026503611514069173|2026-02-26|v2026.2.24|OpenClaw 2026.2.24发布
# 添加新推文ID时使用相同格式
```

### 更新记录 (`output/updates.log`)
```
[2026-02-26 02:00:00] INFO: 开始监控OpenClaw更新
[2026-02-26 02:00:05] INFO: Twitter监控完成，获取1条推文
[2026-02-26 02:00:10] INFO: GitHub监控完成，获取83项更新
[2026-02-26 02:00:15] INFO: 小红书内容生成完成
[2026-02-26 02:00:20] INFO: 流水线执行完成
```

## ⚙️ 高级配置

### 自定义内容模板
编辑 `skills/xiaohongshu-poster/scripts/format_content.py` 中的模板函数：
```python
def create_xiaohongshu_template(title, content, tags):
    """自定义小红书内容模板"""
    template = f"""{title}

{content}

{" ".join(tags)}
"""
    return template
```

### 扩展监控源
在 `scripts/utils.py` 中添加新的数据源：
```python
def fetch_from_custom_source(url):
    """从自定义数据源获取内容"""
    # 实现自定义数据获取逻辑
    pass
```

### 多平台发布
扩展 `scripts/pipeline.py` 支持其他平台：
```python
def publish_to_platforms(content, platforms):
    """发布到多个平台"""
    for platform in platforms:
        if platform == "weibo":
            publish_to_weibo(content)
        elif platform == "zhihu":
            publish_to_zhihu(content)
        # 添加更多平台
```

## 🐛 故障排除

### 常见问题

1. **Twitter API访问失败**
   ```
   错误：无法访问api.fxtwitter.com
   解决方案：检查网络连接，确保可以访问该域名
   ```

2. **GitHub API限制**
   ```
   错误：GitHub API速率限制
   解决方案：添加GitHub Token到配置文件
   ```

3. **内容格式问题**
   ```
   错误：小红书内容格式不符合要求
   解决方案：调整内容长度和格式，移除链接
   ```

4. **技能安装失败**
   ```
   错误：OpenClaw技能安装失败
   解决方案：检查技能文件结构和权限
   ```

### 日志查看
```bash
# 查看处理日志
tail -f output/pipeline.log

# 查看错误日志
tail -f output/error.log

# 查看调试信息
python scripts/pipeline.py --debug --all
```

## 📈 性能优化

### 缓存机制
```python
# 启用数据缓存
python scripts/pipeline.py --use-cache --cache-dir cache/

# 清理旧缓存
python scripts/cleanup.py --older-than 7d
```

### 并发处理
```python
# 启用多线程处理
python scripts/pipeline.py --threads 4 --all

# 分批处理大量数据
python scripts/pipeline.py --batch-size 10 --all
```

### 内存优化
```python
# 限制内存使用
python scripts/pipeline.py --max-memory 512 --all

# 启用流式处理
python scripts/pipeline.py --stream --all
```

## 🔄 更新维护

### 定期更新
```bash
# 更新项目代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 更新配置文件
cp config/config.example.yaml config/config.yaml.new
```

### 数据备份
```bash
# 备份输出数据
tar -czf backup_$(date +%Y%m%d).tar.gz output/

# 备份配置文件
cp -r config/ backup/config_$(date +%Y%m%d)/
```

### 监控状态
```bash
# 检查系统状态
python scripts/status_check.py

# 查看资源使用
python scripts/resource_monitor.py

# 生成状态报告
python scripts/generate_report.py --period 7d
```

## 🤝 贡献指南

### 代码贡献
1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 创建Pull Request

### 问题反馈
1. 查看现有Issue
2. 创建新Issue描述问题
3. 提供复现步骤和日志

### 文档改进
1. 更新README文档
2. 添加使用示例
3. 完善配置说明

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- OpenClaw项目团队
- Twitter/FxTwitter API
- GitHub API
- 所有贡献者和用户

## 📞 联系方式

- 项目主页：https://github.com/huazhoufang789-gif/openclaw-
- 问题反馈：GitHub Issues
- 讨论交流：GitHub Discussions

---

**开始使用：**
```bash
git clone https://github.com/huazhoufang789-gif/openclaw-.git
cd openclaw-update-monitor
python scripts/pipeline.py --all
```

**享受自动化的OpenClaw更新监控体验！** 🚀