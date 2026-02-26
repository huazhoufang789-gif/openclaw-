    # 生成汇总报告
    summary_file = output_dir / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"# GitHub发布监控汇总报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"仓库: {args.repo}\n")
        f.write(f"版本: {release_data['tag_name']}\n\n")
        
        f.write("## 发布信息\n\n")
        f.write(f"- **标题**: {release_data['name']}\n")
        f.write(f"- **发布时间**: {release_data['published_at']}\n")
        f.write(f"- **发布页面**: {release_data.get('html_url', 'N/A')}\n")
        f.write(f"- **资源文件**: {len(release_data.get('assets', []))} 个\n\n")
        
        f.write("## 更新统计\n\n")
        f.write(f"- **新增功能**: {len(release_data['changes'])} 项\n")
        f.write(f"- **重大变更**: {len(release_data['breaking_changes'])} 项\n")
        f.write(f"- **缺陷修复**: {len(release_data['fixes'])} 项\n")
        f.write(f"- **总计**: {len(release_data['changes']) + len(release_data['breaking_changes']) + len(release_data['fixes'])} 项更新\n\n")
        
        if 'summary' in release_data:
            f.write("## 翻译信息\n\n")
            f.write(f"- **翻译时间**: {release_data['summary']['translated_at']}\n")
            f.write(f"- **翻译状态**: 已完成\n\n")
        
        f.write("## 文件列表\n\n")
        f.write(f"- 原始数据: {saved_file}\n")
        if args.translate:
            f.write(f"- 翻译数据: {translated_file}\n")
            f.write(f"- 翻译文本: {translated_txt}\n")
        f.write(f"- 汇总报告: {summary_file}\n")
    
    print(f"📊 汇总报告: {summary_file}")
    
    print(f"\n✅ GitHub监控完成")

if __name__ == "__main__":
    main()