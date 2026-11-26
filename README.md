# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/lhj289902417-glitch/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/lhj289902417-glitch/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

这是一张 2026 年 11 月 26 日（星期四）世界新闻的一图总结：同一天里值得记住的六件事，被排进一张 1024x1024 的头版海报。`main.py` 用 PIL 从零绘制整张海报——深青色报头、头条配一张关税对比小图、其余五条新闻排成编号卡片——运行后把图写到 `/output/entry.png`，仓库里也留了一份 `entry.png`。

## 海报上的六条新闻

- 美国拟对印度商品加征 25% 关税；若两国达成贸易协议，税率可降至 17%。
- 特朗普称自己促成黄仁勋回归英伟达后，可能赦免黄仁勋；万斯公开为黄仁勋辩护。
- 也门胡塞武装再次袭击利雅得；霍尔木兹海峡油轮遇袭，伊朗称油轮触水雷。
- 导弹坠落后北约加强东翼空中监视；俄军机接近，韩国发布疏散警告。
- 巴基斯坦宇航员搭乘中国神舟二十四号升空，成为首位登上中国空间站的外籍宇航员。
- 15 岁印度新星 Vaibhav Sooryavanshi 对阵阿联酋，53 球轰下 204 分，创世界纪录。

新闻来源：当日各大通讯社与主流媒体的公开报道（路透社、美联社、法新社等）。

## 本地运行

```sh
python3 main.py
```

跑完之后，`/output/entry.png` 就是画好的海报；同一份图也保存在仓库根目录的 `entry.png`。程序不联网、两次运行输出逐字节相同。
