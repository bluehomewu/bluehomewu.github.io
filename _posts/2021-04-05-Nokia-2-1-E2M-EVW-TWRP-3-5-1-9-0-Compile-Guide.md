---
title: Nokia 2.1 E2M/EVW TWRP 3.5.1-9-0 編譯
date: 2021-04-05 20:00:00
categories: [Android]
tags: [Android, Recovery, 編譯, 筆記]

---

# Nokia 2.1 E2M/EVW TWRP 3.5.1-9-0 編譯

Nokia 2.1 規格:
---
OS: Android Oreo Go
SOC: Snapdragon 425
RAM/ROM: 1GB/8GB
Battery: 4000 mAh
Screen: 1280x720 pixels / 5.5 inch
###### EVW和E2M的唯一區別就是EVW是verizon訂製機，頻段上對verizon做了優化，別的硬體規格和E2M一模一樣

建立可用 TWRP Device Tree
---
- 首先透過SebaUbuntu提供的TWRP-device-tree-generator
https://github.com/SebaUbuntu/TWRP-device-tree-generator

編譯
---
- 詳細編譯教學，請參考 [Android 第三方 Recovery 繁體中文編譯教學](https://hackmd.io/@EdwardWu/CompileARecovery)
- 在這之後進行編譯，第一個版本(27MB)透過光卡的測試
發現TWRP 檔案太大無法刷入該手機的Recovery分區(原始大小24MB)
在BoardConfig.mk檔案中加入了LZMA壓縮指令後
https://git.io/JYHz8
- 生成第二版本，將體積壓縮到23MB，也終於可以刷入手機
第二版本測試過程中發現
"adb shell" not working & 外接式SD Card無法掛載(可支援terminal手動掛載)
在檢視過log文件後，發現到我壓根沒寫上sdcard的掛載程序
我是天才吧（？
https://git.io/JYHzu
在補上sdcard的掛載程序後 adb shell 就自己好了?神奇!!
- 第三版本也終於誕生
目前測試起來功能都正常

刷入方法:
---
```
fastboot flash recovery twrp.img
fastboot oem HALT
```
- 然後拔掉手機，手機會自動關機。
再來按住音量+連接電腦後就直接進入TWRP了。

TWRP Device Tree : 
https://github.com/Edward-Recovery-Lab/twrp_device_fih_E2M
XDA threads:
https://forum.xda-developers.com/t/recovery-twrp-3-5-1-9-0-nokia-2-1-e2m-evw-unofficial-build.4245221/?fbclid=IwAR3aScyRQb-Uk1yNeSUV5oneWhkYfYQmpuGAr1WE7E_nUXwEyNx82YyBvE8

![](https://i.imgur.com/4lQ1BCC.png)  

![](https://i.imgur.com/kkOh7nW.png)  

![](https://i.imgur.com/2M2XSai.jpg)


###### tags: `Android` `Recovery` `編譯` `筆記`