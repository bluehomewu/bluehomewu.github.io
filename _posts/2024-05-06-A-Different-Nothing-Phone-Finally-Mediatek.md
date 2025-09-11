---
title: 不同以往的 Nothing Phone：睽違已久的 Mediatek
date: 2024-07-27
categories: [Nothing Tech 產品評測]
tags: [Nothing Tech, Android, Nothing, Nothing Phone 2a, ROM]

---

# 不同以往的 Nothing Phone：睽違已久的 Mediatek

![IMG_20240505_225622578](https://hackmd.io/_uploads/Sk1Uz0BfC.jpg)

前言
---

Hi all 各位好～
我是 Edward，目前是一名業餘的 Android Custom ROM Maintainer
也曾在 SITCON 2021 擔任講者，並分享開放式議程主題 [「從零開始編譯 Android 第三方系統！」](https://sitcon.org/2021/agenda/1c9e74cd-aeeb-4e63-8ec4-af33eff16e7d)

以下是我自己寫過的教學文章
[Android 第三方 ROM 繁體中文編譯教學](https://hackmd.io/@EdwardWu/CompileAndroidCustomROM)
[Android 第三方 Recovery 繁體中文編譯教學](https://hackmd.io/@EdwardWu/CompileARecovery)

轉載文章
[快速上手 Android Custom ROM 適配 - Prebuilt Vendor](https://hackmd.io/@EdwardWu/Prebuilt-bringup)

過去我在 [Nothing Phone (1) 的上手體驗文](https://hackmd.io/@EdwardWu/Spacewar_review) 當中有說到，Nothing Tech 有把 Kernel Sources 進行開源，遵循 GPL 協議。
直到現在 Nothing Tech 已經推出了第三款手機，也有持續地在更新維護 Kernel Sources，這也讓 Nothing Tech 這個品牌持續地在開發者社群當中保有一定的聲量以及讚譽。
也因此我對 Nothing Tech 的這個品牌形象，抱持著相當高的期許。期待 Nothing Tech 端出好吃的牛肉。


Nothing Phone (2a)
---
### 硬體規格

以下簡單用表格列出此次 Nothing Phone (2a) 的一些規格參數

[參考來源](https://www.gsmarena.com/nothing_phone_(2a)-12760.php)

| Feature                 | Specification                                                                  |
|:----------------------- |:------------------------------------------------------------------------------ |
| Chipset                 | Mediatek Dimensity 7200 Pro (4 nm)                                             |
| CPU                     | Octa-core (2x2.8 GHz Cortex-A715 & 6x 2.0 Cortex-A510)                         |
| GPU                     | Mali-G610 MC4                                                                  |
| Memory                  | 8GB/12GB                                                                       |
| Shipped Android Version | 14, Nothing OS 2.5.1A                                                           |
| Storage                 | 128/256 GB UFS 2.1                                                             |
| SIM                     | Dual SIM (Nano-SIM, dual stand-by)                                             |
| Battery                 | Li-Po 5000 mAh, non-removable                                                  |
| Dimensions              | 161.7 x 76.3 x 8.6 mm (6.37 x 3.00 x 0.34 in)                                  |
| Display                 | 6.7 inches, 1080 x 2412 pixels, 20:9 ratio                                     |
| Rear Camera 1           | 50 MP, f/1.9, (wide), 1/1.56", PDAF, OIS                                       |
| Rear Camera 2           | 50 MP, f/2.2, 114˚ (ultrawide), 1/2.76", 0.64µm                                |
| Front Camera            | 32 MP, f/2.2, (wide), 1/2.74", HDR, 1080p@60fps                                |
| Sensors                 | Fingerprint (under display, optical), accelerometer, gyro, proximity, compass  |


自從 Nothing Phone (1) 在台上市之後，我便經常留意 Nothing Tech 的許多新聞以及 [Discord](https://discord.com/invite/nothingtech) 上的最新資訊。
感謝過去 Nothing Tech Taiwan，提供 Nothing Phone (1)，讓我可以嘗鮮體驗，因此在後來我也深深成為 Nothing Tech 的粉絲之一，也自費購入 Nothing Phone (2)作為我的副機，後續也購入 Nothing Ear (2) 作為我的通勤必備物件。
這次 Nothing Phone (2a) 在台上市一共推出 2 個顏色，分別為白色以及黑色。這次我所拿到的顏色為黑色。鏡頭擺放方式為橫式置中排列，周邊以 Glyph Light 點綴。
![IMG_20240503_181657940](https://hackmd.io/_uploads/rkqG-YNzC.jpg)
▲ Take By Nothing Phone (2)

在我拿到手機之後，經歷了一次大版本更新（2.5.1A -> 2.5.5a）

<table>
  <tr>
    <td><img src="https://hackmd.io/_uploads/SJpnLK4GC.png" alt="Screenshot_20240503-182403"></td>
    <td><img src="https://hackmd.io/_uploads/SkeOvFVzC.png" alt="Screenshot_20240503-182821~2"></td>
    <td><img src="https://hackmd.io/_uploads/rJGAUFVGA.png" alt="Screenshot_20240503-184648"></td>
  </tr>
</table>
這次的 Nothing Phone (2a) 使用了聯發科天璣 7200 Pro 中階 SOC，性能上雖不及前一代旗艦產品定位的 Nothing Phone (2)。儘管性能上有所不足，但實際使用後，感受意外地流暢，超出預期。
這部分應該歸功於 Nothing OS 的最佳化調教，使得聯發科天璣 7200 Pro 的表現得以發揮。雖然對於中階 SOC 來說，部分重度應用場景和相機 HDR 處理較為吃力，但整體成果還是出人意料。在台灣市場，除了基本的 8G+128GB 版本，還有提供 12G+256GB 的版本，而我使用的正是 12G+256GB 版本。


Nothing OS
---
有了原生輕量化的 Nothing OS 加持，也讓原本中階定位的 SOC 能夠擁有更流暢的使用體驗。
而我也隨手測試了 Nothing Phone (2a) 於 Nothing OS 2.5.5a 上的效能。
<table>
  <tr>
    <td><img src="https://hackmd.io/_uploads/rJPhWjEGR.png" alt="Nothing Phone (2a) NothingOS 2.5.5a"></td>
    <td><img src="https://hackmd.io/_uploads/Hy86-sVGR.png" alt="Nothing Phone (2a) 3DMark"></td>
  </tr>
</table>
▲ GeekBench 6 連續 4 次的測試結果（左圖） / 3DMark Wild Life Extreme 20 輪壓力測試結果（右圖）

以下是對照組，有 Nothing Phone (1) 以及 Nothing Phone (2)

![Nothing Phone (1) NothingOS 2.5.5](https://hackmd.io/_uploads/Bk7ik1rMA.png)
▲ Nothing Phone (1) NothingOS 2.5.5 GeekBench 6 連續 4 次的測試結果（上圖）
▼ Nothing Phone (2) NothingOS 2.5.5 GeekBench 6 連續 4 次的測試結果（下圖）
![Nothing Phone (2) NothingOS 2.5.5](https://hackmd.io/_uploads/HycoyJHzR.png)


![GeekBench6 圖表_單核心](https://hackmd.io/_uploads/HkXQ8yBfA.png)

![GeekBench6 圖表_多核心](https://hackmd.io/_uploads/BymXIkrM0.png)


搭載了原生 Android 14 的 Nothing OS，也不只有原生 Android 的一些基本功能，Nothing Tech 也針對玩家的使用者加入 Glpyh Light 燈效的進度列功能、甚至是支援 AirPods、增強遊戲場景的觸控回應，亦或是遊戲模式的實驗性功能。也期許未來 Nothing 可以提供更多更好玩的功能給極客的玩家使用體驗。（如下圖所示）
<table>
  <tr>
    <td><img src="https://hackmd.io/_uploads/BJDjpRVzC.png" alt="Screenshot_20240505-141455"></td>
    <td><img src="https://hackmd.io/_uploads/HJ0opAEf0.png" alt="Screenshot_20240505-141457"></td>
    <td><img src="https://hackmd.io/_uploads/ryI2TCVzR.png" alt="Screenshot_20240505-141501"></td>
  </tr>
  <tr>
    <td><img src="https://hackmd.io/_uploads/HyHap04fR.png" alt="Screenshot_20240505-141505"></td>
    <td><img src="https://hackmd.io/_uploads/SJMATCEfC.png" alt="Screenshot_20240504-004456"></td>
    <td><img src="https://hackmd.io/_uploads/r1-gCA4fR.png" alt="Screenshot_20240504-004327"></td>
  </tr>
</table>
Nothing OS 也引入了最新的 AI 桌布功能，供使用者可以自行生成出符合風格的獨一無二的桌布。
也持續保留了原本就有加入帶有 Nothing 風格的鎖定螢幕小工具。（如下圖所示）

<table>
  <tr>
    <td><img src="https://hackmd.io/_uploads/HkEWRRVGC.png" alt="Screenshot_20240504-004429"></td>
    <td><img src="https://hackmd.io/_uploads/BJTZR0VzR.png" alt="Screenshot_20240504-004355"></td>
    <td><img src="https://hackmd.io/_uploads/SyofCCEz0.png" alt="Screenshot_20240504-004424"></td>
  </tr>
  <tr>
    <td><img src="https://hackmd.io/_uploads/SkH7ACNM0.png" alt="Screenshot_20240504-004421"></td>
    <td><img src="https://hackmd.io/_uploads/Bk0X00NzA.png" alt="Screenshot_20240504-004432"></td>
    <td><img src="https://hackmd.io/_uploads/H1IV0REGA.png" alt="Screenshot_20240504-004438"></td>
  </tr>
</table>
Nothing Phone (2a) 是我在 6 年之後再度使用聯發科 SOC 的手機產品，成功揮別我對聯發科 SOC 就是「卡頓」、「發熱」、「手機廠商提供更新頻率不高」...等既有的負面印象。


Nothing Camera 相機
---
這次我也攜帶 Nothing Phone (2a) 至餐廳享用美食，除了品嘗美味的佳餚，也拍攝了一些美食的照片。
對照組為我手上自己用的 Nothing Phone (2)

###### 本次拍攝的條件都是原圖直出，僅有開啟手機內建的 HDR (Auto)，其餘都是在一般拍攝模式下直接拍攝。

▼ 由 Nothing Phone (2a) 拍攝
<table>
  <tr>
    <td><img src="https://hackmd.io/_uploads/HydZ7eSMC.jpg" alt="IMG_20240504_190945174"></td>
    <td><img src="https://hackmd.io/_uploads/rkyMQeHG0.jpg" alt="IMG_20240504_191004010"></td>
    <td><img src="https://hackmd.io/_uploads/Hk7zmgrGR.jpg" alt="IMG_20240504_191505444"></td>
  </tr>
  <tr>
    <td><img src="https://hackmd.io/_uploads/B1NmQeSM0.jpg" alt="IMG_20240504_195000280"></td>
    <td><img src="https://hackmd.io/_uploads/S1oXmgHfC.jpg" alt="IMG_20240504_195048853"></td>
    <td><img src="https://hackmd.io/_uploads/rkgEQlBzA.jpg" alt="IMG_20240504_195606445"></td>
  </tr>
  <tr>
    <td><img src="https://hackmd.io/_uploads/HJI47xrGR.jpg" alt="IMG_20240504_200520912"></td>
    <td><img src="https://hackmd.io/_uploads/rJRL7grfC.jpg" alt="IMG_20240504_200725266"></td>
    <td><img src="https://hackmd.io/_uploads/Bymv7gHMR.jpg" alt="IMG_20240504_201228800"></td>
  </tr>
</table>
▼ 由 Nothing Phone (2) 拍攝
<table>
  <tr>
    <td><img src="https://hackmd.io/_uploads/SkGKfzSzR.jpg" alt="IMG_20240504_191045790"></td>
    <td><img src="https://hackmd.io/_uploads/HJ2_MfSz0.jpg" alt="IMG_20240504_191025345"></td>
    <td><img src="https://hackmd.io/_uploads/r1wFffSMR.jpg" alt="IMG_20240504_191440479"></td>
  </tr>
  <tr>
    <td><img src="https://hackmd.io/_uploads/rJHcfzSzC.jpg" alt="IMG_20240504_194949929"></td>
    <td><img src="https://hackmd.io/_uploads/B1RqffHGC.jpg" alt="IMG_20240504_195055484"></td>
    <td><img src="https://hackmd.io/_uploads/H1QiGfHGA.jpg" alt="IMG_20240504_195904322"></td>
  </tr>
  <tr>
    <td><img src="https://hackmd.io/_uploads/HkCiMGBMA.jpg" alt="IMG_20240504_200531595"></td>
    <td><img src="https://hackmd.io/_uploads/SJX2GGBzR.jpg" alt="IMG_20240504_200738055"></td>
    <td><img src="https://hackmd.io/_uploads/r1dhMMrM0.jpg" alt="IMG_20240504_201243479"></td>
  </tr>
</table>
這次 Nothing Phone (2a) 所搭載的後鏡頭分別為兩顆支援 5000 萬畫素，一顆為超廣角，且主鏡頭也支援廣角。
照片的調色上屬於更加鮮豔，討眼球的風格，拍攝出的美食，也令人感到更有食慾。
不過，個人認為在遇到燈光較強烈的場景，目前的算法，針對高光抑制的狀況仍有待加強，這可以期許在未來的 OTA 當中修復。

總結
---
這算是我在暌違已久之後再度使用採用聯發科 SOC 的手機，對於我來說其實是一次新的體驗跟嘗試，上手之前，其實蠻擔心會不會像其他品牌在過往採用聯發科 SOC 手機上遇到的問題。但實際親自上手之後，我完全改觀，至少讓我對於未來聯發科 SOC 的產品不再感冒。
Nothing Phone (2a) 實際表現不輸 Nothing Phone (1)。把價格降低至更符合中階手機的價格區間，並且仍舊有保留 Glpyh Light，可以吸引許多過往普遍認為 Nothing Phone 是藝術品的群眾購入。
也能夠讓原本就附著在中階手機的消費者們，有著更多的選擇，也可以挑選到更有個性的一部手機。
系統功能也隨著 OTA 更新，釋放給所有使用者，並沒有因為 Nothing Phone (2a) 產品定位，而有所區分。這點可以給 Nothing Tech 的工程師們一個大大的讚！


以上便是此次 Nothing Phone (2a) 的開箱體驗。期許未來 Nothing Phone 可以擁有更多的驚喜提供給粉絲及玩家。


About Me
---
我是 EdwardWu
- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram : [_920223](https://www.instagram.com/_920223/)
- GitHub : [bluehomewu](https://github.com/bluehomewu)

<a href="mailto:bluehome.wu@gmail.com"> <img alt="Gmail" src="https://img.shields.io/badge/-Gmail-c14438?style=flat&logo=Gmail&logoColor=white" /></a>

![image](https://hackmd.io/_uploads/BkxA3yHz0.png)




###### tags: `Android` `Nothing` `Nothing Phone (2a)` `ROM` `Nothing Tech`