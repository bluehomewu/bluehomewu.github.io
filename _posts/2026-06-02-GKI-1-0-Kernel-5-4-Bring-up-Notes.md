---
title: GKI 1.0 Kernel 5.4 Bring-up 筆記
date: 2026-06-02 23:34:57 +0800
categories: [Android]
tags: [Android, Qualcomm, SM8350, lahaina, GKI, Kernel, Bring-up]
---

# GKI 1.0 Kernel 5.4 Bring-up 筆記

前言
---

近期正在 bring-up 一台 SM8350（lahaina）裝置，也就是 Snapdragon Insiders Phone。

原本 kernel bring-up 一直是我的罩門，但這次居然無師自通……所以趁我還有印象，趕快把筆記寫下來 XD

環境與工具鏈
---

我這次直接在 LineageOS 18.1 的 ROM source 環境下準備，原始碼可以只同步 `depth=1`，也可以完整同步。

主機環境使用 `Ubuntu 22.04.5 LTS x86_64`。

確認 Kernel 基線
---

這次參考的 kernel source 有三份：

- ASUS 提供的 open-source kernel package
- Qualcomm CLO（CAF）
- [LineageOS/android_kernel_asus_sm8350 lineage-18.1](https://github.com/LineageOS/android_kernel_asus_sm8350/tree/lineage-18.1)

![ASUS kernel source package](/assets/img/posts/Sytl9d3lMe.png)

首先，可以從 kernel tree 的 `Makefile` 看出目前的 kernel 版本是 5.4.147。

![Makefile 中的 Linux 5.4.147 版本資訊](/assets/img/posts/HyJVcu3xfg.png)

接著查看 kernel tree 下的 `android/GKI_VERSION`，找出 kernel version 後方的 hash value。

![android/GKI_VERSION 內的 kernel hash](/assets/img/posts/rkTw5d3lMx.png)

先用 kernel version 到 [Telegram Channel：CAF Release](https://t.me/CAFReleases) 或 [Telegram Channel：CLO Release](https://t.me/CLOReleases) 尋找大致的 tag 範圍，再選擇 Vendor Manifest，對照 `kernel/msm-5.4` repo 的 commit hash（revision）。

以我的例子來說，最後找到的 tag 是 `LA.UM.9.14.r1-18600-LAHAINA.0`。CAF 已經遷移到 CLO，但 CLO 沒有保留 18600，只剩 18400 與 18900，所以我只好到 Wayback Machine 碰碰運氣。運氣還不錯，最後有找到對應的 [LA.UM.9.14.r1-18600-LAHAINA.0.xml](https://web.archive.org/web/20220424122452/https://source.codeaurora.org/quic/la/la/vendor/manifest/tree/LA.UM.9.14.r1-18600-LAHAINA.0.xml)。

合併 Qualcomm 模組
---

找到 OEM kernel 所基於的 base kernel tag 之後，先合併 Qualcomm techpack 與 `vendor_dlkm` 需要的模組。

這邊使用 `git subtree` 進行合併。5.4 kernel 也是最後一個大版本可以使用獨立樹編譯的方案；從 5.10（Qualcomm 平台為 SM8450／SM8475）開始就是 GKI 2.0，無法再用同樣的方式處理。

指令格式如下：

`git subtree add/pull --prefix=<subtree path> <repo URL> <tag / branch / commit hash>`

每個 hash 一樣從 Vendor Manifest 裡的 revision 尋找。

```shell
git subtree add --prefix=drivers/staging/qcacld-3.0 https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/wlan/qcacld-3.0 375e1427d7cef0d4559fc23437e9aede0d012c0c
git subtree add --prefix=drivers/staging/qca-wifi-host-cmn https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/wlan/qca-wifi-host-cmn 0284b04846627ff817d30f1845367369c5a7546d
git subtree add --prefix=drivers/staging/fw-api https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/wlan/fw-api 6024f778d21e2943bbaa6a3cdc0e93f2325d29b7
git subtree add --prefix=techpack/video https://git.codelinaro.org/clo/la/platform/vendor/opensource/video-driver 66d44ae87e787c17a9e57a2649240fff6c9450f2
git subtree add --prefix=techpack/display https://git.codelinaro.org/clo/la/platform/vendor/opensource/display-drivers 33194b0322cf7dbc69e4e9595dc5c238088ad478
git subtree add --prefix=techpack/dataipa https://git.codelinaro.org/clo/la/platform/vendor/opensource/dataipa a1ac1922bc79f2a28b88447630cd6d6b96edac39
git subtree add --prefix=techpack/camera https://git.codelinaro.org/clo/la/platform/vendor/opensource/camera-kernel 945d74685ef27aecbda23f7919f04e025c7055c5
git subtree add --prefix=techpack/audio https://git.codelinaro.org/clo/la/platform/vendor/opensource/audio-kernel e00ea8c677818f9a1bea3567c4aabc8e3768cf25
git subtree add --prefix=techpack/datarmnet https://git.codelinaro.org/clo/la/platform/vendor/qcom/opensource/datarmnet 90c79e7045113de2e1d4011fe7c1a34c27d5913e
git subtree add --prefix=techpack/datarmnet-ext https://git.codelinaro.org/clo/la/platform/vendor/qcom/opensource/datarmnet-ext b622a4d5e63466e2a3810c5f9045a8b8559dbe81
```
{: .linenos }

範例可以參考 [android_kernel_asus_sm8350 的 subtree commits](https://github.com/bluehomewu/android_kernel_asus_sm8350/commits/lineage-18.1-wip/?after=1bdc02b777a5323565350a020faff0289e4c5c70+34)。

![使用 git subtree 匯入 Qualcomm 模組的 commits](/assets/img/posts/BJ7ryF2xzx.png)

更新 Subtree
---

之後需要更新 subtree 時，可以使用下面這組指令：

```shell
git subtree pull --prefix=drivers/staging/qcacld-3.0 https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/wlan/qcacld-3.0 375e1427d7cef0d4559fc23437e9aede0d012c0c
git subtree pull --prefix=drivers/staging/qca-wifi-host-cmn https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/wlan/qca-wifi-host-cmn 0284b04846627ff817d30f1845367369c5a7546d
git subtree pull --prefix=drivers/staging/fw-api https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/wlan/fw-api 6024f778d21e2943bbaa6a3cdc0e93f2325d29b7
git subtree pull --prefix=techpack/video https://git.codelinaro.org/clo/la/platform/vendor/opensource/video-driver 66d44ae87e787c17a9e57a2649240fff6c9450f2
git subtree pull --prefix=techpack/display https://git.codelinaro.org/clo/la/platform/vendor/opensource/display-drivers 33194b0322cf7dbc69e4e9595dc5c238088ad478
git subtree pull --prefix=techpack/dataipa https://git.codelinaro.org/clo/la/platform/vendor/opensource/dataipa a1ac1922bc79f2a28b88447630cd6d6b96edac39
git subtree pull --prefix=techpack/camera https://git.codelinaro.org/clo/la/platform/vendor/opensource/camera-kernel 945d74685ef27aecbda23f7919f04e025c7055c5
git subtree pull --prefix=techpack/audio https://git.codelinaro.org/clo/la/platform/vendor/opensource/audio-kernel e00ea8c677818f9a1bea3567c4aabc8e3768cf25
git subtree pull --prefix=techpack/datarmnet https://git.codelinaro.org/clo/la/platform/vendor/qcom/opensource/datarmnet 90c79e7045113de2e1d4011fe7c1a34c27d5913e
git subtree pull --prefix=techpack/datarmnet-ext https://git.codelinaro.org/clo/la/platform/vendor/qcom/opensource/datarmnet-ext b622a4d5e63466e2a3810c5f9045a8b8559dbe81
```
{: .linenos }

匯入 ASUS OEM 改動
---

完成 Qualcomm 模組的匯入之後，就可以開始套用 OEM 改動。我這邊參考 [LineageOS/android_kernel_asus_sm8350 lineage-18.1](https://github.com/LineageOS/android_kernel_asus_sm8350/tree/lineage-18.1) 的 commits 逐一修改。

bring-up 的範圍是從 `bdbba44aa7844342579011f8f155b2ffbd25fd7b` 到 `c0f842cd451da835ee6d91088d49ac57da01183a`。

特別需要注意的是 `a13732f3b6d00d3546e5c2e02008cd6b2f5aa7b3`：[treewide: Import ASUS changes from 18.1055.2305.249](https://github.com/bluehomewu/android_kernel_asus_sm8350/commit/a13732f3b6d00d3546e5c2e02008cd6b2f5aa7b3)。

我使用 `rsync` 匯入 source，並排除 `techpack` 資料夾：

```shell
rsync -av --exclude="techpack" ~/LexarNM790/WorkSpace/asus_i007_stock_kernel_ASUS_I007_1-18.1055.2305.249/kernel/msm-5.4/ ~/LexarNM790/lineage-18.1/kernel/asus/sm8350-workspace/
```
{: .linenos }

但我現在有一些後悔，因為 ASUS 的部分改動把前面匯入 Qualcomm techpack 的內容蓋回去了，因此後來又補了三個 commits：

1. [picasso: Drop duplicate display UAPI header](https://github.com/bluehomewu/android_kernel_asus_sm8350/commit/10ddf391fe437dafe59f98022d0b53ef757f0f65)
2. [picasso: Move camera device trees into include path](https://github.com/bluehomewu/android_kernel_asus_sm8350/commit/22db7614eb1474b1b40d9333a95b2057eb4b90e9)
3. [qcacld: Fix fw-api include dependencies](https://github.com/bluehomewu/android_kernel_asus_sm8350/commit/dff83019d7b41aa336508f399879d5e97f71a25b)

![補回被 OEM source 覆蓋的 Qualcomm techpack 改動](/assets/img/posts/BJ3IxKhlMg.png)

匯入 DTS 與 Techpack
---

完成 treewide OEM 改動後，接著把 `dts/vendor` 匯入進來：[arm64: dts: vendor: Import ASUS DTS from 18.1055.2305.249](https://github.com/bluehomewu/android_kernel_asus_sm8350/commit/8582c69e495ecc98ca538dff7ceb0c3aaaf9260e)。

DTS 完成之後，剩下的 techpack OEM 改動也要匯入。techpack 的部分我全部直接覆蓋；如果遇到 OEM 沒有修改的部分，就先忽略。

![匯入 ASUS DTS 與 techpack 改動的 commits](/assets/img/posts/S1YLbYhlGe.png)

後面剩下的，就是 bring-up 過程中還需要補上的 commits。

總結
---

這次的 kernel bring-up，讓我更理解 kernel 是怎麼編譯的，以及整個 workflow 是如何接續調用的。

接下來還有 GKI 2.0 的裝置要 bring-up……又是痛苦地獄了。

About Me
---

我是 EdwardWu

- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram：[_920223](https://www.instagram.com/_920223/)
- GitHub：[bluehomewu](https://github.com/bluehomewu)
- Email：[bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)

###### tags: `Android` `Qualcomm` `SM8350` `lahaina` `GKI` `Kernel` `Bring-up`
