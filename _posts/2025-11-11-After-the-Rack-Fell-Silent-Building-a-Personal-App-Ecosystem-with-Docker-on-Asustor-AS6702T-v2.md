---

title: 當機架歸於平靜之後：我如何在 Asustor AS6702T v2 上，用 Docker 打造個人應用生態系
date: 2025-11-10
categories: [Asustor]
tags: [Asustor]

---

# 當機架歸於平靜之後：我如何在 Asustor AS6702T v2 上，用 Docker 打造個人應用生態系

前言 — NAS 的靈魂，在於軟體賦予的可能性
---

> 還沒看過 Asustor AS6702T v2 的上手體驗文章看這邊  
> -> [當機架上的伺服器歸於平靜：我從 True-NAS 轉投 Asustor AS6702T v2 的心路歷程](https://hackmd.io/@EdwardWu/AsustorAS6702Tv2_review)

從「極致客製化」走向「高效穩定」的轉移，本質上是為了徹底落實「化繁為簡」的理念，從 DIY 的折騰回到成品 NAS 的穩定與省心；但如果只停在這裡，終究還是會覺得少了點什麼。

現今多數 NAS 的作業系統皆以 Linux 作為底層核心，也因此大幅提升了整體的可玩性。把硬體安頓好之後，下一步就是榨乾它的潛能：NAS 不該只是一顆網路硬碟，更可以是一台 24/7 運行的個人伺服器。

相較於傳統虛擬機（VM），Docker 容器的資源佔用更少、啟動更快、部署更標準化，非常適合在 NAS 這種硬體資源相對有限的設備上運行。


基礎建設 - 在 ADM 上部署 Docker 與圖形化管理工具 Portainer CE
---
以往在安裝 Docker 服務時，我習慣透過指令來設定參數，甚至連管理 Docker 都是用命令列完成。  
然而，在 SSH 環境下手動輸入指令，對新手來說不夠友善，對我而言也相當耗費時間與心力。  
因此在本篇中，我將改用圖形化管理工具，來管理 ADM 系統上的 Docker。


不過，在我們開始安裝 Portainer CE 之前，最核心也是最重要的，就是先安裝 Docker Engine，畢竟它才是 Docker 服務的核心。

1. 安裝 Docker Engine
    Docker Engine 可以直接在 ADM 的 APP Central 當中直接一鍵下載並完成安裝。
    ![20251109-160016](/assets/img/posts/Hy87c6TJ-x.png)

2. 安裝 Portainer CE
    Portainer 也可以直接在 ADM 的 APP Central 當中直接一鍵下載並完成安裝。  
    分為兩個版本，分別是官方原版，另一個是簡體中文的漢化版。  
    在我這篇，將會使用英文原版進行展示。
    ![20251109-165100](/assets/img/posts/r1vmIR6J-e.png)

3. 初始化 Portainer CE
    可以參考 [Asustor 的官方教學 - Portainer 基本功能介紹](https://www.asustor.com/zh-tw/online/College_topic?topic=145)  
    Asustor 官方提供很多教學相關的資源文件可以參考，寫的相當詳細。

4. 透過 Portainer CE 來管理 Docker
    初始化完成之後，便可以在面板中找到已經連線上的 AS6702T v2 了。
    ![20251109-170738](/assets/img/posts/S17WqC6kZx.png)
    點到左側的 Containers（容器），即可看到所有以 Docker 形式安裝在 AS6702T v2 的軟體。
    ![20251109-171721](/assets/img/posts/rJQN3Aaybx.png)
    ![20251109-171550](/assets/img/posts/HkKgn0pk-e.png)


雖然 Asustor 已經在 APP Central 當中提供許多以 Docker 形式安裝的常用軟體，但是支援的軟體總歸是需要透過 ASUSTOR Developer's Corner 去發行的。  
使用 Portainer CE 便可以自行任意安裝想要安裝的 Docker，深度客製化屬於自己的生態系。

而我會以 Code-Server 為例，將原本不在 APP Central 內的軟體，透過 Portainer CE 安裝在 AS6702T v2。

#### 安裝 Code-Server
1. 點擊 `Create container` 按鈕
2. 輸入要新增的 Docker 容器名稱以及來源
![20251109-173333](/assets/img/posts/SJGvekRJZl.png)
▲ 以 Code-Server 為例。

3. 點擊 `Deploy the container` 直接將 Docker 部屬到 AS6702T v2
![20251109-173736](/assets/img/posts/HyvgbJ0kWl.png)

4. 連線到 Code-Server
    在瀏覽器網址列當中輸入 `http://{AS6702Tv2 的內網 IP}:{Docker 映射出來的端口}`  
    在我的範例當中，就會是 `http://192.168.50.25:32769`
    ![20251109-181052](/assets/img/posts/SJ9gYyAyZl.png)
    如果有連上 Code-Server 的話，就應該會出現類似我圖片這樣：
    ![20251109-175110](/assets/img/posts/rkAgtk0yWl.png)

5. 大功告成！
    這樣就可以在自己的 NAS 上寫 code 了！  
    Happy Hacking！


Docker 應用使用體驗分享 - Tailscale
---
這次使用 Asustor ADM 系統最令我特別有感的是，以前在 True-NAS 上即便使用 Docker，很多欄位和參數都得自己手動填寫。改用 ADM 之後，這些設定大多不必再一項項輸入。  
一方面是因為 ADM 的 APP Central 已經集成了常用的 Docker 軟體包，大多數情況下也替使用者預先設定好基礎參數，讓學習成本大幅降低；另一方面則是搭配 Portainer CE，讓容器管理變得直覺、好上手，原本偏硬核的技術也變得平易近人。

例如這次我在 AS6702T v2 上安裝了 Tailscale 它是一套基於 WireGuard 協議的 VPN 異地組網服務。先前在 True-NAS 上部署時，不但常遇到斷線問題，並且版本不是最新的，初次連線還得手動使用 API Key 作為認證憑證。  
參考文章：[Truenas scale 安装 Tailscale 内网穿透远程连接SMB服务](https://blog.csdn.net/jh1513/article/details/132916005)

![20251110-192611](/assets/img/posts/r1jkhB1eZg.png)
▲ 在 True-NAS 上設定 Tailscale

但在 ADM 裡，我只需要在 APP Central 安裝 Tailscale，完成後點擊圖示，在新分頁中登入我的 Tailscale 帳號，就能完成異地組網。這大大減少了我在網路環境初始化上所花費的時間與心力。

<table>
  <tr>
    <td><img src="/assets/img/posts/Hymq3H1lbe.png" alt="20251110-192753"></td>
    <td><img src="/assets/img/posts/BkHq2rJeWx.png" alt="20251110-192821"></td>
  </tr>
</table>

▲ 在 Asustor NAS 上設定 Tailscale

這樣我便可以讓我放在公司所使用的桌機，甚至是攜帶出門的筆電，也可以直接透過 SMB 連接上放在家裡的 NAS，而不需要設定額外的 VPN，直接讓使用體驗變的絲滑流暢，就好像在家裡一樣。

Docker 應用使用體驗分享 - ollama + WebUI
---
近幾年時下最熱門的話題，無非是 AI 大型語言模型（LLM）。  
從 ChatGPT 的橫空出世到現在百花齊放的開源模型，AI 已經從遙遠的概念，變成了能實際提升生產力的工具。  
許多企業正積極將 AI 導入內部解決方案，但對於個人用戶或小型團隊來說，要在哪裡才能安全又便利地運行這些強大的模型呢？  
Asustor 緊跟這股趨勢，透過其強大的硬體與完善的 ADM 系統，為這個問題提供了一個絕佳的答案：  
讓個人的 NAS 也能參與這場 AI 本地化部署的盛宴，親手建造一台完全屬於自己的私有 AI 解決方案。

這其中最令人驚豔的，莫過於部署的便利性。  
過去，要在本地端運行 AI 模型，往往意味著要與複雜的指令、繁瑣的環境設定和無盡的依賴套件奮戰。  
然而在 Asustor NAS 上，這一切都變得出奇地簡單，只需要在 APP Central 當中下載並安裝 ollama + WebUI 套件，就能夠輕鬆部署目前最受歡迎的本地 AI 模型運行框架 Ollama。


我的部署組合是 Ollama 搭配 Open WebUI，前者是核心引擎，負責管理和運行像是 Llama 3、Mistral、gemma 等各種開源模型；後者則提供了一個媲美 ChatGPT 的精美圖形化聊天介面。整個安裝過程幾乎都在圖形介面下點擊完成，短短幾分鐘內，一個專屬於我的 AI 聊天機器人便已準備就緒。

而本地化部署的真正價值，體現在 「數據主權」 上。當我們使用雲端 AI 服務時，我們的提問、上傳的資料都將被送往第三方伺服器，這不僅有隱私外洩的風險，這些數據也可能被用於模型的後續訓練。  
但透過在 AS6702T v2 上運行的 Ollama，所有的運算都在這台 NAS 內完成。無論是請它總結一份包含敏感資訊的公司財報，或是讓它幫忙潤飾一篇尚未公開的文章，所有資料都始終留存在我的硬碟中，真正做到了 **「隱私零外洩」**。

這不僅僅是一個酷炫的玩具，更是一個強大的生產力工具。它能成為我的程式碼 Copilot、我的文案助理、我的知識檢索庫，而且這一切，都建立在絕對安全與私密的基礎之上。Asustor 讓這一切不再是高手的專利，而是每個使用者都能輕鬆觸及的可能。

![20251110-220549](/assets/img/posts/SJMUWdJxWx.png)

![20251110-220958](/assets/img/posts/Syjrzu1lWg.png)

Ollama 的模型有非常多，可以在 Ollama 的網站上找到清單
- [Ollama Library](https://ollama.com/library)

同場加映 - 把 ADM 的 SSH 終端環境介面變得賞心悅目 oh-my-zsh
---
由於我經常切換多台 Linux 的伺服器（包含了 Proxmox VE / True-NAS / Ubuntu / WSL2...等）多種不同的環境，各系統平台基於的 Linux 發行版也不見得相同。  
因此，使用的系統指令或是我曾在這個平台上所開發 / 修改功能所用到的指令、參數，無法完全熟記於心。

並且，透過使用自己客製化的 oh-my-zsh，也可以讓開發或是設定工作環境變得更高效。

![20251109-041431](/assets/img/posts/rJ33VmpyWx.png)

不過有些可惜的是，ADM 系統畢竟不是基於主流的 Linux 發行版為底進行擴展開發設計的平台，而是建立在 ASUSTOR 自行客製的輕量化 Linux 與封閉的 apkg 套件系統之上，更接近一套為 NAS 情境量身打造的專用韌體環境。  
這樣的設計在穩定性與維護成本上確實有優勢，但也代表使用者在套件選擇、開發工具相容性以及系統客製化的彈性上，難免會比以 Debian、Ubuntu 或 Alpine 等通用發行版為基礎的方案來得受限。

當我萌生想要安裝 oh-my-zsh 在 ADM 的環境上時，我有些不確定怎麼下手。不過，皇天不負有心人，終於還是讓我找到安裝的方法。  
首先，需要在 App Central 當中安裝一個軟體 - **entware**，他是用來將必要的軟體包安裝到我們的 AS6702T v2 上面。

![20251109-032613](/assets/img/posts/BJnKFzT1Wx.png)

接下來就可以盡情愉快的使用 opkg 來安裝必要的組件，其中最必須要透過 opkg 安裝的莫過於 oh-my-zsh 的核心 **zsh** 了。

1. 安裝 zsh
```
$ opkg install zsh
```
2. 檢查一下 zsh 版本
```
$ zsh --version
zsh 5.9 (x86_64-openwrt-linux-gnu)
```
3. 將 zsh 設為預設 shell
這步驟有些許麻煩，由於 Linux 發行版常見的 `chsh` 指令不存在於 ADM 的系統當中，因此只能另闢蹊徑。  
我在國外的論壇 StackExchange 上找到符合我需求的答案
https://superuser.com/a/1685460
![20251109-034848](/assets/img/posts/HkvnAz6yZx.png)

建立一個 `.profile` 檔案，填入以下內容：
```
if [[ -x /opt/bin/zsh ]]; then
  export SHELL=/opt/bin/zsh
  exec /opt/bin/zsh
fi
```
4. 安裝 [oh-my-zsh](https://ohmyz.sh/)，強大的 zsh 框架，下面擇一種方式安裝即可
```shell
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
```
```shell
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

接下來即可按照我有共同編輯的另一篇文章當中的 **設定 Z shell (zsh)** 段落進行設定  
直接由主題的段落開始接續執行 [2.4. 設定主題](https://hackmd.io/@billsun/BJByCIUHf#24-%E8%A8%AD%E5%AE%9A%E4%B8%BB%E9%A1%8C)

同場加映 - 為 ADM 的操作系統增加風格化的資訊界面 neofetch
---
neofetch 為 Linux 的一個軟體包，但由於前面提到的系統因素，終究是無法透過常見的軟體套件管理器把 neofetch 安裝到 Asustor AS6702T v2 上。  
因此，必須借助前面安裝 zsh 所用到的 **opkg** 來安裝 neofetch。  
而我也是參考他人的教學，手動編譯 neofetch 的 sources code，並成功安裝。
- [為 Openwrt 安裝 neofetch](https://milu.ink/80.html)

1. 安裝必要的依賴項目
```
opkg update
opkg install git （可以跳過不做，但需要在 APP Central 安裝 git）
opkg install make -y
```
然而，在 ADM 系統當中就已經有內建 `git` 的套件了，因此在 opkg 就無需重複安裝。

2. 從 GitHub 下載 neofetch 的 sources code
如果是要安裝在 Asustor ADM 系統上的話，建議使用我 fork 並修改過的 GitHub repo，因為我有針對 ADM 系統的需要進行微調。

```
git clone -b --depth=1 https://github.com/bluehomewu/neofetch.git
```

3. 進入資料夾
```
cd neofetch
```

4. 編譯 neofetch sources code
```
make install
```

5. 沒有輸出內容即為正常，可以輸入 `neofetch` 在終端機當中試試效果。

資源控管與效能實測
---
在我安裝了許多 Docker 相關的應用之後，相當好奇如此多的 Docker 是否會對於 NAS 有明顯的資源占用或是負擔，也因此我觀察了 ADM 的資源占用情況，我截至目前總共安裝了 9 個 Docker 的軟體服務，大多數的時候 CPU 以及記憶體均為相當低的情況。

<table>
  <tr>
    <td><img src="/assets/img/posts/HJRn3k01-x.png" alt="20251109-182309"></td>
    <td><img src="/assets/img/posts/SyzThkAkbx.png" alt="20251109-182320"></td>
  </tr>
  <tr>
    <td><img src="/assets/img/posts/S1Vpn10J-g.png" alt="20251109-182329"></td>
    <td><img src="/assets/img/posts/BkDp31AJWx.png" alt="20251109-182343"></td>
  </tr>
</table>

先前我在 True-NAS 上分配的硬體資源較少，資源占用也比 AS6702T v2 低。  
但由於 True-NAS 使用的是 Ryzen 9 9950X 分割出的 CPU 核心，單核心效能遠高於 Intel Celeron N5105，電費也就自然隨之上漲。


總結
---
使用 Docker 不僅能把多個服務集中在同一台裝置上，也能將它們彼此隔離，且佔用的硬體資源比一台 VM 更少。  
這次我把原先分散在各個裝置上的服務整合到 Asustor AS6702T v2 上，主要目的就是省電。透過 Docker，也能快速將原本的 Docker 環境搬移過來。

但這次體驗的核心，遠不止是服務的平移。  
更重要的是 Asustor ADM 平台如何將複雜的部署流程變得無比平易近人。以往在 True-NAS 上需要手動處理繁瑣參數的 Tailscale，如今在 APP Central 中點擊幾下就能完成設定，無痛串連所有裝置。  
甚至，運行 Ollama 這樣時下熱門的私有 AI 模型，也從一場命令列的戰鬥，變成了圖形化介面的一鍵安裝。  
ADM 負責處理了底層的繁雜設定，讓我能更專注於「玩」應用，而非「搞」定應用。  
這份省心，讓我既能享受到 Docker 帶來的強大客製化彈性，又不必被高聳的技術門檻所困。

這才是真正做到 —— **化繁為簡**。



About Me
---
我是 EdwardWu
- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram : [_920223](https://www.instagram.com/_920223/)
- GitHub : [bluehomewu](https://github.com/bluehomewu)
- Email : [bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)

![image](/assets/img/posts/Bk1EYGfYA.png)

###### tags: `Android` `Asustor` `Asustor AS6702T v2` `ROM` `AS6702T v2` `True-NAS`

