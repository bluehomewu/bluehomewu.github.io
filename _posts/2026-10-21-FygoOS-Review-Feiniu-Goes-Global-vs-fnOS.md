---
title: 飛牛走向國際：FygoOS 上手評測，與 fnOS 差在哪？
description: "飛牛國際版 NAS 系統 FygoOS 上手評測：在 Proxmox VE 虛擬機實測語系、儲存空間、應用中心與 Docker，並與 fnOS 比較功能差異。"
date: 2026-10-21
categories: [FnNAS, FygoOS]
tags: [FnNAS, FnOS, FygoOS, NAS]
---

# 飛牛走向國際：FygoOS 上手評測，與 fnOS 差在哪？

![QQ20261021-214950](/assets/img/posts/rJx6uurIhfg.png)

▲ 這次的主角是 FygoOS。

前言
---
在上一篇 Evo 4 Pro 的評測裡，我提到 fnOS 目前只支援簡體中文，對台灣的使用者來說還不夠國際化；而飛牛團隊另外為國際市場推出了 FygoOS。  
當時我留下了一句「之後會另外寫一篇文章進行評測」，這篇就是來兌現這個承諾的。

和前兩篇不同，這次的主角不是一台飛牛的硬體，而是一套系統。  
我把 FygoOS 裝在家中 Proxmox VE 主機的一台虛擬機上，從語系、儲存空間到應用中心與 Docker，實際走過一輪，看看它和我已經熟悉的 fnOS 有哪些相同、又有哪些不同。

也因為是在虛擬機上測試，這篇會以系統功能為主，不涉及硬體效能、功耗與溫度這類和實體機器相關的項目。

> 還沒看過我之前的飛牛文章，可以先從這裡開始：  
> -> [當平靜的機架再起漣漪：飛牛 Evo 2 與我的 Asustor AS6702T v2]({% link _posts/2026-02-03-Ripples-in-the-Quiet-Rack-Integrating-the-FN-Evo-2-with-Asustor-AS6702T-v2.md %})  
> -> [從家庭機架到辦公環境：飛牛 Evo 4 Pro 開箱與使用評測]({% link _posts/2026-10-21-FN-Evo-4-Pro-Review-From-Home-Rack-to-Office.md %})

FygoOS 是什麼
---
從名稱與介面來看，FygoOS 和 fnOS 明顯同屬飛牛的生態系，但兩者的定位不同：fnOS 主要面向中國市場，FygoOS 則是面向國際市場推出的版本。  
介面上的對應關係也相當直接，fnOS 的「飛牛帳號」與「FN Connect」，在 FygoOS 上分別換成了 Fygo Account 與 FygoConnect。

依照 [FygoOS 官方網站](https://www.fygonas.com/)的說明，它可以在 x86 與 ARM 硬體上執行，官網列出的平台包含 Intel、AMD，以及 Rockchip、FriendlyElec、Radxa、Raspberry Pi 等 ARM 平台。  
商業模式上，FygoOS 提供免費版與付費授權兩種選擇，這也是它和 fnOS 很不一樣的地方，後面會再詳細說明。

測試環境
---
這次的 FygoOS 安裝在我家中的 Proxmox VE 主機上。  
這台主機的平台是 AMD Ryzen 9 9950X，升級過程可以參考我之前的這篇：[Proxmox 家用伺服器大升級：TUF Gaming B850-Plus WiFi × Ryzen 9 9950X 實戰紀錄]({% link _posts/2025-06-17-Proxmox-Home-Server-Upgrade-TUF-Gaming-B850-Plus-Ryzen-9-9950X-Build-Log.md %})。

我分配給 FygoOS 虛擬機的資源如下：

| 項目 | 本次配置 |
| --- | --- |
| **虛擬化平台** | Proxmox VE 9.2.11 |
| **主機處理器** | AMD Ryzen 9 9950X |
| **虛擬機 CPU** | 4 核心（CPU 類型：host） |
| **虛擬機記憶體** | 4GB |
| **系統碟** | 60GB 虛擬磁碟（qcow2，VirtIO SCSI） |
| **資料碟** | 100GB 虛擬磁碟（qcow2，VirtIO SCSI） |
| **網路** | VirtIO |
| **安裝映像** | `fygoos_PE_x86_1.2.0604_2686.iso` |
| **系統版本** | FygoOS 1.2.0800 |
| **授權** | 免費版 |

兩顆虛擬磁碟都放在主機上的 Crucial MX500 SATA SSD，並開啟了 `iothread` 與 `ssd=1`。  
我用 1.2.0604 的映像檔完成安裝，再透過系統內建的更新升級到撰文時的 1.2.0800。

![QQ20261021-214714](/assets/img/posts/Bkep__SLhGx.png)

▲ Proxmox VE 中 FygoOS 虛擬機的硬體設定

![QQ20261021-214142](/assets/img/posts/rk6_drUnfx.png)

▲ FygoOS 的裝置資訊頁面：FygoOS 1.2.0800、4 核心、4GB 記憶體

語系：還是沒有繁體中文
---
語系是我想寫這篇文章的起點。  
FygoOS 目前支援英文、日文、簡體中文、德文、西班牙文與法文六種語言，相較於只支援簡體中文的 fnOS，確實更符合「國際版」的定位。

不過，這六種語言裡，同樣還沒有繁體中文。  
對台灣、香港的使用者來說，選擇 FygoOS 並不會讓介面變得更親切：要嘛使用英文，要嘛和 fnOS 一樣面對簡體中文。

![QQ20261021-214058](/assets/img/posts/H1TOdrLnzl.png)

▲ FygoOS 的語系選單：English、日本語、简体中文、Deutsch、Français、Español

我也把介面切換成英文試用了一下，從桌面上的應用名稱到系統設定的各個項目，都已經換成英文，翻譯品質也還不錯，用起來沒有遇到太大的問題。  
不過，因為我已經習慣 fnOS 的操作邏輯，用簡體中文反而能更快找到對應的功能，所以這次評測最後還是選擇用簡體中文操作，文中的截圖也以簡體中文介面為主。

![QQ20261021-215156](/assets/img/posts/SkpduSUhMg.png)

▲ 切換成英文介面的 FygoOS

儲存空間
---
初次進入 FygoOS 時，系統還沒有任何儲存空間。  
建立儲存空間的流程和 fnOS 一樣分成四個步驟：選擇檔案系統、選擇硬碟與儲存模式、選擇可使用的使用者，最後確認資訊。

<table>
  <tr>
    <td><img src="/assets/img/posts/SkTOdB8hGg.png" alt="QQ20261021-214228"></td>
    <td><img src="/assets/img/posts/HJ6ddSLnzl.png" alt="QQ20261021-214241"></td>
  </tr>
  <tr>
    <td><img src="/assets/img/posts/rk6O_SLhzg.png" alt="QQ20261021-214255"></td>
    <td><img src="/assets/img/posts/rkT_OrUhMe.png" alt="QQ20261021-214319"></td>
  </tr>
</table>

▲ 建立儲存空間：初始畫面、選擇檔案系統（上排）／選擇硬碟與儲存模式、選擇使用者（下排）

第一步的檔案系統，FygoOS 提供 ext4、Btrfs 與 ZFS 三種選擇，每一種都附上了優點、缺點與適用情境的說明，對新手來說相當友善：

- **ext4**：成熟、穩定、相容性好，但不支援快照、壓縮與資料校驗等進階功能。
- **Btrfs**：支援快照，同一子卷內複製檔案的效率高，但在大規模儲存與高負載情境下的穩定性較弱。
- **ZFS**：支援快照、壓縮與重複資料刪除，資料保護與錯誤自我修復能力強；代價是資源占用較高，系統建議每 TB 儲存空間配置 1GB 記憶體，最低推薦 8GB 記憶體起步。

能直接在圖形介面中選擇 ZFS，對重視資料完整性的使用者來說是一大加分。  
不過，我自己在 NAS 上一直習慣使用 Btrfs + Linear 的組合，這台虛擬機也只分配了 4GB 記憶體，低於 ZFS 建議的 8GB，所以這次依然選擇了 Btrfs。

第二步的儲存模式會依照選取的硬碟數量變化。  
這台虛擬機只有一顆 100GB 的資料碟，因此只能選擇沒有資料保護的 Basic 或 Linear；介面上會清楚標示可用容量、理論效能與資料防丟能力，Linear 也直接註明了「任意一塊硬碟損壞，將遺失整個儲存空間的所有資料」的風險。  
第三步可以設定哪些使用者能使用這個儲存空間，以及是否限制每位使用者的可用容量；最後一步確認資訊時，還可以選擇是否執行硬碟讀寫檢測。

![QQ20261021-214331](/assets/img/posts/ByauuBU3fl.png)

▲ 確認資訊：Btrfs、Linear、預計可用容量 100GB

應用中心與 Docker
---
建立好儲存空間後，FygoOS 會跳出「歡迎來到 FygoOS」的引導視窗，提供一鍵安裝 Fygo 相簿與 Fygo 影視、設定 FygoConnect 遠端存取（標示為永久免費），以及設定安全信箱等選項。

![QQ20261021-214413](/assets/img/posts/Bkau_rU2zl.png)

▲ 建立儲存空間後的「歡迎來到 FygoOS」引導視窗

### 應用中心
應用中心的版面和 fnOS 幾乎一致，首頁主打 Fygo TV、AI Photo、Fygo Sync 與 File Snapshot，下方則列出 12 個飛牛官方應用，包含文件快照、Fygo Sync、Fygo TV、iSCSI，以及兩款分別對應 AMD Vitis AI 與 AMD MIGraphX 的 Fygo AI 引擎。  
左側的分類則有影音娛樂、攝影錄像、AI、下載、備份同步、開發工具、實用效率、生活等。

![QQ20261021-214401](/assets/img/posts/r1au_H83zx.png)

▲ FygoOS 的應用中心

不過，當我在免費版上點擊安裝時，系統跳出了「無有效許可證，請前往【系統設定-許可證】查看詳情」的提示，無法安裝。  
對照[官方的定價頁面](https://www.fygonas.com/pricing)，免費版列出的內建應用只有備份、Docker 與下載，「App Center Full Features」則只出現在試用、Plus 與 Lifetime 三種授權中。  
換句話說，免費版目前無法透過應用中心安裝這些官方應用。

![QQ20261021-214550](/assets/img/posts/Skga_OSLhMe.png)

▲ 在免費版上安裝應用時出現的「無有效許可證」提示

另外，和 fnOS 相比，FygoOS 應用中心裡的應用並沒有完全同步。  
目前 Fygo 推出的應用，大多還停留在幾個月前 fnOS 的版本，因此部分近期才在 fnOS 上架的應用，在 FygoOS 上還看不到。

### Docker
Docker 是免費版就包含的內建應用。  
第一次開啟時，系統會提示需要先設定 Docker 的儲存路徑；選擇剛建立的儲存空間 1 之後，Docker 服務就能正常啟動，並提供容器、Compose、本地映像、映像倉庫與網路等管理頁面，也可以設定開機自動啟動。

<table>
  <tr>
    <td><img src="/assets/img/posts/rk6OOSInfl.png" alt="QQ20261021-214604"></td>
    <td><img src="/assets/img/posts/rJlp_OH82Ge.png" alt="QQ20261021-214616"></td>
  </tr>
</table>

▲ 首次開啟 Docker 時的路徑設定提示（左）／設定完成後的 Docker 概覽（右）

對於熟悉容器的使用者來說，即使無法使用應用中心，也還能透過 Docker 自行部署需要的服務；不過這次我沒有在 FygoOS 上實際部署容器，因此不在這篇文章中評價它的使用體驗。

與 fnOS 的差異
---
同樣來自飛牛，FygoOS 和我在 Evo 2、Evo 4 Pro 上使用的 fnOS 有不少相似之處，但在幾個關鍵的地方走向了不同的方向。

| 項目 | **fnOS** | **FygoOS** |
| --- | --- | --- |
| **目標市場** | 中國 | 國際 |
| **我測試的版本** | 1.2.0604（Evo 4 Pro） | 1.2.0800（PVE 虛擬機） |
| **介面語系** | 簡體中文 | 英文、日文、簡體中文、德文、法文、西班牙文 |
| **繁體中文** | 不支援 | 不支援 |
| **授權** | 免費使用，少數進階功能另行授權 | 免費版＋付費授權 |
| **應用中心** | 可直接安裝 | 免費版無法安裝官方應用 |
| **遠端存取** | FN Connect | FygoConnect（永久免費） |
| **LDAP** | 不支援 | 不支援 |

兩者最大的差異，其實不在功能，而在商業模式。  
fnOS 本身可以免費使用，少數授權都是真正額外的進階功能，例如我在 Evo 4 Pro 上購機隨附的「飛牛素材庫企業旗艦版」；FygoOS 則把應用中心等功能放進了付費授權裡，免費版能用的範圍明顯比 fnOS 來得小。

授權方案與免費版限制
---
FygoOS 和 fnOS 最大的差別之一，是它採用了付費授權的商業模式。  
依照[官方的授權說明](https://help.fygonas.com/articles/v1/license/about-license)與[定價頁面](https://www.fygonas.com/pricing)，目前共有四種版本：

| 版本 | 價格 | 效期 | 使用者 | 儲存裝置 | 應用中心 |
| --- | --- | --- | --- | --- | --- |
| **Free** | 免費 | 永久 | 最多 3 位 | 最多 4 個 | 未列出 |
| **Trial** | 免費 | 30 天 | 最多 3 位 | 最多 4 個 | 完整功能 |
| **Plus** | US$49 | 1 年 | 不限 | 不限 | 完整功能 |
| **Lifetime** | US$199 | 永久 | 不限 | 不限 | 完整功能 |

> 價格與方案內容以撰文時的官方頁面為準。Plus 授權到期後，使用者與儲存裝置會回到 3 位、4 個的限制。

四種版本都包含 ext4、Btrfs、ZFS 檔案系統、永久免費的遠端存取，以及備份、Docker、下載等內建應用；差別主要在使用者與儲存裝置的數量，以及應用中心是否能完整使用。

這次我使用的是免費版。  
以我在虛擬機上、只有一位使用者與一顆資料碟的測試情境來說，使用者與儲存裝置的數量限制都碰不到；真正影響體驗的，是應用中心無法安裝官方應用。  
如果只打算把 FygoOS 當成單純的檔案儲存，再搭配 Docker 自行部署服務，免費版其實已經夠用；但如果想使用 Fygo 相簿、Fygo TV 這類官方應用，就需要考慮試用或付費授權。

仍待補強的地方
---

### 依然缺少繁體中文（台灣）
FygoOS 雖然把語系擴充到六種，但仍然沒有繁體中文。  
作為一套主打國際市場的系統，繁體中文的缺席，讓台灣與香港的使用者只能在英文與簡體中文之間做選擇。  
期待未來 FygoOS 能把繁體中文（台灣）加入支援的語系。

### 缺少 LDAP 帳號整合
和 fnOS 一樣，FygoOS 目前也不支援 LDAP。  
對家庭使用者來說影響不大，但 FygoOS 的付費授權主打不限使用者數量，顯然也考慮到了多人使用的情境；如果能接入 LDAP，就能讓團隊沿用既有的帳號系統，減少重複建立帳號與帳號管理上的風險。  
期待 FygoOS 與 fnOS 都能在後續版本中加入這項功能。

### 應用中心與 fnOS 尚未同步
FygoOS 的應用中心目前和 fnOS 並沒有完全同步，Fygo 的應用大多還停留在幾個月前 fnOS 的版本，近期才在 fnOS 上架的應用，在 FygoOS 上還找不到。  
既然兩者同屬飛牛的生態系，期待未來兩邊的應用能夠補齊，讓國際版的使用者也能享有和 fnOS 相同的應用選擇。

總結
---
FygoOS 讓我看到，飛牛並不打算只停留在中國市場。  
六種介面語系、圖形介面中就能直接選擇的 ZFS，以及永久免費的 FygoConnect 遠端存取，都顯示它正試著用一套更符合國際使用習慣的方式，把 fnOS 累積下來的經驗帶到更多地方。

實際用下來，對已經熟悉 fnOS 的我來說，FygoOS 幾乎沒有學習成本：從系統設定、儲存空間的建立流程，到應用中心與 Docker 的介面，兩者的操作邏輯都高度一致。  
建立儲存空間時，每一種檔案系統與儲存模式都附有清楚的優缺點與風險說明，對第一次接觸 NAS 的使用者也相當友善。  
在虛擬機上安裝與運作也相當順利，4 核心、4GB 記憶體的配置就能跑得起來。

不過，FygoOS 和 fnOS 最大的不同，在於它的商業模式。  
fnOS 可以免費使用大部分功能；FygoOS 的免費版則把應用中心排除在外，想安裝 Fygo 相簿、Fygo TV 這類官方應用，就得選擇試用或付費授權。  
對只需要檔案儲存與 Docker 的使用者來說，免費版已經足夠；但如果是衝著飛牛的官方應用而來，就需要把授權費用一起納入考量。

另一方面，對台灣的使用者來說，FygoOS 和 fnOS 面對的是同一個問題：沒有繁體中文。  
再加上同樣缺少 LDAP、應用中心也還沒和 fnOS 同步，FygoOS 作為國際版，還有不少可以補齊的地方。

**適合誰：**

- 想自組 NAS 或在虛擬機上部署，希望嘗試飛牛生態系，但偏好英文等非中文介面的使用者
- 重視資料完整性，希望在圖形介面中直接使用 ZFS 的使用者
- 主要需求是檔案儲存與 Docker，使用規模在免費版限制內的個人或家庭使用者

**可能不適合誰：**

- 需要繁體中文介面的使用者
- 想使用飛牛官方應用，但不打算付費的使用者
- 需要與 LDAP 等既有帳號系統整合的團隊

About Me
---

我是 EdwardWu

- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram：[_920223](https://www.instagram.com/_920223/)
- GitHub：[bluehomewu](https://github.com/bluehomewu)
- Email：[bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)

###### tags: `FnNAS` `FnOS` `FygoOS` `NAS`
