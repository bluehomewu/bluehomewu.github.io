---
title: 從家庭機架到辦公環境：飛牛 Evo 4 Pro 開箱與使用評測
categories: [FnNAS]
tags: [FnNAS, FnOS, NAS]
---

# 從家庭機架到辦公環境：飛牛 Evo 4 Pro 開箱與使用評測

![飛牛 Evo 4 Pro 主機外觀](/assets/img/posts/Bkj3lmKKGl.jpg)

▲ 這次的主角是飛牛 Evo 4 Pro。

前言
---
上一次寫飛牛 NAS 的評測時，我的 NAS 環境裡已經有一台 Asustor AS6702T v2。後來加入的 Evo 2，讓這套原本熟悉的配置多了一個新角色。那篇文章裡，我花了不少篇幅記錄兩台機器的分工，也透過這個過程，逐漸熟悉飛牛的硬體與 fnOS。對我來說，那是一次把新設備放進既有生活、重新安排資料存放方式的經驗。

這次輪到 Evo 4 Pro，故事的場景也從家裡換到了公司。我把它架設在辦公座位所在的私有區域網路，讓這台四盤位 NAS 有了和前一次不同的使用環境。從自己的家庭機架走進辦公空間，我對它的關注也跟著改變：除了能放多少資料、能安裝哪些應用，日常管理的方便程度，以及長時間運作時的散熱與功耗，都成了這次評測的一部分。

硬體上的變化同樣明顯。前一次接觸的 Evo 2 使用 Intel N150，這次 Evo 4 Pro 則換上 Intel Core i5-13500H，搭配 16GB 記憶體與四個 HDD 槽位。看到這樣的配置，我對它的期待也延伸到了檔案儲存之外。容器、檔案索引與其他常駐服務，都需要和儲存工作共用主機資源；更充裕的運算配置，讓這台 NAS 有了朝小型應用伺服器發展的空間。

機器已配備 10GbE 網路介面，但我目前的辦公區網仍停留在 1GbE；四個硬碟槽則裝入兩顆 2TB 與兩顆 4TB HDD，並分成兩個儲存空間。

回頭看，Evo 2 那篇記錄的是飛牛加入我原有 NAS 環境的過程；到了 Evo 4 Pro，我已經帶著前一次累積的使用經驗，換一個場景繼續接觸它。這次就從機身與內部結構開始，接著談我目前的儲存配置、fnOS，以及把這台 NAS 放進公司之後的使用觀察。

> 還沒看過我上一篇飛牛文章，可以先從這裡開始：
> -> [當平靜的機架再起漣漪：飛牛 Evo 2 與我的 Asustor AS6702T v2]({% link _posts/2026-02-03-Ripples-in-the-Quiet-Rack-Integrating-the-FN-Evo-2-with-Asustor-AS6702T-v2.md %})

飛牛 Evo 4 Pro 硬體規格
---
我這次使用的是 i5-13500H／16GB DDR4／128GB 系統碟版本。

| 項目 | 本次配置 |
| --- | --- |
| **機型** | 飛牛 Evo 4 Pro |
| **處理器** | Intel Core i5-13500H，12 核心、16 執行緒 |
| **記憶體** | 單條 16GB DDR4 3200MHz |
| **記憶體上限** | 官方標示最高 64GB |
| **系統碟** | 128GB PCIe 3.0 SSD |
| **資料碟** | 2 顆 2TB HDD＋2 顆 4TB HDD |
| **儲存配置** | 2 × 4TB、2 × 2TB 各組一個 Linear 儲存空間，皆為 Btrfs |
| **M.2 插槽** | 4 槽（含系統碟占用 1 槽；目前未另外安裝 M.2 SSD） |
| **網路介面** | 10GbE ×1（Realtek RTL8127）、2.5GbE ×1（Intel I226-V） |
| **無線網路** | Wi-Fi 6＋藍牙（MediaTek MT7920，AzureWave 模組） |
| **目前使用網路** | 2.5GbE 網路孔，以 1GbE 連線 |
| **系統版本** | fnOS 1.2.0604 |
| **售價** | CNY 4,899（i5-13500H／16GB／128GB 版本） |

> 資料來源：[飛牛 Evo 4 Pro 京東商品頁](https://item.jd.com/10234775690067.html)（售價以撰文時為準）

機身內建兩個 SO-DIMM 插槽，我這台目前只插了一條 16GB。記憶體的部分，官方另有出貨 32GB 的版本，並標示最高可擴充到 64GB。如果只看 Intel 官網的規格，i5-13500H 本身最高支援 96GB 記憶體；但 DDR4 SO-DIMM 單條最大通常是 32GB，在雙通道配置下，實際上限就落在 64GB，與官方的標示一致；後面拆機的段落，我也會用系統指令確認這一點。

開箱與機身外觀
---
Evo 4 Pro 的外盒延續飛牛一貫的黑色基調，正面只有金色的飛牛 logo 與「智能存储设备」字樣；背面貼有產品規格標籤，兩側則分別印著「智能存储新时代 从fnOS开始」的標語，以及 fnOS 主要功能的圖示。

<table>
  <tr>
    <td><img src="/assets/img/posts/B1zSw6Psfx.jpg" alt="IMG_20260914_213238826"></td>
    <td><img src="/assets/img/posts/HkMSDaviMl.jpg" alt="IMG_20260914_213245690"></td>
  </tr>
  <tr>
    <td><img src="/assets/img/posts/SJMBPavifg.jpg" alt="IMG_20260914_213249818"></td>
    <td><img src="/assets/img/posts/HJMBvpwszl.jpg" alt="IMG_20260914_213254991"></td>
  </tr>
</table>

▲ 外盒正面、背面規格標籤（上排）／兩側的標語與 fnOS 功能圖示（下排）

打開外盒，最上層是 Evo 4 系列的使用指南，主機則被兩側的緩衝材固定在中間，配件另外收納在一旁的配件盒中。

<table>
  <tr>
    <td><img src="/assets/img/posts/BJMBDaPszx.jpg" alt="IMG_20260914_213454629"></td>
    <td><img src="/assets/img/posts/SkfrDTPizx.jpg" alt="IMG_20260914_214839306"></td>
  </tr>
</table>

▲ 開箱後的使用指南與配件盒（左）／隨附印有飛牛 logo 的螺絲起子（右）

### 正面：只留下最常用的按鍵
機身採用金屬外殼，正面設計得相當簡潔，除了飛牛 logo 之外，只有 Reset 孔、一個 USB-A 與電源按鈕，也就是封面照片中間那台的樣子。和 Evo 2 一樣，Evo 4 Pro 的 Wi-Fi 也採用隱藏式天線，機身外看不到任何天線；面對正面時的右側側板，則印有點陣式的 EVO 字樣，整體就是一個俐落的金屬方塊。

![IMG_20260915_154824101](/assets/img/posts/BJ4BP6wsGe.jpg)

▲ 進駐辦公座位後的 Evo 4 Pro，右側側板印有點陣 EVO 字樣

### 背面：防塵飾板之下的硬碟槽與 I/O
硬碟槽與主要的 I/O 都集中在背面，平常由一片防塵飾板覆蓋。拿掉飾板之後，背面才露出真正的樣子：左側是四個編號 01～04 的硬碟槽，硬碟托盤直接從背面抽換，每個托盤都有拉帶方便抽出；右側則是一整排 I/O，由上而下依序為 3.5mm 音源孔、USB-C、兩個 USB-A、HDMI、10GbE 與 2.5GbE 網路孔，以及 DC 電源輸入。把硬碟槽與線材都收在背面，正面只保留日常會用到的按鍵與 USB，讓它擺在辦公桌上時看起來更加整潔。

![IMG_20260914_214335329](/assets/img/posts/rJzrPaPjfg.jpg)

▲ 拿掉防塵飾板後的背面：四個硬碟槽與 I/O

內部結構
---
Evo 4 Pro 的主機板被設計成一個可以整片抽出的模組，透過板邊的金手指與機身內的背板連接。抽出來之後，主機板背面可以直接看到 SO-DIMM 記憶體插槽，以及兩個覆蓋著散熱片的 M.2 插槽；另一面則是處理器的散熱模組，一顆鼓風扇搭配銅製導熱管，負責帶走 i5-13500H 的熱量，另外兩個 M.2 插槽就藏在這顆風扇下方。

<table>
  <tr>
    <td><img src="/assets/img/posts/HyQBwaviGe.jpg" alt="IMG_20260914_214451603"></td>
    <td><img src="/assets/img/posts/SkbrP6Pofl.jpg" alt="IMG_20260914_214514067"></td>
  </tr>
</table>

▲ 主機板背面的記憶體與兩個 M.2 插槽（左）／另一面的鼓風扇與導熱管，下方還有兩個 M.2 插槽（右）

### 從系統確認硬體
照片之外，我也透過 SSH 進到系統裡，確認這台 Evo 4 Pro 實際使用的網路晶片與記憶體配置。

先用 `lspci` 查看網路相關的裝置：

```
edwardwu@Edward-EVO4Pro:/$ lspci -nnk | grep -iA3 'network\|ethernet'
02:00.0 Ethernet controller [0200]: Realtek Semiconductor Co., Ltd. Device [10ec:8127] (rev 05)
        Kernel driver in use: r8127
2e:00.0 Ethernet controller [0200]: Intel Corporation Ethernet Controller I226-V [8086:125c] (rev 04)
        Kernel driver in use: igc
2f:00.0 Network controller [0280]: MEDIATEK Corp. Device [14c3:7920]
        Subsystem: AzureWave Device [1a3b:6471]
        Kernel driver in use: mt7921e
```

10GbE 網路孔使用的是 Realtek RTL8127，2.5GbE 則是 NAS 與迷你主機上相當常見的 Intel I226-V。無線網路的部分是 MediaTek MT7920 的 Wi-Fi 6 模組（由 AzureWave 製造），藍牙則透過 USB 介面連接，使用 `mt7921e` 驅動。

接著用 `dmidecode` 查看記憶體：

```
edwardwu@Edward-EVO4Pro:/$ sudo dmidecode -t memory
Physical Memory Array
        Location: System Board Or Motherboard
        Error Correction Type: None
        Maximum Capacity: 64 GB
        Number Of Devices: 2

Memory Device
        Size: 16 GB
        Form Factor: SODIMM
        Locator: Controller0-ChannelA-DIMM0
        Type: DDR4
        Speed: 3200 MT/s
        Manufacturer: 0x0080
        Part Number:
        Rank: 2
        Configured Memory Speed: 3200 MT/s
        Configured Voltage: 1.2 V

Memory Device
        Size: No Module Installed
        Locator: Controller1-ChannelA-DIMM0
```

▲ 節錄自 `dmidecode -t memory` 的輸出

主機板的韌體回報最大支援容量為 64GB、共兩個記憶體插槽，與官方標示的擴充上限一致。兩個插槽分別位於兩個記憶體控制器上，其中一個安裝了 16GB（Dual Rank、1.2V），另一個則是空的，也就是說目前是以單通道運作。預裝記憶體的實際運作頻率是完整的 3200 MT/s，不過模組的 SPD 沒有提供可辨識的製造商與料號資訊。如果之後要擴充，補上一條相同規格的記憶體，就能讓它以雙通道運作。

儲存配置：為什麼我選擇 Linear
---
這次的儲存配置，我選擇了 Linear，而不是 RAID 1 或 RAID 5。這個決定源自這台 Evo 4 Pro 在公司裡的角色。

### 它是部門內部的資料交換站
Evo 4 Pro 在辦公室的主要任務，是作為部門同事之間交換資料的地方。由於專案性質，我們日常往來的產品資料與工程 data 檔案都相當龐大。在這種情境下，**可用容量**是最直接的瓶頸：與其讓一半的硬碟空間用於鏡像，我更需要的是讓每一顆硬碟的容量都能被完整利用。

Linear 的特性正好符合這個需求。它會將多顆硬碟依序串接成一個儲存空間，不需要容量一致的硬碟，也不會因為鏡像或同位元檢查而損失容量。對於手上同時有 2TB 與 4TB 硬碟的我來說，這是讓空間最大化的方式。

實際配置上，我將四顆硬碟依容量分成兩組：兩顆 4TB HDD 組成一個 Linear 儲存空間，兩顆 2TB HDD 組成另一個，兩者皆使用 Btrfs 檔案系統。在 fnOS 中，兩個儲存空間的可用容量分別是 7.28TB 與 3.64TB，合計約 10.91TB。

![QQ20260917-000741](/assets/img/posts/HJ9SwTwsMe.png)

▲ fnOS 存儲空間管理：兩個 Linear 儲存空間相同容量的硬碟放在同一組，也讓之後要汰換或升級某一組硬碟時，不會牽動另一個儲存空間。

{% comment %}
可選：補一句兩個儲存空間各自的用途分配（例如哪一個放專案資料、哪一個放交換暫存）。
{% endcomment %}

### 冗餘交給多地備份
當然，Linear 沒有任何冗餘：只要儲存空間內任何一顆硬碟故障，該儲存空間的資料就可能無法存取。這一點我在規劃時就很清楚，因此資料保護並不是靠磁碟陣列，而是靠**多地備份**。

放在 Evo 4 Pro 上的資料，同時也會備份到公司的 File Server，以及公司提供的 OneDrive。一份在公司內部的伺服器上，一份在雲端，即使 Evo 4 Pro 的硬碟發生故障，資料仍然有兩個獨立的來源可以還原。對我來說，RAID 解決的是「硬碟壞掉時服務不中斷」，備份解決的則是「資料不會遺失」。這台 NAS 扮演的是交換與暫存的角色，即使發生硬碟故障，需要的是更換硬碟並從備份還原，而不是讓工作停擺。在這個前提下，我把容量優先於即時冗餘。

{% comment %}
可選：補上備份的排程頻率，若使用 fnOS 內建的備份功能，可附上設定截圖。
{% endcomment %}

### 為什麼沒有加裝 M.2 SSD 快取
Evo 2 那篇我把 SSD 快取視為影音體驗的關鍵，因為隨意拖曳高位元率影片時，機械硬碟的尋道延遲會直接影響播放。但 Evo 4 Pro 的工作型態不同：同事之間交換的多半是大型檔案的循序讀寫，而目前的網路瓶頸落在 1GbE。在這樣的條件下，HDD 的循序讀寫速度已經足以跑滿網路頻寬，SSD 快取能帶來的效益有限，因此我暫時沒有安裝。

不過，這並不代表我會一直讓那三個空著的 M.2 插槽閒置。隨著同事間交換的檔案越來越多，小檔案的隨機存取、資料夾瀏覽與索引，都是 SSD 快取能夠發揮的地方；如果之後網路升級到 2.5GbE 甚至 10GbE，HDD 的瓶頸也會更加明顯。因此我目前也在物色適合的 M.2 SSD，之後再來分享加裝快取後的使用變化。

fnOS 1.2 使用體驗
---
這台 Evo 4 Pro 執行的是 fnOS 1.2.0604。在系統設定的裝置資訊頁面中，可以一次看到系統版本、處理器、記憶體、儲存空間與網路狀態；從這裡也能看出，目前網路孔是以 1000Mbps 連線。

![QQ20260917-000718](/assets/img/posts/By5HvTvozl.png)

▲ fnOS 裝置資訊頁面

### 購機隨附的授權
購買 Evo 4 Pro 硬體，會隨附兩項 fnOS 的權益：一年期的「飛牛素材庫企業旗艦版」授權，以及 FN Connect 高級版（我的效期到 2031-10-19）。裝置完成註冊與啟用後，系統通知就會顯示權益已經生效。

<table>
  <tr>
    <td><img src="/assets/img/posts/H15BvpPjGl.png" alt="QQ20260917-003335"></td>
    <td><img src="/assets/img/posts/Bk9BwaDiGg.png" alt="QQ20260917-003413"></td>
  </tr>
</table>

▲ 許可證頁面（左）／啟用成功的系統通知（右）

不過需要注意的是，這些隨附權益會在**重灌系統後消失**。如果重灌之後需要恢復，就得另外聯繫飛牛官方處理，所以在重灌之前，最好先記下自己的授權資訊。

使用環境與測試方法
---
在進入實測之前，先說明 Evo 4 Pro 在我座位上的網路架構與測試條件。

### 網路架構
公司提供到我座位上的是一條有線網路。我在座位上放了一台刷入 OpenWrt 的 Cudy WR3000S 路由器，由它建立一個屬於我座位的私有區域網路：

```
公司有線網路
     │
    WAN
     │
Cudy WR3000S（OpenWrt）
     ├── LAN ─── 飛牛 Evo 4 Pro（SMB 445 埠經連接埠轉發供同事存取）
     ├── LAN ─── Edward-WorkPC（工作桌機）
     └── Wi-Fi ── 筆電
```

WR3000S 的有線埠皆為 1GbE，因此目前 Evo 4 Pro 與工作桌機之間的有線連線上限是 1GbE。這也是為什麼規格表上的 10GbE 介面，在這次的評測中沒有辦法發揮。

由於 Evo 4 Pro 位在 WR3000S 建立的私有網段內，部門同事無法直接連到它。因此我在 OpenWrt 上設定了連接埠轉發，將路由器 WAN 端（公司網路）的 SMB 連接埠 445 轉發到 Evo 4 Pro 的 445 埠。同事只要在公司網路中連到我這台路由器的位址，就能透過 SMB 存取 NAS 上的共用資料夾；而 fnOS 的管理介面與其他服務則沒有對外開放，只留在我座位的區域網路內。

### 測試條件

| 項目 | 條件 |
| --- | --- |
| **室溫** | 24 ℃ |
| **NAS** | 飛牛 Evo 4 Pro，fnOS 1.2.0604，系統預設設定；以 2.5GbE 網路孔（Intel I226-V）連接路由器 |
| **路由器** | Cudy WR3000S（OpenWrt），1GbE 有線埠 |
| **有線用戶端** | Edward-WorkPC（Intel I211 Gigabit 網路卡），透過 WR3000S 有線網路連接，1GbE |
| **測試工具** | `iperf3` 3.22（Windows 版）、SMB 檔案複製（Windows 檔案總管） |

網路效能實測
---

### iperf3
先用 `iperf3` 測試 Edward-WorkPC 與 Evo 4 Pro 之間的純網路傳輸能力。NAS 端執行 `iperf3 -s`，工作桌機端則以 `-B` 指定從區網介面發送，分別測試上傳（WorkPC → Evo 4 Pro）與加上 `-R` 的下載（Evo 4 Pro → WorkPC），每個方向各測 3 次。

![QQ20261013-153154_iperf3-1](/assets/img/posts/rkHNlPoife.png)
![QQ20261013-153233_iperf3-2](/assets/img/posts/HJBVlvosGe.png)
![QQ20261013-153302_iperf3-3](/assets/img/posts/S1S4xvsjGl.png)

▲ 上傳測試（WorkPC → Evo 4 Pro）連續 3 次的結果，左側為 NAS 端、右側為工作桌機端

![QQ20261013-153352_iperf3-R-1](/assets/img/posts/ByxHNxwjofg.png)
![QQ20261013-153420_iperf3-R-2](/assets/img/posts/HJHVevosGe.png)
![QQ20261013-153449_iperf3-R-3](/assets/img/posts/SkBVePjifg.png)

▲ 下載測試（Evo 4 Pro → WorkPC，`-R`）連續 3 次的結果

| 路徑 | 第 1 次 | 第 2 次 | 第 3 次 | 平均 |
| --- | --- | --- | --- | --- |
| 上傳（WorkPC → Evo 4 Pro） | 949 Mbps | 949 Mbps | 949 Mbps | 949 Mbps |
| 下載（Evo 4 Pro → WorkPC） | 947 Mbps | 949 Mbps | 948 Mbps | 948 Mbps |

> 數值取自接收端（receiver）的 10 秒平均。

雙向都穩定落在 948～949 Mbps，扣除 Ethernet 與 TCP/IP 的封包開銷後，這已經是 1GbE 實際能跑出的上限；每一秒的數值幾乎沒有波動，也代表 Evo 4 Pro 的 Intel I226-V 與整條有線鏈路都相當穩定。

### SMB 檔案傳輸
有了 iperf3 的基準，接下來看實際的檔案傳輸。我從 Edward-WorkPC 透過 Windows 檔案總管，在工作桌機與 Evo 4 Pro 的共用資料夾之間互相複製檔案。NAS 端的目的地是 DATA1，也就是由兩顆 2TB HDD 組成的儲存空間 1；工作桌機端則使用一顆 SATA SSD。測試分成兩種情境：

1. **多檔案資料夾**：一個實際的專案資料夾，包含 233 個檔案、74 個子資料夾，總計 6.56GB。
2. **單一大檔**：一個 15GB 的測試檔案（`test_data_15360.0MB.bin`）。

![QQ20261013-152105_SMB-1_filesize](/assets/img/posts/HyENxvojzl.png)

▲ 測試用專案資料夾的檔案數量與大小

<table>
  <tr>
    <td><img src="/assets/img/posts/rJEVgDijMe.png" alt="QQ20261013-152016_SMB-1"></td>
    <td><img src="/assets/img/posts/ByE4lDjjfg.png" alt="QQ20261013-152629_SMB-2_15GB"></td>
  </tr>
</table>

▲ 寫入：WorkPC → Evo 4 Pro，多檔案資料夾（左）／15GB 單一大檔（右）

<table>
  <tr>
    <td><img src="/assets/img/posts/Hkz1cvjjGe.png" alt="QQ20261013-153703_SMB-backtoWorkPC-1_blur"></td>
    <td><img src="/assets/img/posts/S1VExviozg.png" alt="QQ20261013-153808_SMB_backtoWorkPC-2"></td>
  </tr>
</table>

▲ 讀取：Evo 4 Pro → WorkPC，多檔案資料夾（左）／15GB 單一大檔（右）

| 測試項目 | 寫入（WorkPC → Evo 4 Pro） | 讀取（Evo 4 Pro → WorkPC） |
| --- | --- | --- |
| 多檔案資料夾（233 個檔案、74 個資料夾，6.56GB） | 約 110 MB/s | 約 86 MB/s |
| 單一大檔（15GB） | 約 106 MB/s | 約 108 MB/s |

> 數值為傳輸進行中，Windows 檔案總管顯示的即時速度。

單一大檔的讀寫都落在 106～108 MB/s，工作管理員中 Intel I211 網路卡的傳輸速率也來到 944 Mbps 到 1.0 Gbps，與 iperf3 的結果一致，等於把 1GbE 的頻寬完整跑滿。多檔案資料夾的寫入同樣有 110 MB/s；讀取則稍微降到 86 MB/s 左右。我推測是因為資料夾中混雜了大小不一的檔案，每個檔案之間都需要額外的開檔與中繼資料處理，HDD 也得在不同檔案之間尋道，這在多檔案傳輸中相當常見。

整體來說，在目前的環境裡，瓶頸確實落在 1GbE 網路，而不是 Evo 4 Pro 或 HDD 本身。對於部門之間交換工程資料的情境，這樣的表現已經足夠；而多檔案讀取時出現的落差，也正是前面提到、未來考慮加裝 SSD 快取想要改善的部分。

### 關於 10GbE

目前我手邊沒有 10GbE 網路卡，座位上的網路也只到 1GbE，因此這篇文章沒有測試 10GbE 的實際表現。以這次的配置來說，HDD 的循序讀寫速度本身就已超過 1GbE 的上限，網路才是真正的瓶頸。對於處理大型工程檔案的團隊來說，10GbE 介面等於替日後升級網路保留了空間；等我的環境具備條件，會再補上 10GbE 的實測。

溫度與功耗
---
這台 NAS 就放在我的辦公座位旁，需要長時間不間斷運作，因此散熱與功耗是我在辦公環境中特別留意的部分。

功耗的部分，我把 Evo 4 Pro 接在一個具備電力監測功能的智慧插座上。在四個硬碟槽都裝滿 HDD 的狀態下，待機時的即時功耗在 39～41W 之間。從當天的累計數據來看，運行 9.0 小時共用了 0.348 kWh，換算下來平均約 38.7W，與即時數值相當接近，代表待機時的功耗相當穩定。

![Screenshot_20261020-085934_Tapo](/assets/img/posts/ryMHpEE2Gg.jpg)

▲ 智慧插座 App 顯示的待機功耗：運行 9.0 小時、累計 0.348 kWh、即時功耗 41W

以這個數字推算，Evo 4 Pro 全天候開機一天大約會用掉 0.93 kWh，一個月約 28 kWh。量測時，我也用 `hdparm` 檢查了四顆硬碟的狀態，全部都是 active/idle，也就是四顆硬碟都在運轉中。

![QQ20261020-090259](/assets/img/posts/r1ukRNNhfx.png)

▲ 以 `hdparm -C` 檢查四顆硬碟的狀態，皆為 active/idle

這組 39～41W 反映的是四顆硬碟都在運轉時的待機功耗。對於一台搭載 i5-13500H、同時驅動四顆 3.5 吋 HDD 的 NAS 來說，這樣的數字算是合理。

溫度的部分，同樣在室溫 24 ℃、待機的狀態下，我透過 SSH 分別用 `sensors` 讀取 CPU 溫度，再用 `smartctl` 讀取四顆 HDD 的溫度：

```
edwardwu@Edward-EVO4Pro:/$ sensors | grep -E 'Package|Core'
Package id 0:  +43.0°C  (high = +100.0°C, crit = +100.0°C)
Core 0:        +39.0°C  (high = +100.0°C, crit = +100.0°C)
Core 4:        +34.0°C  (high = +100.0°C, crit = +100.0°C)
Core 8:        +36.0°C  (high = +100.0°C, crit = +100.0°C)
Core 12:       +39.0°C  (high = +100.0°C, crit = +100.0°C)
Core 16:       +40.0°C  (high = +100.0°C, crit = +100.0°C)
...
Core 23:       +44.0°C  (high = +100.0°C, crit = +100.0°C)

edwardwu@Edward-EVO4Pro:/$ for d in /dev/sd[a-d]; do echo -n "$d: "; sudo smartctl -A $d | awk '/Temperature_Celsius/ {print $10 " °C"}'; done
/dev/sda: 38 °C
/dev/sdb: 36 °C
/dev/sdc: 35 °C
/dev/sdd: 37 °C
```

▲ 待機時的 CPU 與 HDD 溫度（節錄）

| 項目 | 待機（室溫 24 ℃） |
| --- | --- |
| **CPU Package** | 43 ℃ |
| **CPU 各核心** | 34～44 ℃ |
| **HDD** | 35～38 ℃ |
| **功耗** | 約 39～41W（四顆 HDD 運轉中） |

CPU 封裝溫度只有 43 ℃，距離 100 ℃ 的上限還有相當大的空間，鼓風扇搭配銅導熱管的散熱設計，在待機時顯得游刃有餘。四顆 HDD 擠在同一個機身裡，溫度也都維持在 35～38 ℃ 之間，彼此差距不大，看得出硬碟槽之間的散熱相當平均；這個溫度區間對機械硬碟來說也相當理想，長時間運作不需要太擔心。

與 Evo 2 的差異
---
同樣是飛牛的硬體、同樣執行 fnOS，Evo 4 Pro 和我家裡的 Evo 2 卻走向了不同的定位。

![IMG_20260914_213942579](/assets/img/posts/BJfSw6wofg.jpg)

▲ 由左至右：Evo 2、Evo 4 Pro，最右側是 Asustor AS6702T v2

| 項目 | **飛牛 Evo 2** | **飛牛 Evo 4 Pro** |
| --- | --- | --- |
| **處理器** | Intel N150（4 核心、4 執行緒） | Intel Core i5-13500H（12 核心、16 執行緒） |
| **記憶體** | 8GB DDR4 | 16GB DDR4 |
| **硬碟槽** | 2 | 4 |
| **M.2 插槽** | 3 | 4 |
| **網路介面** | 5GbE ×1、2.5GbE ×1 | 10GbE ×1、2.5GbE ×1 |
| **我的儲存配置** | 2 × 4TB RAID 0＋512GB M.2 SSD 快取 | 2 × 2TB＋2 × 4TB，兩個 Linear 儲存空間 |
| **使用場景** | 家中影音中心 | 辦公室部門資料交換 |

Evo 2 的重點在於低功耗與影音體驗，N150 的硬體解碼搭配 SSD 快取，足以撐起一個家庭影音庫。Evo 4 Pro 則把重心放在容量與運算能力：四個硬碟槽讓總容量有更大的彈性，i5-13500H 則讓它在儲存之外，有餘裕同時執行容器與其他常駐服務。網路介面從 5GbE 提升到 10GbE，也反映出它更偏向工作用途的定位。

簡單來說，Evo 2 適合放在家中當作低功耗的影音伺服器，Evo 4 Pro 則更像是一台能進入小型團隊的工作儲存設備。

仍待補強的地方
---
把 Evo 4 Pro 放進辦公環境之後，有兩個地方是我在日常使用中最常遇到、也最希望 fnOS 補上的。

### 缺少 LDAP 帳號整合
目前 fnOS 不支援 LDAP。在家裡使用時，這並不是問題，但進入團隊環境後，影響就變得明顯。

我的部門雖然沒有打算讓 NAS 加入公司的 AD，但公司本身有提供 LDAP 服務給我們使用。如果 fnOS 能夠接入 LDAP，同事就能用平常的公司帳號登入 NAS，不必再另外維護一組帳號密碼；帳號的停用與權限調整也能跟著公司的帳號系統走，減少人員異動時遺留帳號的風險。對於管理者來說，這也代表不用在 NAS 上逐一建立與刪除使用者。

這並不只是我個人的需求，在[飛牛官方論壇](https://club.fnnas.com/forum.php?mod=viewthread&tid=26451)上，也有不少使用者提出希望支援 LDAP 的意見。期待 fnOS 能在後續版本中加入這項功能，讓它在團隊與小型辦公室的情境中更加完整。

### 尚未支援繁體中文（台灣）
目前 fnOS 只支援簡體中文。對於台灣的使用者來說，從系統用語到功能名稱，都需要額外花一點時間適應；放進辦公環境後，也不是每位同事都習慣簡體介面。

飛牛團隊另外開發了面向國際市場的 Fygo NAS，其系統 Fygo OS 目前支援英文、日文、簡體中文、德文、西班牙文與法文，但同樣還沒有繁體中文。關於 Fygo OS，我之後會另外寫一篇文章進行評測。

以 fnOS 目前的完成度，語系可說是它走向更多市場的最後一步。期待未來能在 fnOS 或 Fygo OS 上看到繁體中文（台灣）的支援。

總結
---
從家裡的 Evo 2 到公司的 Evo 4 Pro，飛牛在我的使用環境裡，從影音中心延伸到了團隊的資料交換。

Evo 4 Pro 最明顯的優勢，是硬體規格帶來的餘裕。i5-13500H 與 16GB 記憶體，讓它不只是一台存放檔案的設備，也保留了同時負擔儲存、檔案索引與其他服務的運算空間；四個硬碟槽則讓容量規劃更有彈性，即使像我一樣混用不同容量的硬碟，也能透過 Linear 將空間完整利用。10GbE 介面雖然在我目前的環境中還無法發揮，但對於經常處理大型檔案的團隊來說，這是一個值得預留的升級空間。

實際測試下來，Evo 4 Pro 在 1GbE 環境中的表現相當到位：iperf3 雙向都穩定在 948～949 Mbps，SMB 傳輸單一大檔的讀寫也維持在 106～108 MB/s，等於把 1GbE 的頻寬完整跑滿。即使是混雜大量檔案的專案資料夾，寫入仍有 110 MB/s，只有讀取時略降到 86 MB/s 左右。換句話說，在我目前的環境裡，真正的瓶頸是網路，而不是 Evo 4 Pro 本身。

放在座位旁長時間運作，Evo 4 Pro 的表現同樣讓人放心：待機時 CPU 封裝溫度約 43 ℃，四顆 HDD 維持在 35～38 ℃，整機功耗約 39～41W，一個月的用電量大約 28 kWh。

另一方面，fnOS 在團隊情境中仍有可以補強的地方。缺少 LDAP，代表帳號管理仍需要手動維護；缺少繁體中文（台灣），則讓它在台灣的辦公環境中多了一道門檻。這兩點都不影響它作為檔案交換與儲存設備的核心功能，但會是它能否真正走進更多辦公室的關鍵。

**適合誰：**
- 需要大容量共用空間、經常交換大型檔案的小型團隊或部門
- 想在同一台 NAS 上執行容器與常駐服務，需要比 N 系列處理器更多運算資源的使用者
- 已經有 10GbE 網路，或計畫在未來升級網路的環境

**可能不適合誰：**
- 需要與既有 LDAP／AD 帳號系統整合的組織
- 團隊成員需要繁體中文介面的環境
- 只需要家庭影音或輕量備份，以 Evo 2 這類雙盤位機種就已足夠的使用者

如果說 Evo 2 讓我認識了飛牛，那麼 Evo 4 Pro 則讓我看到，飛牛的硬體已經具備走出家庭機架、進入辦公環境的條件。接下來，就看 fnOS 能不能在帳號整合與在地化上，跟上硬體的腳步。

About Me
---

我是 EdwardWu

- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram：[_920223](https://www.instagram.com/_920223/)
- GitHub：[bluehomewu](https://github.com/bluehomewu)
- Email：[bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)

###### tags: `FnNAS` `FnOS` `飛牛` `Fn Evo 4 Pro` `Fn Evo 2` `NAS`
