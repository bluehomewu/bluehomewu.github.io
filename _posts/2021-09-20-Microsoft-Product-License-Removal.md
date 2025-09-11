---
title: Microsoft 產品授權移除
date: 2021-09-20
categories: [Windows]
tags: [Windows, Microsoft, Office]

---

# Microsoft 產品授權移除

移除 Microsoft Office 產品授權
---
###### 本文以 Office 2016 Professional Plus 為例
- 到 Microsoft Office 產品安裝路徑下
64 位元 `C:\Program Files\Microsoft Office\Office16`
32 位元 `C:\Program Files(x86)\Microsoft Office\Office16`
- 以系統管理者身分，在這個資料夾下執行命令提示字元
輸入 `cscript "C:\Program Files\Microsoft Office\Office16\ospp.vbs" /dstatus`

![](https://i.imgur.com/R42WV1Z.png)

- 可以看到紅色圈起來的部分，為此次範例需要移除的產品授權
- 接下來請執行 
`cscript "C:\Program Files\Microsoft Office\Office16\ospp.vbs" /unpkey:xxxxx`
- 根據本文範例，因此筆者實作時應該輸入的指令為
`cscript "C:\Program Files\Microsoft Office\Office16\ospp.vbs" /unpkey:33W3X`

### 移除 Office 2016 Professional Plus 授權之前
![](https://i.imgur.com/AbgKaXV.png)

### 移除 Office 2016 Professional Plus 授權之後
![](https://i.imgur.com/oO2wFtM.png)

[參考原文](https://joechang0113.github.io/2020/04/20/kms-license-clean.html)

###### tags: `Windows` `Microsoft` `Office`