---
title: PVE 踩坑紀錄
date: 2023-03-10
categories: [PVE]
tags: [PVE, UNIKO's]

---

# EdwardWu 的 PVE 踩坑紀錄


網路卡消失術
---
- 前情提要：
    改完 BIOS RTC 喚醒之後，重開機，就再也連不上 PVE 後台了。
    起初還以為是我 BIOS 設定有誤，導致開不起來，這個平台剛好沒裝 speaker，沒辦法聽 debug 聲。（手邊沒有多的了）
    
    裝上顯卡（[ASUS ENGTS450](https://www.asus.com/tw/supportonly/engts450_series/helpdesk_download/)），發現可以正常進入 PVE 系統
    嘗試 login root 之後，注意到所有網路卡都是處於 DOWN 狀態
    透過 `ifup vmbr0` 橋接網路卡之後注意到 error message，`error vmbr0 bridge port enp7s0 doesn't exist`
    
- 解決辦法：
    `nano /etc/network/interfaces`
    修改 /etc/network/interfaces 檔案
    把原本的 enp7s0 都改為 enp9s0
    修改完如下圖所示
    
    修改後：
    ![](https://i.imgur.com/OI02nWh.png)
    
    
    
- 術後記錄
    ![](https://i.imgur.com/3eqid6u.png)
    
    ![](https://i.imgur.com/EvtzqPH.png)
    
    [Chapter 11. Consistent Network Device Naming](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/ch-consistent_network_device_naming)
    [討論對話開頭](https://t.me/homepve/9825/10209)
    
    
    
    
###### tags: `PVE` `UNIKO's`