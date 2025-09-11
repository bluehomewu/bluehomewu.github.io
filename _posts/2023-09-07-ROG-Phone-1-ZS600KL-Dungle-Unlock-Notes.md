---
title: ROG Phone 1 (ZS600KL) Dungle Unlock notes
date: 2023-09-07
categories: [ASUS]
tags: [ASUS, Android]

---

# ROG Phone 1 (ZS600KL) Dungle Unlock notes

#### Thanks: ASUS Taiwan for help

`fastboot oem gen-random`

```
C:\Users\EdwardWu>fastboot oem gen-random
< waiting for any device >
(bootloader) ==================================
(bootloader) Random Num = 1114ca59159229aa0dc91f4e3d65277f
(bootloader) ==================================
OKAY [  0.009s]
Finished. Total time: 0.010s
```

```
fastboot flash asuskey2 hash_file.bin
fastboot flashing unlock
```

![](https://i.imgur.com/3ZRcjvA.png)

![](https://i.imgur.com/cEyRFIW.png)


```
D:\待整理\hash_file>fastboot oem auth-hash
(bootloader) ==================================
(bootloader)    Calculate hash =
(bootloader)     229e7d95573ab004c75a2fb155ea4626
(bootloader)     573ab004c75a2fb155ea4626
(bootloader)     c75a2fb155ea4626
(bootloader) ==================================
(bootloader) ==================================
(bootloader)    Receiver hash =
(bootloader)     229e7d95573ab004c75a2fb155ea4626
(bootloader)     573ab004c75a2fb155ea4626
(bootloader)     c75a2fb155ea4626
(bootloader) ==================================
(bootloader)    Authorized Result : PASS
OKAY [  0.031s]
Finished. Total time: 0.032s
```


###### tags: `Android` `ASUS` `ROG`