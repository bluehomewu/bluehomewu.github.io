---
title: 關閉 / 刪除 Zenfone / ROG Phone 全局顯示 IMEI 浮水印方法筆記
date: 2025-10-21
categories: [ASUS]
tags: [ASUS, Android]

---

# 關閉 / 刪除 Zenfone / ROG Phone 全局顯示 IMEI 浮水印方法筆記

由於華碩會在特殊的系統版本中加入全局顯示 IMEI 浮水印的功能，導致使用者在使用手機時會一直看到 IMEI 浮水印，~~影響使用體驗XD~~。

所以我在這邊紀錄一下關閉 / 刪除 Zenfone / ROG Phone 全局顯示 IMEI 浮水印的方法筆記。


- 一開始我先使用 `dumpsys activity services | grep -iE "imei|watermark"` 指令查看目前系統中有關 IMEI 浮水印的服務，抓到 `com.asus.ims.watermark/.ImsWatermarkService` 這個服務

```
ASUS_AI2301:/ $ dumpsys activity services | grep -iE "imei|watermark"
  * ServiceRecord{2b3bc26 u0 com.asus.ims.watermark/.ImsWatermarkService}
    intent={act=com.asus.ims.watermark.service cmp=com.asus.ims.watermark/.ImsWatermarkService}
    packageName=com.asus.ims.watermark
    permission=com.asus.ims.watermark.BIND
    baseDir=/system/priv-app/ImsWatermarkService/ImsWatermarkService.apk
    dataDir=/data/user/0/com.asus.ims.watermark
    infoAllowStartForeground=[callingPackage: android; callingUid: 1000; uidState: PER ; intent: Intent { act=com.asus.ims.watermark.service cmp=com.asus.ims.watermark/.ImsWatermarkService }; code:PROC_STATE_PERSISTENT; tempAllowListReason:<,reasonCode:SYSTEM_ALLOW_LISTED,duration:9223372036854775807,callingUid:-1>; targetSdkVersion:33; callerTargetSdkVersion:33; startForegroundCount:0; bindFromPackage:null]

```

- 嘗試使用 `pm disable-user` & `am stopservice --user 0 -n com.asus.ims.watermark/.ImsWatermarkService || true` & `pm disable --user 0 com.asus.ims.watermark/.ImsWatermarkService` 指令來停用這個服務，都沒有辦法成功停用

```
ASUS_AI2301:/ $ pm disable-user --user 0 com.asus.ims.watermark

Exception occurred while executing 'disable-user':
java.lang.IllegalArgumentException: com.asus.ims.watermark can't be disabled!
        at com.android.server.pm.PackageManagerService.setEnabledSettings(PackageManagerService.java:3812)
        at com.android.server.pm.PackageManagerService.-$$Nest$msetEnabledSettings(Unknown Source:0)
        at com.android.server.pm.PackageManagerService$IPackageManagerImpl.setApplicationEnabledSetting(PackageManagerService.java:5645)
        at com.android.server.pm.PackageManagerShellCommand.runSetEnabledSetting(PackageManagerShellCommand.java:2356)
        at com.android.server.pm.PackageManagerShellCommand.onCommand(PackageManagerShellCommand.java:274)
        at com.android.modules.utils.BasicShellCommandHandler.exec(BasicShellCommandHandler.java:97)
        at android.os.ShellCommand.exec(ShellCommand.java:38)
        at com.android.server.pm.PackageManagerService$IPackageManagerImpl.onShellCommand(PackageManagerService.java:6162)
        at android.os.Binder.shellCommand(Binder.java:1049)
        at android.os.Binder.onTransact(Binder.java:877)
        at android.content.pm.IPackageManager$Stub.onTransact(IPackageManager.java:4437)
        at com.android.server.pm.PackageManagerService$IPackageManagerImpl.onTransact(PackageManagerService.java:6146)
        at android.os.Binder.execTransactInternal(Binder.java:1285)
        at android.os.Binder.execTransact(Binder.java:1244)
255|ASUS_AI2301:/ $ am stopservice --user 0 -n com.asus.ims.watermark/.ImsWatermarkService || true
Stopping service: Intent { cmp=com.asus.ims.watermark/.ImsWatermarkService }
Error stopping service
ASUS_AI2301:/ $ pm disable --user 0 com.asus.ims.watermark/.ImsWatermarkService

Exception occurred while executing 'disable':
java.lang.IllegalArgumentException: com.asus.ims.watermark can't be disabled!
        at com.android.server.pm.PackageManagerService.setEnabledSettings(PackageManagerService.java:3812)
        at com.android.server.pm.PackageManagerService.-$$Nest$msetEnabledSettings(Unknown Source:0)
        at com.android.server.pm.PackageManagerService$IPackageManagerImpl.setComponentEnabledSetting(PackageManagerService.java:5769)
        at com.android.server.pm.PackageManagerShellCommand.runSetEnabledSetting(PackageManagerShellCommand.java:2363)
        at com.android.server.pm.PackageManagerShellCommand.onCommand(PackageManagerShellCommand.java:272)
        at com.android.modules.utils.BasicShellCommandHandler.exec(BasicShellCommandHandler.java:97)
        at android.os.ShellCommand.exec(ShellCommand.java:38)
        at com.android.server.pm.PackageManagerService$IPackageManagerImpl.onShellCommand(PackageManagerService.java:6162)
        at android.os.Binder.shellCommand(Binder.java:1049)
        at android.os.Binder.onTransact(Binder.java:877)
        at android.content.pm.IPackageManager$Stub.onTransact(IPackageManager.java:4437)
        at com.android.server.pm.PackageManagerService$IPackageManagerImpl.onTransact(PackageManagerService.java:6146)
        at android.os.Binder.execTransactInternal(Binder.java:1285)
        at android.os.Binder.execTransact(Binder.java:1244)


```
- 最後索性直接使用 `pm uninstall -k --user 0 com.asus.ims.watermark` 指令來刪除這個 APP，成功刪除後重啟手機，IMEI 浮水印就不見了。


```
ASUS_AI2301:/ $ pm uninstall -k --user 0 com.asus.ims.watermark
Success
ASUS_AI2301:/ $ reboot

C:\Users\EdwardWu>adb shell
ASUS_AI2301:/ $ dumpsys activity services | grep -iE "imei|watermark"
1|ASUS_AI2301:/ $

```


###### tags: `Android` `ASUS` `ROG`

