---
title: 快速上手 Android Custom ROM 適配 - Prebuilt Vendor (zhTW)
date: 2022-11-21
categories: [Android]
tags: [Android, ' 刷機', ' 適配']

---

---
layout: post
title:  "快速上手 Android Custom ROM 適配 - Prebuilt Vendor (zhTW)"
date:   2022-11-20 13:42:27
categories: Android 刷機 適配
author: Lynnrin, EdwardWu
excerpt: 本人非專業 Android 開發者，本文僅參考，如有錯誤，歡迎指正！
tags: Android, 刷機, 適配
---

* 註1：本篇原作者為 Lynnrin，本人（EdwardWu）僅協助繁體中文化以及少數文字佈局上的調整
* 註2：本繁化版本已取得原作者同意後發布
* 註3：簡體中文版本原文 [Lynnrin's Blog - 快速上手 Android Custom ROM 适配 - Prebuilt Vendor](https://blog.lynnrin.moe/posts/ROM-bringup-guide-prebuilt/)

# 快速上手 Android Custom ROM 適配 - Prebuilt Vendor

> ⚠️ 注意：本人非專業 Android 開發者，本文僅參考，如有錯誤，歡迎指正！
> 
> ⚠️ 注意：本人非專業 Android 開發者，本文僅參考，如有錯誤，歡迎指正！
> 
> ⚠️ 注意：本人非專業 Android 開發者，本文僅參考，如有錯誤，歡迎指正！

本文章以適配小米 10S 為例, 小米 10S 為 VAB 設備, 不相容 GKI, VNDK 版本 30。

編譯伺服器系統: Ubuntu 22.04

## 什麼是 Prebuilt Vendor, 為什麼要用 Prebuilt Vendor

Prebuilt Vendor, 顧名思義, 預編譯 Vendor。指的是使用廠商已經編譯好的 Vendor 進行 Custom 適配。這樣可以大大降低適配難度, 減少適配 debug 時間。

Google 在 Android 8.0 引入了 PT(Project Treble), 這使得 Android Custom ROM 的適配和 debug 難度大大降低。再加上今年 Google 再次引入 GRF(Google Requirements Freeze) aka Vendor Freeze, 這使得適配難度再次降低。

在 Android 8.0 之前, 要適配 Custom ROM, 需要通過 AOSP, CAF 或其它晶片組, 硬體廠商開源的原始碼編譯設備硬體所需要的函式庫, HAL 或驅動, 且每次 Android 大版本升級都需要重新編譯, 且極有可能在新版本 Andorid 運行或編譯中出現問題, 需要等待原始碼更新修復或自己手動修復。

在引入 PT, GRF 後, 我們可以直接使用Stock ROM 中的 Vendor, 只需要編譯 Kernel 和 System 即可, 且因為 GRF 的引入, Vendor 至少可以相容 3 個大版本的 Android 更新。(例如小米 12 預裝 Android 12, VNDK 版本 32, 則此版本的 Vendor image 至少可以相容到 Android 15, VNDK 35)

## 需要準備的東西
1. 可以編譯 Android 的 PC 或伺服器
2. MIUI 官方刷機包
3. 小米 10S

## 準備開始

### 安裝所需依賴套件

```shell
# 安裝編譯依賴
sudo apt install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev libelf-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev git

# 配置 repo
sudo curl https://storage.googleapis.com/git-repo-downloads/repo > /usr/bin/repo
sudo chmod a+x /usr/bin/repo
```

### 同步 LineageOS 原始碼

在設備適配初期, 我推薦使用 LineageOS 進行設備的 bring up

```shell
# 新建資料夾用於存放原始碼
mkdir lineage

# 初始化 repo
repo init -u https://github.com/LineageOS/android.git -b lineage-19.1 # 同步完整倉庫, 包含提交歷史, 占用空間大
repo init -u https://github.com/LineageOS/android.git -b lineage-19.1 --depth=1 # 僅拉取最新提交, 不包含提交歷史, 占用空間小

# 開始同步
repo sync
```

## 開始適配

### 解包 MIUI

我們需要原廠系統中的部分文件來保證部分功能的正常使用, 例如 IMS, 所以我們需要先解包原廠系統

```shell
# 下載解包工具
git clone https://github.com/ShivamKumarJha/android_tools --depth=1
cd android_tools

# 初始化工具所需環境
chmod +x setup.sh
sudo bash setup.sh

# 開始解包
./tools/rom_extract.sh MIUI_PACKAGE.zip
```

### 提取所需文件

#### 提取 vendor 以及 odm

因為是 prebuilt vendor, 所以我們需要從原廠系統中提取出 vendor, odm image

```shell
unzip MIUI_PACKAGE.zip
./../android_tools/tools/Firmware_extractor/tools/update_payload_extractor/extract.py payload.bin --output_dir images/
```

然後將 images 目錄下的 vendor.img 和 odm.img 複製到 `device/xiaomi/thyme-prebuilt/` 下

#### 提取 kernel

因為是適配初期我們使用 prebuilt kernel 簡化適配流程

```shell
# 下載 magiskboot 用於解包 boot.img 以及 vendor_boot.img
wget https://github.com/TeamWin/external_magisk-prebuilt/raw/android-12.1/prebuilt/magiskboot_x86
chmod a+x magiskboot_x86

# 解包 boot.img 以及 vendor_boot.img
./magiskboot_x86 unpack boot.img
./magiskboot_x86 unpack vendor_boot.img
```

然後將解出來的 `kernel`, `dtb` 和 `dtbo.img` 複製到 `device/xiaomi/thyme-prebuilt/` 下

### 開始 Bring up device tree
#### 初始化 device tree 並編譯 recovery

我們需要先初始化 device tree, 然後編譯 recovery, 來驗證 kernel 的可用性

##### Android.mk

這是 Android make 編譯系統中的編譯配置文件, Android 編譯系統會 include 原始碼目錄下的所有 Android.mk 文件, 包括設備資料夾中的 Android.mk
我們需要在這個文件 include 當前資料夾下的所有 makefile 文件, 否則 Android 編譯系統不會去 include 設備資料夾中的其它 makefile 文件。

```makefile
LOCAL_PATH := $(call my-dir) # 設定一個 LOCAL_PATH 變數, 並將當前資料夾的路徑賦值給它
ifeq ($(TARGET_DEVICE),thyme) # 如果 TARGET_DEVICE 變數等於 thyme
subdir_makefiles=$(call first-makefiles-under,$(LOCAL_PATH)) # 設定一個 subdir_makefiles 變數, 並將當前資料夾下的所有 makefile 文件賦值給它
$(foreach mk,$(subdir_makefiles),$(info including $(mk) ...)$(eval include $(mk))) # 遍歷 subdir_makefiles 變數中的所有 makefile 文件, 並 include 進來
endif # 結束 if 語句
```

##### Android.bp

這是 Android 引入 soong 編譯系統後的編譯配置文件, Android 編譯系統會 include 原始碼目錄下的所有 Android.bp 文件, 包括設備資料夾中的 Android.bp
目前我們不需要編譯外部的 soong 模組, 因此直接創建一個空的 Android.bp 文件即可

```
soong_namespace { // soong 編譯系統的命名空間
    imports: [], // 導入的 soong 模組路徑
}
```

##### AndroidProducts.mk

這是用於定義設備編譯配置的地方, 我們可以在這裡定義多個設備配置用於編譯多個設備或同設備的變種版本

```makefile
PRODUCT_MAKEFILES := \
    $(LOCAL_DIR)/lineage_thyme.mk # 要使用的設備編譯配置文件

COMMON_LUNCH_CHOICES := \ # 定義可用的 lunch 選項
    lineage_thyme-eng \ # eng 版本
    lineage_thyme-userdebug \ # userdebug 版本
    lineage_thyme-user # user 版本
```

##### lineage_thyme.mk

這是我們的設備編譯配置文件, 我們需要在這裡定義設備的基本訊息, 以及設備的編譯配置。

```makefile
# Inherit common products
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk) # 繼承 core_64_bit.mk 編譯配置
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk) # 繼承 full_base_telephony.mk 編譯配置

# Inherit device configurations
$(call inherit-product, device/xiaomi/thyme/device.mk) # 繼承 device/xiaomi/thyme/device.mk 編譯配置

# Inherit common ArrowOS configurations
$(call inherit-product, vendor/arrow/config/common.mk) # 繼承 vendor/arrow/config/common.mk 編譯配置

PRODUCT_CHARACTERISTICS := nosdcard # 產品特性, 這裡表示不支援 sd 卡

PRODUCT_BRAND := Xiaomi # 產品品牌
PRODUCT_DEVICE := thyme # 產品設備名
PRODUCT_MANUFACTURER := Xiaomi # 產品製造商
PRODUCT_MODEL := M2102J2SC # 產品型號
PRODUCT_NAME := lineage_thyme # 產品名

PRODUCT_GMS_CLIENTID_BASE := android-xiaomi # 產品 GMS 用戶端 ID
```

##### BoardConfig.mk

這是設備的板級配置文件, 我們需要在這裡定義設備的硬體配置。

```makefile
DEVICE_PATH := device/xiaomi/thyme # 定義一個 DEVICE_PATH 變數, 指向設備資料夾

# A/B
AB_OTA_UPDATER := true # 開啟 A/B OTA 更新

AB_OTA_PARTITIONS += \ # A/B OTA 更新的分區
    boot \
    dtbo \
    product \
    system \
    system_ext \
    vbmeta \
    vbmeta_system

# Architecture
TARGET_ARCH := arm64 # 指定目標架構為 arm64
TARGET_ARCH_VARIANT := armv8-a # 指定目標架構變體為 armv8-a
TARGET_CPU_ABI := arm64-v8a # 指定目標 CPU ABI 為 arm64-v8a
TARGET_CPU_ABI2 := # 指定目標 CPU ABI 2 為空
TARGET_CPU_VARIANT := generic # 指定目標 CPU 變體為 generic
TARGET_CPU_VARIANT_RUNTIME := kryo385 # 指定目標 CPU 變體運行時為 kryo385

TARGET_2ND_ARCH := arm # 指定第二目標架構為 arm
TARGET_2ND_ARCH_VARIANT := armv8-a # 指定第二目標架構變體為 armv8-a
TARGET_2ND_CPU_ABI := armeabi-v7a # 指定第二目標 CPU ABI 為 armeabi-v7a
TARGET_2ND_CPU_ABI2 := armeabi # 指定第二目標 CPU ABI 2 為 armeabi
TARGET_2ND_CPU_VARIANT := generic # 指定第二目標 CPU 變體為 generic
TARGET_2ND_CPU_VARIANT_RUNTIME := kryo385 # 指定第二目標 CPU 變體運行時為 kryo385

# Bootloader
TARGET_BOOTLOADER_BOARD_NAME := kona # 指定目標 bootloader 名為 kona, 該值可以從 MIUI 的 vendor/build.prop 中獲取

# Kernel
BOARD_BOOT_HEADER_VERSION := 3 # 指定內核頭版本為 3, 內核頭版本從 3 開始支援 vendor_boot 分區
BOARD_KERNEL_BASE := 0x00000000 # 指定內核基地址為 0x00000000
BOARD_KERNEL_BINARIES := kernel # 指定內核二進位制檔案名為 kernel
BOARD_KERNEL_CMDLINE := console=ttyMSM0,115200n8 androidboot.hardware=qcom  # 指定內核命令行
BOARD_KERNEL_CMDLINE += androidboot.console=ttyMSM0 androidboot.memcg=1
BOARD_KERNEL_CMDLINE += lpm_levels.sleep_disabled=1
BOARD_KERNEL_CMDLINE += msm_rtb.filter=0x237 service_locator.enable=1
BOARD_KERNEL_CMDLINE += androidboot.usbcontroller=a600000.dwc3 swiotlb=0
BOARD_KERNEL_CMDLINE += loop.max_part=7 cgroup.memory=nokmem,nosocket
BOARD_KERNEL_CMDLINE += pcie_ports=compat loop.max_part=7
BOARD_KERNEL_CMDLINE += iptable_raw.raw_before_defrag=1
BOARD_KERNEL_CMDLINE += ip6table_raw.raw_before_defrag=1
BOARD_KERNEL_CMDLINE += androidboot.selinux=permissive
BOARD_KERNEL_IMAGE_NAME := Image # 指定內核鏡像名為 Image
BOARD_KERNEL_PAGESIZE := 4096 # 指定內核頁大小為 4096
BOARD_KERNEL_SEPARATED_DTBO := true # 指定內核分離 DTBO
BOARD_MKBOOTIMG_ARGS := --header_version $(BOARD_BOOT_HEADER_VERSION) # 指定 mkbootimg 參數, 這裡指定了內核頭版本
KERNEL_LD := LD=ld.lld # 指定內核連結器為 ld.lld
TARGET_KERNEL_ADDITIONAL_FLAGS := DTC_EXT=$(shell pwd)/prebuilts/misc/linux-x86/dtc/dtc # 指定使用外部 DTC
TARGET_KERNEL_APPEND_DTB := false # 指定不追加 DTB
BOARD_INCLUDE_DTB_IN_BOOTIMG := true # 指定在 boot.img 中包含 DTB
TARGET_KERNEL_ARCH := arm64 # 指定內核架構為 arm64
TARGET_KERNEL_HEADER_ARCH := arm64 # 指定內核頭架構為 arm64

ifeq ($(TARGET_PREBUILT_KERNEL),) # 如果沒有使用預編譯內核
  TARGET_KERNEL_CONFIG := thyme_defconfig # 指定內核配置文件為 thyme_defconfig
  TARGET_KERNEL_CLANG_COMPILE := true # 指定使用 Clang 編譯內核
  TARGET_KERNEL_SOURCE := kernel/xiaomi/thyme # 指定內核原始碼路徑為 kernel/xiaomi/thyme
endif

# Metadata
BOARD_USES_METADATA_PARTITION := true # 使用 metadata 元數據加密

# Partitions
BOARD_BOOTIMAGE_PARTITION_SIZE := 201326592 # 指定 boot 分區大小為 201326592
BOARD_DTBOIMG_PARTITION_SIZE := 33554432 # 指定 dtbo 分區大小為 33554432
BOARD_FLASH_BLOCK_SIZE := 262144 # 指定刷入塊大小為 262144
BOARD_USERDATAIMAGE_PARTITION_SIZE := 114135379968 # 指定 userdata 分區大小為 114135379968
BOARD_VENDOR_BOOTIMAGE_PARTITION_SIZE := 100663296 # 指定 vendor_boot 分區大小為 100663296

BOARD_THYME_DYNAMIC_PARTITIONS_PARTITION_LIST := product system system_ext # 指定動態分區列表
BOARD_SUPER_PARTITION_SIZE := 9126805504 # 指定 super 分區大小為 9126805504
BOARD_SUPER_PARTITION_GROUPS := thyme_dynamic_partitions # 指定 super 分區組為 thyme_dynamic_partitions
BOARD_THYME_DYNAMIC_PARTITIONS_SIZE := 4559208448 # 指定動態分區組 thyme_dynamic_partitions 大小為 4559208448

BOARD_PARTITION_LIST := $(call to-upper, $(BOARD_THYME_DYNAMIC_PARTITIONS_PARTITION_LIST)) # 遍歷 BOARD_THYME_DYNAMIC_PARTITIONS_PARTITION_LIST 並賦值給 BOARD_PARTITION_LIST
$(foreach p, $(BOARD_PARTITION_LIST), $(eval BOARD_$(p)IMAGE_FILE_SYSTEM_TYPE := ext4)) # 遍歷 BOARD_PARTITION_LIST 並賦值給 p, 然後設定 BOARD_$(p)IMAGE_FILE_SYSTEM_TYPE := ext4
$(foreach p, $(BOARD_PARTITION_LIST), $(eval TARGET_COPY_OUT_$(p) := $(call to-lower, $(p)))) # 遍歷 BOARD_PARTITION_LIST 並賦值給 p, 然後設定 TARGET_COPY_OUT_$(p) := $(call to-lower, $(p))

BOARD_USERDATAIMAGE_FILE_SYSTEM_TYPE := f2fs # 指定 userdata 分區檔案系統類型為 f2fs

# Platform
BOARD_USES_QCOM_HARDWARE := true # 指定使用 Qualcomm 硬體
TARGET_BOARD_PLATFORM := kona # 指定平台為 kona

# Recovery
BOARD_INCLUDE_RECOVERY_DTBO := true # 指定包含 recovery DTBO
BOARD_USES_RECOVERY_AS_BOOT := true # 指定 recovery 在 boot 分區中
TARGET_NO_RECOVERY := true # 指定設備沒有 recovery 分區
TARGET_RECOVERY_FSTAB := $(DEVICE_PATH)/recovery/recovery.fstab # 指定 recovery fstab 文件
TARGET_RECOVERY_PIXEL_FORMAT := RGBX_8888 # 指定 recovery 像素格式
TARGET_USERIMAGES_USE_F2FS := true # 指定 userdata 使用 f2fs

# Verified Boot
BOARD_AVB_ENABLE := true # 指定啟用 AVB
BOARD_AVB_MAKE_VBMETA_IMAGE_ARGS += --flags 3 # 指定 AVB flags 為 3
BOARD_AVB_MAKE_VBMETA_IMAGE_ARGS += --set_hashtree_disabled_flag # 指定 AVB 為停用
BOARD_AVB_VBMETA_SYSTEM := system system_ext# 指定使用 AVB 的分區
BOARD_AVB_VBMETA_SYSTEM_ALGORITHM := SHA256_RSA2048 # 指定 AVB 加密算法為 SHA256_RSA2048
BOARD_AVB_VBMETA_SYSTEM_KEY_PATH := external/avb/test/data/testkey_rsa2048.pem # 指定 AVB 金鑰
BOARD_AVB_VBMETA_SYSTEM_ROLLBACK_INDEX := $(PLATFORM_SECURITY_PATCH_TIMESTAMP) # 指定 AVB 回滾索引
BOARD_AVB_VBMETA_SYSTEM_ROLLBACK_INDEX_LOCATION := 1 # 指定 AVB 回滾索引位置

# VNDK
BOARD_VNDK_VERSION := current # 指定 VNDK 版本為 current
```

##### device.mk

這是設備的編譯配置文件, 在這裡面可以 include 其它編譯配置文件, 也可以指定要編譯的模組, 功能類同 lineage_thyme.mk。

```makefile
# Enable updating of APEXes
$(call inherit-product, $(SRC_TARGET_DIR)/product/updatable_apex.mk) # 啟用 apex 更新

# Virtual A/B
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota.mk) # 啟用虛擬 A/B

# Enable Dalvik
$(call inherit-product, frameworks/native/build/phone-xhdpi-6144-dalvik-heap.mk) # 導入 6G dalvik 配置

# API
PRODUCT_SHIPPING_API_LEVEL := 30 # 指定預裝 Android API 級別為 30, 例如 thyme 預裝 Android 11, 故此處為 30

# A/B
AB_OTA_POSTINSTALL_CONFIG += \
    RUN_POSTINSTALL_system=true \
    POSTINSTALL_PATH_system=system/bin/otapreopt_script \
    FILESYSTEM_TYPE_system=ext4 \
    POSTINSTALL_OPTIONAL_system=true

# Boot animation
TARGET_SCREEN_HEIGHT := 2400 # 指定螢幕高度為 2400
TARGET_SCREEN_WIDTH := 1080 # 指定螢幕寬度為 1080

# Common init scripts
PRODUCT_PACKAGES += \
    init.recovery.qcom.rc # 編譯額外的自訂 rc 腳本

# fastbootd
PRODUCT_PACKAGES += \
    android.hardware.fastboot@1.0-impl-mock \ # 編譯 fastbootd
    fastbootd

# F2FS utilities
PRODUCT_PACKAGES += \
    sg_write_buffer \ # 編譯 f2fs 工具
    f2fs_io \
    check_f2fs

# Partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true # 指定使用動態分區
PRODUCT_BUILD_SUPER_PARTITION := false # 指定不編譯 super 分區

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH) # 指定 soong 命名空間

# Update engine
PRODUCT_PACKAGES += \
    otapreopt_script \ # 編譯 otapreopt 腳本
    update_engine \ # 編譯 update_engine
    update_engine_sideload \ # 編譯 update_engine_sideload
    update_verifier \ # 編譯 update_verifier

PRODUCT_PACKAGES_DEBUG += \
    update_engine_client \ # 編譯 update_engine_client

PRODUCT_HOST_PACKAGES += \
    brillo_update_payload \ # 編譯 brillo_update_payload

# Vendor boot
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/rootdir/etc/fstab.qcom:$(TARGET_COPY_OUT_VENDOR_RAMDISK)/first_stage_ramdisk/fstab.qcom # 複製 fstab 到 vendor ramdisk

# VNDK
PRODUCT_TARGET_VNDK_VERSION := 30 # 指定 VNDK 版本為 30, 該值可以在 vendor/build.prop 中找到
```

##### 導入 recovery 所需基本文件

這是 fstab 文件, 用於指定分區的掛載點, 以及掛載點的屬性, 例如是否可讀寫等。
必須要有這個文件, 否則 Linux Kernel 會無法掛載所需的分區, 導致 Android 或 Recovery 無法啟動

這個文件可以在 vendor 分區中被找到, 具體可以使用此命令尋找

```shell
cd dump/vendor
find | grep fstab.qcom
```

找到後 copy 到設備資料夾中的 rootdir/etc/ 目錄下

然後我們可以在 device.mk 中使用 PRODUCT_COPY_FILES 複製到 ramdisk 或者 vendor ramdisk 中, [例](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme-oss/blob/arrow-13.0/rootdir/Android.mk#L12)
也可以在 rootdir 目錄中新建 Android.mk 去定義自訂模組然後在 device.mk 中指定編譯, [例](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/commit/cce87ffbd1416eaa8cda26a71aeaebc19890c505#diff-247ee86229a709a6e2eedfc1d3c4a557825aee073e20b0112ab76f4ca8e4bc4eR71-R72)

##### 開始編譯 recovery

完成上述步驟後我們便可以開始編譯 recovery 來測試了

```shell
. build/envsetup.sh # 初始化編譯環境
lunch lineage_thyme-userdebug # 初始化設備編譯環境
m bootimage # 編譯 boot image, 由於是 A/B 設備, 故此處編譯 boot image 而不是 recovery image
```

編譯完成後刷入設備

```shell
fastboot flash boot out/target/product/thyme/boot.img # 刷入 boot image
fastboot reboot recovery # 重啟到 recovery
```

如果設備可以正常進入編譯後到 recovery 我們便可以進入下一步，否則請參考文章末的 debug 指南進行 debug。

#### 完善 device tree 準備開始編譯 Android

由於這部分內容較多，具體請參考本人 GitHub 倉庫中的[提交歷史](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/commits/twelve)
此文章僅挑出其中一些重要的部分進行說明

##### `proprietary-files.txt`, `extract-files.sh` 和 `setup-makefiles.sh`

這三個文件複製 vendor tree 中的文件建立，改動和提取
如果要建立或修改 vendor tree 中的文件，請務必使用 extract-files.sh 腳本提取建立或修改。
詳情請參考 LineageOS 官方文件: 
1. [https://wiki.lineageos.org/extracting_blobs_from_zips](https://wiki.lineageos.org/extracting_blobs_from_zips)
2. [https://wiki.lineageos.org/proprietary_blobs](https://wiki.lineageos.org/proprietary_blobs)

###### `proprietary-files.txt`

該文件屬於一個清單，用於列出需要從原廠系統中提取的文件，以及它們的目標位置。
`extract-files.sh` 會遍歷這裡面的文件，然後從原廠系統中提取出來，放到 vendor tree 中。

###### `extract-files.sh`

該腳本會根據 `proprietary-files.txt` 中的文件，從原廠系統中提取出來，放到 vendor tree 中，然後調用 `setup-makefiles.sh` 腳本建立 makefile。

###### `setup-makefiles.sh`

該腳本會被 `extract-files.sh` 調用，用於建立 makefile。

##### `FCM` 或 `manifest.xml` 或 `compatibility_matrix.device.xml`

這是 HAL 的清單文件，用於指定設備支援的 HAL，以及它們的版本。Android 會根據清單中的 HAL 來載入對應的 HAL。
詳情請參考 AOSP 官方文件:
[https://source.android.com/docs/core/architecture/vintf?hl=zh-cn](https://source.android.com/docs/core/architecture/vintf?hl=zh-cn)

##### `bootctrl` 以及 `gpt-utils` 或 `mtk_plpath_utils`

A/B 設備需要這些模組用於進行無損升級，詳情請參考 AOSP 官方文件:
[https://source.android.com/docs/core/ota/ab](https://source.android.com/docs/core/ota/ab)

> ⚠️ 注意: 高通設備與聯發科設備所使用的 bootctrl 不同

高通設備的 bootctrl 以及 gpt-utils 可以從 CAF 或 CLO 中拿取。
1. [CAF](https://source.codeaurora.org/quic/la/platform/vendor/qcom-opensource/recovery-ext/)
2. [CLO](https://git.codelinaro.org/clo/la/platform/vendor/qcom-opensource/recovery-ext)

> ⚠️ 注意: 高通已經在 2022 年 5 月 31 日停止對 CAF 的更新，並決定在 2023 年 5 月 31 日徹底停用，所以建議使用 CLO 中的 bootctrl 和 gpt-utils

聯發科設備的 bootctrl 以及 mtk_plpath_utils 請參考:
1. [bootctrl](https://github.com/Lynnrin-Studio/android_device_xiaomi_chopin/tree/lineage-18.1/bootctrl)
2. [mtk_plpath_utils](https://github.com/Lynnrin-Studio/android_device_xiaomi_chopin/tree/lineage-18.1/mtk_plpath_utils)

如果上面的兩個模組對您的聯發科設備不起作用，請考慮使用 prebuilt 的 bootctrl 和 mtk_plpath_utils。

##### VoLTE

我們需要編譯部分組建以及從原廠系統提取部分文件來支援 VoLTE。

高通設備參考: 
1. [https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/commit/e6d415fbc9c1ad947ceea4e2860a7a1101e8feec](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/commit/e6d415fbc9c1ad947ceea4e2860a7a1101e8feec)
2. [https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/blob/twelve/proprietary-files.txt#L78-L87](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/blob/twelve/proprietary-files.txt#L78-L87)

聯發科設備參考: 
1. [https://github.com/Lynnrin-Studio/android_device_xiaomi_chopin/blob/lineage-18.1/device.mk#L105-L121](https://github.com/Lynnrin-Studio/android_device_xiaomi_chopin/blob/lineage-18.1/device.mk#L105-L121)
2. [https://github.com/Lynnrin-Studio/android_device_xiaomi_chopin/blob/lineage-18.1/proprietary-files.txt#L5-L41](https://github.com/Lynnrin-Studio/android_device_xiaomi_chopin/blob/lineage-18.1/proprietary-files.txt#L5-L41)

同時請確保所編譯的 ROM 以及增加了 MTK IMS 的支援，具體可以參考: [https://gerrit.pixelexperience.org/q/topic:mtk-ims](https://gerrit.pixelexperience.org/q/topic:mtk-ims)

##### Overlay

Overlay 是個很重要的東西，可以動態的調節一些系統特性，比如說狀態欄的高度，圓角的大小等

部分 Overlay 配置可以從原廠系統中提取，具體路徑在
1. vendor/overlay
2. product/overlay

如果需要自己增加 overlay 可以參考這些連結來檢查哪些 overlay 是可用的，下面列出的是比較常用的: 
1. [framework/base](https://cs.android.com/android/platform/superproject/+/master:frameworks/base/core/res/res/values/)
2. [framework/base/packages/SystemUI](https://cs.android.com/android/platform/superproject/+/master:frameworks/base/packages/SystemUI/res/values/)
3. [packages/apps/Settings](https://cs.android.com/android/platform/superproject/+/master:packages/apps/Settings/res/values/)

如果需要找更多的 overlay 可以進入 [cs.android.com](https://cs.android.com) 尋找相應 app 模組的 res/values/ 目錄。

##### SELinux

SELinux 是一個安全機制，可以防止一些惡意的 app 讀取系統檔案，但是這個機制也會導致一些問題，比如錯誤的 Sepolicy rules 可能會導致部分硬體或軟體工作不正常。甚至無法啟動操作系統。
在適配初期我建議將 SELinux [設為寬容](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme-oss/commit/b3ea8a9355828776c63bd114bacd62d61206b7a3#diff-151aef4e286613b79b65e512509f8c5b43c20939baff4c9e65e38ab639e0e7a5L64)
等到硬體和軟體的適配工作基本完成後再將 SELinux 設定為 Enforcing。

關於 Sepolicy rules 的編寫可以參考這些連結:
1. [https://source.android.com/security/selinux/](https://source.android.com/security/selinux/)
2. [https://www.cnblogs.com/schips/p/android-selinux_about_avc.html](https://www.cnblogs.com/schips/p/android-selinux_about_avc.html)
3. [https://lineageos.org/engineering/HowTo-SELinux](https://lineageos.org/engineering/HowTo-SELinux)

#### 硬體功能的修復

一般 prebuilt vendor tree 編譯出來的 ROM 大部分硬體都可以正常工作，但是部分機型的硬體可能需要一些額外的修復才能正常工作，比如說指紋，呼吸燈等

##### 螢幕下指紋

> ⚠️ 注意: 本部分以小米 10S 為例，該機型採用光學螢幕下指紋，Global HBM。如果你的設備是 Local HBM 具體實現方式可能稍有不同

在小米 10S上由於使用的是螢幕下指紋，所以不能直接使用 vendor 內已經編譯好的 Fingerprint 2.1 HAL，在 Android 12 或以上系統需要手動編譯一個 Fingerprint 2.3 HAL 用來處理 UDFPS 事件，在 Android 12 以下系統需要使用 Lineage inscreen fingerprint HAL 來處理指紋事件。

UDFPS 是 Google 在 Android 12 中新增的一種螢幕下指紋的實現方式，具體可以閱讀[相關原始碼](https://cs.android.com/android/platform/superproject/+/master:frameworks/base/packages/SystemUI/src/com/android/systemui/biometrics/)

###### Android 12 以下系統

具體實現方式可以參考這個[提交歷史](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/commits/lineage-18.1/fod)

> ⚠️ 注意: 由於小米 10S 使用 Global HBM，因此我們需要進行 kernel dimming 或 framework dimming，否則在使用指紋解鎖時全螢幕亮度將調至最高，因為小米 10S 使用 prebuilt kernel，因此只能使用 framework 進行 dimming 具體實現參考[這個提交](https://github.com/dataoutputstream/platform_frameworks_base/commit/86a2a0901b8af99019996286decbc6510f77e375)

##### Android 12 及以上系統

具體實現方式可以參考這個[提交歷史](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/commit/a681ba360b31fd7103f1323926c5561fcd13c5a4)

此外我們還需要在 overlay 中設定部分參數, 以使得螢幕下指紋識別功能正常工作, 具體參考這個[提交](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/commit/263342af84e43838bfe37f8b3ad24c6f14659125)

> ⚠️ 注意: 由於小米 10S 使用 Global HBM，因此我們需要進行 kernel dimming 或 framework dimming，否則在使用指紋解鎖時全螢幕亮度將調至最高，因為小米 10S 使用 prebuilt kernel，因此只能使用 framework 進行 dimming 具體實現參考[這個提交](https://review.arrowos.net/c/ArrowOS/android_frameworks_base/+/16767)
> ⚠️ 注意: 由於 Android 13 使用 Kotlin 重寫了 UDFPS 部分，因此上面的實現不相容 Android 13，建議使用 kernel dimming 來獲得更好的體驗，具體提交可以參考[這些](https://github.com/PixelExperience-Devices/kernel_xiaomi_thyme/commits/53248741c3a24008a440e55cb96869d7c26136e9)

##### 藍牙音訊

##### Android 12 及以下系統

通常原廠系統都採用 QCOM BT，因此我們需要一些更改來支援 vendor 中的 QCOM BT，具體可以參考這個[提交](https://github.com/Lynnrin-Studio/android_device_xiaomi_thyme/commit/ae9c7040b68d9904c55bf5ce810f5ce8a3212662)

##### Android 13

Google 在 Android 13 中模組化了多個組件，其中就包括藍牙，但是 vendor 中的 QCOM BT 並不相容這一更改，因此我們需要編譯修改過後的 `android.hardware.bluetooth.audio` 來停用掉 QCOM BT, 並切換到 AOSP BT

具體實現參考這些提交: 
1. [https://review.arrowos.net/q/topic:13-gsi](https://review.arrowos.net/q/topic:13-gsi)
2. [https://github.com/Lynnrin-Studio/android_device_xiaomi_nabu/commit/b26c98951d1e8c0397983ed4f96224bd9e836489](https://github.com/Lynnrin-Studio/android_device_xiaomi_nabu/commit/b26c98951d1e8c0397983ed4f96224bd9e836489)
3. [https://github.com/Lynnrin-Studio/android_device_xiaomi_nabu/commits/arrow-13.0/bluetooth/audio](https://github.com/Lynnrin-Studio/android_device_xiaomi_nabu/commits/arrow-13.0/bluetooth/audio)

#### 聲音

部分設備可能廠商魔改了 libvolumelistener，因此我們需要替換掉 libvolumelistener 中的，具體可以參考這個[提交](https://github.com/Lynnrin-Studio/android_device_xiaomi_nabu/commit/27e74adfbc30444380e471841957c56b74ffb79b)

### Debug 指南

#### 設備卡在 oem logo (卡一屏)

造成這個的原因有很多種，這裡拿幾種出來講

##### data 分區未正確格式化

1. 嘗試在 recovery 中格式化 data 分區
2. 嘗試使用 `fastboot -w` 格式化 data 分區
3. 嘗試使用原廠 recovery 格式化 data 分區
4. 在 fstab 中關閉 data 分區的加密

##### Sepolicy rules 的錯誤配置

1. 嘗試設定 SELinux 狀態為 permissive
2. 獲取 logcat 或 pstore 日誌，檢查是否有相關錯誤，並修復

##### 未正確配置 vendor image

1. 檢查 BoardConfig 中的 vendor image 配置是否正確

##### 未正確配置 ramdisk

1. 檢查 fstab 是否已經正確複製到 ramdisk 中

##### 未正確配置 kernel 或 prebuilt kernel 不可用

1. 檢查 kernel 是否已經正確配置
2. 切換到 OSS kernel

##### BPF 載入失敗

1. 嘗試使用以下提交來修復 BPF 載入問題
    * Prebuilt kernel
    1. [https://github.com/AcmeUI/android_frameworks_libs_net/commit/6fcad94ca26fbcf17ae33fca864ab80bf2b1d642](https://github.com/AcmeUI/android_frameworks_libs_net/commit/6fcad94ca26fbcf17ae33fca864ab80bf2b1d642)
    2. [https://github.com/AcmeUI/android_system_bpf/commit/50a4dece82954745e40b5d354cfd222642f6fdce](https://github.com/AcmeUI/android_system_bpf/commit/50a4dece82954745e40b5d354cfd222642f6fdce)
    3. [https://github.com/AcmeUI/android_frameworks_libs_net/commit/08de55ee6bb3774123ed8bd303855c542093ebb4](https://github.com/AcmeUI/android_frameworks_libs_net/commit/08de55ee6bb3774123ed8bd303855c542093ebb4)

    * OSS kernel
    1. [https://github.com/PixelExperience-Devices/kernel_xiaomi_thyme/commit/f1facc1aa372dd2c9eb1336d57e574ace2cbfec7](https://github.com/PixelExperience-Devices/kernel_xiaomi_thyme/commit/f1facc1aa372dd2c9eb1336d57e574ace2cbfec7)

##### 獲取 logcat 或 pstore 日誌

如果以上方法都沒有解決問題，可以嘗試獲取日誌來分析問題

###### 獲取 logcat 日誌

如果設備連線到電腦可以被 `adb devices` 識別到，便可以使用 `adb logcat` 獲取 logcat 日誌

可以通過檢查 logcat 中帶 `error`, `crash`, `fatal` 等關鍵字的日誌來定位問題

###### 獲取 pstore 日誌

如果設備連線到電腦不能被 `adb devices` 識別到，則需要獲取 pstore 日誌

> ⚠️ 注意: pstore 需要在 kernel 中開啟，如果沒有開啟則無法獲取 pstore 日誌

1. 將設備重啟到 recovery
2. 啟用 recovery 的 adb (如果沒有啟用)
3. 使用 `adb pull /sys/fs/pstore` 獲取 pstore 日誌

可以通過檢查 pstore 日誌中帶 `error`, `crash`, `fatal` 等關鍵字的日誌來定位問題

#### 設備卡在開機動畫 (卡二屏)

設備卡二屏代表系統已經啟動，kernel 部分已經正常工作，但是系統服務沒有正常啟動
我們可以通過 logcat 日誌來分析問題，具體參考上一節的獲取 logcat 日誌

#### logcat 日誌中出現 linker 錯誤

一般出現該錯誤代表有動態庫沒有正確載入或缺失，具體參考日誌中的報錯然後補全缺失的動態庫

#### logcat 日誌中出現 Permission denied 錯誤

一般出現該錯誤代表沒有正確配置 SELinux，具體參考日誌中的報錯然後修復 SELinux

#### logcat 日誌中出現 `fatal signal 11 (SIGSEGV), code 1 (SEGV_MAPERR)` 錯誤

一般出現該錯誤代表系統服務出現了崩潰，具體參考日誌中的報錯然後修復崩潰

About Lynnrin
---
[GitHub](https://github.com/LynnrinChan)
[YouTube](https://youtube.com/@Lynnrin)

About EdwardWu
---
[GitHub](https://github.com/bluehomewu)
[YouTube](https://youtube.com/@edwardwu23)
[Edward-Project](https://github.com/Edward-Projects)
