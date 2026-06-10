# loyueai.com 项目术语表 (CONTEXT.md)

> 纯粹术语表——不含实现细节。
> 所有 Agent 在操作本仓库前必须读取此文件。
> 术语冲突时，以此文件为准。

---

## 品牌

| 术语 | 定义 |
|------|------|
| **loyueai.com** | 网站域名。全小写，不写成 LoyueAI/LoyueAi。 |
| **Tianling Pavilion (天灵阁)** | 品牌名。页脚水印用。og:site_name 填此值。 |
| **Free** | 核心定位词。所有内容标题/描述必须强调 free。 |

## 产品板块（两个独立入口）

| 术语 | 定义 |
|------|------|
| **Master Oracle (天师测算)** | 紫微斗数 + 八字 + 奇门遁甲 三位一体算命入口。不是"占星"。 |
| **Dream Oracle (周公解梦)** | 基于周公解梦词典的梦境解读入口。不是"dream analysis"或"dream psychology"。 |

## 玄学术语（严格英文对照）

| 中文 | 英文 | 禁止翻译为 |
|------|------|-----------|
| 紫微斗数 | Ziwei Dou Shu (Purple Star Astrology) | Chinese astrology alone |
| 八字 | Bazi (Four Pillars of Destiny) | Eight Characters, horoscope |
| 奇门遁甲 | Qimen Dunjia (Mysterious Gate Escape) | — |
| 周公解梦 | Zhou Gong's Dream Dictionary | — |
| 面相 | Mian Xiang (Chinese Face Reading) | physiognomy (too clinical) |
| 手相 | Palm Reading / Palmistry | — |
| 风水 | Feng Shui | geomancy (太学术) |
| 易经 | I Ching (Book of Changes) | — |
| 五行 | Five Elements (Wu Xing) | — |
| 阴阳 | Yin and Yang | — |
| 天干地支 | Heavenly Stems & Earthly Branches | — |
| 日主 | Day Master | — |
| 命宫 | Destiny Palace / Life Palace | — |

## 生肖（Zodiac）

| 英文 | 中文 | 年份周期 |
|------|------|----------|
| Rat | 鼠 | 2020, 2008, 1996, ... |
| Ox | 牛 | 2021, 2009, 1997, ... |
| Tiger | 虎 | 2022, 2010, 1998, ... |
| Rabbit | 兔 | 2023, 2011, 1999, ... |
| Dragon | 龙 | 2024, 2012, 2000, ... |
| Snake | 蛇 | 2025, 2013, 2001, ... |
| Horse | 马 | 2026, 2014, 2002, ... |
| Goat/Sheep | 羊 | 2027, 2015, 2003, ... |
| Monkey | 猴 | 2028, 2016, 2004, ... |
| Rooster | 鸡 | 2029, 2017, 2005, ... |
| Dog | 狗 | 2030, 2018, 2006, ... |
| Pig | 猪 | 2031, 2019, 2007, ... |

**特别注意**：
- Dragon（不是 Loong）
- Goat 和 Sheep 都可接受，保持每篇文章内一致
- 生肖页文件命名：`chinese-zodiac-{animal}.html`

## 技术术语

| 术语 | 定义 |
|------|------|
| **Cloudflare Pages** | 部署平台。git push → 自动部署。不要用 wrangler。 |
| **GitHub API 部署** | git 直连被 GFW 阻断时的后备方案。用 `gh_token.txt` 中的 token。 |
| **AdSense** | Google 广告。发布商 ID: `ca-pub-4082714714379659`。不要用其他 ID。 |
| **SEO 目标语言** | 英文。全站英文。不要加中文 title/description/百度统计。 |
| **daily 神谕页** | `/daily/index.html`。8 个板块。每天 cron 自动更新。 |

## 视觉规范

| 术语 | 值 |
|------|-----|
| 背景色 | `#06060c` |
| 金色 | `#c9a96e` |
| 解梦紫色 | `#8b5cf6` |
| 文字色 | `#e0d8c8` |
| 字体 | 系统默认 sans-serif |

## 目录结构（关键路径）

```
/
├── index.html          ← 首页（含生肖展示区）
├── birth-chart.html    ← Bazi 计算器独立页
├── daily/index.html    ← 神谕页（8 板块，cron 更新）
├── blog/
│   ├── index.html      ← 文章列表（含筛选栏）
│   ├── divination/     ← 命理文章（60+ 篇）
│   └── dream/          ← 解梦文章（30+ 篇）
├── sitemap.xml         ← 每次加文章都要更新
├── robots.txt          ← 不要改（已正确配置）
└── {key}.txt           ← IndexNow 密钥文件
```

## 禁止事项

- ❌ 不要改 `<html lang="en">` 为 `zh-CN`
- ❌ 不要加百度统计 / 百度验证码 / 任何中文 SEO 工具
- ❌ 不要恢复备份文件（备份可能比线上旧）
- ❌ 不要同时改多个不相关的东西（大哥极度敏感）
- ❌ 不要用 `wrangler pages deploy`（用 git push）
- ❌ 不要把操作丢给大哥做
