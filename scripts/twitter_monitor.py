#!/usr/bin/env python3
"""
Twitter监控脚本
获取OpenClaw官方Twitter更新内容
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import requests

def fetch_tweet(tweet_id: str) -> Optional[Dict[str, Any]]:
    """
    通过FxTwitter API获取单条推文
    
    Args:
        tweet_id: 推文ID
        
    Returns:
        推文数据字典，失败返回None
    """
    api_url = f"https://api.fxtwitter.com/openclaw/status/{tweet_id}"
    
    try:
        headers = {
            'User-Agent': 'OpenClaw-Update-Monitor/1.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('code') != 200:
            print(f"API错误: {data.get('message', '未知错误')}")
            return None
        
        tweet = data['tweet']
        
        # 提取关键信息
        result = {
            'tweet_id': tweet_id,
            'username': tweet.get('author', {}).get('screen_name', ''),
            'text': tweet.get('text', ''),
            'created_at': tweet.get('created_at', ''),
            'likes': tweet.get('likes', 0),
            'retweets': tweet.get('retweets', 0),
            'views': tweet.get('views', 0),
            'replies': tweet.get('replies', 0),
            'bookmarks': tweet.get('bookmarks', 0),
            'is_note_tweet': tweet.get('is_note_tweet', False),
            'lang': tweet.get('lang', ''),
            'source': 'twitter',
            'fetched_at': datetime.now().isoformat()
        }
        
        # 如果有媒体内容
        if tweet.get('media'):
            result['media'] = tweet['media']
        
        # 如果有引用推文
        if tweet.get('quote'):
            result['quote'] = tweet['quote']
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return None
    except KeyError as e:
        print(f"数据格式错误，缺少键: {e}")
        return None

def translate_tweet_text(text: str) -> str:
    """
    简单的中文翻译函数
    实际使用时可以替换为真正的翻译API
    
    Args:
        text: 英文推文文本
        
    Returns:
        中文翻译文本
    """
    # 这里使用简单的关键词替换
    # 实际应该使用翻译API如Google Translate、DeepL等
    
    translations = {
        'OpenClaw': 'OpenClaw',
        'Stop phrases': '停止短语',
        'languages': '语言',
        'your bot finally understands': '你的机器人终于能理解',
        'Typing indicators': '输入指示器',
        "don't ghost you": '不会消失',
        'PowerShell 7': 'PowerShell 7',
        "it's not 2019": '现在不是2019年了',
        'security fixes': '安全修复',
        "we don't sleep so you can": '我们不睡觉，这样你才能安心',
        'Updating is self-care': '更新就是自我关爱'
    }
    
    translated = text
    for eng, chi in translations.items():
        translated = translated.replace(eng, chi)
    
    return translated

def is_version_update(tweet_text: str) -> bool:
    """
    判断是否是版本更新推文
    
    Args:
        tweet_text: 推文文本
        
    Returns:
        是否是版本更新
    """
    patterns = [
        r'v?\d{4}\.\d{1,2}\.\d{1,2}',  # v2026.2.24 或 2026.2.24
        r'version\s+\d+',
        r'release\s+\d',
        r'更新|升级|发布|版本',
        r'update|release|version',
    ]
    
    for pattern in patterns:
        if re.search(pattern, tweet_text, re.IGNORECASE):
            return True
    
    return False

def extract_version_info(tweet_text: str) -> Optional[str]:
    """
    从推文中提取版本信息
    
    Args:
        tweet_text: 推文文本
        
    Returns:
        版本号字符串，未找到返回None
    """
    patterns = [
        r'v?(\d{4}\.\d{1,2}\.\d{1,2})',  # v2026.2.24
        r'version\s+(\d+\.\d+\.\d+)',
        r'release\s+(\d+\.\d+\.\d+)',
        r'v(\d+)\.(\d+)\.(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, tweet_text, re.IGNORECASE)
        if match:
            if match.groups():
                # 如果有分组，使用第一个分组
                return match.group(1)
            else:
                # 如果没有分组，使用整个匹配
                return match.group(0)
    
    return None

def save_tweet_data(tweet_data: Dict[str, Any], output_dir: Path) -> Path:
    """
    保存推文数据到文件
    
    Args:
        tweet_data: 推文数据
        output_dir: 输出目录
        
    Returns:
        保存的文件路径
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    tweet_id = tweet_data['tweet_id']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # JSON文件
    json_file = output_dir / f"tweet_{tweet_id}_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(tweet_data, f, ensure_ascii=False, indent=2)
    
    # 文本文件（便于查看）
    txt_file = output_dir / f"tweet_{tweet_id}_{timestamp}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"推文ID: {tweet_data['tweet_id']}\n")
        f.write(f"用户名: @{tweet_data['username']}\n")
        f.write(f"发布时间: {tweet_data['created_at']}\n")
        f.write(f"点赞: {tweet_data['likes']} | 转推: {tweet_data['retweets']} | 浏览: {tweet_data.get('views', 'N/A')}\n")
        f.write("=" * 50 + "\n")
        f.write("原文:\n")
        f.write(tweet_data['text'] + "\n")
        f.write("=" * 50 + "\n")
        
        # 如果有翻译
        if 'translated_text' in tweet_data:
            f.write("中文翻译:\n")
            f.write(tweet_data['translated_text'] + "\n")
            f.write("=" * 50 + "\n")
    
    # 更新最新文件
    latest_file = output_dir / "latest_tweet.json"
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump(tweet_data, f, ensure_ascii=False, indent=2)
    
    return json_file

def load_known_tweets(tweets_file: Path) -> list:
    """
    加载已知推文ID列表
    
    Args:
        tweets_file: 推文ID文件路径
        
    Returns:
        推文ID列表
    """
    if not tweets_file.exists():
        return []
    
    tweet_ids = []
    with open(tweets_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # 格式: tweet_id|checked_date|version|title
                parts = line.split('|')
                if parts and parts[0].isdigit():
                    tweet_ids.append(parts[0])
    
    return tweet_ids

def update_known_tweets(tweets_file: Path, tweet_id: str, version: str = None, title: str = None):
    """
    更新已知推文数据库
    
    Args:
        tweets_file: 推文ID文件路径
        tweet_id: 推文ID
        version: 版本号（可选）
        title: 标题（可选）
    """
    tweets_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取现有内容
    lines = []
    if tweets_file.exists():
        with open(tweets_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    # 检查是否已存在
    exists = False
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith('#'):
            parts = line.strip().split('|')
            if parts and parts[0] == tweet_id:
                # 更新现有记录
                today = datetime.now().strftime('%Y-%m-%d')
                new_line = f"{tweet_id}|{today}|{version or parts[2] if len(parts) > 2 else ''}|{title or parts[3] if len(parts) > 3 else ''}"
                lines[i] = new_line + '\n'
                exists = True
                break
    
    # 如果不存在，添加新记录
    if not exists:
        today = datetime.now().strftime('%Y-%m-%d')
        new_line = f"{tweet_id}|{today}|{version or ''}|{title or ''}"
        lines.append(new_line + '\n')
    
    # 写回文件
    with open(tweets_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Twitter更新监控')
    parser.add_argument('--tweet-id', help='推文ID')
    parser.add_argument('--tweet-file', help='推文ID文件，每行一个ID')
    parser.add_argument('--output-dir', default='./output/twitter', help='输出目录')
    parser.add_argument('--translate', action='store_true', help='启用中文翻译')
    parser.add_argument('--update-db', action='store_true', help='更新推文数据库')
    parser.add_argument('--config', default='./config/config.yaml', help='配置文件路径')
    
    args = parser.parse_args()
    
    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取推文ID列表
    tweet_ids = []
    
    if args.tweet_id:
        tweet_ids.append(args.tweet_id)
    
    if args.tweet_file:
        tweet_file = Path(args.tweet_file)
        if tweet_file.exists():
            tweet_ids.extend(load_known_tweets(tweet_file))
    
    # 如果没有指定ID，使用默认的已知ID
    if not tweet_ids:
        config_dir = Path(__file__).parent.parent / 'config'
        known_tweets_file = config_dir / 'twitter_ids.txt'
        tweet_ids = load_known_tweets(known_tweets_file)
    
    if not tweet_ids:
        print("错误：未指定推文ID")
        sys.exit(1)
    
    print(f"开始监控 {len(tweet_ids)} 条推文...")
    
    results = []
    
    for tweet_id in tweet_ids:
        print(f"\n处理推文ID: {tweet_id}")
        
        # 获取推文数据
        tweet_data = fetch_tweet(tweet_id)
        
        if not tweet_data:
            print(f"  ❌ 获取失败")
            continue
        
        print(f"  ✅ 获取成功: {tweet_data['created_at']}")
        
        # 检查是否是版本更新
        if is_version_update(tweet_data['text']):
            print(f"  🎯 检测到版本更新")
            version = extract_version_info(tweet_data['text'])
            if version:
                print(f"     版本号: {version}")
                tweet_data['version'] = version
        
        # 翻译
        if args.translate:
            translated = translate_tweet_text(tweet_data['text'])
            tweet_data['translated_text'] = translated
            print(f"  📝 已翻译")
        
        # 保存数据
        saved_file = save_tweet_data(tweet_data, output_dir)
        print(f"  💾 已保存: {saved_file}")
        
        # 更新数据库
        if args.update_db:
            config_dir = Path(__file__).parent.parent / 'config'
            known_tweets_file = config_dir / 'twitter_ids.txt'
            
            version = tweet_data.get('version')
            title = f"OpenClaw {version}发布" if version else "OpenClaw更新"
            
            update_known_tweets(known_tweets_file, tweet_id, version, title)
            print(f"  📋 数据库已更新")
        
        results.append(tweet_data)
        
        # 避免请求过快
        time.sleep(1)
    
    # 生成汇总报告
    if results:
        summary_file = output_dir / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Twitter监控汇总报告\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"处理推文数: {len(results)}\n\n")
            
            f.write("## 推文列表\n\n")
            for tweet in results:
                f.write(f"### 推文ID: {tweet['tweet_id']}\n")
                f.write(f"- 用户名: @{tweet['username']}\n")
                f.write(f"- 发布时间: {tweet['created_at']}\n")
                f.write(f"- 互动数据: 👍{tweet['likes']} 🔄{tweet['retweets']} 👁️{tweet.get('views', 'N/A')}\n")
                
                if 'version' in tweet:
                    f.write(f"- 版本号: {tweet['version']}\n")
                
                f.write(f"- 内容预览: {tweet['text'][:100]}...\n\n")
        
        print(f"\n📊 汇总报告: {summary_file}")
    
    print(f"\n✅ Twitter监控完成，处理 {len(results)}/{len(tweet_ids)} 条推文")

if __name__ == "__main__":
    main()