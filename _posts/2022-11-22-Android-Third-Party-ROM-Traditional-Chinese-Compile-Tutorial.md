---
title: Android 第三方 ROM 繁體中文編譯教學
date: 2022-11-22
categories: [Android]
tags: [Android, ROM, 編譯, 第三方, 教學]

---

# Android 第三方 ROM 繁體中文編譯教學
<small>2021.09.01 更新文章 （支援 Android 11）
2022.02.05 更新文章 （支援 Android 12）</small>
#### 從零開始的編譯指南

挑選一個想要編譯的第三方 ROM
---
- [Havoc OS](https://github.com/Havoc-OS/android_manifest)
- [Arrow-OS](https://github.com/ArrowOS/android_manifest)
- [crDroid](https://github.com/crdroidandroid/android)
- [Pixel Experience](https://github.com/PixelExperience/manifest)
- [Lineage OS](https://github.com/LineageOS/android)
- 還有其他，這邊僅舉例常見的幾個 ROM

先備知識
---
- Linux 終端指令語法
- git 指令（至少需要基礎的能力）
- 永不放棄的心
- 一顆清晰的頭腦

配置一台主機
---
- CPU:建議8核心
- RAM:至少16GB (Android 10)，建議配置32GB (Android 12)以上
- 儲存空間容量:至少500GB，建議2TB
- 儲存裝置類型:HDD即可 (SATA 3)，SSD更好
- 系統:初學者建議安裝 Ubuntu 20.04 LTS

安裝必要的編譯套件
----
- 臺灣國家高速網路中心 :
```
sudo sed -i 's/tw.archive.ubuntu.com/free.nchc.org.tw/ubuntu' /etc/apt/sources.list
sudo sed -i 's/archive.ubuntu.com/free.nchc.org.tw/ubuntu' /etc/apt/sources.list
sudo sed -i 's/security.ubuntu.com/free.nchc.org.tw/ubuntu' /etc/apt/sources.list
sudo apt-get clean all
sudo apt-get update
```

- Ubuntu 18.04 LTS
```
sudo apt install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev openjdk-11-jdk git vim repo libwxgtk3.0-dev
```
- Ubuntu 20.04 LTS
```
sudo apt install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev openjdk-11-jdk git vim jq
```

設定 git 環境
```
git config --global user.email "您的e-mail"
git config --global user.name "您的名字"
```

同步 Android 原始碼
---
#### 參考各個 Android ROM 的 Android Manifest
##### 本文皆以 Arrow-OS（Android 12）與 ASUS ZenFone 5Z (Z01R) 進行舉例
- 先建立資料夾
```
mkdir -p ~/bin
mkdir -p ~/arrow-12
```

```
curl http://commondatastorage.googleapis.com/git-repo-downloads/repo > ~/bin/repo && chmod a+x ~/bin/repo
```
```
cd ~/arrow-12
```
```
repo init -u https://github.com/ArrowOS/android_manifest.git -b arrow-12.0
```
- 接下來便開始同步 Android 源代碼(大約150GB左右，視 Android 版本不同及編譯的ROM不同而有所差異)
```
repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags
```
#### 更新原始碼
- 在這之後如果有需要更新原始碼，請使用 repo sync 進行同步（更新系統原始碼）
```
repo sync
```
- 待所有原始碼同步完成後，還需要配置 Device Tree / Vendor Tree / Kernel Tree
- 另外，還需要額外下載 Kernel 的編譯器
#### GCC
```
git clone --depth=1 https://github.com/arter97/arm64-gcc -b master prebuilts/gcc/linux-x86/aarch64/aarch64-elf
git clone --depth=1 https://github.com/arter97/arm32-gcc -b master prebuilts/gcc/linux-x86/arm/arm-eabi
```
或是
```
git clone --depth=1 https://github.com/mvaisakh/gcc-arm64 -b gcc-master prebuilts/gcc/linux-x86/aarch64/aarch64-elf
git clone --depth=1 https://github.com/mvaisakh/gcc-arm -b gcc-master prebuilts/gcc/linux-x86/arm/arm-eabi
```
```
git clone --depth=1 https://github.com/Edward-Projects/gcc-arm64 -b Z01R prebuilts/gcc/linux-x86/aarch64/aarch64-elf
git clone --depth=1 https://github.com/Edward-Projects/gcc-arm -b Z01R prebuilts/gcc/linux-x86/arm/arm-eabi
```

#### Clang
```
git clone --depth=1 https://github.com/kdrag0n/proton-clang -b master prebuilts/clang/host/linux-x86/clang-proton
```

# 修改 Device Tree / Device Common Tree
#### 對於初學者來說，修改已經開發完成的Device Tree / Device Common Tree，應該會簡易許多
1. 首先在GitHub上面尋找對應裝置的Device Tree / Device Common Tree
2. Fork一份到自己的 GitHub 帳號底下
3. 修改以下列舉的檔案
```
# 箭頭表示需要重新命名
AndroidProducts.mk
Device.mk
extract-files.sh
lineage.dependencies → arrow.dependencies
lineage_Z01R.mk → arrow_Z01R.mk
setup-makefiles.sh
overly-lineage/ → overly-arrow/
```
4. 在這些檔案及資料夾當中尋找原本的系統所使用的代號，修改成你當前要編譯的系統代號
###### 參考範例: [Z01R: Initial Arrow bringup](https://github.com/Edward-Projects/android_device_asus_Z01R/commit/e1ea428085d65deda95bc4d5949f99c6a91037fc)
5. 系統代號如下：
```
Havoc OS : havoc
Arrow-OS : arrow
crDroid : lineage
Pixel Experience : aosp
Lineage OS : lineage
```
6. 系統代號有些地方是採用大寫字母，切勿更改為小寫字母，應保留原有樣式

 同步 Device Tree / Vendor Tree / Kernel Tree
---
##### 備註一下:有些裝置還有Device Common Tree / Vendor Common Tree / Kernel Common Tree 也要記得同步
###### 小提醒!!如果有遇到Vendor Tree內包含很多裝置的資料，可以善用文末的資料(最後一個網站) svn co 去下載單一個資料夾的東西
```
Example: git clone {ssh url} -b {branch name} {directory}

git clone Github連結 -b 分支 device/品牌名/機型代號

git clone GitHub連結 -b 分支 device/品牌名/SOC名稱-common

git clone Github連結 -b 分支 kernel/品牌名/SOC

git clone Github連結 -b 分支 vendor/品牌名
```
#### 範例如下:
```
git clone git@github.com:Edward-Projects/android_device_asus_Z01R.git -b arrow-12.0 device/asus/Z01R

git clone git@github.com:bluehomewu/kernel_z01r.git -b twelve kernel/asus/sdm845

git clone git@github.com:Edward-Projects/proprietary_vendor_asus_Z01R.git -b arrow-12.0 vendor/asus/Z01R
```
- 設定Cache
```
export USE_CCACHE=1
export CCACHE_EXEC=/usr/bin/ccache
ccache -M 50G
```
- 都把檔案放置完成後，可以開始進行編譯
```
. build/envsetup.sh
lunch 系統代號_裝置代號-編譯類型
brunch 系統代號_裝置代號-編譯類型
```
#### 範例如下：
```
. build/envsetup.sh
lunch arrow_Z01R-userdebug
brunch arrow_Z01R-userdebug
```

# 腳本
### 編譯ROM腳本
```
#!/bin/bash
#Build 裝置代號
cd ~/arrow
. build/envsetup.sh
brunch 系統代號_裝置代號-編譯類型| tee 系統代號_裝置代號_$(date +"%Y%m%d_%H.%M")GMT8.txt
 ```

#### 範例如下：
```
#!/bin/bash
#Build Z01R
cd ~/arrow
. build/envsetup.sh
brunch arrow_Z01R-userdebug | tee arrow_Z01R_$(date +"%Y%m%d_%H.%M")GMT8.txt
```

### 同步 Device Tree / Vendor Tree / Kernel Tree 的腳本

#### 把這個腳本修改完成後，保存成roomservices.xml檔案，複製至
```
~/havoc/.repo/local_manifest
```
```
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <project path="vendor/品牌名" name="帳號/repo name" remote="github" revision="分支名" />
    <project path="device/品牌名/機型代號" name="帳號/repo name" remote="github" revision="分支名" />
    <project path="kernel/品牌名/SOC" name="帳號/repo name" remote="github" revision="分支名" />
    <project path="prebuilts/gcc/linux-x86/aarch64/aarch64-elf" name="Edward-Projects/gcc-arm64" remote="github" revision="Z01R" clone-depth="1" /> 
    <project path="prebuilts/gcc/linux-x86/arm/arm-eabi" name="Edward-Projects/gcc-arm" remote="github" revision="Z01R" clone-depth="1" /> 
</manifest>
```


#### 範例如下：
```
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <project path="vendor/asus/Z01R" name="Edward-Projects/proprietary_vendor_asus_Z01R" remote="github" revision="arrow-12.0" />
    <project path="device/asus/Z01R" name="Edward-Projects/android_device_asus_Z01R" remote="github" revision="arrow-12.0" />
    <project path="kernel/asus/sdm845" name="bluehomewu/kernel_z01r" remote="github" revision="twelve" />
    <project path="prebuilts/gcc/linux-x86/aarch64/aarch64-elf" name="Edward-Projects/gcc-arm64" remote="github" revision="Z01R" clone-depth="1" /> 
    <project path="prebuilts/gcc/linux-x86/arm/arm-eabi" name="Edward-Projects/gcc-arm" remote="github" revision="Z01R" clone-depth="1" /> 
</manifest>
```

# Happy Hacking!!

# 其他注意事項
### 編譯 ROM 是一個大工程
- 推薦在編譯的時候使用 tmux 指令去新增一個 session 以便把當前的工作階段保留在背景
- 編譯的同時建議在（ brunch 系統代號_機型代號-編譯類型）後方加上 tee 指令，方便保存log檔案，如果有遇到 FAILED 便可以找到問題來源
- 如果要上傳檔案到雲端硬碟，推薦使用 rclone 上傳檔案
- 需要熟悉 git 指令
- 建議編寫一些簡單的腳本方便自己執行命令

#### 參考資料連結：
1. [tmux](https://git.io/JIUrH)
2. [tee](http://linux.vbird.org/linux_basic/0320bash.php#pipe_3)
3. [rclone](https://www.timelate.com/archives/install-rclone-on-ubuntu.html)
4. [為你自己學 Git 筆記 — GitHub 應用篇](https://link.medium.com/oQfJxibSRbb)
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
2. 如果真的遇到自己無法解決的問題，可以加入這三個 Telegram 群組
[Android Building Help](https://t.me/AndroidBuildersHelp)
[RomDevelopment](https://t.me/alaskalinuxuser_romdevelopment)
[Android OS Building Support](https://t.me/android_builders_help)
3. [快速上手 Android Custom ROM 適配 - Prebuilt Vendor](https://hackmd.io/@EdwardWu/Prebuilt-bringup)
4. 等我想到還有什麼問題再加上來



## 聯絡我
- Telegram：[Edward Wu](https://t.me/edwardwu0223)
- 行有餘力的話，可以考慮捐款給我
[Paypal](https://www.paypal.me/edwardwu0223)
- 同場加映
[Android 第三方 Recovery 繁體中文編譯教學](https://hackmd.io/@EdwardWu/CompileARecovery)
<p align="center">
<a href="https://github.com/bluehomewu"> <img src="https://img.shields.io/badge/-Github-000?style=flat&logo=Github&logoColor=white" /></a>
<a href="mailto:bluehome.wu@gmail.com"> <img src="https://img.shields.io/badge/-Gmail-c14438?style=flat&logo=Gmail&logoColor=white" /></p></a>


###### tags: `Android` `ROM` `編譯` `第三方` `教學`
