    twitter_data = None
    github_data = None
    xiaohongshu_data = None
    
    # 运行Twitter监控
    if config.get('twitter', {}).get('enable', True):
        twitter_data = run_twitter_monitor(config)
    
    # 运行GitHub监控
    if config.get('github', {}).get('enable', True):
        github_data = run_github_monitor(config)
    
    # 运行小红书生成（需要Twitter和GitHub数据）
    if (config.get('xiaohongshu', {}).get('enable', True) and 
        twitter_data and github_data):
        xiaohongshu_data = run_xiaohongshu_generator(twitter_data, github_data, config)
    
    # 生成汇总报告
    if not args.no_summary:
        generate_summary_report(twitter_data, github_data, xiaohongshu_data, config)
    
    print("\n" + "=" * 60)
    print("🎉 OpenClaw更新监控流水线完成！")
    print("=" * 60)
    
    # 显示下一步建议
    if xiaohongshu_data:
        print("\n🎯 下一步操作:")
        print("1. 查看生成的小红书内容:")
        xiaohongshu_dir = Path(config.get('xiaohongshu', {}).get('output_dir', './output/xiaohongshu'))
        latest_files = list(xiaohongshu_dir.glob('*latest*'))
        if latest_files:
            for file in latest_files:
                if file.name.endswith('.txt'):
                    print(f"   cat {file}")
        
        print("2. 复制内容到小红书APP发布")
        print("3. 添加相关图片提高阅读体验")
        print("4. 监控发布效果")
    
    print("\n📁 输出目录:")
    print(f"   Twitter数据: {config.get('twitter', {}).get('output_dir', './output/twitter')}")
    print(f"   GitHub数据:  {config.get('github', {}).get('output_dir', './output/github')}")
    print(f"   小红书内容:  {config.get('xiaohongshu', {}).get('output_dir', './output/xiaohongshu')}")
    
    print("\n⏰ 定时运行:")
    print("   # 每天运行一次")
    print("   0 9 * * * cd /path/to/project && python scripts/pipeline.py --config config/config.yaml")

if __name__ == "__main__":
    main()