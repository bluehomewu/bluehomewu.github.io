---
title: 繞過 Zenfone / ROG Phone 阻擋跑分軟體方法筆記
date: 2025-10-22
categories: [ASUS]
tags: [ASUS, Android]

---

# 繞過 Zenfone / ROG Phone 阻擋跑分軟體方法筆記

由於華碩會在特殊的系統版本中加入阻擋跑分軟體的功能，導致使用者在使用手機時無法進行跑分測試，~~影響使用體驗XD~~。

所以我在這邊紀錄一下繞過 Zenfone / ROG Phone 阻擋跑分軟體的方法筆記。


- 從我抓到的一份 adb logcat 來看，阻擋跑分軟體的功能是由 `BenchmarkBlockerService` 這個服務所提供的。

```
	行號 88601: 10-22 12:06:53.087  1652  1681 I ActivityManager: Force stopping com.primatelabs.geekbench6 appid=10242 user=0: from pid 7084
	行號 88913: 10-22 12:06:53.885  1652  1985 I ActivityManager: Force stopping com.primatelabs.geekbench6 appid=10242 user=0: from pid 7084
	行號 89175: 10-22 12:06:54.573  1652  1680 I ActivityManager: Force stopping com.primatelabs.geekbench6 appid=10242 user=0: from pid 7084
	行號 89434: 10-22 12:06:55.157  1652  3114 I ActivityManager: Force stopping com.primatelabs.banff appid=10243 user=0: from pid 7084
	行號 90185: 10-22 12:06:58.660  1652  4246 I ActivityManager: Force stopping com.futuremark.dmandroid.application appid=10240 user=0: from pid 7084
	行號 90667: 10-22 12:06:59.567  1652  1681 I ActivityManager: Force stopping com.antutu.ABenchMark appid=10244 user=0: from pid 7084
```

```
C:\Users\EdwardWu>adb shell
ASUS_AI2301:/ $ ps -A | grep 7084
system        7084   786 15289716 138224 0                  0 S com.asus.benchmarkblocker
```

從這兩段可以得到 pid 為 7084 的程式為 `com.asus.benchmarkblocker`，而這個服務正是 `BenchmarkBlockerService`。

- 接著我們可以使用 `dumpsys activity services` 指令來查看這個服務的詳細資訊：

```
ASUS_AI2301:/ $ dumpsys activity services | grep -n BenchmarkBlockerService -A 20
2220:  * ServiceRecord{f7921d3 u0 com.asus.benchmarkblocker/.BenchmarkBlockerService}
2221-    intent={act=com.asus.benchmarkblocker.service.TaskWatcherService pkg=com.asus.benchmarkblocker}
2222-    packageName=com.asus.benchmarkblocker
2223-    processName=com.asus.benchmarkblocker
2224-    permission=com.asus.permission.SUPPORT_BENCHMARK
2225-    baseDir=/system/priv-app/BenchmarkBlocker/BenchmarkBlocker.apk
2226-    dataDir=/data/user/0/com.asus.benchmarkblocker
2227-    app=ProcessRecord{4c57586 7084:com.asus.benchmarkblocker/1000}
2228-    allowWhileInUsePermissionInFgs=true
2229-    recentCallingPackage=com.asus.focusapplistener
2230-    recentCallingUid=1000
2231-    allowStartForeground=PROC_STATE_PERSISTENT
2232-    startForegroundCount=0
2233-    infoAllowStartForeground=[callingPackage: com.asus.focusapplistener; callingUid: 1000; uidState: PER ; intent: Intent { act=com.asus.benchmarkblocker.service.TaskWatcherService pkg=com.asus.benchmarkblocker }; code:PROC_STATE_PERSISTENT; tempAllowListReason:<,reasonCode:SYSTEM_ALLOW_LISTED,duration:9223372036854775807,callingUid:-1>; targetSdkVersion:33; callerTargetSdkVersion:33; startForegroundCount:0; bindFromPackage:null]
2234-    createTime=-4m35s36ms startingBgTimeout=--
2235-    lastActivity=-4m35s35ms restartTime=-4m35s35ms createdFromFg=true
2236-    Bindings:
2237-    * IntentBindRecord{1806029 CREATE}:
2238-      intent={act=com.asus.benchmarkblocker.service.TaskWatcherService pkg=com.asus.benchmarkblocker}
2239-      binder=android.os.BinderProxy@9ab9fae
2240-      requested=true received=true hasBound=true doRebind=false
--
2243:          ConnectionRecord{4c9afc2 u0 CR com.asus.benchmarkblocker/.BenchmarkBlockerService:@393140d}
2244-    All Connections:
2245:      ConnectionRecord{4c9afc2 u0 CR com.asus.benchmarkblocker/.BenchmarkBlockerService:@393140d}
2246-
2247-  * ServiceRecord{cab7f5f u0 com.asus.gamecenter/.aurasync.headset.HeadsetControlService}
2248-    intent={pkg=com.asus.gamecenter cmp=com.asus.gamecenter/.aurasync.headset.HeadsetControlService}
2249-    packageName=com.asus.gamecenter
2250-    processName=com.asus.gamecenter
2251-    permission=com.asus.aurasync.AURASYNC
2252-    baseDir=/system/priv-app/ROGGameCenter/ROGGameCenter.apk
2253-    dataDir=/data/user/0/com.asus.gamecenter
2254-    app=ProcessRecord{571812f 2715:com.asus.gamecenter/u0a95}
2255-    allowWhileInUsePermissionInFgs=true
2256-    recentCallingPackage=android
2257-    recentCallingUid=1000
2258-    allowStartForeground=PROC_STATE_PERSISTENT
2259-    startForegroundCount=0
2260-    infoAllowStartForeground=[callingPackage: android; callingUid: 1000; uidState: PER ; intent: Intent { pkg=com.asus.gamecenter cmp=com.asus.gamecenter/.aurasync.headset.HeadsetControlService }; code:PROC_STATE_PERSISTENT; tempAllowListReason:<,reasonCode:SYSTEM_ALLOW_LISTED,duration:9223372036854775807,callingUid:-1>; targetSdkVersion:33; callerTargetSdkVersion:33; startForegroundCount:0; bindFromPackage:null]
2261-    createTime=-5m1s423ms startingBgTimeout=--
2262-    lastActivity=-5m1s281ms restartTime=-5m1s281ms createdFromFg=true
2263-    Bindings:
2264-    * IntentBindRecord{16b40dc CREATE}:
2265-      intent={pkg=com.asus.gamecenter cmp=com.asus.gamecenter/.aurasync.headset.HeadsetControlService}
--
4466:  * ConnectionRecord{4c9afc2 u0 CR com.asus.benchmarkblocker/.BenchmarkBlockerService:@393140d}
4467:    binding=AppBindRecord{74e314f com.asus.benchmarkblocker/.BenchmarkBlockerService:com.asus.services}
4468-    conn=android.os.BinderProxy@393140d flags=0x1
4469-  * ConnectionRecord{15b8281 u0 CR com.asus.powersaver/.PowerSaverService:@3978e68}
4470-    binding=AppBindRecord{bef1969 com.asus.powersaver/.PowerSaverService:com.android.systemui}
4471-    conn=android.os.BinderProxy@3978e68 flags=0x1
4472-  * ConnectionRecord{e0dbd82 u0 CR WACT CAPS com.google.android.gms/.chimera.PersistentApiService:@3cbc0cd}
4473-    binding=AppBindRecord{5086ddb com.google.android.gms/.chimera.PersistentApiService:com.google.android.gms.persistent}
4474-    conn=android.os.BinderProxy@3cbc0cd flags=0x1081
4475-  * ConnectionRecord{abd3566 u0 com.android.bluetooth/.csip.CsipSetCoordinatorService:@3d859c1}
4476-    binding=AppBindRecord{f83dbaf com.android.bluetooth/.csip.CsipSetCoordinatorService:com.android.settings}
4477-    conn=android.os.BinderProxy@3d859c1 flags=0x0
4478-  * ConnectionRecord{a69400e u0 com.android.bluetooth/.le_audio.LeAudioService:@3e8c609}
4479-    binding=AppBindRecord{83a13c6 com.android.bluetooth/.le_audio.LeAudioService:system}
4480-    conn=android.app.LoadedApk$ServiceDispatcher$InnerConnection@3e8c609 flags=0x0
4481-  * ConnectionRecord{f227ee9 u0 CR com.asus.hardwarestub/.cpulimit.CpuLimitControlService:@3f49b70}
4482-    binding=AppBindRecord{b54b8f5 com.asus.hardwarestub/.cpulimit.CpuLimitControlService:com.asus.services}
4483-    conn=android.os.BinderProxy@3f49b70 flags=0x1
4484-  * ConnectionRecord{cdc8ca0 u0 CR com.moji.tencent.weather/com.moji.api.service.APIBGService:@43201a3}
4485-    binding=AppBindRecord{c721807 com.moji.tencent.weather/com.moji.api.service.APIBGService:com.moji.tencent.weather}
4486-    conn=android.os.BinderProxy@43201a3 flags=0x1
4487-  * ConnectionRecord{a9f9155 u0 CR CAPS com.google.android.gms/.cast.media.CastMediaRoute2ProviderService_Persistent:@442040c}
```

從上面的輸出可以看到 `BenchmarkBlockerService` 的相關資訊，包括它的 package name 是 `com.asus.benchmarkblocker`，並且它有一個權限 `com.asus.permission.SUPPORT_BENCHMARK`。


- 接著我們可以使用 `cmd package list packages` 指令來查看系統中有哪些與跑分軟體相關的 package：

```
ASUS_AI2301:/ $ cmd package list packages | grep -i benchmark
package:com.antutu.aibenchmark
package:com.asus.benchmarkblocker
package:com.antutu.ABenchMark
package:com.asus.ims.benchmarkblocker
```

從上面的輸出可以看到有兩個與跑分軟體相關的 package，分別是 `com.asus.benchmarkblocker` 和 `com.asus.ims.benchmarkblocker`。

經由[上一篇文章](https://bluehomewu.github.io/posts/Disable-ASUS-Phone-IMEI-Watermark/)的經驗，我已經不考慮停用 `com.asus.benchmarkblocker` 這個服務，因為沒有足夠的權限停用它。  
因此我決定嘗試直接對 `user 0` 刪除 `com.asus.benchmarkblocker` & `com.asus.ims.benchmarkblocker` 這兩個 package。


```
ASUS_AI2301:/ $ pm uninstall -k --user 0 com.asus.benchmarkblocker
Success
ASUS_AI2301:/ $ pm uninstall -k --user 0 com.asus.ims.benchmarkblocker
Success
ASUS_AI2301:/ $

```

成功刪除這兩個 package 後，跑分軟體就可以正常運作了！  
Happy Hacking !


###### tags: `Android` `ASUS` `ROG`

