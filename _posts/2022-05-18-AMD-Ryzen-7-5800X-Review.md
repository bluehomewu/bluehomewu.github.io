---
title: AMD Ryzen 7 5800X 遲來的「主觀」評測
date: 2022-05-18
categories: [AMD]
tags: [Windows, Linux, AMD]

---

# AMD Ryzen 7 5800X 遲來的「主觀」評測

\ 本篇同步發布於 [Mobile01](https://www.mobile01.com/topicdetail.php?f=296&t=6537991#84151395) /

Hi 各位好～
我是 Edward，目前是一名業餘的 Android Custom ROM Maintainer
也曾在 SITCON 2021 擔任講者，並分享開放式議程主題 [「從零開始編譯 Android 第三方系統！」](https://sitcon.org/2021/agenda/1c9e74cd-aeeb-4e63-8ec4-af33eff16e7d)

以下是我自己寫的教學文章
[Android 第三方 ROM 繁體中文編譯教學](https://hackmd.io/@EdwardWu/CompileAndroidCustomROM)
[Android 第三方 Recovery 繁體中文編譯教學](https://hackmd.io/@EdwardWu/CompileARecovery)
前陣子有緣與 AMD 合作，收到了來自 AMD 爸爸的一顆 Ryzen 7 5800X 以及火鳥科技的 750W 電源供應器

相信大家在 AM5 腳位 CPU 即將上市之際，已經對 AM4 腳位的家族成員不陌生了。
不論是帳面規格或是遊戲方面的性能表現也都非常熟悉，因此我這次將會對於 Ryzen 7 5800X 在編譯 Android 第三方系統所帶來的優勢以及幫助進行評測。

![](https://i.imgur.com/mT4wFVJ.jpg)

![](https://i.imgur.com/zODUqGo.jpg)

![](https://i.imgur.com/s9FEy0S.jpg)




AMD Ryzen 7 5800X 上機實測
---
這次所使用的測試平台的規格如下

### AMD 測試平台：

主機板： [ASUS TUF Gaming B550M-Plus](https://www.asus.com/tw/Motherboards-Components/Motherboards/TUF-Gaming/TUF-GAMING-B550M-PLUS/techspec/) （[BIOS 版本 2423](https://dlcdnets.asus.com/pub/ASUS/mb/BIOS/TUF-GAMING-B550M-PLUS-ASUS-2423.ZIP)）
處理器：AMD Ryzen 5 3600 (6核心/12執行緒) && AMD Ryzen 7 5800X (8核心/16執行緒)
（皆有開啟 PBO2）
記憶體：美光 Micron Crucial Ballistix D4 3600/32G(16G2)超頻(雙通)白散熱片（開啟 D.O.C.P.）
###### WSL2 記憶體為動態調整（最高可以使用到 30GB 的記憶體）
散熱：AMD Wraith Prism 幽靈風扇
顯示卡：ASUS ROG-STRIX-RX570-O4G-GAMING
電源供應器：BitFenix Formula Gold 750W(BF750G)
硬碟：4TB HGST HDD 以及 Samsung 970 EVO Plus 500GB
作業系統：Windows 11 Pro for Workstation Dev 22538 with WSL2（Ubuntu-21.10）
ccache 全程設定 100GB
###### 註1：Windows 系統硬碟使用 AGI 256GB M.2 PCIE SSD，兩套 WSL2 分別存放在 4TB HGST HDD 以及 Samsung 970 EVO Plus 500GB
###### 註2：Windows 平台背景皆無開啟額外的程式，除工作管理員以及部分 ASUS RGB 燈光服務


![R53600_Spec](https://i.imgur.com/DFLA47T.png)

![R75800X_Spec](https://i.imgur.com/hgOBs1u.png)

### Intel 測試平台：
##### 此兩套平台為 VPS 主機（部分硬體規格不清楚）
處理器：Intel Xeon E5-2690 v2(16執行緒) (10核心/20執行緒)
記憶體：32GB RAM
硬碟：2TB HDD
作業系統：Ubuntu-21.10
ccache 全程設定 100GB

![Intel-VPS1_Spec](https://i.imgur.com/UgdMEZA.png)

處理器：Intel Xeon Gold 6230R (32 執行緒) (26核心/52執行緒)
記憶體：32GB RAM
硬碟：2TB NVME PCIE SSD
作業系統：Ubuntu-21.10
ccache 全程設定 100GB

![Intel-VPS1_Spec](https://i.imgur.com/pjQdqc5.png)

### 編譯的 Android 設備
型號：ASUS ZenFone 5Z (Z01R)
SOC：Snapdragon 845 (SDM845)
RAM：6GB
ROM：64GB




AMD 平台測試
---
原本使用 Ryzen 5 3600 編譯 ROM 的過程中
CPU 基本上是 12 個執行緒，都處於滿載的情況
CPU 占用率 100% 的情況下，
需要花費 4 個多小時左右的時間進行 Clean Build 編譯
需要花費 2 個小時又 40 分鐘左右的時間進行 InstallClean Build 編譯
即便是 Dirty Build 也需要花費大約接近 2 小時的時間，在維護系統的過程中，花費過久的時間。

在更換到 AMD Ryzen 7 5800X 之後，編譯 Clean Build 整整比 Ryzen 5 3600 少了一個小時，InstallClean Build 的時間僅僅只需要一個半小時。

在過去我也測試過 WSL2 （Ubuntu 20.04.3 LTS）與 純 Ubuntu 20.04.3 LTS 系統並且使用當時最新的 Kernel（ 使用 Ryzen 5 3600 進行測試）花費時間大約差在15 分鐘左右，並且是由 WSL2 勝出。純 Ubuntu 系統比 WSL2 還慢，或許是 WSL2 可能有針對 AMD 的多核心 CPU 進行 Kernel 方面的調教。

使用 Samsung 970 EVO Plus 500GB 進行編譯 Android 系統，完整 ClenBuild 僅僅花費 50 分鐘，由此可見，使用 Ryzen 7 5800X 搭配上 PCIE SSD 可以為生產力工作帶來相當程度上的助益。


![Ryzen 5 3600 CleanBuild](https://i.imgur.com/Gemy2bS.png)

![Ryzen 7 5800X InstallCleanBuild](https://i.imgur.com/jbYaDGk.png)

![Ryzen 7 5800X CleanBuild HDD](https://i.imgur.com/oHnOz4q.png)

![Ryzen 7 5800X CleanBuild PCIE SSD](https://i.imgur.com/j6vZGki.png)



Intel 平台測試
---

此主機為 VPS 主機，且系統是完整的 Ubuntu-21.10，並非 WSL2 虛擬機系統，因此編譯時間上的對比無法進行比較，僅供參考。 

附圖是第一台 VPS 虛擬主機 Clean Build 的花費時間
大約是兩個小時又 40 分鐘
第一台使用的是 HDD
![VPS CleanBuild](https://i.imgur.com/VfKEnxh.png)

第二台虛擬主機 Clean Build 的花費時間
大約是半小時
第二台使用的是 SSD
![](https://i.imgur.com/y1iUSX9.png)



AMD Ryzen 7 5800X 實測心得
---
感謝 AMD 以及火鳥科技這次提供的產品，使得我在 Android Custom ROM 的維護上，可以更迅速的為 Users 提供修復 bugs。
就我這一陣子的體驗來說，更換上 Ryzen 7 5800X 可以有效的減少編譯過程中的等待時間。對比國外開發者的實測使用 5800X 搭配 64GB DDR4-4266 超頻記憶體以及 4TB PCIE4.0 SSD 可以將一次的 CleanBuild 時間壓縮至半小時左右，搭配 PCIE 3.0 SSD 則可以有效壓縮時間至 40 分鐘到 1 小時左右，可見 AMD Ryzen 7 5800X 對於生產力方面是相當有潛力的，不僅僅只是在遊戲方面表現優異，更能為開發者帶來更好的工作效率。
得益於 AMD Ryzen 採用了 7nm 台積電工藝，且 Ryzen 7 5800X 對比 Ryzen 5 3600 有更多的 CPU 核心以及執行緒使得多核工作上的表現可以勝過於 Ryzen 5 3600

目前我所使用的 CPU 散熱為 AMD 自家所推出的 AMD Wraith Prism 幽靈風扇，一般文書情況下使用上倒是沒什麼問題，但由於我經常編譯 Android 系統，大多數時候風扇皆必須保持在高轉速的狀況，因此我想在未來有必要更換為 PA120 或是其他的散熱器。



###### tags: `Windows` `Linux` `Git` `GitHub` `AMD` `Intel`