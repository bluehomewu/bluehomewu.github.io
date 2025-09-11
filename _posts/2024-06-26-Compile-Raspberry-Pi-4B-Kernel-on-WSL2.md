---
title: 在 WSL2 上 Compile Raspberry Pi 4B 的 Kernel
date: 2024-06-26
categories: [RaspberryPi]
tags: [RaspberryPi, Kernel]

---

# 在 WSL2 上 Compile Raspberry Pi 4B 的 Kernel

## Topic: [Modified OV5647 CMOS Camera](https://github.com/bluehomewu/rpi-linux/commit/c57793d39319dbc0995bcef11534594835123995)

Ref1: [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/computers/linux_kernel.html#cross-compiling-the-kernel)
Ref2: [Raspberry Pi GitHub](https://github.com/raspberrypi)
Ref3: [Applying Patches To The Linux Kernel](https://www.kernel.org/doc/html/next/process/applying-patches.html)

Cross-Compiling the Kernel
---
### 安裝必要的編譯套件 && Toolchain

#### 所需的依賴項
```shell=
$ sudo apt install git bc bison flex libssl-dev make libc6-dev libncurses5-dev -y
```

#### Toolchain

32 位元 Kernel
```shell=
$ sudo apt install crossbuild-essential-armhf -y
```

64 位元 Kernel
```shell=
$ sudo apt install crossbuild-essential-arm64 -y
```

### 下載 kernel source

```shell=
$ cd < path >
$ git clone git@github.com:raspberrypi/linux.git -b < branch name >
```

### Build Source

#### 32 位元 configs

For Raspberry Pi 1, Zero and Zero W, and Raspberry Pi Compute Module 1:
```shell=
$ cd linux
$ KERNEL=kernel
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcmrpi_defconfig
```

For Raspberry Pi 2, 3, 3+ and Zero 2 W, and Raspberry Pi Compute Modules 3 and 3+:
```shell=
$ cd linux
$ KERNEL=kernel7
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2709_defconfig
```

For Raspberry Pi 4 and 400, and Raspberry Pi Compute Module 4:
```shell=
$ cd linux
$ KERNEL=kernel7l
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2711_defconfig
```

#### 64 位元 configs

For Raspberry Pi 3, 3+, 4, 400 and Zero 2 W, and Raspberry Pi Compute Modules 3, 3+ and 4:

```shell=
$ cd linux
$ KERNEL=kernel8
$ make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- bcm2711_defconfig
```

For Raspberry Pi 5:

```shell=
$ cd linux
$ KERNEL=kernel_2712
$ make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- bcm2712_defconfig
```

:::success
##### Note:
標準的 bcm2711_defconfig 基於的核心 (kernel8.img) 也可以在 Raspberry Pi 5 上使用。不過為了獲得最佳效能，您應該使用 kernel_2712.img，但對於需要 4KB 頁面大小的情況，則應使用  kernel8.img (kernel=kernel8.img)
:::

#### Customising the Kernel Version Using `LOCALVERSION`
除了核心配置變更之外，您可能還想調整 LOCALVERSION 以確保新核心不會收到與上游核心相同的版本字串。 這不僅表明您在 uname 的輸出中運行自己的內核，也確保 /lib/modules 中的現有模組不會被覆蓋。

為此，請更改 .config 中的以下行：


```
CONFIG_LOCALVERSION="-v8-Edward_Kernel"
```


### Build with Configs

#### For all 32-bit Builds
```shell=
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs
```
#### For all 64-bit Builds
:::success
#### Note:
Note the difference between Image target between 32 and 64-bit.
```shell=
$ make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- Image modules dtbs
```
:::


Installing Kernel to SDCard
---
Ref4: [Windows Mount Linux Partition in WSL 掛載 存取 Linux USB SD Card 隨身碟 EXT4](https://casparting.github.io/windows/Windows_mount_Linux_partition_wsl/)
Ref5: [編譯 替換 Windows WSL Kernel 方法 步驟](https://casparting.github.io/windows/Windows_wsl_build_kernel/)


## 使用 USBIPD 來掛載 USB Drive/ SD Card

#### 列出目前 USB bus 狀態
```powershell=
PS C:\Users\EdwardWu> usbipd list
Connected:
BUSID  VID:PID    DEVICE                                                        STATE
1-3    13d3:56ff  Integrated Camera                                             Not shared
2-2    03f0:028e  USB 輸入裝置                                                  Not shared
2-3    27c6:5503  Goodix fingerprint                                            Not shared
2-4    8087:0032  Intel(R) Wireless Bluetooth(R)                                Not shared
3-1    0b95:1790  ASIX AX88179 USB 3.0 to Gigabit Ethernet Adapter #3           Not shared
3-3    05e3:0749  USB Mass Storage Device                                       Not shared
```

#### Allow Share USB bus 3-3
```powershell=
PS C:\Users\EdwardWu> usbipd bind -b 3-3

PS C:\Users\EdwardWu> usbipd list
Connected:
BUSID  VID:PID    DEVICE                                                        STATE
1-3    13d3:56ff  Integrated Camera                                             Not shared
2-1    2109:2817  Generic USB Hub                                               Not shared
2-2    03f0:028e  USB 輸入裝置                                                  Not shared
2-3    27c6:5503  Goodix fingerprint                                            Not shared
2-4    8087:0032  Intel(R) Wireless Bluetooth(R)                                Not shared
3-1    0b95:1790  ASIX AX88179 USB 3.0 to Gigabit Ethernet Adapter #3           Not shared
3-3    05e3:0749  USB Mass Storage Device                                       Shared
```

#### 向 WSL 轉送 usb bus 3-3 device
```powershell=
PS C:\Users\EdwardWu> usbipd attach --wsl --busid 3-3
usbipd: info: Using WSL distribution 'Ubuntu-22.04' to attach; the device will be available in all WSL 2 distributions.
usbipd: info: Using IP address 172.19.112.1 to reach the host.
```

#### 關閉 WSL
```powershell=
PS C:\Users\EdwardWu> wsl --shutdown
```

#### 列出 USB 裝置
```powershell=
PS C:\Users\EdwardWu> usbipd list
Connected:
BUSID  VID:PID    DEVICE                                                        STATE
1-3    13d3:56ff  Integrated Camera                                             Not shared
2-2    03f0:028e  USB 輸入裝置                                                  Not shared
2-3    27c6:5503  Goodix fingerprint                                            Not shared
2-4    8087:0032  Intel(R) Wireless Bluetooth(R)                                Not shared
3-1    0b95:1790  ASIX AX88179 USB 3.0 to Gigabit Ethernet Adapter #3           Not shared
3-3    05e3:0749  USB Mass Storage Device                                       Attached
```

#### 移除 USB bus 3-3
```powershell=
PS C:\Users\EdwardWu> usbipd detach --busid 3-3
```

## 將 Raspberry Pi 4B 的 SDCard 分割區掛載到資料夾

```shell=
$ lsblk
NAME MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda    8:0    0 389.8M  1 disk 
sdb    8:16   0     3G  0 disk [SWAP]
sdc    8:32   0   256G  0 disk /mnt/wslg/distro
                               /
```

```shell=
$ lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      8:0    0 389.8M  1 disk 
sdb      8:16   0     3G  0 disk [SWAP]
sdc      8:32   0   256G  0 disk /mnt/wslg/distro
                                 /
sdd      8:48   1     0B  0 disk 
sde      8:64   1  59.5G  0 disk 
├─sde1   8:65   1   512M  0 part 
└─sde2   8:66   1    59G  0 part 
```

#### 掛載分割區
:::warning
您應該根據您的設定適當調整磁碟代號，例如，如果您的 SD 卡顯示為 而 /dev/sdc 不是 /dev/sdb。
:::
```shell=
$ sudo mount /dev/sde1 ../mnt/fat32
$ sudo mount /dev/sde2 ../mnt/ext4
```

```shell=
$ lsblk                            
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      8:0    0 389.8M  1 disk 
sdb      8:16   0     3G  0 disk [SWAP]
sdc      8:32   0   256G  0 disk /mnt/wslg/distro
                                 /
sdd      8:48   1     0B  0 disk 
sde      8:64   1  59.5G  0 disk 
├─sde1   8:65   1   512M  0 part /home/edwardwu/rpi-kernel/mnt/fat32
└─sde2   8:66   1    59G  0 part /home/edwardwu/rpi-kernel/mnt/ext4
```

#### Install the Kernel Modules

```shell=
$ sudo env PATH=$PATH make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- INSTALL_MOD_PATH=../mnt/ext4 modules_install
```

#### 備份原先的 Kernel
```shell=
$ sudo cp ../mnt/fat32/kernel8.img ../mnt/fat32/kernel8-backup.img
```

#### Copy Kernel & Device Tree blobs
```shell=
$ sudo cp arch/arm64/boot/Image ../mnt/fat32/kernel8.img
$ sudo cp arch/arm64/boot/dts/broadcom/*.dtb ../mnt/fat32/
$ sudo cp arch/arm64/boot/dts/overlays/*.dtb* ../mnt/fat32/overlays/
$ sudo cp arch/arm64/boot/dts/overlays/README ../mnt/fat32/overlays/
```

#### 移除掛載分割區
```shell=
$ sudo umount ../mnt/fat32
$ sudo umount ../mnt/ext4
```

#### 測試鏡頭
```shell=
libcamera-hello 
```
#### 拍照
```shell=
libcamera-jpeg -o test.jpg
```

Build Script
---
```shell=
#!/bin/bash

# 定義 kernel tree 的路徑
LINUX_DIR="/home/edwardwu/rpi-kernel/linux"

echo "選擇要編譯的 Raspberry Pi 版本:"
echo "1. Raspberry Pi 4"
echo "2. Raspberry Pi 5"
read -p "請輸入選擇 (1 或 2): " choice

# 提問是否需要執行 make clean
read -p "是否需要執行 make clean? (y/n): " clean_choice

start_time=$(date +%s)  # 記錄開始時間

case $choice in
  1)
    echo "正在編譯 Raspberry Pi 4 的 Kernel..."
    cd $LINUX_DIR
    if [ "$clean_choice" == "y" ]; then
        echo "正在執行 make clean..."
        make clean -j$(nproc)
    fi
    KERNEL=kernel8
    #CONFIG_LOCALVERSION="-v8-Edward_Kernel"
    make -j$(nproc) ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- bcm2711_defconfig
    sed -i 's/CONFIG_LOCALVERSION="-v8"/CONFIG_LOCALVERSION="-v8-Edward_Kernel"/' .config
    make -j$(nproc) ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- Image modules dtbs | tee ../build.log
    cd -
    ;;
  2)
    echo "正在編譯 Raspberry Pi 5 的 Kernel..."
    cd $LINUX_DIR
    if [ "$clean_choice" == "y" ]; then
        echo "正在執行 make clean..."
        make clean -j$(nproc)
    fi
    KERNEL=kernel_2712
    #CONFIG_LOCALVERSION="-v2712-Edward_Kernel"
    make -j$(nproc) ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- bcm2712_defconfig
    sed -i 's/CONFIG_LOCALVERSION="-v8-16k"/CONFIG_LOCALVERSION="-v2712-Edward_Kernel"/' .config
    make -j$(nproc) ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- Image modules dtbs
    cd -
    ;;
  *)
    echo "無效的選擇"
    ;;
esac

end_time=$(date +%s)  # 記錄結束時間
elapsed=$((end_time - start_time))  # 計算總耗時
minutes=$((elapsed / 60))
seconds=$((elapsed % 60))
echo "編譯完成，總耗時: ${minutes}分鐘 ${seconds}秒"

```

Install Script
---
```shell=
#!/bin/bash

:<<comment
Reference: https://hackmd.io/9f2GysWvR5eA1Y_t56Vtmw?view#Installing-Kernel-to-SDCard
comment

# 定義掛載點目錄
MOUNT_POINT="/home/edwardwu/rpi-kernel/mnt"

# 定義 kernel tree 的路徑
LINUX_DIR="/home/edwardwu/rpi-kernel/linux"

# 顯示選單
echo "選擇要刷入的 Raspberry Pi 版本:"
echo "1. Raspberry Pi 4"
echo "2. Raspberry Pi 5"
read -p "請輸入選擇 (1 或 2): " choice

# 根據選擇設置 kernel 和 device tree blobs 的目標路徑
if [ "$choice" -eq 1 ]; then
    KERNEL_IMG="kernel8.img"
    DEVICE="Raspberry Pi 4"
elif [ "$choice" -eq 2 ]; then
    KERNEL_IMG="kernel_2712.img"
    DEVICE="Raspberry Pi 5"
else
    echo "無效的選擇，請輸入 1 或 2."
    exit 1
fi

echo "檢查 SD 卡是否已掛載到 WSL..."
lsblk

# 檢查是否有可掛載的 SD 卡分割區
if lsblk | grep -q 'sde'; then
    echo "找到 SD 卡分割區，準備掛載..."
else
    echo "未找到 SD 卡分割區，請確認 SD 卡已正確插入並重試。"
    exit 1
fi

# 建立掛載目錄
# mkdir -p $MOUNT_POINT/fat32
# mkdir -p $MOUNT_POINT/ext4

# 掛載分割區
echo "掛載 FAT32 分割區到 $MOUNT_POINT/fat32"
sudo mount /dev/sde1 $MOUNT_POINT/fat32
echo "掛載 EXT4 分割區到 $MOUNT_POINT/ext4"
sudo mount /dev/sde2 $MOUNT_POINT/ext4

# 檢查掛載是否成功
mount | grep sde

start_time=$(date +%s)  # 記錄開始時間

# 安裝 kernel 模組
echo "安裝 kernel 模組..."
cd $LINUX_DIR
pwd
sudo env PATH="$PATH" make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- INSTALL_MOD_PATH=$MOUNT_POINT/ext4 modules_install
cd $LINUX_DIR/../
pwd

# 複製 Kernel 和 Device Tree blobs
echo "複製 Kernel 和 Device Tree blobs..."
sudo cp $LINUX_DIR/arch/arm64/boot/Image $MOUNT_POINT/fat32/$KERNEL_IMG
sudo cp $LINUX_DIR/arch/arm64/boot/dts/broadcom/*.dtb $MOUNT_POINT/fat32/
sudo cp $LINUX_DIR/arch/arm64/boot/dts/overlays/*.dtb* $MOUNT_POINT/fat32/overlays/
sudo cp $LINUX_DIR/arch/arm64/boot/dts/overlays/README $MOUNT_POINT/fat32/overlays/

# 移除掛載
echo "移除掛載分割區..."
sudo umount $MOUNT_POINT/fat32
sudo umount $MOUNT_POINT/ext4

# 計算總耗時
end_time=$(date +%s)  # 記錄結束時間
elapsed=$((end_time - start_time))  # 計算總耗時
minutes=$((elapsed / 60))
seconds=$((elapsed % 60))
echo "刷寫完畢，總耗時: ${minutes}分鐘 ${seconds}秒"

# 輸出完成訊息
echo "已經完成 $DEVICE kernel 的刷寫"

```

Finally !!
---
![](https://i.imgur.com/uHWbs7b.jpg)





