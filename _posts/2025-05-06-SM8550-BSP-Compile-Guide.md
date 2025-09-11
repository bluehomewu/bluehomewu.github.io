---
title: SM8550 BSP Compile Guide
date: 2025-05-06
tags: [BSP, SM8550, Compile Guide]
categories: [BSP]

---

# SM8550 BSP Compile Guide

# Build HLOS for SM8550
BSP Information:
---
SPF: snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1.r1_00005.0

Repo Sync:
---
https://github.com/QRD-Development/SM8550_BSP_Sync/tree/LA.VENDOR.13.2.0.r1-25900-KAILUA.QSSI15.0-1


BSP 編譯步驟：
---
1. 使用 `bash setup.sh` 下載 manifest
2. 使用 `bash sync.sh` 下載 SM8550 BSP 必要的 OpenSource code 部分
3. 複製用 zip 下載的 SM8550 BSP 到 `vendor/qcom/proprietary` 目錄下
3-1. 解壓縮 BSP zip 檔案
```shell=1
~/WorkSpace/7zip/7zz x snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1.r1_00005.0-86b1473a21e3c1f6eb84892ea60f952cb3f1cbfa.zip
```
3-2. 複製 QSSI BSP 到 `vendor/qcom/proprietary` 目錄下
```shell=1
cd qssi/
mkdir -p vendor/qcom/proprietary
cd vendor/qcom/proprietary
git init

/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/LA.QSSI.15.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
```
3-3. 複製 Vendor BSP 到 `vendor/qcom/proprietary` 目錄下
```shell=1
cd vendor
mkdir -p vendor/qcom/proprietary
cd vendor/qcom/proprietary
git init

/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/LA.QSSI.13.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/AUDIO.LA.8.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/DISPLAY.LA.3.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/VIDEO.LA.3.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/XR.LA.1.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/CV.LA.1.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/SENSORS.LA.3.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/GRAPHICS.LA.1.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/CAMERA.LA.3.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/LA.VENDOR.13.2.0/LINUX/android/vendor/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
```
3-4. 複製 kernel BSP 到 `vendor/qcom/proprietary` 目錄下
```shell=1
cd vendor/kernel_platform/
mkdir -p qcom/proprietary
cd qcom/proprietary
/bin/cp -rf /mnt/SX8200Pro/SM8550_BSP/snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/KERNEL.PLATFORM.2.0/kernel_platform/qcom/proprietary/* ./
git add . && git commit -s -m "$(head -n 1 prebuilt_HY11/AU_INFO.txt)"
```
3-5. （可選）複製 Linux Embedded (LE) BSP
- 先準備 LE 的編譯環境 user variant
```shell=1
cd kernel_platform &&
BUILD_CONFIG=msm-kernel/build.config.msm.kalama.tuivm VARIANT=defconfig ./build/build.sh
mkdir -p <LE workpace path>/src/kernel-5.15/
cp -rp <kernel SI workspace path>/kernel_platform <LE workpace path>/src/kernel-5.15/
cp -rp <kernel SI workspace path>/kernel_platform/out/ <LE workpace path>/src/kernel-5.15/
```
- 如果最後有需要編譯 non-HLOS，則需要編譯 LE BSP 的 userdebug variant
```shell=1
cd kernel_platform &&
BUILD_CONFIG=msm-kernel/build.config.msm.kalama.tuivm VARIANT=debug_defconfig ./build/build.sh
mkdir -p <LE workpace path>/src/kernel-5.15/
cp -rp <kernel SI workspace path>/kernel_platform <LE workpace path>/src/kernel-5.15/
cp -rp <kernel SI workspace path>/kernel_platform/out/ <LE workpace path>/src/kernel-5.15/
```

當複製完成後，目錄結構如下：
```shell=1
<LE workpace path>src/kernel-5.15/
|-- kernel_platform
|-- out
```

- 複製 LE BSP 到 `vendor/qcom/proprietary` 目錄下
```shell=1
mkdir DisplaySI
cd DisplaySI
repo init --depth=1 -q -u https://git.codelinaro.org/clo/la/techpack/display/manifest.git -b release -m AU_TECHPACK_DISPLAY.LA.3.0.R1.00.00.00.000.127.xml
repo sync -q -c --force-sync --optimized-fetch --no-tags --retry-fetches=5 -j"$(nproc --all)"
/bin/cp -rf ../snapdragon-premium-high-2022-spf-2-0-1_amss_standard_oem-r2.0.1/DISPLAY.LA.3.0/LINUX/android/vendor/qcom/proprietary ./vendor/qcom/
cp -rp <Display SI>/* <LE workpace path>/src/display/
```
當複製完成後，目錄結構如下：
```shell=1
<LE workpace path>src/display/
|-- hardware/qcom/display/
|-- <other folders>
```

4. 使用 `bash build.sh` 編譸 SM8550 BSP

5-1. （可選）編譯 LE BSP user variant
```shell=1
cd le/
1. export SHELL=/bin/bash
2. source setup-environment (select trustedvm and qti-distro-base-user)
            OR
3. export MACHINE=trustedvm
4. export DISTRO=qti-distro-base-user
5. source poky/qti-conf/set_bb_env.sh

bitbake qti-vm-image
```
`vm-bootsys.img` and `vm-persist.img` will be generated in the `<LE_workspace_path>/<DISTRO>/tmp-glibc/deploy/images/trustedvm/` folder.

5-2. 如果最後有需要編譯 non-HLOS，則需要編譯 LE BSP 的 userdebug variant
```shell=1
cd le/
1. export SHELL=/bin/bash
2. source setup-environment (select trustedvm and qti-distro-base-debug)
            OR
3. export MACHINE=trustedvm
4. export DISTRO=qti-distro-base-debug
5. source poky/qti-conf/set_bb_env.sh

bitbake qti-vm-image
```

編譯此份 BSP 會遇到的問題：
---
1. 編譯 QSSI 15 的時候，會遇到 `# ERROR: Modification detected of stable AIDL API file`。
```shell=1
[ 72% 145379/199357] Verify vendor/qcom/proprietary/commonsys-intf/data/dmapconsent/aidl/aidl_api/vendor.qti.data.dmapconsent/1 files have not been modified
FAILED: out/soong/.intermediates/vendor/qcom/proprietary/commonsys-intf/data/dmapconsent/aidl/vendor.qti.data.dmapconsent-api/checkhash_1.timestamp
if [ $(cd 'vendor/qcom/proprietary/commonsys-intf/data/dmapconsent/aidl/aidl_api/vendor.qti.data.dmapconsent/1' && { find ./ -name "*.aidl" -print0 | LC_ALL=C sort -z | xargs -0 sha1sum && echo latest-version; } | sha1sum | cut -d " " -f 1) = $(tail -1 'vendor/qcom/proprietary/commonsys-intf/data/dmapconsent/aidl/aidl_api/vendor.qti.data.dmapconsent/1/.hash') ]; then touch out/soong/.intermediates/vendor/qcom/proprietary/commonsys-intf/data/dmapconsent/aidl/vendor.qti.data.dmapconsent-api/checkhash_1.timestamp; else cat 'system/tools/aidl/build/message_check_integrity.txt' && exit 1; fi
###############################################################################
# ERROR: Modification detected of stable AIDL API file                        #
###############################################################################
Above AIDL file(s) has changed, resulting in a different hash. Hash values may
be checked at runtime to verify interface stability. If a device is shipped
with this change by ignoring this message, it has a high risk of breaking later
when a module using the interface is updated, e.g., Mainline modules.
16:20:43 ninja failed with: exit status 1

#### failed to build some targets (01:55:43 (hh:mm:ss)) ####
```
- 解決方法：
```shell=1
cd 'vendor/qcom/proprietary/commonsys-intf/data/dmapconsent/aidl/aidl_api/vendor.qti.data.dmapconsent/1' && { find ./ -name "*.aidl" -print0 | LC_ALL=C sort -z | xargs -0 sha1sum && echo latest-version; } | sha1sum | cut -d " " -f 1 > vendor/qcom/proprietary/commonsys-intf/data/dmapconsent/aidl/aidl_api/vendor.qti.data.dmapconsent/1/.hash
```
重新執行 `./build.sh dist --qssi_only -j "$(nproc --all)"` 即可。

2. 按照步驟去編譯 GKI kernel 的時候，會遇到
```shell=1
 Running extra dist command(s):
+ eval install_dtbs '&&' prepare_vendor_dlkm '&&' prepare_system_dlkm '&&' make_dtbo_img '&&' generate_extra_cmdline '&&' copy_dist_bins
++ install_dtbs
++ local INSTALL_DTBS_PATH=/mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/dtb_staging
++ local dtb_types=kalama-
++ '[' 1 -eq 1 ']'
++ dtb_types=kalama-overlays-
++ rm -rf /mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/dtb_staging
++ cd ./msm-kernel
++ make 'LLVM=1 DEPMOD=depmod DTC=/mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/build/kernel/build-tools/path/linux-x86/dtc' O=/mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/msm-kernel KBUILD_MIXED_TREE=/mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/gki_kernel/dist INSTALL_DTBS_PATH=/mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/dtb_staging DTB_TYPES=kalama-overlays- dtbs_install
make[1]: Entering directory '/mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/msm-kernel'
make[1]: Leaving directory '/mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/msm-kernel'
+++ find /mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/dtb_staging -type f '(' -name '*.dtb' -o -name '*.dtbo' ')'
find: '/mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/dtb_staging': No such file or directory
++ cp /mnt/SX8200Pro/SM8550_BSP/vendor/kernel_platform/out/msm-kernel-kalama-gki/dist
cp: Needs 2 arguments
```

- 解決方法：
```shell=1
cd vendor/
bash kernel_platform/qcom/proprietary/prebuilt_HY11/vendorsetup.sh
```
重新執行 `./kernel_platform/build/android/prepare_vendor.sh kalama gki` 即可。

## Build non-HLOS for SM8550
- 準備 snapdragon-premium-high-2022-spf-2-0-1_test_device-r2.0.1.r1_00005.0

1. 解壓縮 test_device
```shell=1
~/WorkSpace/7zip/7zz x snapdragon-premium-high-2022-spf-2-0-1_test_device-r2.0.1.r1_00005.0-118f0d26750297089278ef2ee013eb9f8b42f332.zip
```
2. 複製 vendor BSP 的 out/ 到 test_device
```shell=1
cd vendor/
/bin/cp -rf out/ snapdragon-premium-high-2022-spf-2-0-1_test_device/LA.VENDOR.13.2.0/LINUX/android/
```
3. 複製 LE 的產物
- 參考 Kailua.LA.2.0.1/contents.xml

4. 編譯 non-HLOS
```shell=1
cd Kailua.LA.2.0.1/common/build
python2 build.py
```
