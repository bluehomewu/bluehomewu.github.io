---
title: SM84xx BSP Compile Guide
date: 2025-05-18
tags: [BSP, SM84xx, Compile Guide]
categories: [BSP]

---

# SM84xx BSP Compile Guide

# Build HLOS for SM84xx
BSP Information:
---
SPF: snapdragon-premium-high-2021-spf-2-0-2_amss_standard_oem-r2.0.2.r1_00007.0

Repo Sync:
---
https://github.com/QRD-Development/SM84xx_BSP_Sync/tree/LA.VENDOR.1.0.r1-27000-WAIPIO.QSSI15.0-1

BSP 編譯步驟：
---
1. 使用 `bash setup.sh` 下載 manifest
2. 使用 `bash sync.sh` 下載 SM84xx BSP 必要的 OpenSource code 部分
3. 複製用 zip 下載的 SM84xx BSP 到 `vendor/qcom/proprietary` 目錄下
3-1. 解壓縮 BSP zip 檔案
```shell=1
~/WorkSpace/7zip/7zz x snapdragon-premium-high-2021-spf-2-0-2_amss_standard_oem-r2.0.2.r1_00007.0.zip
```
3-2. 複製 QSSI BSP 到 `vendor/qcom/proprietary` 目錄下
```shell=1
cd qssi/
mkdir -p vendor/qcom/proprietary
cd vendor/qcom/proprietary
git init

/bin/cp -rf ~/BSP/SM84xx_BSP_Sync/snapdragon-premium-high-2021-spf-2-0-2_amss_standard_oem-r2.0.2.r1_0007.0/LA.QSSI.15.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
```
3-3. 複製 Vendor BSP 到 `vendor/qcom/proprietary` 目錄下
```shell=1
cd vendor
mkdir -p vendor/qcom/proprietary
cd vendor/qcom/proprietary
git init

/bin/cp -rf ~/BSP/SM84xx_BSP_Sync/snapdragon-premium-high-2021-spf-2-0-2_amss_standard_oem-r2.0.2.r1_0007.0/LA.QSSI.12.0.r1/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf ~/BSP/SM84xx_BSP_Sync/snapdragon-premium-high-2021-spf-2-0-2_amss_standard_oem-r2.0.2.r1_0007.0/DISPLAY.LA.2.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf ~/BSP/SM84xx_BSP_Sync/snapdragon-premium-high-2021-spf-2-0-2_amss_standard_oem-r2.0.2.r1_0007.0/VIDEO.LA.2.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf ~/BSP/SM84xx_BSP_Sync/snapdragon-premium-high-2021-spf-2-0-2_amss_standard_oem-r2.0.2.r1_0007.0/CAMERA.LA.2.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf ~/BSP/SM84xx_BSP_Sync/snapdragon-premium-high-2021-spf-2-0-2_amss_standard_oem-r2.0.2.r1_0007.0/LA.VENDOR.1.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
```
3-4. 複製 kernel BSP 到 `vendor/qcom/proprietary` 目錄下
```shell=1
cd vendor/kernel_platform/
mkdir -p qcom/proprietary
cd qcom/proprietary
git init

/bin/cp -rf ~/BSP/SM84xx_BSP_Sync/snapdragon-premium-high-2021-spf-2-0-2_amss_standard_oem-r2.0.2.r1_0007.0/KERNEL.PLATFORM.1.0/kernel_platform/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
```


