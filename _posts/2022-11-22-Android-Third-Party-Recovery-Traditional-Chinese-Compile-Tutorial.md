---
title: Android 第三方 Recovery 繁體中文編譯教學
date: 2022-11-22
categories: [Android]
tags: [Android, Recovery, 編譯, 第三方, 教學]

---

# Android 第三方 Recovery 繁體中文編譯教學
#### 從零開始的編譯指南

挑選一個想要編譯的 Recovery
---
- [TWRP-omni](https://github.com/minimal-manifest-twrp/platform_manifest_twrp_omni)
- [TWRP-aosp](https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp)
- [TWRP-extra_repo](https://github.com/TeamWin/buildtree_manifests)
- [Orange Fox Recovery Project](https://gitlab.com/OrangeFox/Manifest)
- [SHRP](https://github.com/SHRP/platform_manifest_twrp_omni)
- [PBRP](https://github.com/PitchBlackRecoveryProject/manifest_pb)
- [RWRP](https://github.com/RedWolfRecovery/rw_manifest)

先備知識
---
- Linux 終端指令語法
- git 指令（至少需要基礎的能力）
- 永不放棄的心
- 一顆清晰的頭腦

配置一台主機
---
- CPU:至少4核心，建議8核心
- RAM:至少4GB (Android 10)，建議配置8GB以上
- 儲存空間容量:至少50GB，建議100GB
- 儲存裝置類型:HDD即可 (SATA 3)，SSD更好
- 系統:初學者建議安裝 Ubuntu 18.04 LTS / Ubuntu 20.04 LTS

安裝必要的編譯套件
---
- Ubuntu 18.04 LTS
```
sudo apt install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev openjdk-11-jdk git vim repo libwxgtk3.0-dev
```
- Ubuntu 20.04 LTS
```
sudo apt install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev openjdk-11-jdk git vim
```

設定 git
```
git config --global user.email "您的e-mail"
git config --global user.name "您的名字"
```

同步 Recovery 原始碼
---
#### 參考各個 Android Custom Recovery 的編譯 Manifest
##### 本文皆以 Orange Fox Recovery Project 與 ASUS ZenFone 4 Max (X00I)進行舉例
- 先建立資料夾
```
mkdir -p ~/OrangeFox
cd ~/OrangeFox
```
- 同步 Recovery 源代碼
```
repo init -u https://gitlab.com/OrangeFox/Manifest.git -b fox_9.0
```
```
repo sync -j8 --force-sync
```
#### 更新原始碼
- 在這之後如果有需要更新原始碼，請使用 repo sync 進行同步（更新 Recovery 原始碼）
```
repo sync
```
- 待原始碼同步完成之後，還需要配置 TWRP Device Tree

同步 TWRP Device Tree
---
```
Example: git clone {url} -b {branch name} {directory}

git clone Github連結 -b 分支 device/品牌名/機型代號
```
#### 範例如下：
```
git clone https://github.com/asusdevices/twrp_device_asus_X00I -b omni-9.0 device/asus/X00I
```
- 設定 Cache
```
export USE_CCACHE=1
export CCACHE_EXEC=/usr/bin/ccache
ccache -M 50G
```
- 都把檔案放置完成後，可以開始進行編譯
```
cd OrangeFox
source build/envsetup.sh
export ALLOW_MISSING_DEPENDENCIES=true
export FOX_USE_TWRP_RECOVERY_IMAGE_BUILDER=1
export LC_ALL="C"
lunch omni_裝置代號-eng && mka recoveryimage
```
##### 範例如下：
```
cd OrangeFox
source build/envsetup.sh
export ALLOW_MISSING_DEPENDENCIES=true
export FOX_USE_TWRP_RECOVERY_IMAGE_BUILDER=1
export LC_ALL="C"
lunch omni_X00I-eng && mka recoveryimage
```
##### 編譯 Orange Fox Recovery Project 使用的參數
[官方支援參數列表](https://gitlab.com/OrangeFox/vendor/recovery/-/raw/master/orangefox_build_vars.txt)
# 腳本
### 編譯 OFRP 腳本
```
#!/bin/bash
cd OrangeFox
. build/envsetup.sh
export ALLOW_MISSING_DEPENDENCIES=true
export LC_ALL="C"
export OF_AB_DEVICE=0
export FOX_REPLACE_BUSYBOX_PS=1
export FOX_REPLACE_TOOLBOX_GETPROP=1
export FOX_USE_TAR_BINARY=1
export FOX_USE_ZIP_BINARY=1
export FOX_USE_NANO_EDITOR=1
export OF_DISABLE_MIUI_SPECIFIC_FEATURES=1
export OF_NO_TREBLE_COMPATIBILITY_CHECK=1
export FOX_DELETE_AROMAFM=1
export OF_USE_LOCKSCREEN_BUTTON=1
export OF_SUPPORT_OZIP_DECRYPTION=1
export FOX_ADVANCED_SECURITY=1
export OF_MAINTAINER=維護者名字
export TW_DEVICE_VERSION="R11.0"
export FOX_VERSION=R11.0_0
export FOX_R11=1
export OF_USE_TWRP_SAR_DETECT=1
export TARGET_DEVICE_ALT="代號1,代號2"
lunch omni_裝置代號-eng && mka recoveryimage
```

#### 範例如下：
```
#!/bin/bash
cd OrangeFox
. build/envsetup.sh
export ALLOW_MISSING_DEPENDENCIES=true
export LC_ALL="C"
export OF_AB_DEVICE=0
export FOX_REPLACE_BUSYBOX_PS=1
export FOX_REPLACE_TOOLBOX_GETPROP=1
export FOX_USE_TAR_BINARY=1
export FOX_USE_ZIP_BINARY=1
export FOX_USE_NANO_EDITOR=1
export OF_DISABLE_MIUI_SPECIFIC_FEATURES=1
export OF_NO_TREBLE_COMPATIBILITY_CHECK=1
export FOX_DELETE_AROMAFM=1
export OF_USE_LOCKSCREEN_BUTTON=1
export OF_SUPPORT_OZIP_DECRYPTION=1
export FOX_ADVANCED_SECURITY=1
export OF_MAINTAINER=EdwardWu
export TW_DEVICE_VERSION="R11.0"
export FOX_VERSION=R11.0_0
export FOX_R11=1
export OF_USE_TWRP_SAR_DETECT=1
export TARGET_DEVICE_ALT="X00I,X00ID"
lunch omni_X00I-eng && mka recoveryimage
```
# Happy Hacking!

# 其他注意事項
### 編譯 Recovery 是一個不小的工程
- 推薦在編譯的時候使用 tmux 指令去新增一個 session 以便把當前的工作階段保留在後台
- 如果要上傳檔案到雲端硬碟，推薦使用 rclone 上傳檔案
- 需要熟悉 git 指令
- 建議編寫一些簡單的腳本方便自己執行命令

#### 參考資料連結
1. [tmux](https://git.io/JIUrH)
2. [tee](https://linux.vbird.org/linux_basic/0320bash.php#pipe_3)
3. [rclone](https://www.timelate.com/archives/install-rclone-on-ubuntu.html)
4. [git](https://link.medium.com/oQfJxibSRbb)
[修改 Commit 紀錄](https://gitbook.tw/chapters/using-git/amend-commit1.html)
[剛才的 Commit 後悔了，想要拆掉重做…](https://gitbook.tw/chapters/using-git/reset-commit.html)
[追加檔案到最近一次的 Commit](https://gitbook.tw/chapters/using-git/amend-commit2.html)
[同步遠端分支](https://zlargon.gitbooks.io/git-tutorial/content/remote/sync.html)
[Git 基礎 - 與遠端協同工作](https://git-scm.com/book/zh-tw/v2/Git-%E5%9F%BA%E7%A4%8E-%E8%88%87%E9%81%A0%E7%AB%AF%E5%8D%94%E5%90%8C%E5%B7%A5%E4%BD%9C)
[rename git branch locally and remotely](https://git.io/JIUKI)
[Git cherry-pick from another repository](https://coderwall.com/p/sgpksw/git-cherry-pick-from-another-repository)
[使用 Git 時如何做出跨 repo 的 cherry-pick](https://blog.m157q.tw/posts/2017/12/30/git-cross-repo-cherry-pick/)
[git 場景 ：從一個分支cherry-pick多個commit](https://www.itread01.com/content/1529341336.html)
[合併發生衝突了，怎麼辦？](https://gitbook.tw/chapters/branch/fix-conflict.html)
[下載Github上特定Repository內的資料夾](https://notes.andywu.tw/2018/%e4%b8%8b%e8%bc%89github%e4%b8%8a%e7%89%b9%e5%ae%9arepository%e5%85%a7%e7%9a%84%e8%b3%87%e6%96%99%e5%a4%be/)



# Q&A
1. 編譯過程遇到 FAILED 的時候，可以嘗試去看看哪個檔案造成的，它會寫在 FAILED 的後方
2. 如果真的遇到自己無法解決的問題，可以加入這兩個 Telegram 群組
[Android Building Help](https://t.me/AndroidBuildersHelp)
[RomDevelopment](https://t.me/alaskalinuxuser_romdevelopment)
3. [快速上手 Android Custom ROM 適配 - Prebuilt Vendor](https://hackmd.io/@EdwardWu/Prebuilt-bringup)
4. 等我想到還有什麼問題再加上來



## 聯絡我
- Telegram：[Edward Wu](https://t.me/edwardwu0223)
- 行有餘力的話，可以考慮捐款給我
[Paypal](https://www.paypal.me/edwardwu0223)
- 同場加映
[Android 第三方 ROM 繁體中文編譯教學](https://hackmd.io/@EdwardWu/CompileAndroidCustomROM)
- GitHub : [bluehomewu](https://github.com/bluehomewu)
- Email : [bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)


###### tags: `Android` `Recovery` `編譯` `第三方` `教學`
