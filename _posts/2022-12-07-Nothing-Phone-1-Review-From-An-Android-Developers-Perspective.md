---
title: 從 Android 系統開發者的角度評價 Nothing Phone(1)
date: 2022-12-07
categories: [Nothing Tech 產品評測]
tags: [Nothing Tech, Android, Nothing, Nothing Phone(1), ROM]

---

# 從 Android 系統開發者的角度評價 Nothing Phone(1)


前言
---

Hi 各位好～
我是 Edward，目前是一名業餘的 Android Custom ROM Maintainer
也曾在 SITCON 2021 擔任講者，並分享開放式議程主題 [「從零開始編譯 Android 第三方系統！」](https://sitcon.org/2021/agenda/1c9e74cd-aeeb-4e63-8ec4-af33eff16e7d)

以下是我自己寫過的教學文章
[Android 第三方 ROM 繁體中文編譯教學](https://hackmd.io/@EdwardWu/CompileAndroidCustomROM)
[Android 第三方 Recovery 繁體中文編譯教學](https://hackmd.io/@EdwardWu/CompileARecovery)

轉載文章
[快速上手 Android Custom ROM 適配 - Prebuilt Vendor](https://hackmd.io/@EdwardWu/Prebuilt-bringup)

身為一位 Android 第三方系統的維護者，每次新機發表，最看重的往往不一定是強大的硬體規格，但必定是官方對於新機的更新支援以及後續維護的難易度評估。

Nothing Tech 創辦人 - 裴宇，過去曾是 OnePlus 手機的共同創辦人。
在 Nothing Phone(1) 推出之後，我便持續關注 Nothing 這個品牌，看到 Nothing Tech 開源 Kernel Sources，Nothing Tech 把過去在 OnePlus 有 OpenSources 的優點保留下來，對於 Android ROM 開發者的我來說，無疑是在心中給了 Nothing Tech 這個品牌一個不錯的評分以及良好的印象。

[NothingOSS/android_kernel_msm-5.4_nothing_sm7325](https://github.com/NothingOSS/android_kernel_msm-5.4_nothing_sm7325)
[NothingOSS/android_kernel_devicetree_nothing_sm7325](https://github.com/NothingOSS/android_kernel_devicetree_nothing_sm7325)

### 硬體規格

以下簡單用表格列出此次 Nothing Phone(1) 的一些規格參數

| Feature                 | Specification                                                                  |
|:----------------------- |:------------------------------------------------------------------------------ |
| Chipset                 | Qualcomm SM7325-AE Snapdragon 778G+ 5G (6 nm)                                  |
| CPU                     | Octa-core (1x2.5 GHz Cortex-A78 & 3x2.4 GHz Cortex-A78 & 4x1.8 GHz Cortex-A55) |
| GPU                     | Adreno 642L                                                                    |
| Memory                  | 8GB/12GB                                                                       |
| Shipped Android Version | 12, Nothing OS                                                                 |
| Storage                 | 128/256 GB UFS 3.1                                                             |
| SIM                     | Dual SIM (Nano-SIM, dual stand-by)                                             |
| Battery                 | Li-Po 4500 mAh, non-removable                                                  |
| Dimensions              | 159.2 x 75.8 x 8.3 mm (6.27 x 2.98 x 0.33 in)                                  |
| Display                 | 6.55 inches, 1080 x 2400 pixels, 20:9 ratio                                    |
| Rear Camera 1           | 50 MP, f/1.9, 24mm (wide), 1/1.56", 1.0µm, PDAF, OIS                           |
| Rear Camera 2           | 50 MP, f/2.2, 114˚ (ultrawide), 1/2.76", 0.64µm                                |
| Front Camera            | 16 MP, f/2.5, (wide), 1/3.1", 1.0µm                                            |
| Sensors                 | Fingerprint (under display, optical), accelerometer, proximity, gyro, compass  |


Nothing Phone(1)
---

Nothing Phone(1) 的推出在全球各地都造成一股轟動，由於酷炫的外型以及神似 iPhone 的中框設計，成功在科技圈製造話題，引起許多人的討論。
這次有幸可以跟 Nothing Tech Taiwan 合作，可以評測一下 Nothing Phone(1)，這台定位中階但具有旗艦機顏質的手機。

Nothing Phone(1) 雖然搭載的是一顆定位中階的 Snapdragon 778G+，但由於 778G+ 是由護國神山台積電 TSMC 代工的 6nm SOC，因此我在使用這部 Nothing Phone(1) 上的使用體驗相當的流暢以及省電。

在使用了大約一週的時間之後，我想和各位分享一下我使用 Nothing Phone(1) 所搭載 Nothing OS 的使用體驗。

在我收到 Nothing Phone(1) 之後，總共收到 2 次的 OTA 更新（1.0.1 -> 1.1.6 -> 1.1.7）
在使用 Nothing OS 的過程當中，其實我個人沒有遇到太多的 bug，畢竟 Nothing OS 是非常接近原生 AOSP 的系統，因此整體使用上對於我經常使用 AOSP base ROM 的人來說，非常的友善。

每次的 Nothing OS OTA 更新，看到 Changelog 之後，其實我都蠻訝異的，因為大部分的都是針對使用體驗最佳化，以及針對功能的新增支援。
大部分的手機廠商都會針對系統穩定性去做最佳化，但對於功能的支援增減，絕大多數的時候都不會寫在 Changelog 上，讓使用者了解狀況。

![](https://i.imgur.com/8R7HOgx.jpg)

雖然以目前對其他廠商的標準來審視 Nothing OS 來說還是有些過於高了，對於一般使用者來說，與其花時間陪一個品牌成長，到不如跳槽去別的手機品牌。
可是到了 Android ROM 開發者這邊，這正合我胃口啊......！畢竟我也經常用著不穩定的系統，因此我已經見怪不怪了。
雖然有一些不那麼影響使用的小問題，我相信在工程師的不斷最佳化下，會給用戶帶來更優秀的體驗。
我個人覺得，就以目前來說，Nothing Tech 在步入手機的開發還算是很新的階段，因此，我覺得現階段的成果已經很棒了，可以取得如此優秀的成果。


Nothing OS
---

使用上第一直覺居然是發覺跟我平常在使用的第三方 ROM 使用體驗毫無區別，一樣包含了許多自訂性，但同時也保證了一定的系統流暢度跟使用體驗。
對於身為 Android 開發者的我來說，如果原廠系統可以在保證自訂性的同時並且也保持著流暢度，我便可以不用花費大把時間進行編譯 Android Custom ROM，也不用解鎖 bootloader。
貼近 AOSP 不代表功能變少，但對於開發者來說，貼近 AOSP 的好處，遠遠大於「深度客製化」。
舉例來說，深度客製化之後的系統，當面臨大版本更新時（如 Android 版本更新），相當容易發生系統層級的致命 bug，這將大幅降低系統的穩定性以及可用性。最容易發現的部分，就是大版本更新時，所遇到的發燙問題。

Nothing OS 在版本更新過後，Geekbench 5 的跑分表現有明顯的提升，可見工程師可是在調教系統穩定性以及效能上持續努力以及進步。

![](https://i.imgur.com/emHFZ2h.png)


#### 你知道這是什麼嗎？雖然我不是特斯拉車主，但這聽起來還不錯對吧？
這次 Nothing OS 在手機內加入了一個實驗室的有趣功能，其中就包含了「連接 Tesla」以及「支援 AirPods 顯示電池電量」的功能，希望未來可以在此加入更多有趣的實驗性功能，讓 Users 可以獲得更深入的使用體驗。

從幾次下來的系統 OTA 更新可以看出來負責維護 Nothing OS 的工程師們都十分用心在解決 bugs，不過也有不小心鬧出個笑話
![](https://i.imgur.com/It7zF7p.png)
[Archive](https://web.archive.org/web/20221027104701/https://github.com/NothingOSS/android_kernel_oneplus_sm8350)
工程師們在使用 GitHub 瀏覽 Kernel code 時候，大概不小心點擊了 edit 的按鈕。
根據 GitHub 的使用邏輯，對一個自己沒有權限的 repo 點擊編輯按鈕之後，會觸發 fork 項目。
（希望 R&D 們可以小心一些XDD）

Nothing Camera 相機
---

附上一些今年我在中壢中原大學以及新北耶誕城所拍攝的樣張給大家參考。

這次我使用 Nothing Phone(1) 進行拍攝的場景大多數都是晚上的室外，因此我覺得這將是針對 Nothing Phone(1) 原廠相機的一大考驗。


<table>
  <tr>
    <td><img src="https://i.imgur.com/h42sesU.jpg" alt=""></td>
    <td><img src="https://i.imgur.com/RewrnB1.jpg" alt=""></td>
    <td><img src="https://i.imgur.com/QZlCnDp.jpg" alt=""></td>
  </tr>
  <tr>
    <td><img src="https://i.imgur.com/71svYdj.jpg" alt=""></td>
    <td><img src="https://i.imgur.com/vJGG2Cm.jpg" alt=""></td>
    <td><img src="https://i.imgur.com/AsYLEHu.jpg" alt=""></td>
  </tr>
  <tr>
    <td><img src="https://i.imgur.com/dQJZYHH.jpg" alt=""></td>
    <td><img src="https://i.imgur.com/v2isEJy.jpg" alt=""></td>
    <td><img src="https://i.imgur.com/5U3fLIw.jpg" alt=""></td>
  </tr>
  <tr>
    <td><img src="https://i.imgur.com/uufWz2M.jpg" alt=""></td>
    <td><img src="https://i.imgur.com/PZQ6rTW.jpg" alt=""></td>
    <td><img src="https://i.imgur.com/18Mi5IP.jpg" alt=""></td>
  </tr>
</table>

Nothing Phone(1) 採用了 50MP + 50MP（主攝 + 超廣角）+ 16MP（前攝）的設計，並且透過相機的夜景演算法以及搭載 IMX766 的主攝很大程度上提供了協助，即使在暗光的環境下，也可以輕鬆拍攝出清晰的照片。

不得不說，我體驗下來 Nothing Camera 帶給我的使用體驗還蠻不錯的，夜景模式拍攝照片後的處理時間，相當的快，手邊還有 ASUS ZenFone 9，相較之下 Nothing Camera 拍攝出來的樣張，可以快速的讓使用者進行預覽。
當然，就以色彩表現來說，Nothing Phone(1) 是無法跟不同產品定位的 ASUS ZenFone 9 進行比較，但就使用體驗來說，可以明顯感受到 Nothing Tech 針對相機的軟體調教，相當的貼近使用者的需求。

![](https://i.imgur.com/cGDauYm.jpg)

同時 Nothing Phone(1) 也提供了專業模式的拍攝選項，讓玩家可以自行調整相機拍攝參數，其中我個人覺得最訝異的是居然支援拍攝 RAW 檔，這真的是一大福音。
這樣我就可以拍完 RAW 檔之後，回家打開 Adobe Photoshop 直接開啟修圖模式，太讚了吧！


總結
---

Nothing 這個品牌在剛發表第一款耳機產品的時候，老實說，我當時不是很興奮的。
因為目前做耳機的品牌實在太多了，很難因為外型而迫使我購買一個相較於其他老品牌如 Sony，考量到挑選耳機大部分的因素其實是實用性跟穩定度。所以當時我並不是很關注這個品牌。
直到 Nothing Phone(1) 上市，在臺灣以及世界各地的科技媒體圈刮起一陣旋風，這個規格跟外型深深吸引我的注意，其中我個人最看重的點還是在 Snapdragon 778G+ 這顆特別訂製的中高階 SOC，支援了無線充電，並且同時兼具類原生 Android AOSP 的乾淨清爽，終於讓我不用為了使用原生的 Android 而投入開發工作（終於可以休息的意思XDDD！）

Nothing OS 對我來說，就像是找到一個志同道合的夥伴，所以自然的 Nothing Tech 這個新創品牌在我的心裡自然是給予不錯的評價。終於有公司可以把類原生的 Android AOSP 帶入 OEM 系統裡。

以上便是此次 Nothing Phone(1) 的開箱體驗。可以說這次 Nothing Phone(1) 的推出，成功打入中高階的手機市場。




About Me
---
我是 EdwardWu
- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram : [_920223](https://www.instagram.com/_920223/)
- GitHub : [bluehomewu](https://github.com/bluehomewu)
- Email : [bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)

![](https://i.imgur.com/HTWnoGl.png)





###### tags: `Android` `Nothing` `Nothing Phone(1)` `ROM` `Nothing Tech`