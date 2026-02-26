  skills/          # OpenClaw技能"

echo ""
echo "🌐 访问地址:"
echo "  - OpenClaw网关: http://localhost:${GATEWAY_PORT} (如果已安装)"
echo "  - OpenClaw Web: http://localhost:${WEBCHAT_PORT} (如果已安装)"

echo ""
echo "📋 下一步操作:"
echo "  1. 查看配置文件: cat config/config.yaml"
echo "  2. 运行完整测试: ./test.sh"
echo "  3. 设置自动化: ./setup_cron.sh"
echo "  4. 查看文档: cat README.md"

echo ""
echo "🔧 故障排除:"
echo "  - 查看日志: tail -f logs/*.log"
echo "  - 网络问题: 检查代理配置"
echo "  - 端口问题: 检查端口占用"

echo ""
echo "📞 获取帮助:"
echo "  - GitHub: https://github.com/huazhoufang789-gif/openclaw-"
echo "  - 查看详细文档: cat 精准部署指南.md"

echo ""
echo "⏰ 部署完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 创建部署完成标记
echo "DEPLOYMENT_COMPLETE=true" > .deployed
echo "DEPLOYMENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')" >> .deployed
echo "PROJECT_DIR=$PROJECT_DIR" >> .deployed
echo "GATEWAY_PORT=$GATEWAY_PORT" >> .deployed
echo "WEBCHAT_PORT=$WEBCHAT_PORT" >> .deployed

print_success "✅ 一键部署完成！"