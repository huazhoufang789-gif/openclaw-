# 小红书自动发布助手技能

## 功能描述
将OpenClaw更新内容自动转换为小红书笔记格式，支持一键生成和发布准备。

## 使用场景
- 将OpenClaw官方Twitter和GitHub更新转换为小红书内容
- 自动化技术内容社交媒体发布
- 多平台内容同步
- 内容营销自动化

## 核心功能
1. **内容格式化**：将技术更新转换为小红书富文本格式
2. **标签优化**：智能生成热门技术标签
3. **链接处理**：自动移除或处理外部链接（小红书限制）
4. **发布准备**：生成完整的发布指南和配置文件
5. **批量处理**：支持多篇内容批量生成

## 使用方法

### 作为OpenClaw技能使用
```bash
# 安装技能
openclaw skills install ./skills/xiaohongshu-poster

# 使用技能生成小红书内容
openclaw run --prompt "使用小红书发布助手生成OpenClaw v2026.2.24更新内容"

# 使用技能发布内容
openclaw run --prompt "发布OpenClaw更新到小红书"
```

### 作为独立脚本使用
```bash
# 生成小红书内容
python scripts/post_note.py \
  --title "OpenClaw更新" \
  --content "更新内容..." \
  --tags "技术,AI,编程"

# 从Twitter和GitHub数据生成
python scripts/post_openclaw_update.py \
  --twitter data/twitter.json \
  --github data/github.json \
  --output xiaohongshu_note.md
```

### 集成到流水线
```bash
# 使用完整流水线
python scripts/pipeline.py --all

# 只生成小红书内容
python scripts/pipeline.py --xiaohongshu-only
```

## 文件结构
```
xiaohongshu-poster/
├── SKILL.md                    # 技能说明文档
├── scripts/
│   ├── post_note.py           # 单篇笔记发布
│   ├── post_openclaw_update.py # OpenClaw专用发布
│   ├── format_content.py      # 内容格式化
│   └── xhs_api.py             # 小红书API客户端（预留）
├── templates/
│   ├── note_template.md       # 笔记模板
│   └── tags_template.json     # 标签模板
└── config/
    └── config.yaml            # 配置文件
```

## 配置说明

### 基本配置
```yaml
xiaohongshu:
  output_dir: "./output/xiaohongshu"
  include_links: false  # 小红书不允许外部链接
  default_tags:
    - "OpenClaw"
    - "AIGC"
    - "技术更新"
  max_content_length: 2000
```

### 高级配置
```yaml
# 内容模板配置
templates:
  note_template: |
    {title}
    
    {content}
    
    {tags}
  
  # 标签生成规则
  tag_rules:
    - keyword: "security"
      tags: ["安全", "AI安全"]
    - keyword: "update"
      tags: ["更新", "技术更新"]

# 发布策略
publish:
  strategy: "manual"  # manual, auto, scheduled
  best_time: "09:00-18:00"
  avoid_weekends: true
```

## 内容格式化规则

### 小红书平台限制
1. **不支持Markdown**：转换为纯文本+Emoji
2. **不允许外部链接**：自动移除或替换
3. **内容长度**：建议1000-2000字
4. **标签数量**：最多15个标签
5. **图片要求**：建议添加相关图片

### 转换规则
- `# 标题` → `✨ 标题`
- `**粗体**` → `🔸粗体🔸`
- `- 列表项` → `• 列表项`
- `[链接](url)` → `链接（详情见评论区）`
- 代码块 → `📝 代码内容`

## 使用示例

### 输入数据
```json
{
  "twitter": {
    "text": "OpenClaw 2026.2.24 🦞\n🌍 Stop phrases in 10+ languages...",
    "likes": 1250
  },
  "github": {
    "version": "v2026.2.24",
    "changes": ["Auto-reply/Abort shortcuts..."]
  }
}
```

### 输出内容
```
OpenClaw 2026年2月25日 🦞 上新啦上新啦！
全是硬货不玩虚的，AI能力、安全防护、多端体验直接拉满✅

🔥 官方Twitter更新速览：
@openclaw: OpenClaw 2026.2.24 🦞
🌍 支持10+种语言的停止短语...

#OpenClaw #AIGC #技术更新
```

## 错误处理

### 常见错误
1. **内容过长**：自动截断或分段
2. **包含链接**：自动移除或替换
3. **标签过多**：自动筛选热门标签
4. **格式错误**：自动修正格式

### 日志记录
- 所有操作记录到日志文件
- 错误信息详细记录
- 支持调试模式

## 更新维护

### 版本历史
- v1.0.0: 初始版本，基础功能
- v1.1.0: 添加OpenClaw专用模板
- v1.2.0: 优化标签生成算法

### 依赖更新
```bash
# 更新依赖
pip install -r requirements.txt --upgrade

# 检查兼容性
python scripts/check_compatibility.py
```

## 注意事项

### 平台合规
1. 遵守小红书社区规范
2. 不发布违规内容
3. 注意发布频率限制
4. 尊重版权和知识产权

### 技术限制
1. 需要网络访问权限
2. 依赖外部API服务
3. 内容生成需要计算资源
4. 存储空间需求

## 技术支持

### 问题反馈
1. 查看日志文件定位问题
2. 检查配置文件是否正确
3. 验证网络连接
4. 更新到最新版本

### 社区支持
- GitHub Issues: 问题反馈
- 文档Wiki: 使用指南
- 示例项目: 参考实现

## 许可证
MIT License - 详见 LICENSE 文件

## 贡献指南
1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 创建Pull Request

---
*技能版本: v1.0*
*最后更新: 2026-02-26*