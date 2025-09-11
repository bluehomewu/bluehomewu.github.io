---
title: ROG Phone 2 & 3 騰訊陸版刷入國際版
date: 2021-02-14 20:00:00 +0800
categories: [Android]
tags: [Android]

---

# ROG Phone 2 & 3 騰訊陸版刷入國際版

改機思路說明:
---
- 解鎖 bootloader
- 先透過 RAW 檔線刷刷入國際版原廠ROM
- 刷入 Patch 過後的 Magisk boot.img
- 修改 Country Code
- 進行系統更新(手動更新) 升級至當前最新版本
- (可選)保留 **Magisk** 或是 **上鎖bootloader**
- (僅限 ROG Phone 3 上鎖後使用)
```
關閉OTA時顯示系統並非原廠系統：
在電腦adb 開啟CMD或是powershell->輸入指令
adb shell pm uninstall -k --user 0 com.asus.hardwarestub

可以禁用應用程式設定，但以後可能會再次出現警報。
```
- 交機

檔案下載
---
### ROG Phone 2
[ROG Phone 2 官方支援網站](https://rog.asus.com/tw/phones/rog-phone-ii-model/helpdesk_download/)
[官解工具](https://dlcdnets.asus.com/pub/ASUS/ZenFone/ZS660KL/ZS660KL_0807-1814_SIGNED_UnlockTool_9.2.0.0_200807_fulldpi.apk)
[1908.12 國際版 RAW 檔下載](https://drive.google.com/file/d/1d0gcTCvAwW9-VTQexdvhlO8dJyRnpwzk/view?usp=sharing)
![](https://i.imgur.com/6fVITg8.jpg)
[QFIL 9008 救磚包](https://drive.google.com/file/d/1Ds82t7RmHT5XaJ-iImcYKnWluVYy_QyC/view?usp=sharing)
### ROG Phone 3
[ROG Phone 3 官方支援網站](https://rog.asus.com/tw/phones/rog-phone-3-model/helpdesk_download/)
[官解工具](https://dlcdnets.asus.com/pub/ASUS/ZenFone/ZS661KS/obiwan-0902-1738_SIGNED_UnlockTool_9.3.0.0_200820_fulldpi.apk)
[2005.25 國際版 RAW 檔下載](https://drive.google.com/file/d/1t8yfWBpliNUBRHFS88saHgkSA-sHh-0n/view?usp=sharing)
![](https://i.imgur.com/cm1kntC.jpg)
[自製 QFIL 9008 救磚包](https://drive.google.com/file/d/13d0YYQIY8lWUw69n6VSp0hlkMW2UsJhS/view?usp=sharing)(救到 bootloader)

線刷刷入國際版
---
### ROG Phone 2
```
手機開機到 fastboot 模式
雙擊 RAW 檔內的 flashall_AFT.cmd
```
### ROG Phone 3
```
手機開機到 fastboot 模式
雙擊 RAW 檔內的 zs661ks_raw_flashall.bat
```
修改 Country Code
---
- 安裝 MT 檔案管理器
[下載 MT 檔案管理器](https://www.coolapk.com/apk/bin.mt.plus)
- 授權 Magisk root 權限
- 修改 `/vendor/factory/COUNTRY` 內的文字
```
CN
```
- 修改為
```
WW
```
- 存檔退出
- 重新開機

上鎖 bootloader
---
```
fastboot oem asus-csc_lk
```

後記
---
### ROG Phone 2 fastboot 命令
##### 感謝 [@Shakalaca](https://github.com/shakalaca)
```
@======== Fastboot command ========
@Get info :
  @>>> fastboot oem gpt-info
  @>>> fastboot oem isn-info
  @>>> fastboot oem ssn-info
  @>>> fastboot oem system-info
  @>>> fastboot oem device-info
@Get ID :
  @>>> fastboot oem get-prjid
  @>>> fastboot oem get-hwid
  @>>> fastboot oem get-dtid
  @>>> fastboot oem get-skuid
  @>>> fastboot oem get-rfsku
  @>>> fastboot oem get-cpuid
  @>>> fastboot oem get-featureid
  @>>> fastboot oem get-jtagid
@Get battery capacity :
  @>>> fastboot oem get-batcap
@Get battery voltage :
  @>>> fastboot oem get-batvol
@Get image version :
  @>>> fastboot oem get_build_version
@Get boot count :
  @>>> fastboot oem get-bootcount
@Check if do copy CN tar to fsg for CN low cost sku or not :
  @>>> fastboot oem get-CNtar
@Check fuse status :
  @>>> fastboot oem check-fuse
@Check setup wizard status :
  @>>> fastboot oem checksetupwizard
@Show barcode :
  @>>> fastboot oem show-barcode
@Reset count info (the device need to be authorized) :
  @>>> fastboot oem reset-boot_count
  @>>> fastboot oem reset-lock_count
  @>>> fastboot oem reset-a_retry_count
  @>>> fastboot oem reset-a_unbootable_count
  @>>> fastboot oem reset-b_retry_count
  @>>> fastboot oem reset-b_unbootable_count
@Lock device authorized :
  @>>> fastboot oem reset-dev_info
@Lock device authorized2:
  @>>> fastboot oem reset-auth2
@Reset if do copy CN tar to fsg for CN sku or not flag :
  @>>> fastboot oem reset-CNtar
@ASUS lock (the device need to be authorized) :
  @>>> fastboot oem asus-csc_lk
@Disable/Enable verity status :
  @>>> fastboot oem disable-verity
  @>>> fastboot oem enable-verity
@Read pmic register :
  @>>> fastboot oem dump-pmic-reg_
  @[Usage]: fastboot oem dump-pmic-reg_[PmicIndex][RegAddress]
  @[Ex]: fastboot oem dump-pmic-reg_0810
@Write pmic register :
  @>>> fastboot oem write-pmic-reg_
  @[Usage]: fastboot oem write-pmic-reg_[PmicIndex][RegAddress][WriteValue]
  @[Ex]: fastboot oem write-pmic-reg_081102
@Force HW ID :
  @>>> fastboot oem force-hwid_
  @      fastboot set_active a
  @      fastboot continue
@Default enable adb :
  @>>> fastboot oem adb_enable
@Factory reset and reboot the device :
  @>>> fastboot oem factory-reset
@Factory reset and reboot the device to bootloader :
  @>>> fastboot oem factory-reset2
@Reboot the device to recovery :
  @>>> fastboot oem reboot-recovery
@Shutdown the device :
  @>>> fastboot oem shutdown
@Enter shipping mode :
  @>>> fastboot oem EnterShippingMode
@Enable/Disable charger screen :
  @>>> fastboot oem enable-charger-screen
  @>>> fastboot oem disable-charger-screen
  @>>> fastboot oem off-mode-charge
@Select panel :
  @>>> fastboot oem select-display-panel
  @[Usage]: fastboot oem select-display-panel [Mode]
  @[Ex]: fastboot oem select-display-panel none
  @[Ex]: fastboot oem select-display-panel prim:
@Get fastboot variable :
  @>>> fastboot getvar
  @[Usage]: fastboot getvar [Var]
  @[Ex]: fastboot getvar all
  @[Ex]: fastboot getvar cid
@Dungle unlock :
  @>>> fastboot oem gen-random
  @>>> fastboot oem auth-hash
  @>>> fastboot oem auth-hash_2
@Check crc :
  @>>> fastboot oem crc32_
  @[Usage]: fastboot oem crc32_[PartitionName]
  @[Ex]: fastboot oem crc32_boot_a
  @>>> fastboot oem hash_
  @[Usage]: fastboot oem hash_[PartitionName]
  @[Ex]: fastboot oem hash_boot_a
@Rsa test :
  @>>> fastboot oem rsa_test_
@Enter emergency download mode :
  @>>> fastboot oem enter-dload
@Check S3 pm_app_pon_reset_source_type :
  @>>> fastboot oem check-s3
@Set default permissive :
  @>>> fastboot oem set-permissive
@Set slot b enable :
  @>>> fastboot oem slot_b_enable
@Get verify vbmeta ret :
  @>>> fastboot oem get-verify_vbmeta_ret  
```


Happy Hacking!
---

###### tags: `Android`