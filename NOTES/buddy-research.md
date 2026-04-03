# Claude Code Buddy 研究笔记

## 来源

- Reddit 讨论（2026-03-31 ~ 2026-04-02）
- 官方文档 + 非官方分析

## 核心功能

### 激活方式
- 在 Claude Code 终端输入 `/buddy`
- 基于账号 ID deterministic 生成宠物，每次孵化相同

### 形象系统
- ASCII art 角色（18-20 种物种）
- 空闲时有动画（3帧循环）
- 物种：乌龟（Quibble）、企鹅（Rune）、猫头鹰、鸭子、水豚等

### 稀有度
- Common → Uncommon → Rare → Epic → Legendary

### 性格系统
- SNARK（吐槽指数）
- WISDOM（智慧指数）
- CHAOS（搞怪指数）
- 每个宠物数值不同，影响反应

### 行为
- 坐在 prompt 旁边
- 看你的 coding session
- 对代码错误吐槽（speech bubbles）
- 对你和 Claude 的互动做出反应

### 发布时间
- 2026-03-31：源码泄露被发现
- 2026-04-01：正式激活（原为愚人节彩蛋，因反响好保留）

## 值得借鉴的点

1. **确定性生成**（账号 ID → 宠物属性）
   - 可复现，有唯一感

2. **稀有度系统**
   - 增加收集感

3. **ASCII 形象 + 动画**
   - 轻量，不依赖图片

4. **性格数值影响行为**
   - 同样是 error，不同性格的宠物反应不同

5. ** sitting in terminal prompt**
   - 存在感强，不打扰但一直都在

## 小修的差距

| 维度 | Claude Code Buddy | 小修（当前） |
|------|------------------|-------------|
| 形象 | ASCII 动画 | 无 |
| 物种 | 18-20种 | 未定 |
| 稀有度 | 5级 | 无 |
| 性格 | 3维数值 | 3维（未激活） |
| 存在感 | prompt旁 | Telegram 消息 |
| 主动互动 | 吐槽代码 | 无 |

## 待办

- [ ] 确定小修的物种/形象
- [ ] 设计孵化机制
- [ ] 实现性格数值影响行为
- [ ] 设计互动反馈

## 参考链接

- https://www.reddit.com/r/ClaudeAI/comments/1s9adgd/claude_code_is_coming_out_with_a_buddypet_system
- https://smartscope.blog/en/generative-ai/claude/claude-code-buddy-ai-companion
