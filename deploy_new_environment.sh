#!/bin/bash
# OpenClaw更新监控系统 - 新环境一键部署脚本

set -e  # 遇到错误立即退出

echo "🚀 OpenClaw更新监控系统部署开始"
echo "========================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数：打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 阶段1：检查环境
print_info "阶段1：检查系统环境"

# 检查Python
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version | awk '{print $2}')
    print_info "Python3 已安装: $python_version"
else
    print_error "Python3 未安装，正在安装..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
fi

# 检查Git
if command -v git &> /dev/null; then
    git_version=$(git --version | awk '{print $3}')
    print_info "Git 已安装: $git_version"
else
    print_error "Git 未安装，正在安装..."
    sudo apt-get install -y git
fi

# 检查pip
if command -v pip3 &> /dev/null; then
    print_info "pip3 已安装"
else
    print_error "pip3 未安装，正在安装..."
    sudo apt-get install -y python3-pip
fi

# 阶段2：配置代理（可选）
print_info "阶段2：配置网络代理"
read -p "是否需要配置代理？(y/n): " need_proxy

if [[ $need_proxy == "y" || $need_proxy == "Y" ]]; then
    read -p "请输入代理地址（如 http://proxy.example.com:8080）: " proxy_url
    
    # 设置环境变量
    export HTTP_PROXY="$proxy_url"
    export HTTPS_PROXY="$proxy_url"
    
    # 设置Git代理
    git config --global http.proxy "$proxy_url"
    git config --global https.proxy "$proxy_url"
    
    print_info "代理已配置: $proxy_url"
else
    print_info "跳过代理配置"
fi

# 阶段3：获取项目代码
print_info "阶段3：获取项目代码"

# 检查是否已存在项目
if [ -d "openclaw-update-monitor" ]; then
    print_warn "项目目录已存在，跳过克隆"
    cd openclaw-update-monitor
    git pull origin main
else
    # 克隆项目
    print_info "正在克隆项目..."
    git clone git@github.com:huazhoufang789-gif/openclaw-.git openclaw-update-monitor
    cd openclaw-update-monitor
    
    # 检查克隆是否成功
    if [ $? -eq 0 ]; then
        print_info "项目克隆成功"
    else
        print_error "项目克隆失败，尝试使用HTTPS..."
        git clone https://github.com/huazhoufang789-gif/openclaw-.git openclaw-update-monitor
        cd openclaw-update-monitor
    fi
fi

# 阶段4：安装依赖
print_info "阶段4：安装Python依赖"

# 安装基础依赖
pip3 install requests pyyaml --user

# 检查安装结果
if python3 -c "import requests, yaml; print('依赖检查通过')" &> /dev/null; then
    print_info "Python依赖安装成功"
else
    print_error "Python依赖安装失败"
    exit 1
fi

# 阶段5：项目配置
print_info "阶段5：项目配置"

# 创建配置文件
if [ ! -f "config/config.yaml" ]; then
    cp config/config.example.yaml config/config.yaml
    print_info "配置文件已创建: config/config.yaml"
    print_warn "请编辑配置文件设置你的参数"
else
    print_info "配置文件已存在"
fi

# 创建输出目录
mkdir -p output/twitter output/github output/xiaohongshu logs

# 阶段6：OpenClaw集成（可选）
print_info "阶段6：OpenClaw集成"
read -p "是否集成到OpenClaw？(y/n): " integrate_openclaw

if [[ $integrate_openclaw == "y" || $integrate_openclaw == "Y" ]]; then
    # 检查OpenClaw是否安装
    if command -v openclaw &> /dev/null; then
        print_info "OpenClaw 已安装"
        
        # 安装技能
        if [ -d "skills/xiaohongshu-poster" ]; then
            openclaw skills install ./skills/xiaohongshu-poster
            print_info "小红书发布助手技能已安装"
        else
            print_warn "技能目录不存在，跳过技能安装"
        fi
        
        # 配置环境变量
        echo "export OPENCLAW_WORKSPACE=$(pwd)" >> ~/.bashrc
        echo "export OPENCLAW_CONFIG=$(pwd)/config/config.yaml" >> ~/.bashrc
        source ~/.bashrc
        print_info "OpenClaw环境变量已配置"
    else
        print_warn "OpenClaw 未安装，跳过集成"
        print_info "你可以稍后手动安装: https://docs.openclaw.ai/installation"
    fi
else
    print_info "跳过OpenClaw集成"
fi

# 阶段7：端口配置（如果需要）
print_info "阶段7：端口配置"
read -p "OpenClaw是否运行在非标准端口？(y/n): " custom_port

if [[ $custom_port == "y" || $custom_port == "Y" ]]; then
    read -p "请输入OpenClaw网关端口（默认8080）: " gateway_port
    gateway_port=${gateway_port:-8080}
    
    read -p "请输入WebChat端口（默认3000）: " webchat_port
    webchat_port=${webchat_port:-3000}
    
    # 创建端口配置文件
    cat > openclaw_ports.env << EOF
# OpenClaw端口配置
OPENCLAW_GATEWAY_PORT=$gateway_port
OPENCLAW_WEBCHAT_PORT=$webchat_port
OPENCLAW_GATEWAY_URL=http://localhost:$gateway_port
EOF
    
    print_info "端口配置文件已创建: openclaw_ports.env"
    print_info "请根据此配置调整OpenClaw服务"
fi

# 阶段8：测试运行
print_info "阶段8：测试运行"

# 测试Twitter监控
print_info "测试Twitter监控..."
python3 scripts/twitter_monitor.py --tweet-id 2026503611514069173 --translate

if [ $? -eq 0 ]; then
    print_info "Twitter监控测试通过"
else
    print_warn "Twitter监控测试失败（可能是网络问题）"
fi

# 测试GitHub监控
print_info "测试GitHub监控..."
python3 scripts/github_monitor.py --latest --translate

if [ $? -eq 0 ]; then
    print_info "GitHub监控测试通过"
else
    print_warn "GitHub监控测试失败（可能是网络问题）"
fi

# 阶段9：创建自动化脚本
print_info "阶段9：创建自动化脚本"

# 创建运行脚本
cat > run_monitor.sh << 'EOF'
#!/bin/bash
# OpenClaw更新监控运行脚本

cd "$(dirname "$0")"

echo "开始运行OpenClaw更新监控..."
echo "时间: $(date)"

# 运行完整流水线
python3 scripts/pipeline.py --all --config config/config.yaml

echo "监控完成"
echo "时间: $(date)"
EOF

chmod +x run_monitor.sh
print_info "运行脚本已创建: run_monitor.sh"

# 创建定时任务配置
cat > cron_setup.md << 'EOF'
# 定时任务配置

## 每天上午9点运行
```bash
0 9 * * * cd /path/to/openclaw-update-monitor && ./run_monitor.sh >> logs/cron.log 2>&1
```

## 每小时运行（测试用）
```bash
0 * * * * cd /path/to/openclaw-update-monitor && python3 scripts/pipeline.py --all >> logs/hourly.log 2>&1
```

## 添加定时任务
```bash
crontab -e
# 添加上述配置
```

## 查看日志
```bash
tail -f logs/cron.log
```
EOF

print_info "定时任务配置已创建: cron_setup.md"

# 阶段10：完成
print_info "阶段10：部署完成"

echo ""
echo "========================================"
echo "🎉 部署完成！"
echo "========================================"
echo ""
echo "📁 项目目录: $(pwd)"
echo "📋 配置文件: config/config.yaml"
echo "🚀 运行脚本: ./run_monitor.sh"
echo "⏰ 定时任务: 查看 cron_setup.md"
echo ""
echo "🔧 下一步操作:"
echo "1. 编辑 config/config.yaml 配置你的参数"
echo "2. 运行 ./run_monitor.sh 测试完整流程"
echo "3. 设置定时任务自动运行"
echo "4. 查看 output/ 目录获取生成的内容"
echo ""
echo "📞 帮助:"
echo "- 查看 README.md 获取详细文档"
echo "- 运行 python3 scripts/pipeline.py --help 查看帮助"
echo "- 检查 logs/ 目录查看运行日志"
echo ""
echo "GitHub仓库: https://github.com/huazhoufang789-gif/openclaw-"
echo "部署时间: $(date)"
echo "========================================"