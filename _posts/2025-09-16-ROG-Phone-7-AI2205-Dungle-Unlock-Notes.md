---
title: ROG Phone 7 (AI2205) Dungle Unlock notes
date: 2025-09-16
categories: [ASUS]
tags: [ASUS, Android]

---

# ROG Phone 7 (AI2205) Dungle Unlock notes

#### Thanks: ASUS Taiwan for help

`fastboot oem gen-random`

```
C:\Users\EdwardWu>fastboot oem gen-random
(bootloader) Random Num = 5c5c1001d2fb190a6a6d421fe924645b
OKAY [  0.003s]
Finished. Total time: 0.003s
```

```
fastboot flash asuskey2 %unlock_file%
fastboot oem auth-hash
fastboot oem factory-reset
```

![image](https://hackmd.io/_uploads/HJ0pJjLige.png)

```
C:\Users\EdwardWu>fastboot flash asuskey2 %unlock_file%
Sending 'asuskey2' (0 KB)                          OKAY [  0.002s]
Writing 'asuskey2'                                 OKAY [  0.002s]
Finished. Total time: 0.058s

C:\Users\EdwardWu>fastboot oem auth-hash
(bootloader)    Authorized Result : PASS
OKAY [  0.023s]
Finished. Total time: 0.024s

C:\Users\EdwardWu>fastboot oem factory-reset
OKAY [  0.001s]
Finished. Total time: 0.001s
```


###### tags: `Android` `ASUS` `ROG`
