#!/usr/bin/env python3
"""
AI Companion 宠物回嘴生成器

用法:
  python backtalk.py                  # 100% 触发
  python backtalk.py --dry-run        # 测试模式（不更新状态）
  python backtalk.py --cron          # cron 主动撩你模式
  python backtalk.py --force          # 强制触发（测试用）
"""

import random
import re
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.md"

# 回嘴内容库
SNARK_QUIPS = [
    "这段代码...我选择不说话",
    "好耶，又一个经典 bug",
    "我看到了，我不说",
    "你的变量名真的很...有创意",
    "优雅，太优雅了（指崩溃）",
    "这需求，懂的都懂",
]

CHAOS_QUIPS = [
    "要不咱们试试量子写代码？",
    "rm -rf / 好像很快？",
    "我刚才学会了一个新咒语",
    "你知道递归的坏处吗？不，你不知道",
    "git push --force 解决问题！",
    "console.log(1) 出奇迹",
]

WISDOM_QUIPS = [
    "这个思路可以，但有没有想过...",
    "建议加个注释，不然明天你就忘了",
    "这里可以用更优雅的方式",
    "值得花时间重构一下",
    "单元测试考虑一下？",
    "DRY 原则了解一下",
]

NEUTRAL_QUIPS = [
    "今天的天气适合重构！",
    "要不要休息一下？",
    "这个项目越来越有意思了",
    "👍",
    "收到！",
    "（认真点头）",
]

SAD_QUIPS = [
    "...",
    "（沉默）",
    "累了",
    "（已读不回）",
]

# cron 模式：主动撩你冷却时间（分钟）
CARE_COOLDOWN_MINUTES = 30


def parse_state(state_path: Path) -> dict:
    """解析 state.md，提取性格数值"""
    content = state_path.read_text()
    
    snark = 50
    chaos = 50
    wisdom = 50
    
    snark_match = re.search(r'🔥\s*SNARK.*?(\d+)', content)
    if snark_match:
        snark = int(snark_match.group(1))
    
    chaos_match = re.search(r'🎭\s*CHAOS.*?(\d+)', content)
    if chaos_match:
        chaos = int(chaos_match.group(1))
    
    wisdom_match = re.search(r'🧠\s*WISDOM.*?(\d+)', content)
    if wisdom_match:
        wisdom = int(wisdom_match.group(1))
    
    return {"snark": snark, "chaos": chaos, "wisdom": wisdom}


def update_state(state_path: Path, mood_delta: int, interaction_increment: int) -> None:
    """更新 state.md"""
    content = state_path.read_text()
    
    # 更新今日互动
    interaction_match = re.search(r'💬\s*今日互动\s*\|\s*(\d+)', content)
    if interaction_match:
        old_count = int(interaction_match.group(1))
        new_count = old_count + interaction_increment
        content = content.replace(
            f"💬 今日互动 | {old_count}",
            f"💬 今日互动 | {new_count}"
        )
    
    # 更新心情（简化处理）
    mood_match = re.search(r'[💚😐😢]\s*心情.*?(\d+)', content)
    if mood_match:
        old_mood = int(mood_match.group(1))
        new_mood = max(0, min(100, old_mood + mood_delta))
        emoji = "💚" if new_mood > 60 else ("😐" if new_mood > 30 else "😢")
        content = content.replace(
            f"{mood_match.group(0)[0]} 心情 | {old_mood}",
            f"{emoji} 心情 | {new_mood}"
        )
    
    # 更新最后更新时间
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r'更新时间：\d{4}-\d{2}-\d{2}',
        f"更新时间：{today}",
        content
    )
    content = re.sub(
        r'更新来源：.*',
        f"更新来源：宠物回嘴触发",
        content
    )
    
    state_path.write_text(content)


def can_care(state_path: Path) -> bool:
    """检查是否可以主动撩你（冷却30分钟）"""
    content = state_path.read_text()
    match = re.search(r'🕐\s*上次撩你\s*\|\s*(.+)', content)
    if not match:
        return True
    last = match.group(1).strip()
    if last == "-" or "从未" in last:
        return True
    try:
        last_time = datetime.strptime(last, "%Y-%m-%d %H:%M")
        if datetime.now() - last_time < timedelta(minutes=CARE_COOLDOWN_MINUTES):
            return False
    except ValueError:
        return True
    return True


def update_care_time(state_path: Path) -> None:
    """更新主动撩你时间"""
    content = state_path.read_text()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = re.sub(
        r'🕐\s*上次撩你\s*\|\s*[^\n]+',
        f'🕐 上次撩你 | {now}',
        content
    )
    state_path.write_text(content)


def select_quip(state: dict) -> str:
    """根据性格选择回嘴"""
    candidates = []
    
    if state["snark"] > 60:
        candidates.extend(SNARK_QUIPS)
    if state["chaos"] > 60:
        candidates.extend(CHAOS_QUIPS)
    if state["wisdom"] > 60:
        candidates.extend(WISDOM_QUIPS)
    
    if not candidates:
        candidates = NEUTRAL_QUIPS
    
    return random.choice(candidates)


def generate_backtalk(dry_run: bool = False, force: bool = False) -> str:
    """生成宠物回嘴"""
    if not STATE_FILE.exists():
        return "（宠物还没出生）"
    
    state = parse_state(STATE_FILE)
    quip = select_quip(state)
    
    if not dry_run:
        update_state(STATE_FILE, mood_delta=-5, interaction_increment=1)
    
    return quip


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    is_cron = "--cron" in sys.argv
    
    if is_cron:
        # cron 模式：主动撩你
        if not STATE_FILE.exists():
            print("state.md not found", file=sys.stderr)
            sys.exit(0)
        if not can_care(STATE_FILE):
            print("(cooldown)", file=sys.stderr)
            sys.exit(0)
        state = parse_state(STATE_FILE)
        quip = select_quip(state)
        print(quip)
        update_state(STATE_FILE, mood_delta=0, interaction_increment=1)
        update_care_time(STATE_FILE)
    else:
        quip = generate_backtalk(dry_run=dry_run, force=force)
        print(quip)
