---
title: Pixel Watch 2 Demo 展示機改回正常零售版系統
date: 2025-09-22
categories: [Android]
tags: [Android, Pixel]

---

# Pixel Watch 2 Demo 展示機改回正常零售版系統


前言
---
[@HikariCalyx](https://t.me/HCT_Nekobot) 在今年 3 月中收到 2 隻 Pixel Watch 2 展示機，我當時就向他詢問是否可以給我一隻玩玩XD

![image](/assets/img/posts/H1YYyhGnxl.png)

在我 6 月底飛去上海玩的時候，就讓光卡寄到我的酒店，讓我帶回台灣。
感謝光卡寄了兩隻給我，而我在 8 月中去香港玩的時候，就又寄了一隻去給 [@MlgmXyysd](https://GitHub.com/MlgmXyysd)

![image](/assets/img/posts/HJzVCiG2gl.png)


研究過程
---
當我嘗試想要解鎖 bootloader 時，發現無法進入開發人員選項開啟 OEM 解鎖，因此還是得要繞一圈回來先解決眼前的 Demo Mode 才行

進到 bootloader 之後發現一個很可疑的項目欄位 `bootmode`
![image](/assets/img/posts/SJ_FRsf2le.png)

然而，修改 bootmode 則需要 unlock bootloader，而我也無法透過正常方式解鎖 bootloader，完全陷入了無窮迴圈。

在 8 月底的時候，光卡說他使用了編程器，拆機解了一台 Pixel Watch 2 展示機
![image](/assets/img/posts/r1V6ZhM3eg.png)

Ref:  
[1] https://xdaforums.com/t/pixel-2-watch-in-demo-mode.4671420/  
[2] https://support.google.com/googlepixelwatch/thread/288732630/my-pixel-watch-2-is-stuck-in-demo-mode-the-device-status-in-fastboot-is-locked?hl=en

解鎖 / 改回正常零售版系統
---
就在今天，光卡又告訴我 pixelunlocktool.com 可以解鎖美版有鎖 Pixel 以及 Pixel Watch 展示機

| ![image](/assets/img/posts/rJYzInz3lx.png) | ![image](/assets/img/posts/SyG4U3fhll.png) |
| --------------------------------------------------- | --------------------------------------------------- |
| ![image](/assets/img/posts/By3uInGnel.png) | ![image](/assets/img/posts/Hkt6IhG2gl.png) |

在光卡幫我解鎖完成之後，我便使用我先前發現到的指令修改了 bootmode，讓這一台 Pixel Watch 2 回到正常的版本做使用了。

![image](/assets/img/posts/BJuBv3Gnxg.png)
![image](/assets/img/posts/rJQ8D2z3xg.png)


About Me
---
我是 EdwardWu
- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram : [_920223](https://www.instagram.com/_920223/)
- GitHub : [bluehomewu](https://github.com/bluehomewu)
- Email : [bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)

![image](/assets/img/posts/Bk1EYGfYA.png)

###### tags: `Android` `Pixel` `Pixel Watch 2` `ROM` `Google Pixel` `Google Pixel Watch 2`
