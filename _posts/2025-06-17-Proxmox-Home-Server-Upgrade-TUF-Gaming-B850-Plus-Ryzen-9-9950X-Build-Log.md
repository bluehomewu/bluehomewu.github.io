---
title: Proxmox 家用伺服器大升級：TUF Gaming B850-Plus WiFi × Ryzen 9 9950X 實戰紀錄
date: 2025-06-17
categories: [開箱評測]
tags: [ASUS, Android, AMD, TUF, PVE]

---

# Proxmox 家用伺服器大升級：TUF Gaming B850-Plus WiFi × Ryzen 9 9950X 實戰紀錄

前情提要
---
2025 年 4 月初，遠在美國的同學向我詢問他電腦的問題，我建議他可以先測試看看記憶體。而他的電腦也很順利的通過 [MemTest86](https://www.memtest86.com/) 檢查。
而我也想著我可以順便檢查一下我電腦的記憶體是否存在問題。

結果不查不知道，一查嚇一跳，一整排紅字，整個晚上都睡不好了。
![IMG_20250406_092731413](/assets/img/posts/S1_s_7NWeg.jpg)

然而我手上這組記憶體，其實是一組絕版品，來自美光 Crucial Ballistix MAX DDR4-4000 16G x4
![IMG_20250406_010544702](/assets/img/posts/Hy77FmNZgx.jpg)

同時也因為一些特別的因素，導致這組記憶體是不可以 RMA 送修的，因此萌生我想把整台主機砍掉重練的想法。
碰巧與 Asus Taiwan 一拍即合，開始了我的燒錢之路。
同時也很感謝 AMD Taiwan，其實本次燒錢之路開始之前，AMD Taiwan 是有意願借我 Ryzen 9 9900X，進行相關測試，但礙於我個人覺得 9900X 與 9950X 相差不大，不如還是選 9950X 更具有意義。
且於當時洽談時，我的其他硬體零件都尚未湊齊，因此不適合進行借用測試。

> 還沒看過 ROG Strix SCAR 18 (2023) G834 的開箱評測文章看這邊
> -> [ROG Strix SCAR 18 (2023) G834 開箱評測](https://hackmd.io/@EdwardWu/ROG_Strix_SCAR_18_2023_G834JY_Unboxing)
> 
> 還沒看過 華碩 Vivobook S15(S5507) 的開箱評測文章看這邊
> -> [攜手 Microsoft Copilot+：華碩 Vivobook S15 重新定義生產力](https://hackmd.io/@EdwardWu/VivobookS15_S5507)

硬體規格說明
---
舊平台硬體規格：

| 零件 | 規格                             |
| ---- | -------------------------------- |
| CPU  | AMD Ryzen 7 5800X                    |
| RAM  | Crucial Ballistix MAX DDR4-4000 CL18-19-19-39 1.35V 64GB (4x16G) |
| MB   | TUF Gaming B550M-Plus                   |
| Cooler | 鐮刀 Scythe 無限伍 塔扇                     |
| PSU  | Cooler Master 650W MPE-6501-ACAAW 銅牌                             |
| Case | 全漢 CMT220 聖俠士機殼              |

新平台硬體規格：

| 零件 | 規格                             |
| ---- | -------------------------------- |
| CPU  | AMD Ryzen 9 9950X                    |
| RAM  | 芝奇 Trident Z5 RGB DDR5-6400 CL32-39-39-102 1.40V 64GB (2x32GB) |
| MB   | TUF Gaming B850-Plus WiFi                  |
| Cooler | TUF Gaming LC II 240 ARGB                     |
| PSU  | EVGA 850 GS 850W 金牌全模組                             |
| Case | NZXT H5 Flow 2022              |

TUF Gaming B850-Plus WiFi
---

這次所採用的 TUF Gaming B850-Plus WiFi 與上一代的 TUF Gaming B650-Plus WiFi 對比，除了晶片組的常規升級，也將 WiFi 模組一並從 WiFi 6 升級至 WiFi 7。
（雖然 WiFi 在我的使用場景可能用不上，有些許可惜）
同時也調整了一些線路插槽的佈局，把原先連續排在一起的 4 個 SATA 接孔，拆分成 2+2 的佈局安排。
透過晶片組的升級迭代，也將其中一個全尺寸的 PCIE x16 由 Gen 4 升級為 Gen 5，使消費者可以在其餘零件的選擇上有更彈性的空間，較不會被 PCIE 通道頻寬限制住。

根據華碩提供的使用手冊所述，PCIE x16 Gen 5 這個通道也有支援拆分，故可以有更彈性的安排
![image](/assets/img/posts/ryrsQENWxx.png)

這也是我正是踏入 AM5 Socket 的第一套平台。在此之前我手邊的其他主機都還是採用 AM4 Socket，像是我的主力電腦，就是採用 Ryzen 9 5950X + ROG Crosshair VIII Dark Hero 的 AM4 頂級組合。
而我放在公司服役中的 Coding 主機則是 Ryzen 5 3600XT + Prime X470-Pro 的組合，也是先前用在這套 Proxmox VE 主機的平台組合。
也有在思考是不是把這次更換下來的 Ryzen 7 5800X + TUF Gaming B550M-Plus 帶到公司去取代現在所使用的平台。

![image](/assets/img/posts/B1b1jEVWxg.jpg)
由於本人實在不擅長走線，也有經常拆拆裝裝修改配件的需求，所以在線路佈局上看起來有些雜亂。

TUF Gaming B850-Plus WiFi 這張主機板現階段對於我用作為一台 HomeServer 來說，比較可惜的是 SATA 孔位不夠用，因此可以在圖中看到，我必須額外安裝一張 PCIE 轉 SATA 的擴充卡。
同時，我也在安裝過程中發現一個問題，根據華碩於使用手冊上描述
```
PCIEX16(G4) 插槽與 M.2_3 插槽共享頻寬·當 M.2_3 插槽運作時 PCIEX16(G4）插槽將無法使用。
```

但根據我的實驗，我將 M.2 PCIE SSD 插在 M.2_2 也會造成 PCIEX16(G4) 無法使用。
![image](/assets/img/posts/B1_AnE4Zgl.png)
藍色框選處是 PCIE x16；紅色框選處是 M.2 PCIE Socket
###### 註：已經向華碩詢問這部分的問題，若有回覆會更新在這段落下方
![image](/assets/img/posts/ByIg75LXxg.png)

且我在更新 BIOS 到 1028 版本之後，這個問題就被排除了，因此可以合理推測，這個特殊情況只在 1022 版發生，也很感謝華碩 RD 願意協助排除釐清相關問題。


### 友善功能
華碩針對每次迭代所推出的主機板，皆有聽取消費者的建議，因此開發出許多對於使用者來說相當友善的功能，同時也逐步提升 DIY 玩家在組裝方面的便利程度。

1. Q-Release
第一個要介紹的是 PCIE 插槽的 Q-Release。
由於近幾年顯卡都越做越大張，透過 Q-Release 的設計，就可以很方便的卸下卡扣。
就不用為了找卡榫，手指伸到顯卡底下，而被划傷了。
（不過，我暫時也沒這個需求，畢竟我現在可是用來作為 HomeServer，暫且也沒機會加上新世代的顯卡XD）
![image](/assets/img/posts/SJddTVLMle.png)

2. Q-Antenna
這個則是用來將 WiFi 天線快速安裝到後面 I/O 擋板的設計。
就以我現在主力在使用的 ROG C8DH 來說，WiFi 天線是採用傳統的旋轉方式安裝，這對於像我一樣有些微的強迫症的人來說，有點難以接受，因為在安裝的時候，線的部分會被翻轉，使得最後安裝完畢還要再順一遍，有一些不便。
同時也對於一些直接把主機交由店家組裝後，就帶回家的小白使用者來說，多少有一些風險存在。
因此這次支援 Q-Antenna 其實不論是對於資深 DIY 玩家，又或者是電腦小白，都是提供了相當便利的設計。
![image](/assets/img/posts/rkMcpEUGeg.png)

3. M.2 Q-Latch
這個快速固定 M.2 硬碟的機制，我真的要給好評，在我過去使用 TUF B550M-Plus 主機板的過程中，每次更換 M.2 SSD 或是更換 M.2 SSD 上的導熱墊片時，就是我的噩夢。
由於 TUF B550M-Plus 的 M.2 SSD 固定機制，是將外面的散熱片的其中一個螺絲固定在 SSD 上，因此在安裝過程中，需要非常小心，才可以安裝完成。也增加了螺絲掉落的風險。
所以 Q-Latch，對於手殘黨來說，其實是相當實用的設計。
![image](/assets/img/posts/H1ejpNUMxx.png)

4. Q-LED
前面三個功能，對我來說，都是友善設計，但這一個功能，對我來說就有一些不便。
華碩在這代 TUF B850 Plus WiFi 主機板上取消了 Speaker（蜂鳴器）接口的 PIN 針腳設計，對於相當依賴 Speaker 的長短音去判斷開機成功或是失敗的老玩家來說，確實是有一點不習慣的。
不過，整體來說是好的設計，畢竟 Speaker 會因為不同品牌的 BIOS 設計，有不同的聲音組合。然而，Q-LED 的設計就可以很好的避免這個問題，因為顯示出來的直接是燈號，也在側邊標上進度的項目。
![image](/assets/img/posts/SkAs648Gxg.png)

### 主機板散熱設計
> 圖片截自華碩官網
![image](/assets/img/posts/BkLNWS8Mxe.png)

這次令我感到最意外的，莫過於加大許多的 VRM 散熱器，除了視線上看到的面積變大了之外，同時也變得更厚更加結實，根本不怕熱量導不出去。
對於 M.2_2 & M.2_3 的散熱片，更是一次包含兩個 M.2 SSD 面積，華碩可是在散熱這方面費盡心思，將溫度控制好，發揮出硬體最大的效能。



### Realtek RTL8125 2.5Gigabit Ethernet
得益於 TUF Gaming B850-Plus WiFi 板載了一張 Realtek RTL8125 的 2.5G 網路卡，讓我在與 Server 或是 NAS 互傳檔案時，可以跑滿 2.5G，對於工作效率以及多工方面都有顯著的提升。
我也在 True-NAS 當中以 Docker 搭建了一個 OpenSpeedTest，進行內網測速。

- 直接跑好跑滿 2.5G
![image](/assets/img/posts/rJI9bwEWle.png)
![image](/assets/img/posts/HkHiZwNZlg.png)
![image](/assets/img/posts/HkcaWPVbxl.png)


Ryzen 9 9950X
---
![Ryzen 9 9950X](/assets/img/posts/Hk3fEE4-ee.jpg)

這次在挑選 CPU 的過程可謂是相當艱辛、坎坷，礙於預算有限，且又有多核心的需求，只能把目光投向 Ryzen 7 & Ryzen 9，且同時考慮 7000 或是 9000 系列。
一開始想說可以購買二手的 Ryzen 9 7950X，但市場上幾乎沒有看到多少人在販售，縱使有看到二手的銷售貼文，但我總覺得價格不夠漂亮，而 9950X 也是類似情況。

直到某天早上起的比較早，我於 Facebook MarketPlace 上看到售價只要 $16000 的全新未拆 Ryzen 9 9950X 我便動了直接攻頂的念頭。在經過一番交涉之後，最終以 $15000 + 賣貨便運費 $38 成功購買。
但也由於，購買的價格實在是低於市場行情（全新未拆品），我也曾一度懷疑是否遇上詐騙，賣家的 Facebook 帳號個人檔案是鎖住的，於 MarketPlace 另外 2 個的販售商品是高雄的兩戶房子，實在有些令人懷疑 XD。
（如果賣家本人看到這篇文，還希望不要介意）
其實本次可以買到便宜的 Ryzen 9 9950X，主要的原因是這顆 9950X 其實是來自英國 eBay，而非台灣公司貨，也因此台灣是沒有辦法送修的。

- 驗明正身
![IMG_20250515_200556027](/assets/img/posts/HkIGqENblx.jpg)

也得益於 AMD 於 AM5 開始有把 RDNA 的內顯加入到更多的 CPU 產品，也讓我這次裝機可以少加裝一張亮機卡。

NZXT H5 Flow 2022 + EVGA 850GS 金牌全模組 + TUF Gaming LC II 240 ARGB
---
NZXT 的機殼是真的對於強迫症患者友善，對於線材的路線規劃，可以說是每一個環節都有巧思，連我一個平常是屬於眼不見為淨的人，都有想要整線的念頭。
這兩個零件，其實是碰巧看到我學弟要拆賣，我就一併買下來的。否則，若是使用原先的 650W PSU 用於 9950X 總感覺會有些吃緊。
也多虧於 NZXT H5 Flow 2022 前面板有支援 Type-C，都 2025 年了，還有些機殼前面板沒有支援 Type-C。

不過有些可惜的是這個機殼僅能支援 240 的水冷，沒辦法安裝上 360 水冷，未來還要持續觀察，如果到時候真的投入我的開發環境時，會不會壓不住溫度。

這次雖然使用的不是最新推出的 LC III TUF Gaming 水冷，但是 LC II 其實也足夠使用，對於預算上有考量的，可以選擇 LC II 的水冷。
過去我協助朋友組裝電腦，也多次選擇 TUF Gaming 的 LC II 240/360 ARGB 水冷系列，對於 TUF Gaming LC 一體式水冷的可靠程度，是相當有信心的。
對於 TUF Gaming LC II 水冷，我還是能給出不錯的評價，但更希望未來可以推出 LOGO 是模組化的版本，就如同我這次的安裝，會使得 TUF Gaming 的 LOGO 上下顛倒，是稍加讓我覺得可惜的部分，如果可以重新根據安裝方向自行調整，那就真的是無可挑剔了。
![P_20250611_130806](/assets/img/posts/HJEnG5U7xx.jpg)

![IMG_20250515_200547074](/assets/img/posts/rkhB0FImxx.jpg)

![IMG_20250530_145124933](/assets/img/posts/H1AyUC8zee.jpg)

![P_20250611_130730](/assets/img/posts/Bkx2f58mxl.jpg)

現在這台 HomeServer 距離成為電子花車還有好幾步路，未來將逐步升級剩下的部分，使其成為一台稱職的 HomeServer。


芝奇 Trident Z5 RGB DDR5-6400 CL32-39-39-102 1.40V 64GB (2x32GB)
---
這次的 DDR5 記憶體，感謝我的左岸友人（@Henri），先借我他手邊暫時用不上的，替我省下一筆花費。

Proxmox VE v7.4
---
我目前的 Proxmox VE 架構其實仍舊與之前相同，主要是將大多數的硬體資源分配給 Android Build-Server，並把 2 Core / 4GB RAM 分配給 True-NAS

- 接下來的 HomeServer 請多多指教
![image](/assets/img/posts/r16NzLVblg.png)
![image](/assets/img/posts/Syn8zU4ble.png)

- 誰說只有 Windows 可以數框框，Linux 也不是不行
![image](/assets/img/posts/Bkd2gDEZeg.png)


其實升級完硬體，Proxmox VE 是可以直接開機的，不需要重新安裝 OS。只有那...奇怪的 Windows 還是建議重新安裝 OS。
不過，在更換完硬體之後，我又遇到了網路卡消失術，查了很多網站的文章，我都已經修好了之後…我才想起來我自己也曾經寫過解決辦法的筆記。
[網路卡消失術](https://hackmd.io/@EdwardWu/PVE_pit#%E7%B6%B2%E8%B7%AF%E5%8D%A1%E6%B6%88%E5%A4%B1%E8%A1%93)

其中令我比較意外的是，板載的 Realtek RTL8125 被改為 eno1。因為在此之前，我在 TUF Gaming B550M-Plus 上板載 Realtek RTL8125 是被設定為 enp6s0，也因此我在修改網路卡設定時，額外花了一些時間。
追蹤了一下之後了解到，是在 systemd v197 當中進行修改的。
詳情可以參考[官方說明文件](https://github.com/systemd/systemd/blob/main/docs/PREDICTABLE_INTERFACE_NAMES.md)
![image](/assets/img/posts/rJtbgONWxg.png)


總結
---
這篇文章，純粹是紀錄一下 HomeServer 的升級之路，且同時感謝各路人馬，在得知我有升級企劃之後，協助我將 AM4 Socket 平台更新迭代至 AM5 Socket。
希望在更新成 Ryzen 9 9950X 之後可以提升我在 Android 系統開發編譯方面的效率，持續對 Android Custom ROM 做出貢獻（雖然也要對電費做出貢獻就是了XD）
而我也預計於今年在 COSCUP 2025 進行議程演講，主題將著重於 GKI Kernel 是如何終結 Android Kernel 的碎片化時代。


About Me
---
我是 EdwardWu
- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram : [_920223](https://www.instagram.com/_920223/)
- GitHub : [bluehomewu](https://github.com/bluehomewu)
- Email : [bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)

![image](/assets/img/posts/Bk1EYGfYA.png)


###### tags: `Android` `Asus` `TUF Gaming` `TUF Gaming B850-Plus WiFi` `ROM` `Asus Taiwan` `AMD Taiwan`




