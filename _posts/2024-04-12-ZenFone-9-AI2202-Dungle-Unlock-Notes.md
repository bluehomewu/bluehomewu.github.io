---
title: ZenFone 9 (AI2202) Dungle Unlock notes
date: 2024-04-12
categories: [ASUS]
tags: [ASUS, Android, ROG]

---

# ZenFone 9 (AI2202) Dungle Unlock notes

#### Thanks: ASUS Taiwan for help
#### Need SN & CPUID


```
C:\Users\EdwardWu>fastboot oem cpuid
(bootloader) CpuID = E39EA78C
OKAY [  0.002s]
Finished. Total time: 0.002s

C:\Users\EdwardWu>fastboot oem cpuid
(bootloader) CpuID = 7990DC40
OKAY [  0.002s]
Finished. Total time: 0.002s
```
```
C:\Users\EdwardWu>fastboot flash asuskey E39EA78C.mbn
Sending 'asuskey' (0 KB)                           OKAY [  0.007s]
Writing 'asuskey'                                  OKAY [  0.002s]
Finished. Total time: 0.028s

C:\Users\EdwardWu>fastboot flash asuskey 7990DC40.mbn
Sending 'asuskey' (0 KB)                           OKAY [  0.007s]
Writing 'asuskey'                                  OKAY [  0.002s]
Finished. Total time: 0.028s
```

```
C:\Users\EdwardWu>fastboot oem asus-unlock
(bootloader) Device unlocked successfully.
OKAY [  0.023s]
Finished. Total time: 0.023s
```


![](https://hackmd.io/_uploads/SJ-haZPAn.png)
![](https://hackmd.io/_uploads/rkF_C88gA.png)




###### tags: `Android` `ASUS` `ROG`
