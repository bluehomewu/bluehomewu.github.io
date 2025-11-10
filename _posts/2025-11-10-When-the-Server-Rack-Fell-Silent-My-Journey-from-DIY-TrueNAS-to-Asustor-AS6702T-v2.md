---

title: 當機架上的伺服器歸於平靜：我從 True-NAS 轉投 Asustor AS6702T v2 的心路歷程
date: 2025-11-10
categories: [Asustor]
tags: [Asustor]

---

# 當機架上的伺服器歸於平靜：我從 True-NAS 轉投 Asustor AS6702T v2 的心路歷程

![P_20251101_151251](/assets/img/posts/H1wdQEmkZg.jpg)


前言 — 敬，那段折騰不息的歲月
---
DIY NAS，與成品 NAS 最大的不同，就是高度的客製化，從硬體到軟體這種無與倫比的客製化彈性、極致的效能追求，是我過去持續在掌控的。

但這份「掌控感」的代價是什麼，更多的是無數個除錯的夜晚，又或者是高昂的電費帳單，因此我最終還是決定將 NAS 從自組的 True-NAS 中脫離，回到成品 NAS 的懷抱。

我的性能巨獸 — Proxmox VE 上的 True-NAS 虛擬化方案
---
#### 我的硬體平台：為信仰充值
由於我個人的 Side-Project 是開發 Android 的第三方系統，也經常編譯 BSP，因此有一台性能強悍的電腦是開發路上必須要有的設備之一。


升級紀錄可以參考這篇：
[Proxmox 家用伺服器大升級：TUF Gaming B850-Plus WiFi × Ryzen 9 9950X 實戰紀錄](https://bluehomewu.github.io/posts/Proxmox-Home-Server-Upgrade-TUF-Gaming-B850-Plus-Ryzen-9-9950X-Build-Log/)

在前陣子，我升級了正在使用中的 Server，同時也在更換硬體的過程中出現了一些問題，最終經由我的除錯，而完美升級完成。

我目前在 Proxmox VE Server 上使用的平台規格如下：

| 零件 | 規格                             |
| ---- | -------------------------------- |
| CPU  | AMD Ryzen 9 9950X                    |
| RAM  | 芝奇 Trident Z5 RGB DDR5-6400 CL32-39-39-102 1.40V 64GB (2x32GB) |
| MB   | TUF Gaming B850-Plus WiFi                  |
| Cooler | TUF Gaming LC II 240 ARGB                     |
| PSU  | EVGA 850 GS 850W 金牌全模組                             |
| Case | NZXT H5 Flow 2022              |

或許是我更換 Ryzen 9 9950X 作為 All-in-One 之後，我可以感知到的是我的電費正在悄然上漲，由於 NAS 的特性，難以使 Server 的資源占用下降，因此讓我起心動念，額外準備一台 NAS，將原本的需求進行拆分。  
雖然，這規格在效能上，是真的非常強悍。  
不過電費的支出，但對於目前仍是學生身分為主的我來說，長此以往，多少會有些感到力不從心。  
且不巧的是，我手上的 True-NAS 平台遭遇多顆硬碟同時故障，也因此讓我重新思考，是否改繼續使用 True-NAS，亦或是繼續使用虛擬機安裝 True-NAS。

#### 虛擬化架構：在 All-in-One 道路上的探索
目前我的 True-NAS 是以虛擬機的形式，安裝在 Proxmox VE Server 當中。  
選擇 Proxmox VE 作為主系統的原因，就只是因為透過 Proxmox VE 可以把原有的硬體進行拆分，讓一台電腦就可以安裝不同的 OS，成為 All In One 的 HomeLab。

我在 PVE 內，分配給 True-NAS 的硬體規格只有 2-Core 以及 4 GB RAM，並且在 True-NAS 上，我安裝了 4 顆硬碟，其中有兩顆 4TB HDD，以及一顆 2TB HDD，還有一顆是 250GB 的 SATA SSD（原先是另一顆 1TB HDD）。

![image](/assets/img/posts/HJaJUTJAel.png)

這些硬碟都是以直通的方式，直接分配給 True-NAS 的虛擬機系統。
![image](/assets/img/posts/H1QoITkAee.png)



主角登場 — Asustor AS6702T v2 開箱與初見
---
![P_20251021_121026](/assets/img/posts/r1SEbMYRle.jpg)

在我第一眼看到 Asustor AS6702Tv2 的時候，就總感覺這個包裝相當簡潔，一點也沒有多餘花俏的額外設計。

![P_20251021_121053](/assets/img/posts/HkXaZGY0xe.jpg)

隨著主機附帶的另一盒裝，是其他的周邊配件，Asustor 在這個物價漸漲的時代，非但沒有減配，甚至還有增配。

![P_20251021_121313](/assets/img/posts/HJNLfMYRel.jpg)

隨機附帶的包含了台達製造的 65W 變壓器，還有兩條 Cat5E 的網路線，以及兩種長度的螺絲各 16 顆。

<table>
  <tr>
    <td><img src="/assets/img/posts/S12fEftCgl.jpg" alt="P_20251021_121322"></td>
    <td><img src="/assets/img/posts/SyM7VzF0eg.jpg" alt="P_20251021_121332"></td>
  </tr>
</table>


外觀上繼承了上一代 AS6702T 相同的外觀，但在規格上，Asustor 把上一代的 2.5GbE 的網路介面卡，進行升級成為 5GbE。  
~~就是一種雖然我用不到，但你不能不給。~~ 在我目前的使用情境之下，我將兩張網路介面卡，接入 2.5GbE 的交換機，並且啟用鏈路聚合的功能，這樣便可以使兩張網路介面卡均發揮他們自己的職責。


#### 詳細拆機
<table>
  <tr>
    <td><img src="/assets/img/posts/r12dUfFRlg.jpg" alt="P_20251021_121510"></td>
    <td><img src="/assets/img/posts/SJlY8fKAlx.jpg" alt="P_20251021_121907"></td>
  </tr>
  <tr>
    <td><img src="/assets/img/posts/ByEY8zKRll.jpg" alt="P_20251021_121957"></td>
    <td><img src="/assets/img/posts/Hk5FIGFAxl.jpg" alt="P_20251021_122303"></td>
  </tr>
</table>

1. 兩個 HDD 硬碟托盤
    這部分需要使用到螺絲安裝。
2. 4 個 M.2 硬碟插槽
    M.2 PCIE SSD 可透過免螺絲安裝，對於使用者來說相當友善。
3. 額外的 DDR4 SO-DIMM 插槽
    機器上已經先預裝一條 DDR4 3200 4GB（在背面）
4. 完整的主機板（背面），以及我自行擴充上的 DDR4 3200 8GB
    剛好我手邊還有一條 DDR4 3200 8GB 的聯想筆電拆機記憶體

<table>
  <tr>
    <td><img src="/assets/img/posts/HJc1YGtRxg.jpg" alt="P_20251021_122357"></td>
    <td><img src="/assets/img/posts/SJ1gYGFRll.jpg" alt="P_20251021_122430"></td>
  </tr>
</table>


透過側邊空隙，可以拍到另一條預先安裝的 DDR4 3200 4GB 記憶體，不過我就有點不知道該如何更換這條記憶體了，貌似需要把整塊主機板拆下來（？）

透過在 SSH Terminal 執行 `dmidecode -t memory` 指令，可以取得我已安裝的兩條 DDR4 3200 SO-DIMM 記憶體資訊，且預裝的記憶體是 **ACPI Digital Co Ltd** 的產品。

```
root@Edward-AS6702T:/volume1/home/edwardwu # dmidecode -t memory
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 3.2.0 present.

Handle 0x0000, DMI type 16, 23 bytes
Physical Memory Array
        Location: System Board Or Motherboard
        Use: System Memory
        Error Correction Type: None
        Maximum Capacity: 32 GB
        Error Information Handle: Not Provided
        Number Of Devices: 2

Handle 0x0001, DMI type 17, 92 bytes
Memory Device
        Array Handle: 0x0000
        Error Information Handle: Not Provided
        Total Width: 64 bits
        Data Width: 64 bits
        Size: 8 GB
        Form Factor: SODIMM
        Set: None
        Locator: Controller0-ChannelA
        Bank Locator: BANK 0
        Type: DDR4
        Type Detail: Synchronous
        Speed: 3200 MT/s
        Manufacturer: SK Hynix
        Serial Number: 75C3D261
        Asset Tag: 9876543210
        Part Number: HMAA1GS6CJR6N-XN
        Rank: 1
        Configured Memory Speed: 2933 MT/s
        Minimum Voltage: Unknown
        Maximum Voltage: Unknown
        Configured Voltage: 1.2 V
        Memory Technology: DRAM
        Memory Operating Mode Capability: Volatile memory
        Firmware Version: Not Specified
        Module Manufacturer ID: Bank 1, Hex 0xAD
        Module Product ID: Unknown
        Memory Subsystem Controller Manufacturer ID: Unknown
        Memory Subsystem Controller Product ID: Unknown
        Non-Volatile Size: None
        Volatile Size: 8 GB
        Cache Size: None
        Logical Size: None

Handle 0x0002, DMI type 17, 92 bytes
Memory Device
        Array Handle: 0x0000
        Error Information Handle: Not Provided
        Total Width: 64 bits
        Data Width: 64 bits
        Size: 4 GB
        Form Factor: SODIMM
        Set: None
        Locator: Controller0-ChannelB
        Bank Locator: BANK 1
        Type: DDR4
        Type Detail: Synchronous
        Speed: 3200 MT/s
        Manufacturer: ACPI Digital Co Ltd
        Serial Number: 0620000C
        Asset Tag: 9876543210
        Part Number: 7D402902
        Rank: 1
        Configured Memory Speed: 2933 MT/s
        Minimum Voltage: Unknown
        Maximum Voltage: Unknown
        Configured Voltage: 1.2 V
        Memory Technology: DRAM
        Memory Operating Mode Capability: Volatile memory
        Firmware Version: Not Specified
        Module Manufacturer ID: Bank 8, Hex 0xF7
        Module Product ID: Unknown
        Memory Subsystem Controller Manufacturer ID: Unknown
        Memory Subsystem Controller Product ID: Unknown
        Non-Volatile Size: None
        Volatile Size: 4 GB
        Cache Size: None
        Logical Size: None
```

除此之外，可以在輸出結果中看到，BIOS 設定的記憶體最大值是 32GB，但官網上只寫最大支援 16GB，這部分我可以之後再進行實測。
![image](/assets/img/posts/rJbWSE7kZe.png)


由繁化簡的旅程 — ADM 系統體驗
---
在我初次接上電源開機之後，就相當期待上手體驗 Asustor NAS 所搭載的 ADM 系統。  
我將兩張網路介面卡都插上網路線，所以在我的 Router 中，可以看到兩個 Mac Address 以及透過 DHCP 取得兩個區域網路 IP。

![20251021-124104](/assets/img/posts/BkkMlraRgx.png)


Asustor 也有提供 Asustor Contorl Center，簡稱 ACC，可以協助使用者更快的在區域網路內檢測到 Asustor 的產品，進一步選擇產品進行連線或是其他相關設定。

![20251021-124443](/assets/img/posts/BJv5lrT0lx.png)

其中我也將我的初始化步驟進行截圖：

<table>
  <tr>
    <td><img src="/assets/img/posts/ByGLZBpRxg.png" alt="20251021-124511"></td>
    <td><img src="/assets/img/posts/rkfLWH6Ael.png" alt="20251021-124521"></td>
  </tr>
  <tr>
    <td><img src="/assets/img/posts/S1MIbH6Cxl.png" alt="20251021-124536"></td>
    <td><img src="/assets/img/posts/B1M8WB60xx.png" alt="20251021-124732"></td>
  </tr>
  <tr>
    <td><img src="/assets/img/posts/Sy6RKs6Rel.png" alt="20251021-124752"></td>
    <td><img src="/assets/img/posts/H1pRFiaCge.png" alt="20251021-124850"></td>
  </tr>
  <tr>
    <td><img src="/assets/img/posts/HJa0KjTRgl.png" alt="20251021-124949"></td>
    <td><img src="/assets/img/posts/S1pRKs60gg.png" alt="20251021-125256"></td>
  </tr>
</table>

其中最令我驚豔的是，過去在 True-NAS 上要設定網路介面卡鏈路聚合得花不少工夫，而在 ADM 上因系統易用、成品 NAS 設計完整，現在只要幾個步驟就能完成相關設定的初始化。

但我短期內不打算撤掉現有的 True-NAS。  
部分考量是近期硬碟價格偏高，導致安裝在 Asustor AS6702T v2 上的只有兩顆 WD Purple 4TB，無法容納全部資料，因此接下來只會將 True-NAS 的配置做精簡。  
未來我會把較重要的資料放在 AS6702T v2，True-NAS 則作為家庭影音的儲存庫。

初始化完成後，我開始轉移原本的資料。由於 True-NAS 仍在運作，有些資料一度只存在其中一端。  
為了避免這種情況，我透過 ADM 系統提供的「備份中心」排程同步，True-NAS 雖然也有類似功能，但僅支援 rsync 傳輸。  
相較之下，ADM 上 Asustor 提供了 rsync、SMB、FTP 等多種協議，替使用者省下不少心力與時間。


<table>
  <tr>
    <td><img src="/assets/img/posts/BkHIUEQkZe.png" alt="20251101-152545"></td>
    <td><img src="/assets/img/posts/Syz98N71bl.png" alt="20251030-155052"></td>
  </tr>
</table>

而我也在使用過後，多次收到系統更新，Asustor 在更新系統這方面，相當積極解決系統 bug 以及修復穩定性、安全性。

<table>
  <tr>
    <td><img src="/assets/img/posts/rk2jPNm1-x.png" alt="20251024-003335"></td>
    <td><img src="/assets/img/posts/B1x3w4m1Zg.png" alt="20251101-153119"></td>
  </tr>
</table>

同時，ADM 系統仍保留許多平時不太會特別注意的細節功能，例如 MOV 影片格式的縮圖。反觀隔壁家，竟然還得花 11.99 美元購買這種基礎功能的授權。

![Screenshot_20251107-075411_Facebook](/assets/img/posts/BJ9_xjh1bg.jpg)

至於另一家 S 牌，甚至是將影片縮圖直接取消，這大大的影響了所有將 NAS 作為影音資料庫的使用者，無論是專業創作者還是家庭用戶。這項改動，等於是親手關上了檔案預覽的窗口，讓檔案總管不再是直觀的媒體庫，而是一長串冰冷的檔名列表。

試想一下，當你想從數十個家庭旅遊影片中，找到孩子第一次看見雪的那個片段，卻只能一個個點開檔案、等待載入，原本溫馨的回味瞬間變成了惱人的尋寶遊戲。  
而對於影片剪輯師或攝影師而言，這更是災難性的工作流程中斷，在海量素材中快速預覽、挑選合適的 B-roll 畫面是創作的日常，少了縮圖等於是被蒙上了眼睛，嚴重拖慢專案進度。  
將這種攸關核心體驗的基礎功能拔除，並將其包裝成需要額外付費的項目，無疑是將商業考量凌駕於使用者體驗之上，也讓 Asustor 在這方面「理所當然」的堅持，顯得格外可貴。

![20251110-193812](/assets/img/posts/Skcn0Byx-x.png)


#### Dr. ASUSTOR
由於近幾年，勒索病毒盛行，Asustor 也相當貼心，於 ADM 系統中提供了 **Dr. ASUSTOR** 套件軟體，透過一鍵式的檢測服務，替使用者進行安全性的把關。

<table>
  <tr>
    <td><img src="/assets/img/posts/Bkq_J6hJZe.png" alt="20251108-210048"></td>
    <td><img src="/assets/img/posts/H1a_yphy-l.png" alt="20251108-210114"></td>
  </tr>
</table>

這樣一來，使用者可以很快看出自己的 NAS 是否位在相對安全的網路環境中，進而降低資料外洩、遭勒索加密等風險，也減少對資安的擔憂。  
也正是這種從使用者角度出發的設計理念，讓我對品牌 NAS 改觀，並逐漸放下過去堅持的 DIY NAS。


區域網路效能實測
---
首先，我使用 `iperf3` 進行區域網路的速度測試，分別是我的 True-NAS 到 AS6702Tv2 以及 Proxmox VE 主機到 AS6702Tv2。

<table>
  <tr>
    <td><img src="/assets/img/posts/Hk59Dqh1Wx.png" alt="20251108-180659"></td>
    <td><img src="/assets/img/posts/SyT9w9hy-x.png" alt="20251108-181132"></td>
  </tr>
</table>

▲ 圖一是從 True-NAS 到 AS6702Tv2 / 圖二是從 Proxmox VE 主機到 AS6702Tv2

由於我目前的網路環境最高只有 2.5GbE 的 Switch，因此暫時也只能跑出 2.5GbE 的速度。從 `iperf3` 的測試數據可以看出，AS6702T v2 能夠把 2.5GbE 的區域網路頻寬完整榨乾。至於 5GbE 網卡，對家庭、小型工作室或個人工作者來說，雖然仍屬於「戰未來」的規格，但在這個價位帶願意提供 5GbE 網路介面的廠商中，Asustor 仍是少數之一。

在區域網路測試的部分，我在撰寫本文時原本預計使用 AS6702T v2 內建軟體中心（APP Central）所提供的 OpenSpeedtest，並從我的主力桌機進行測速。

<table>
  <tr>
    <td><img src="/assets/img/posts/rJNPA521-e.png" alt="20251108-184110"></td>
    <td><img src="/assets/img/posts/rkKXRq2k-e.png" alt="20251108-183959"></td>
  </tr>
</table>

比較可惜的是，我的主機板 ROG CROSSHAIR VIII DARK HERO（ROG C8DH）在 10/23 凌晨故障，並於當天送至華碩皇家申請保固維修，因此暫時無法透過桌機進行區域網路效能測試。
![20251108-181824](/assets/img/posts/B1cK6cnJZx.png)

同時我也慶幸，自己早就把重要資料和短期內需要的工作檔案放在 NAS 上。  
雖然桌機裡的硬碟改成外接也能暫時讀取資料，但在我這種硬碟數量不少的情況下，還是有些不便。  
尤其主機板送修這段時間，還得臨時把原本的工作環境和資料搬到筆電上，因此對經常需要在多台電腦間切換的我而言，NAS 可說正好擊中需求。

By the way，現在在蝦皮的官方商城購買新品，竟然還有送 2.5G*5 Asustor ASW205T 的交換器，有夠划算，替使用者的荷包省下一筆開銷。
![20251110-191807](/assets/img/posts/H1R-qHJe-e.png)
購買連結：[asustor 華芸蝦皮官方旗艦店](https://tw.shp.ee/CkdzK4D)

總結 - 權衡之後，我選擇了穩定與效率
---
DIY NAS 的彈性確實迷人，但其維護成本（時間與金錢）也是無法忽視的現實。  
從我原先高規格的 Proxmox VE + True-NAS 平台，轉換到 Asustor AS6702T v2，本質上就是一次從「極致客製化」走向「高效穩定」的戰略轉移，核心目的在於降低功耗與管理複雜度。

Asustor AS6702T v2 的表現可說超出我的預期。  
它不僅在這個價位帶提供相當前瞻的硬體規格（雙 5GbE 網孔、四組 M.2 插槽），搭載的 ADM 系統也大幅降低了管理門檻，使用體驗有明顯的躍升，讓我終於可以卸下「網管」這層身分。

之後主力主機雖然意外故障，卻剛好驗證了這個決定的附加價值。  
它清楚證明：當擁有一個獨立且可靠的資料儲存中心時，面對單一硬體故障，依然能維持工作流程的連續性與資料完整性。  
這起事件並不是我決定轉換的主因，但的確進一步凸顯了，從 All-in-One 轉向獨立 NAS 設備，在風險分散上有多麼重要。

About Me
---
我是 EdwardWu
- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram : [_920223](https://www.instagram.com/_920223/)
- GitHub : [bluehomewu](https://github.com/bluehomewu)
- Email : [bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)

![image](/assets/img/posts/Bk1EYGfYA.png)

###### tags: `Android` `Asustor` `Asustor AS6702T v2` `ROM` `AS6702T v2` `True-NAS`
