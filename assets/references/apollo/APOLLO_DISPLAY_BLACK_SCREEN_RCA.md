---
layout: page
title: Nokia G60 5G（Apollo）LineageOS 背光亮但無畫面 RCA 與解法評估
permalink: /references/apollo/display-black-screen-rca/
toc: true
comments: false
sitemap: false
noindex: true
mermaid: true
---

- 調查期間：2026-08-20 至 2026-08-21
- 裝置：Nokia G60 5G（apollo / APO_sprout）
- 系統：LineageOS 22.2 / Android 15
- 實機 kernel：`5.4.254-qgki-960012-g82c1fdf6d69c`
- 實機 slot：`_b`
- Display HAL fork：`Edward-Projects/android_hardware_qcom_display`，branch `lineage-22.2-apollo`
- 調查時 HAL HEAD：`e7ed277dd1da6b1e23a67528723c5d00ffe1d30b`（first-commit defer；尚未包含本文提出的 ABI compatibility）
- 實機狀態：Android userspace 已完成開機、ADB root 可用、觸控正常、面板只有背光而無可見 pixels
- 結論狀態：已由實機 SurfaceFlinger／SDM dump、Stock binary disassembly 與 Current ELF DWARF 三條獨立證據閉合；修正尚待編譯與實機 A/B 驗證

## 1. 結論摘要

這次黑屏不是 Android 沒有完成開機，也不是 SurfaceFlinger 沒有產生畫面。實機 screenshot 含完整 UI，HWC 也收到多個 layers；但 SDM 的硬體 pipe 表只有表頭和表尾，沒有任何有效 pipe row。

直接根因是目前顯示堆疊混用了兩個不同 private ABI 世代：

- `libsdmcore.so` 與 composer service：由 Lineage sm8350 display source 編譯；
- `libsdmextension.so`：Nokia Android 14 Stock blob。

Stock extension 將 `HWPipeInfo::valid=true` 寫到 offset `0x228`，Current source core 卻從 `0x22c` 讀取 `valid`。因此 extension 認為 pipe 已成功分配，core 則始終認為 pipe 無效，最後在 `HWDeviceDRM::SetupAtomic()` 跳過所有 `PLANE_SET_*` 操作。

其唯一已確認的 layout 差異來源，是 Current sm8350 `DisplayDetailEnhancerData` 比 Stock extension ABI 多出的 4-byte `content_type`：

~~~cpp
DeContentType content_type = kContentTypeUnknown;
~~~

它讓內嵌於 `HWPipeInfo` 的 `HWScaleData` 從 `0x1d8` 增長為 `0x1dc`，使 `z_order`、`flags`、`valid`、`is_virtual` 與 `inverse_pma_info` 全部向後位移 4 bytes。

最終建議不是把 `libsdmcore` 換成 Stock blob，而是保留 source-built core，採用只對 Apollo 生效的 legacy-extension ABI build。若要先做最小、完全不改共用 HAL source 的確認，可先不安裝 `libsdmextension.so`，讓 source core 使用內建 `ResourceDefault`／GPU client-target fallback。

## 2. 證據可信度標記

本文使用三種標記：

- **直接證據**：可直接在實機 log、ELF、DTB、source 或 binary disassembly 中讀到。
- **解析結果**：由 DWARF layout、AArch64 disassembly、hash／byte comparison 或 source control flow 得到，可重算。
- **待驗證修正**：根因證據已閉合，但 proposed build 尚未刷入實機。

## 3. 問題現象

### 3.1 實機可觀察行為

完整系統 OTA sideload 後：

1. 裝置停留在 Android One／Powered by Android logo 一段時間；
2. 接著面板背光亮起，但沒有任何可見畫面；
3. MTP 可枚舉；
4. 使用 `vendor_boot-debug.img` 後可取得 ADB root；
5. `sys.boot_completed=1`；
6. 觸控正常；
7. 實體 Power OFF→ON 後仍是只有背光。

這表示問題已經不是「Android 尚未開機」，而是 display output path 的某一層沒有把已完成合成的 pixels送進面板。

### 3.2 有效 framebuffer 的直接證據

實機 screencap：

~~~text
/tmp/apollo-live-display-final-eIqlu5/83-screen-after-cycle.png
~~~

資料：

~~~text
PNG 1080x2408 RGBA
SHA-256 d3bbbe5cb8565369a5c098755ebc5960478e294d2c6df130c450c554d30c0edf
5550 colors
~~~

這張圖不是全黑，證明：

- SystemUI／Launcher 與 SurfaceFlinger 已工作；
- SurfaceFlinger composition／capture path內有有效 UI pixels；
- 黑屏發生在 framebuffer 產生之後。

## 4. 先排除的方向

### 4.1 Recovery、boot 與 panel payload

已確認 Apollo 是 recovery-as-boot；Lineage Recovery 可正常顯示且觸控已由 recovery ramdisk touch firmware修正。

Current：

- Apollo base DTB 與 Nokia Stock V3.230 第一顆 Blair DTB byte-identical；
- Apollo DTBO 與 Stock `dtbo.img` entry 0 byte-identical；
- active panel 是 FT8720 TCL；
- panel DCS ON table包含 Sleep Out `0x11`、120 ms wait、Display On `0x29`；
- panel OFF table包含 Display Off `0x28` 與 Sleep In `0x10`。

所以 active panel node、timing、DSC parameters 與 DCS tables並非搬運錯誤。

### 4.2 First-commit DMS

早期 build 曾在第一幀直接要求 120 Hz，造成：

~~~text
DMS not supported on first frame
DSI display prepare failed, rc=-22
~~~

sm8350 composer 已補上與相鄰 Qualcomm HAL 一致的 first-commit defer；實機目前沒有再出現：

- `DMS not supported on first frame`；
- `DSI display prepare failed`；
- `Unexpected engine state`；
- `Connector Post kickoff rc=-22`。

但畫面仍然黑，因此 DMS 是先前獨立問題，不是目前剩餘黑屏的根因。

### 4.3 SM5109C panel bias

已依 Stock ABI 與順序補入：

~~~text
vregs ON
  -> active pinctrl
  -> 5 ms
  -> sm5109c_on()
  -> 5 ms
  -> panel reset
~~~

以及 gesture-mode gated `sm5109c_off()`。

實機 Power OFF→ON：

~~~text
21:12:12.050  sm5109c_off
21:12:17.823  dsi_display_set_mode ... fps=60
21:12:17.851  sm5109c_on
~~~

OFF／ON 路徑確實執行，沒有 DSI prepare 或 commit error，畫面仍黑。因此 SM5109C call omission已被修正，但不是目前剩餘 root cause。

### 4.4 `display_panel_avdd`

`display_panel_avdd` 在 boot completed 後被 regulator core列為 unused 並停用，一度看似與黑屏時間吻合。

Stock DTB／DTBO 交叉驗證後確認：

- active FT8720 TCL／DJ panel使用 `dsi_panel_pwr_supply_no_labibb`；
- active supply只有 `vddio`；
- `display_panel_avdd` 沒有被 FT8720 panel引用；
- Stock `dsi_panel_power_on()` 同樣只有 generic vregs、pinctrl、SM5109C 與 reset。

因此 `display_panel_avdd` 是非 active panel的 orphan rail，不能改接到 FT8720，也不應設成 always-on。

### 4.5 Panel digital state、DSI 與 ESD

實機 active panel啟用 `reg_read` ESD status check，每 5 秒讀：

| DCS register | Expected |
|---|---:|
| `0x0A` | `0x9c` |
| `0x0B` | `0x00` |
| `0x0D` | `0x00` |

Power cycle 後持續約 18 分鐘，沒有：

- `read status failed`；
- `mismatch`；
- `PANEL_DEAD`；
- DSI timeout；
- underflow；
- atomic commit／fence error。

現存 capture沒有逐次列出每一輪實際回讀 bytes；能直接確認的是 ESD monitor按 5 秒週期運作，且約 18 分鐘內沒有回報 read failure、value mismatch或 `PANEL_DEAD`。這與 `0x9c/0x00/0x00` expected responses持續被接受相符，強烈支持 panel digital path、DCS readback與 link仍活著，但不是每一筆 raw value的直接紀錄，也不能單獨證明每個 video payload pixel被正確 scanout。

### 4.6 DSC、topology 與 60 Hz timing

Current 與 Stock 的 Holi／Blair DSC catalog、topology table與 register packing已逐項比對。

Native 120 Hz timing：

~~~text
Vtotal = 2408 + VBP 16 + VSW 4 + VFP 46 = 2474
~~~

VFP DFPS 切至 60 Hz：

~~~text
new_vfp = 46 + 2474 * (120 - 60) / 60
        = 2520
new_vtotal = 4948
~~~

實機 SDM dump：

~~~text
cur:60
v_front_porch:2520
v_total:4948
clk:149924
Topology:2
~~~

完全吻合。`Topology:2` 是 single-LM DSC；`VFP=2520` 不是 overflow或異常 porch。

### 4.7 UBWC

實機 HWC layers與 client target 都是 `RGBA_8888_UBWC`，因此 UBWC曾是合理 hypothesis。

但 Stock／Current：

- base DTB byte-identical；
- UBWC version都是 2.0；
- swizzle都是 6；
- highest-bank-bit相同；
- `sde_format_map_ubwc`、`plane_formats`、`plane_formats_vig` raw tables逐 byte相同；
- live allocation size符合 source與 Stock gralloc layout。

因此沒有證據支持「Current kernel UBWC catalog與 Stock不同」。`vendor.gralloc.disable_ubwc=1` 只能作診斷 A/B，不能當作已有證據的永久修正。

## 5. 決定性實機線索：有 HWC layers，但沒有有效 pipe

`dumpsys SurfaceFlinger` 顯示多個 HWC layers與有效 client target：

~~~text
composition: Device/Device ... format: RGBA_8888_UBWC
composition: Device/Client ... format: RGBA_8888_UBWC
client target ... format: RGBA_8888_UBWC
~~~

同一份 dump 的 SDM section：

~~~text
ROI(LTRB)#0 LEFT(0 0 1080 2408)

|-----|---------------|-----------|------| ... |
| Idx |   Comp Type   |   Split   | Pipe | ... |
|-----|---------------|-----------|------| ... |
|-----|---------------|-----------|------| ... |
~~~

表頭後直接是表尾，沒有任何 pipe row。

對應 source：

- `display_builtin.cpp:1182-1189`：只有 `hw_layers_.info.hw_layers.size()==0` 才印 `No hardware layers programmed` 並 return；
- `display_builtin.cpp:1225-1233`：vector非空才進入每 layer dump；
- `display_builtin.cpp:1291-1304`：只有 `pipe.valid==true` 才輸出 pipe row；
- `display_base.cpp:697`：`Flush()` 會直接清空 `hw_layers`，清空後應印 `No hardware layers programmed`。

實機沒有印 `No hardware layers programmed`，所以不是單純 vector為空或 Flush 後 snapshot；而是 cached HW layers存在，但每個 left／right pipe的 `valid` 都是 false。

這是從「panel／DSI」轉向「SDM resource ABI」的關鍵。

## 6. Current 與 Stock 顯示元件來源

目前 Apollo 並非使用完整 Stock display stack：

| 元件 | Current 來源 | Stock／Current關係 |
|---|---|---|
| composer service | sm8350 source-built | 與 Stock binary不同 |
| `libsdmcore.so` | sm8350 source-built | 與 Stock binary不同 |
| `libsdmextension.so` | Nokia Stock blob | 與 Stock逐 byte相同 |

### 6.1 `libsdmcore` 是 source-built

`hardware/qcom-caf/sm8350/display/sdm/libs/core/Android.bp`：

~~~bp
cc_library_shared {
    name: "libsdmcore",
    ...
    srcs: [
        "core_interface.cpp",
        "core_impl.cpp",
        "display_base.cpp",
        "display_builtin.cpp",
        "resource_default.cpp",
        "drm/hw_device_drm.cpp",
        ...
    ],
}
~~~

Binary：

| Build | Size | SHA-256 |
|---|---:|---|
| Nokia Stock `libsdmcore.so` | 685,200 | `42e2de60440c81efde1208d36429f4ed8319577b523eec54717b125824f89375` |
| Current source `libsdmcore.so` | 452,744 | `03dbb73a06d32ba12e40a5e7a0a2bc405504a058e2b66b3703f821ff8613b9cc` |

### 6.2 `libsdmextension` 是 Stock blob

`device/nokia/apollo/proprietary-files.txt` 明確列出：

~~~text
vendor/lib/libsdmextension.so
vendor/lib64/libsdmextension.so
~~~

`vendor/nokia/apollo/Android.bp` 生成 `cc_prebuilt_library_shared`。

64-bit hash：

~~~text
5713b26b5b03d31254e8f186a9e122bc2fc20ee8c2c4306d3ef76f27ce5fae55
~~~

Current installed、vendor proprietary與 Nokia Stock三者完全相同。

## 7. Private ABI mismatch 的直接二進位證據

### 7.1 Stock extension期待的 `HWPipeInfo` layout

Stock `libsdmextension.so` disassembly：

- `ResourceImpl::SrcSplitConfig` 在 `0x9de38` 將 `1` 寫至 `HWPipeInfo+0x228`；
- `PipeAlloc::AcquirePipes` 在 `0x88f7c` 讀 `HWPipeInfo+0x228`；
- `PipeAllocDrm::ReservePipe` 讀寫 flags `+0x224`；
- 同函式寫 `is_virtual +0x229`。

由多個獨立函式交叉確認 Stock layout：

| Stock field | Offset |
|---|---:|
| `z_order` | `0x220` |
| `flags` | `0x224` |
| `valid` | `0x228` |
| `is_virtual` | `0x229` |
| `inverse_pma_info` subobject base | `0x22c` |

### 7.2 Current source core的實際 layout

Current unstripped `libsdmcore.so` DWARF：

| Current field | Offset |
|---|---:|
| `z_order` | `0x224` |
| `flags` | `0x228` |
| `valid` | `0x22c` |
| `is_virtual` | `0x22d` |
| `inverse_pma_info` subobject base | `0x230` |

Current `DisplayBuiltIn::Dump()` disassembly亦直接在：

~~~text
ldrb w8, [HWPipeInfo, #0x22c]
~~~

讀取 `valid`，與 DWARF一致。

### 7.3 寫入落到錯誤欄位

Stock extension寫入 Current object後：

| Stock extension動作 | Current core實際解讀 |
|---|---|
| 寫 `z_order@0x220` | 寫到 Current `HWScaleData` 尾端 |
| 寫 `flags@0x224` | 寫到 Current `z_order` |
| 寫 `valid=true@0x228` | 寫到 Current `flags` low byte |
| 寫 `is_virtual@0x229` | 寫到 Current `flags` 第二個 byte |
| Current讀 `valid@0x22c` | 保持 false |

因此 extension內部的 resource／strategy code認為 pipe有效，source core與 DRM code卻認為所有 pipe無效。

## 8. 唯一已確認的 4-byte layout來源

Current sm8350：

~~~cpp
struct DisplayDetailEnhancerData {
  ...
  uint32_t de_blend = 0;
  DeContentType content_type = kContentTypeUnknown;
};
~~~

Stock extension對應的舊 ABI與本樹 sm7250／sm8250 source：

~~~cpp
struct DisplayDetailEnhancerData {
  ...
  uint32_t de_blend = 0;
};
~~~

連鎖 size變化：

| Structure | Stock ABI | Current ABI | Delta |
|---|---:|---:|---:|
| `DisplayDetailEnhancerData` | `0x28` | `0x2c` | +4 |
| `HWDetailEnhanceData` | `0x3c` | `0x40` | +4 |
| `HWScaleData` | `0x1d8` | `0x1dc` | +4 |

Stock scaler disassembly更進一步證明：

- Stock `prec_shift` 寫在 `HWScaleData+0x1b4`；
- Current DWARF把 `content_type` 放到該位置；
- Current `prec_shift` 因此被推到 `+0x1b8`。

這不是單純 `valid` 一個 bool不同，而是 scaler detail data到 `inverse_pma_info` 的整段 private layout都偏移。

從 `dgm_csc_info@0x238` 起，因 8-byte alignment重新對齊：

- `dgm_csc_info`；
- CSC payload；
- LUT vector；
- transform；
- tonemap；
- format；
- solid-fill；
- `sizeof(HWPipeInfo)==0x300`；
- right pipe offset；
- `HWLayerConfig` stride；

Stock／Current再次一致。完整掃描沒有找到第二個會影響本次 pipe chain的 offset drift。

## 9. 黑屏完整因果鏈

~~~mermaid
flowchart TD
    A[SurfaceFlinger 產生正常 UI framebuffer] --> B[Composer 建立 HWC layers]
    B --> C[Stock libsdmextension 執行 resource / pipe allocation]
    C --> D[extension 將 valid=true 寫入 HWPipeInfo + 0x228]
    D --> E[Current libsdmcore 將 +0x228 解讀為 flags]
    E --> F[Current valid + 0x22c 保持 false]
    F --> G[SDM dump 有 HW layers但零 pipe rows]
    G --> H[HWDeviceDRM::SetupAtomic 跳過 PLANE_SET]
    H --> I[DPU 沒有 SSPP framebuffer plane]
    I --> J[DSI / panel / backlight仍開啟]
    J --> K[實體結果：背光亮但沒有 pixels]
~~~

Current source的終點條件：

~~~cpp
uint32_t fb_id = registry_.GetFbId(&layer, input_buffer->handle_id);

if (pipe_info->valid && fb_id) {
    drm_atomic_intf_->Perform(DRMOps::PLANE_SET_ALPHA, ...);
    ...
}
~~~

由於 `pipe_info->valid` 是 false，所有 plane programming被跳過；這精確解釋為何 atomic commit本身不一定報錯，但實體畫面仍黑。

## 10. 解法評估

### 10.1 方案 A：Apollo-only 不安裝 `libsdmextension.so`

#### 機制

`libsdmcore` 以 `dlopen("libsdmextension.so")` 載入 extension。非 Trusted VM build在載入失敗時只印 warning，不會中止：

1. `CoreImpl::Init()` 繼續初始化；
2. `CompManager::Init()` 改用 source `ResourceDefault`；
3. `Strategy::GetNextStrategy()` 將 app layers改成 GPU composition；
4. client target使用 source core分配的單一／雙 pipe輸出。

Current vendor掃描中，沒有其他 ELF以 `DT_NEEDED` 直接依賴 `libsdmextension.so`；它是由 `libsdmcore` 動態載入。

#### 優點

- 不修改共用 sm8350 HAL source；
- 只改 Apollo proprietary packaging；
- 完全避開 Stock extension private ABI；
- 是最乾淨、最容易判讀的 A/B。

#### 代價

- 所有 app layers退化為 GPU client-target composition；
- 失去 Stock multi-plane strategy；
- 失去 extension partial-update；
- 失去 extension DPPS control；
- destination scaler停用；
- 可能增加功耗、GPU負載與 jank；
- 高刷新下效能需另行驗證。

#### 定位

推薦作為第一個 controlled A/B或暫時 bring-up方案，不建議未經效能／功耗測試直接作為最終量產設定。

### 10.2 方案 B：Apollo-only source-built legacy ABI

這是保留 Stock extension功能的推薦長期方案。

#### 原則

不應全域刪除 `content_type`。應新增只由 Apollo選用的 Soong config，例如：

~~~make
$(call soong_config_set,qtidisplay,apollo_stock_extension_abi,true)
~~~

在 sm8350 display建立一個獨立 `cc_defaults`，由：

~~~bp
select(soong_config_variable("qtidisplay", "apollo_stock_extension_abi"), {
    "true": ["-DSDM_APOLLO_STOCK_EXTENSION_ABI"],
    default: [],
})
~~~

產生 cflag。

只將該 defaults套到：

- `libsdmcore`；
- `vendor.qti.hardware.display.composer-service`。

不要：

- 放進共用 `qtidisplay_defaults`；
- export到 `display_headers`；
- 對 gralloc或其他 display modules全域套用；
- 讓其他產品預設啟用。

#### Source layout切換

~~~cpp
struct DisplayDetailEnhancerData {
  ...
  uint32_t de_blend = 0;
#ifndef SDM_APOLLO_STOCK_EXTENSION_ABI
  DeContentType content_type = kContentTypeUnknown;
#endif
};
~~~

Composer中唯一對 `de_data.content_type` 賦值的 switch亦使用同一條件；vendor tuning parameter與原本的 debug log可保留。

#### 為何 core與composer都必須重編

Composer會建構 `DisplayDetailEnhancerData`，再跨 `DisplayInterface` 傳入 core。若只有 core使用舊 layout而 composer仍使用新 layout，會在另一個邊界再次形成 ABI mismatch。

#### ABI assertions

只在 Apollo legacy ABI與 LP64 build啟用：

~~~cpp
static_assert(sizeof(DisplayDetailEnhancerData) == 0x28);
static_assert(sizeof(HWDetailEnhanceData) == 0x3c);
static_assert(sizeof(HWScaleData) == 0x1d8);
static_assert(__builtin_offsetof(HWPipeInfo, flags) == 0x224);
static_assert(__builtin_offsetof(HWPipeInfo, valid) == 0x228);
static_assert(__builtin_offsetof(HWPipeInfo, is_virtual) == 0x229);
static_assert(sizeof(HWPipeInfo) == 0x300);
~~~

`HWPipeInfo` 含 STL members，`offsetof` 可能觸發 `-Winvalid-offsetof`；若 compiler判斷為 non-standard-layout，應只在 dedicated ABI assertion translation unit周圍局部 push／ignore／pop該 diagnostic，不要對整個 module加全域 `-Wno-invalid-offsetof`。

#### 對其他裝置的影響

其他裝置沒有設定 Apollo Soong flag，仍保留：

- Current `content_type`；
- Current struct sizes；
- Current sm8350 ABI；
- 原本 composer行為。

因此 source tree雖包含兩種 layout，實際產物是 product-scoped，不會改變其他裝置的 binary。

目前 HAL fork本身也放在 Apollo專用分支：

~~~text
https://github.com/Edward-Projects/android_hardware_qcom_display
branch: lineage-22.2-apollo
~~~

這提供 repository branch與product flag兩層隔離。

### 10.3 方案 C：單獨改用 Stock `libsdmcore.so`

技術上可以包成 prebuilt，但不建議單獨替換。

Stock與Current `libsdmcore` 的 `DT_NEEDED` 名稱大致相同，但實際 binary均不同：

- composer不同；
- `libsdmutils` 不同；
- `libsdedrm` 不同；
- `libdrmutils` 不同；
- gralloc／metadata libraries不同。

Current composer只直接 import `CoreInterface::CreateCore`／`DestroyCore` 這類少量具名 symbols；建立 interface後主要透過：

- C++ virtual calls；
- vtable；
- Layer／HW struct pointers；
- private enums與containers；

與 core互動。ELF symbol checker看不到這些 data layout風險。

這次已經實際證明「symbol存在」不等於 private C++ ABI相容。因此只替換 Stock core，很可能把一個已定位的 4-byte mismatch換成多個更難觀察的 mismatch。

### 10.4 方案 D：完整 Stock display stack

若一定要使用 Stock core，最低限度應把 Stock composer與core視為一對；嚴謹做法是配對：

- Stock composer；
- `libsdmcore`；
- `libsdmextension`；
- `libsdmutils`；
- `libsdedrm`；
- `libdrmutils`；
- `libqdMetaData`；
- gralloc／displayconfig dependencies。

之後仍需驗證 Android 14 vendor binaries對 Android 15：

- HIDL／VINTF；
- binder與libc++ vendor ABI；
- mapper／allocator；
- framework display APIs；
- SELinux；
- boot與runtime stability。

範圍遠大於目前的單一 layout相容修正，應視為 fallback，不是首選。

## 11. 不建議的修法

### 11.1 全域刪除 `content_type`

會改變所有使用該 sm8350 branch的產品 ABI。即使 Apollo能亮，也可能讓使用新版 extension的其他裝置出問題。應使用 product-scoped flag。

### 11.2 只改 `HWPipeInfo::valid` offset或 patch blob

問題不是只有一個 bool：

- scaler detail data；
- pre-downscale fields；
- `z_order`；
- `flags`；
- `valid`；
- `is_virtual`；
- `inverse_pma_info`；

整段都受 +4 影響。只 patch `valid` 會留下其他 silent corruption。

### 11.3 永久關閉 UBWC

Stock本身也使用 UBWC，Current／Stock static catalog與layout已一致。沒有 positive A/B前不應把 `vendor.gralloc.disable_ubwc=1` 當修正。

### 11.4 修改 FT8720 supply或強制 `display_panel_avdd`

違反 Stock DT與Stock display power flow，可能造成硬體 rail sequencing風險。

### 11.5 永久鎖定 60 Hz

Current 60 Hz VFP計算正確，且 zero pipe issue與 refresh rate無關。鎖 60只能掩蓋其他問題並失去功能。

## 12. 建議執行順序

### Controlled A/B 驗證矩陣

| 檢查項目 | Phase 1：No extension | Phase 2：Apollo legacy ABI |
|---|---|---|
| 唯一主要變因 | 不安裝 `libsdmextension.so` | 恢復同一 Stock extension；core／composer切成 Apollo ABI |
| Extension log | `dlopen` 失敗 warning，core繼續 | extension成功載入 |
| Resource path | source `ResourceDefault`／GPU client target | Stock resource／strategy extension |
| SDM pipe table預期 | 至少一個 valid client-target pipe row | 出現由 extension分配的 valid pipe rows |
| 實體畫面預期 | 可見，但效能／功耗可能退化 | 可見，且保留 Stock顯示最佳化 |
| 結果判讀 | 若仍為零 pipe，需推翻或擴充目前 RCA | 若 static asserts通過但仍為零 pipe，需搜尋第二個未覆蓋的 runtime ABI邊界 |

### Phase 1：No-extension controlled A/B

只對 Apollo停止安裝 32／64-bit `libsdmextension.so`，重建 vendor／完整 image。

成功判準：

1. composer log顯示 extension載入失敗但 core繼續；
2. `ResourceDefault`／GPU client-target fallback啟用；
3. SDM dump pipe table出現至少一個 valid pipe row；
4. 實體畫面可見；
5. screenshot與實體畫面內容一致；
6. 無 DRM atomic／DSI error。

若實體畫面恢復，即以不依賴 offset推理的 runtime A/B再次確認 extension ABI是 root cause。

### Phase 2：Apollo-scoped legacy ABI

恢復 Stock extension，加入只對 Apollo生效的 ABI flag，重編：

- composer service；
- `libsdmcore`；
- vendor image／OTA相關產物。

Build-time成功判準：

1. 所有 ABI static assertions通過；
2. Current unstripped core DWARF顯示：

~~~text
DisplayDetailEnhancerData 0x28
HWDetailEnhanceData       0x3c
HWScaleData               0x1d8
HWPipeInfo.flags          0x224
HWPipeInfo.valid          0x228
HWPipeInfo.is_virtual     0x229
~~~

3. composer與core均收到相同 ABI cflag；
4. 其他產品未設定 flag時仍保留 Current layout。

### Phase 3：實機功能回歸

至少驗證：

- cold boot；
- screen OFF→ON多次；
- 60／90／120 Hz切換；
- Launcher、Settings、動畫與影片；
- screenshot與實體畫面；
- SDM pipe table有有效 rows；
- client-target與device composition都能提交；
- 無 `PLANE_SET`／atomic／fence／underflow錯誤；
- partial update；
- 長時間 idle與喚醒；
- 功耗、溫度與掉幀；
- Recovery顯示不回歸。

## 13. 建議決策

| 方案 | 影響其他裝置 | 功能完整度 | ABI風險 | 建議 |
|---|---|---|---|---|
| Apollo不安裝 extension | 無 | 較低 | 低 | 第一個 A/B |
| Apollo-scoped source ABI | 無（預設關閉） | 高 | 已精確控制 | 最終首選 |
| 單獨 Stock core | Apollo-only但相依面廣 | 不確定 | 高 | 不建議 |
| 完整 Stock display stack | Apollo-only | 可能高 | Android 14→15風險高 | 最後 fallback |
| 全域修改 sm8350 layout | 可能影響所有裝置 | 高 | 高 | 禁止 |

最合理路徑：

~~~text
先以 no-extension fallback做一次 runtime確認
    ↓
確認 pipe rows與實體畫面恢復
    ↓
加入 Apollo-only ABI flag
    ↓
恢復 Stock extension並保留完整顯示功能
    ↓
執行 refresh／partial-update／功耗回歸測試
~~~

## 14. 主要證據索引

### 實機 logs

~~~text
/tmp/apollo-live-display-final-eIqlu5/12-dumpsys-SurfaceFlinger.txt
/tmp/apollo-live-display-final-eIqlu5/60-boot-display-kernel-sequence.txt
/tmp/apollo-live-display-final-eIqlu5/71-dmesg-after-power-cycle.txt
/tmp/apollo-live-display-final-eIqlu5/72-sf-after-power-cycle.txt
/tmp/apollo-live-display-final-eIqlu5/79-active-panel-status-dt.txt
/tmp/apollo-live-display-final-eIqlu5/83-screen-after-cycle.png
/tmp/apollo-live-display-final-eIqlu5/87-logcat-late-after-cycle.txt
/tmp/apollo-live-display-final-eIqlu5/88-dmesg-late-after-cycle.txt
/tmp/apollo-live-display-final-eIqlu5/89-late-status-esd-interval.txt
~~~

`/tmp` 是暫存區；本報告已保存所有決定性 offset、hash、公式與結論，不應只依賴該目錄長期存在。

### Current source

~~~text
hardware/qcom-caf/sm8350/display/Android.bp
hardware/qcom-caf/sm8350/display/composer/Android.bp
hardware/qcom-caf/sm8350/display/composer/hwc_display_builtin.cpp
hardware/qcom-caf/sm8350/display/sdm/include/core/display_interface.h
hardware/qcom-caf/sm8350/display/sdm/include/private/hw_info_types.h
hardware/qcom-caf/sm8350/display/sdm/libs/core/Android.bp
hardware/qcom-caf/sm8350/display/sdm/libs/core/core_impl.cpp
hardware/qcom-caf/sm8350/display/sdm/libs/core/comp_manager.cpp
hardware/qcom-caf/sm8350/display/sdm/libs/core/strategy.cpp
hardware/qcom-caf/sm8350/display/sdm/libs/core/display_builtin.cpp
hardware/qcom-caf/sm8350/display/sdm/libs/core/drm/hw_device_drm.cpp
device/nokia/apollo/proprietary-files.txt
vendor/nokia/apollo/Android.bp
~~~

### Stock binaries

~~~text
/home/edwardwu/workspace/dump/working/nokia_apo_sprout_dump/vendor/lib64/libsdmcore.so
/home/edwardwu/workspace/dump/working/nokia_apo_sprout_dump/vendor/lib64/libsdmextension.so
~~~

## 15. 分析邊界與透明揭露

- 本輪最終 ABI RCA與解法評估沒有修改 source、沒有 build，也沒有對裝置寫入。
- 大部分 live檢查為 ADB讀取 log、properties、sysfs與 dumpsys。
- 早期 display調查中曾有一次使用 `i2cget -f` 讀取 SM5109 register。它沒有寫入 configuration value，但會產生主動 I²C transaction；本報告的根因與任何結論均不依賴該讀值，也不建議重複。
- 「ABI mismatch造成零 pipe」已由 live dump、Stock disassembly與Current DWARF閉合；「Apollo-scoped修正後實體畫面恢復」仍屬待驗證修正，必須以新的 build與實機結果完成最後一層確認。
