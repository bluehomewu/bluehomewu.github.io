---
title: Nothing Phone (2a) 工程機 DVT 恢復基頻 & IMEI 紀錄
date: 2026-02-27 00:05:00 +0800
tags: [Nothing Tech, CMF]
categories: [Nothing Tech 產品評測]
---

# Nothing Phone (2a) DVT 工程機：恢復基頻 (Baseband) 與 IMEI 紀錄

## 前言
最近幸運地透過朋友 **Yuze Wu (@MlgmXyysd)** 的協助，取得了一台 Nothing Phone (2a) 的 DVT (Design Verification Test) 工程機。剛入手時，手機處於無限重啟（Bootloop）的狀態。

在嘗試線刷的過程中，我發現 `connsys_bt`、`connsys_wifi`、`connsys_gnss` 以及 `logo` 這四個分區在寫入時會發生 Flash Error。

**錯誤 Log 如下：**
```text
[18396][02-26 00:01:51.455]<3> LINE_1123 FlashPartitions() spfl(0x0A7F8720), connsys_bt_a
[18396][02-26 00:01:51.480]<3> LINE_578 ExecuteCommandErasePartition() spfl(0x0A7F8720), 
[18396][02-26 00:01:51.522]<3> LINE_586 ExecuteCommandErasePartition() spfl(0x0A7F8720), succeed 
[18396][02-26 00:01:51.522]<3> LINE_557 ExecuteCmddWritePartitionFromBuffer() spfl(0x0A7F8720), 
[18396][02-26 00:01:51.604]<3> LINE_565 ExecuteCmddWritePartitionFromBuffer() spfl(0x0A7F8720), succeed 
[18396][02-26 00:01:51.660]<0> LINE_718 ReadBinToWritePartition() spfl(0x0A7F8720), error(write/read is different)
```

雖然原因不明，但手動忽略這四個分區後，手機即可完成刷機並正常開機。

值得一提的是，這台手機本體為黑色，最初「關於手機」頁面的設備圖示也是黑色的；但在我執行 `fastbot erase persist` 分區後，該頁面的圖示變成了白色。  
我原本計畫透過備份自己手邊零售版 Nothing Phone (2a) 的基頻相關分區，並還原至這台 DVT 機台上，以修復基頻遺失及 IMEI 為空（null）的問題。

**參考來源：** [spike0en/nothing_archive - Backing Up Essential Partitions](https://github.com/spike0en/nothing_archive?tab=readme-ov-file#backing-up-essential-partitions-after-unlocking-bootloader)

![image](/assets/img/posts/BJLLDJRu-g.png)

根據文件說明，修復過程需要刷寫 `persist` 分區。  
然而，當我將備份的 `persist.img` 刷入 DVT 之後，手機卻無法進入系統，並反覆重啟至 Recovery 模式提示需要「Wipe Data」。  
即便執行清除數據後情況依舊，因此我最終只能透過 `fastboot erase persist` 來確保手機能正常啟動。

---

## 恢復基帶 (Baseband)
由於可以透過備份還原的方式修復基帶，我使用 `NothingFlashTool.exe` 從我另一台未解鎖（Locked Bootloader）的零售機中提取必要分區。

![image](/assets/img/posts/rkP_Ok0OZg.png)

取得備份後，依序執行以下指令即可恢復基帶：

```bash
fastboot flash nvram nvram.img
fastboot flash nvdata nvdata.img
fastboot flash nvcfg nvcfg.img
```

刷入完成後，基帶即成功恢復。此時 IMS 與行動網路皆可正常運作。

![image](/assets/img/posts/r1dbF1Cd-x.png)

從截圖中可以看到，狀態列的 VoLTE 與 VoWi-Fi 已成功註冊，經測試撥打電話也完全正常。不過，此時的 IMEI 仍顯示為未知（null）。

---

## 恢復 IMEI
要修復 IMEI，必須使用 **ModemMeta Tool**。

*   **工具下載：** [ModemMeta Tool for Windows](https://androidmtk.com/download-modemmeta-tool)
*   **教學參考：** [How to use Modem Meta Tool](https://androidmtk.com/use-modem-meta-tool)

修復過程基本上參考上述網站操作即可，沒有太大的阻礙。僅有兩點需要特別注意：

1.  **Load DB 階段：** 程式會詢問要從檔案載入還是從手機讀取，請直接選擇 **"Load from target"**。
2.  **IMEI 格式：** 填寫時僅需輸入前 14 位數字。通常 IMEI 為 15 位，最後一位是校驗碼（Checksum），程式會自動計算並補全，無需手動輸入。

![image](/assets/img/posts/r15Nj10d-e.png)

至此，這台 Nothing Phone (2a) DVT 的基帶與 IMEI 已完全恢復正常。

About Me
---
我是 EdwardWu
- Telegram：[EdwardWu](https://t.me/edwardwu0223)
- Instagram : [_920223](https://www.instagram.com/_920223/)
- GitHub : [bluehomewu](https://github.com/bluehomewu)
- Email : [bluehome.wu@gmail.com](mailto:bluehome.wu@gmail.com)

![image](/assets/img/posts/Bk1EYGfYA.png)

###### tags: `Android` `Nothing` `Nothing Phone (2a)` `ROM` `Nothing Tech`
