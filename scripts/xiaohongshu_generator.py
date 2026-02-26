    # 保存文件
    print("💾 保存文件...")
    files = save_xiaohongshu_content(
        xiaohongshu_data,
        output_dir,
        include_links=args.include_links
    )
    
    print("✅ 文件保存完成:")
    for file_type, file_path in files.items():
        print(f"   {file_type.upper()}: {file_path}")
    
    # 显示内容预览
    print("\n📱 小红书内容预览:")
    print("=" * 60)
    
    lines = xiaohongshu_data['content'].split('\n')
    for i, line in enumerate(lines[:30]):
        if i < 30:
            print(line)
    
    if len(lines) > 30:
        print("...")
        print(f"（完整内容共{len(lines)}行，请查看文件）")
    
    print("=" * 60)
    
    # 生成使用指南
    guide_file = output_dir / f"guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(f"# 小红书发布指南\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 发布内容\n\n")
        f.write(f"**标题**: {xiaohongshu_data['title']}\n\n")
        f.write(f"**版本**: {xiaohongshu_data['version']}\n\n")
        f.write(f"**字符数**: {xiaohongshu_data['character_count']} (小红书建议1000-2000字)\n\n")
        
        f.write("## 发布步骤\n\n")
        f.write("1. **打开小红书APP**\n")
        f.write("2. **点击底部\"+\"按钮**创建新笔记\n")
        f.write("3. **复制以下内容**到笔记编辑区\n")
        f.write("4. **添加相关图片**（建议添加OpenClaw logo或截图）\n")
        f.write("5. **检查标签**是否完整\n")
        f.write("6. **发布笔记**\n\n")
        
        f.write("## 内容预览\n\n")
        f.write("```\n")
        f.write(xiaohongshu_data['content'][:500] + "...\n")
        f.write("```\n\n")
        
        f.write("## 完整文件\n\n")
        f.write(f"- 纯文本文件: {files['txt']}\n")
        f.write(f"- Markdown文件: {files['md']}\n")
        f.write(f"- JSON数据: {files['json']}\n\n")
        
        f.write("## 注意事项\n\n")
        f.write("1. **链接限制**: 小红书不允许外部链接，已自动移除\n")
        f.write("2. **内容审核**: 发布前请确保内容符合社区规范\n")
        f.write("3. **发布时间**: 建议工作日白天发布，效果更好\n")
        f.write("4. **图片建议**: 添加相关图片可提高阅读体验\n")
        f.write("5. **互动引导**: 发布后可引导用户评论和分享\n\n")
        
        f.write("## 标签列表\n\n")
        f.write(", ".join(xiaohongshu_data['tags']) + "\n\n")
        
        f.write("## 数据来源\n\n")
        f.write(f"- Twitter推文ID: {xiaohongshu_data['metadata']['twitter_tweet_id']}\n")
        f.write(f"- GitHub发布版本: {xiaohongshu_data['metadata']['github_release']}\n")
        f.write(f"- 总计更新项数: {xiaohongshu_data['metadata']['total_updates']}\n")
    
    print(f"\n📖 发布指南: {guide_file}")
    
    print("\n🎯 下一步:")
    print("1. 复制纯文本内容到小红书APP")
    print("2. 或按照发布指南操作")
    print("3. 发布时记得添加相关图片")
    print("4. 监控发布效果")

if __name__ == "__main__":
    main()