# Starlink 使用者終端(User Terminal / UT,「Dishy」)深度技術研究

> 整理範圍:每一代終端的產品規格、硬體拆解、天線(相位陣列)設計、系統整合、
> MCU/SoC 選型、機構設計、專利、供應鏈與安全研究。
>
> 資料日期:2026-07。以下內容彙整自公開拆解、官方規格書、第三方成本分析、專利文件與
> 安全研究。**注意**:SpaceX 從未公開終端的完整硬體規格與晶片資料表,許多細節來自
> 第三方拆解與逆向工程,晶片代號(如 "Shiraz"、"Pulsar")多為拆解社群的非官方暱稱,
> 元件數量/成本為估算值,請以「工程級推定」看待。

---

## 目錄
1. [世代總覽表](#1-世代總覽表)
2. [各世代詳解](#2-各世代詳解)
3. [天線設計:相位陣列深入](#3-天線設計相位陣列深入)
4. [RF 晶片架構(Beamformer / FEM 演進)](#4-rf-晶片架構beamformer--fem-演進)
5. [MCU / SoC 與核心晶片選型](#5-mcu--soc-與核心晶片選型)
6. [系統整合(路由器、纜線、供電、App)](#6-系統整合路由器纜線供電app)
7. [機構設計(致動器、外殼、散熱、防護)](#7-機構設計致動器外殼散熱防護)
8. [供應鏈與製造成本](#8-供應鏈與製造成本)
9. [專利](#9-專利)
10. [安全研究](#10-安全研究)
11. [資料來源](#11-資料來源)

---

## 1. 世代總覽表

| 世代 / 型號 | 暱稱 | 上市期間 | 外形 / 對星方式 | 天線口徑 | 陣列元素 | 波束成形晶片數(估) | FEM 數(估) | FoV(視野) | 平均功耗 | 天線重量 | 天線型號 / 路由器 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Gen 1 圓形** | Round Dishy / Circular Actuated | 2020–2021(公測起) | 圓盤 + 馬達致動 | ⌀ ~23.2″(約 590 mm) | 1280 | ~80(高度分散) | ~64 | ~100° | 65–150 W(閒置 40–50 W) | ~3.9 kg | UTA-201 / UTR-201 |
| **Gen 2 方形** | Rectangular Dishy / Standard Actuated | 2021-11 – 2023 末 | 矩形 + 馬達致動 | ~513 × 303 mm | 1280 | ~16(Rev3)| 508(每 FEM 約 2 元素) | ~100° | 50–75 W | ~2.9 kg | UTA-211/212 / UTR-211 |
| **Gen 3 標準** | Standard(無馬達) | 2023 末 – 迄今 | 矩形、電子掃描、手動對準 + 腳架 | 更大矩形 | ~1280+ | ~6(新一代 Shiraz) | 更整合 | ~110° | 75–100 W(峰值更高) | 2.9 kg(含腳架 3.2 kg) | / Gen 3 Router(WiFi 6) |
| **(Flat)High Performance** | HP / Flat HP | 2021(圓頂 HP)/2023(平板 HP) | 平板固定,無馬達 | 679 × 613 mm(Flat HP) | 更大陣列 | 更多 | 更多 | 140°(Flat HP) | 峰值可達 ~150 W+ | 較重 | 企業級 |
| **Starlink Mini** | Mini | 2024 | 一體式平板 + 內建路由器 | ~298 × 259 × 38.5 mm | 較少(2 數位波束成形器) | 整合於 Catapult SoC | — | 110° | 25–40 W | 1.10 kg | 一體式(內建 WiFi 5) |

> 命名補充:SpaceX 對外的商品名(Standard / Mini / High Performance)與硬體世代
> (Gen 1/2/3)、內部硬體修訂版(REV1–REV4)並不是一一對應。拆解社群常用
> **REV1/REV2 = Gen1 圓盤、REV3 = Gen2 矩形(V2)、REV4 = Gen3 標準版**。

---

## 2. 各世代詳解

### 2.1 Gen 1 — 圓形「Round Dishy」(Circular Actuated Dish)
- **定位**:2020 年「Better Than Nothing Beta」公測起的首代量產終端,俗稱
  "Dishy McFlatface"。
- **外形/對星**:圓盤,底部有明顯的**雙馬達致動器**(方位 azimuth + 俯仰
  elevation),開機時物理旋轉「找天空」,之後由相位陣列電子掃描追星。
- **天線**:1280 元素相位陣列,六角蜂巢排列;PCB 直徑約 55 cm;背面是一台
  「自帶處理器 + RAM」的完整電腦,執行波束控制軟體。
- **電子**:板上含 GPS 接收器、PoE 磁性元件、快閃儲存、驅動兩顆對位馬達的
  **H-Bridge 馬達驅動**。
- **功耗**:平均 65–150 W,閒置 40–50 W(初代最耗電)。
- **拆解要點**:天線陣列極薄,結構背板以「誇張分量」的膠合固定在 PCB 上,
  幾乎無法無損拆解(iFixit / Kenneth Keiter 破壞式拆解)。
- **型號**:天線 UTA-201,配 UTR-201 路由器;供電由 PoE 注入器提供。

### 2.2 Gen 2 — 矩形「Rectangular Dishy」(Standard Actuated Dish,硬體 REV3 / V2)
- **定位**:2021-11 至 2023 末的主力終端,體積更小、成本更低。
- **尺寸**:約 513 mm(寬)× 303 mm(高),整組深度約 544 mm;安裝立管
  ⌀ 34 mm。天線重約 2.9 kg。
- **對星**:仍保留馬達致動(方位/俯仰),但機構簡化。
- **天線/RF**:1280 元素;第三方(Yole)拆解觀察到 **508 顆 FEM(前端模組)**,
  推測每顆 FEM 對應約 2 個天線元素;**16 顆波束成形 ASIC(Shiraz,REV3)**。
- **纜線**:改為**可拆式**專用纜線(壞了可單獨換線,不必整機報廢)。
- **供電**:PoE 供電,功耗約 50–75 W(比 Gen1 更省)。
- **型號**:天線 UTA-211 / UTA-212,配 UTR-211 路由器。
- **成本**:第三方估製造成本約 **US$400**。

### 2.3 Gen 3 — 標準版(Standard,硬體 REV4)
- **定位**:2023 末推出,現行主力。
- **最大改變**:**取消所有馬達**,改為 **110° 更寬視野 + App 引導手動對準**;
  一次擺好後靠電子掃描追星,不再物理移動。附**內建腳架(kickstand)**。
- **重量**:天線 2.9 kg(含腳架 3.2 kg),比 Gen2 更輕。
- **RF**:重新設計 PCB,採**新一代 Shiraz 數位波束成形器**,支援更多 RF 通道,
  波束成形 IC 由 REV3 的 16 顆**降到僅 6 顆**;主要面板仍鋪滿 ST 製造的 RF 前端晶片。
- **SoC/記憶體**:與 REV3 相同(ST 客製四核 Cortex-A53、同款 DRAM 與 eMMC)。
- **外殼**:更複雜的構造,以**汽車級密封膠黏合**(非超音波焊接),很難無損拆開。
- **散熱/防護**:整合融雪系統(最高清除 40 mm/hr 降雪);IP67;工作溫度
  −30 °C ~ 50 °C;可抗 96 km/h 以上強風。
- **路由器**:分離式 Gen 3 Router(WiFi 6、Tri-Band 4×4 MU-MIMO、2 個帶鎖扣
  乙太網 LAN 埠、IP56、支援最多 235 台裝置、覆蓋約 297 m²);標準套件由外接
  電源供應器對路由器供電,再經 PoE 送電給天線。

### 2.4 High Performance / Flat High Performance(企業/高階)
- **圓頂 HP(Gen 1 時代)**:更大、更耐候的固定式圓頂終端,面向企業/在動中通。
- **Flat High Performance(平板高效能)**:
  - 尺寸 679 × 613 × 191 mm;
  - **視野 140°**(比標準多看約 35% 天空,連更多衛星);
  - 下行最高約 220 Mbps、上行約 25 Mbps;
  - 支援 **Ku + Ka 雙頻**(Ka:約 17.8–18.6 / 18.8–19.3 GHz);
  - 面向高溫、高負載、極端環境的商用/企業應用;峰值功耗更高。

### 2.5 Starlink Mini(2024)
- **定位**:最小、最輕的可攜終端,約筆電大小,可放背包。
- **尺寸/重量**:298.5 × 259 × 38.5 mm、1.10 kg。
- **一體化**:**內建 WiFi 路由器**(WiFi 5、雙頻 3×3 MU-MIMO),不需外接路由盒。
- **功耗**:僅 **25–40 W**;可用行動電源、車充或 USB-C PD 供電。
- **關鍵晶片**:全新 **Catapult SoC**(內建 secure core)、單顆 8 Gb RAM、
  **2 個數位波束成形器**、GNSS 接收器(外接 LNA + patch 天線)。
- **對星**:電子相位陣列 + App 軟體輔助手動擺放,FoV 110°。
- **防護**:IP67、抗 96 km/h+ 風、融雪最高 25 mm/hr。
- **可維修性**:高度整合 → 拆解社群給出**最低可維修評分**(黏合嚴實、難拆難修)。

---

## 3. 天線設計:相位陣列深入

- **原理**:不同於傳統拋物面「碟」,Starlink 用**平面相位陣列**——上千個微型天線
  單元協同運作,靠**調整各單元的相位**做**電子波束成形(beamforming)**,不必物理
  轉向即可指向並追蹤高速掠過的 LEO 衛星,並在**微秒級**完成波束切換與換手。
- **陣列規模**:約 **1,280 個相同天線單元**,**六角蜂巢(hexagonal honeycomb)**排列;
  PCB 直徑約 **55 cm**。
- **增益/等效口徑**:約 **33–34 dBi**,相當於一面 60 cm 衛星電視碟的能量聚焦能力
  (較全向天線聚焦約 2000×),但可電子掃描。
- **頻段**:
  - **下行 Ku 頻**:約 **10.7–12.7 GHz**(約 2 GHz 頻寬,~17% 分數頻寬),
    切成 8 個 250 MHz 通道(10.7 / 10.95 / 11.2 / 11.45 / 11.7 / 11.95 / 12.2 / 12.45 GHz)。
  - **上行 Ku 頻**:約 **14.0–14.5 GHz**(500 MHz)。
  - **HP/企業級**另用 **Ka 頻**(約 17.8–19.3 GHz)。
- **PCB 疊構(stack-up)**:天空面是層壓結構——塑膠六角網格層、被動天線單元、
  外層玻璃纖維蒙皮,層壓在一起;背面是主動電子。SpaceX 用**混合板材**(把昂貴 RF
  疊層與便宜 FR-4 混用)來壓成本。
- **校準**:大量採用**軟體定義校準**補償製程與相位誤差,降低對硬體一致性的要求。

---

## 4. RF 晶片架構(Beamformer / FEM 演進)

拆解社群依 PCB 絲印給了兩個非官方代號:

- **Shiraz(波束成形 ASIC / 數位波束成形器,DBF)**
  - 角色:**扇區控制器**;接收基帶處理器的數位 I/Q 取樣,做上/下變頻到 Ku 頻,
    並把訊號分配給其下一串 Pulsar FEM;晶片內部也做部分相位偏移。
  - 每顆約掌管 **~200 個元素**。
- **Pulsar(前端模組 / FEM)**
  - 角色:貼近天線單元(僅數毫米)的小晶片,內含 **LNA + PA + 額外類比相位偏移器**,
    負責末端放大與細相位微調。
  - 每顆對應 **2–4 個元素**(Gen2 Yole 觀察為每 FEM 約 2 元素、共 508 顆)。
  - 控制方式:**菊鏈(daisy-chain)**,波束指令沿鏈一路傳(晶片1→2→…→N),
    再以**全域 latch 訊號**一次套用所有更新(類似 LED 燈串的單線串控)。

**晶片數量的世代演進(整合化 = 降本主線)**:

| 世代 | 波束成形晶片數 |
|---|---|
| Gen 1(圓盤) | ~80(高度分散,每顆控約 15–20 元素,類比相移 / 向量調變) |
| Gen 2(REV3) | ~16 |
| Gen 3(REV4) | **~6**(新一代 Shiraz,單顆支援更多 RF 通道) |

> 晶片數從 ~80 降到 ~6,連帶減少封裝、焊點、測試點、走線複雜度與組裝工時,
> 使整機 BOM 大幅下降——這是 SpaceX 把相位陣列「商品化」到消費級價位的核心手段。

---

## 5. MCU / SoC 與核心晶片選型

拆解(DARKNAVY、wccftech、TechInsights、Oleg Kutkov、KU Leuven COSIC)揭示:

- **主 SoC(應用處理器)**:**STMicroelectronics 為 SpaceX 客製**的
  **四核 ARM Cortex-A53**,flip-chip BGA 封裝,金屬蓋標記 **"ST GLLCCOCA6BF"**。
  硬體與資料表**保密未公開**。REV3 與 REV4 用同款 SoC。
- **非揮發儲存(eMMC)**:**Micron MTFC4GACAJCN-1M**,4 GB,BGA-153。
- **揮發記憶體**:外掛 DRAM(REV3/REV4 相同)。
- **安全元件(Secure Element)**:**STMicroelectronics STSAFE-A110**,宣稱
  **CC EAL5+**;用途推測為**遠端驗證終端身分**(防偽/防未授權終端接入)。
- **GNSS 接收器**:**STMicroelectronics STA8089**(Teseo 系列);REV4 換了新的
  PCB patch 天線但 GNSS 晶片沿用。
- **RF 前端**:板上大部分面積是 **ST 製造的 RF 前端晶片(FEM)**。
- **供電**:板上有 **PoE(Power over Ethernet)** 電路供整機用電。

**Starlink Mini 的差異(全新架構)**:
- **Catapult SoC**:全新、內建 **secure core**(把安全元件整進 SoC);
- 單顆 **8 Gb RAM**;
- **2 個數位波束成形器**整合;
- GNSS 接收器 + 外接 LNA + patch 天線。

> 重點:SpaceX 幾乎**不用現成 MCU/SoC**,而是與 ST **共同設計客製矽晶**
> (應用處理器、波束成形器、FEM 皆為客製),把「MCU/基帶/波束控制」高度整合,
> 這是它相對於傳統相位陣列(靠大量商用移相器/FPGA)能降本的關鍵。

---

## 6. 系統整合(路由器、纜線、供電、App)

- **兩件式架構(標準)**:天線(UTA)+ 路由器(UTR),中間走**專用纜線**。
  - Gen1:UTA-201 ↔ UTR-201。
  - Gen2:UTA-211/212 ↔ UTR-211。
  - Gen3:天線 ↔ Gen 3 Router(+ 外接電源供應器,經 PoE 供電給天線)。
- **纜線/供電**:專用 PoE 纜線,可傳輸高功率(拆解提到可達 ~100 W 級);
  Gen2 起改**可拆式**纜線(便於維修)。Gen1 為固定纜線。
- **路由器演進**:
  - 初代方形路由器 → Gen2 圓柱形路由器 → **Gen 3 Router**(WiFi 6、
    Tri-Band 4×4 MU-MIMO、2 個帶鎖扣 LAN 埠、IP56、最多 235 台裝置、覆蓋 ~297 m²、
    可組 Mesh)。
  - **Starlink Mini**:路由器**內建於天線本體**(WiFi 5、3×3 MU-MIMO),一體式。
- **管理**:以 **Starlink App** 做開通、**對準引導(對 Gen3/Mini 尤其關鍵,因無馬達)**、
  障礙物檢測、速度/狀態監測與韌體更新。
- **韌體**:KU Leuven COSIC 團隊成功**萃取/dump UT 韌體**;採**安全啟動**鏈,
  由 STSAFE 支援身分驗證。

---

## 7. 機構設計(致動器、外殼、散熱、防護)

- **致動器(Gen1/Gen2)**:底座含**雙軸馬達**(方位 + 俯仰)+ 齒輪箱,由 **H-Bridge**
  驅動,開機自動「找天空」,之後靠電子掃描。**Gen3/Mini 完全取消馬達**(靠 110° 寬
  FoV + App 手動擺放 + 電子掃描),減少機械故障點、降重、降本。
- **外殼/黏合**:
  - Gen1/Gen2 外殼多以**超音波焊接 / 大量膠合**,難無損拆解;
  - **REV4(Gen3)** 改用**汽車級密封膠黏合**,更難拆(拆必破壞)。
  - Mini 高度整合、黏合嚴實 → **可維修性最差**。
- **天線疊構**:玻璃纖維蒙皮 + 六角網格 + 被動單元層壓,兼顧結構、透波與耐候。
- **散熱/融雪**:內建**融雪加熱**(Gen3 最高 40 mm/hr、Mini 25 mm/hr);
  大面積 PCB 兼作散熱面。
- **防護等級**:天線 **IP67**;工作溫度約 **−30 °C ~ +50 °C**;抗風 **96 km/h+**。
- **安裝**:Gen3/Mini 附**腳架 / kickstand**;標準立管 ⌀ 34 mm,支援多種抱杆/牆座。

---

## 8. 供應鏈與製造成本

- **ST × SpaceX 十年合作**(2025-12 官方公布):
  - 共同設計 UT 與衛星用的**客製半導體**;
  - 產出**數十億顆元件**,供應**數百萬台終端**與 **10,000+ 顆衛星**
    (含提供 >1 Tbps fronthaul 的 V3 衛星);
  - 採 **ST 的 BiCMOS 製程 + 新的 panel-level packaging(面板級封裝)**;
  - 產能規模達 **每天 >500 萬顆晶片**,支撐 Starlink **每天生產 >2 萬台終端**;
  - 製造分佈於 ST 的**法國、馬爾他、馬來西亞**廠;服務 150+ 國、800 萬+ 用戶。
- **成本分析(Yole / 第三方)**:對 Gen 2 系統做逐級拆解 + die/EDX/剖面/方塊圖/成本分析,
  辨識出 DSP、DRAM、GPS、FEM(508 顆)、DBF 等主要元件;**整機製造成本估 ~US$400**
  (SpaceX 長期以低於成本或貼近成本補貼硬體以擴大用戶)。
- **降本三支柱**:①**積極矽整合**(波束成形晶片 ~80→~6)、②**混合板材**
  (RF 疊層 + FR-4)、③**軟體定義校準**。

---

## 9. 專利

SpaceX(Space Exploration Technologies Corp.)在相位陣列/波束成形上的代表性專利:

- **US20190253125A1 — "Beamformer Lattice for Phased Array Antennas"**(2019-02-14 申請)
  - 核心:多層結構——第一層放**波束成形 cell 陣列**(每個 cell 有多輸入/輸出與
    input/output vias)、第二層是**多工饋電網路(multiplex feed / H-network)**、
    第三層是**天線單元**;透過 via 連接輸入端至饋電網路、輸出端至天線單元。
  - 系統含:天線 lattice、mapping system、beamformer lattice、multiplex feed network、
    combiner/distributor、modulator/demodulator。
  - 有 **22 個 INPADOC 同族專利**,涵蓋波束成形、self-multiplexing、訊號路由。
- **US20190252801A1 — "Antenna Aperture in Phased Array Antenna Systems"**
  - 第一部分載**空間漸縮(space-tapered)排列**的天線 lattice,第二部分載
    beamformer lattice。
- 相關領域另有:**Partitioned phased array fed reflector antenna system**
  (US 9,806,433 / US 10,193,240,分割式相位陣列饋源反射面)等。
- **策略**:專注在**新穎實作**(陣列結構、訊號路由、波束成形/定向),對應「同時追蹤
  星座衛星與地面單元」的工程挑戰,並訴求**能效、頻寬、輕量、製造簡化**的升級。
- 另有第三方申請(如 justia US20240405420「MECHANISM TYPE ANTENNA FOR TRACKING
  STARLINK SATELLITE」),屬追星機構類,非 SpaceX 本體。

> 提醒:完整專利族龐大且持續更新,上列為代表性項目;精確權利範圍請以 USPTO/
> Google Patents 原文為準。

---

## 10. 安全研究

- **KU Leuven / COSIC(Lennert Wouters,DEF CON 30, 2022)**:
  - 「Black Box Security Evaluation of SpaceX Starlink」;
  - 用**電壓毛刺(voltage glitching / fault injection)**繞過安全啟動,
    dump 並萃取 UT 韌體,取得 root/研究存取;
  - 促使 SpaceX 建立**負責任揭露計畫**。
- **STSAFE-A110**:硬體信任根,做終端遠端身分驗證(CC EAL5+)。
- **可維修性/改裝社群**:Oleg Kutkov 等人做電源架構分析、專用接頭替換、
  讓 Mini 脫離內建路由器運作等改裝研究。

---

## 11. 資料來源

**世代/規格總覽**
- Starlink Tips — Gen1/2/3 硬體比較:https://starlink-tips.com/guides/starlink-hardware-comparison-understanding-gen-1-gen-2-and-gen-3-differences
- Powertec — Standard Actuated Dish, Gen 2 (REV3) Datasheet:https://manuals.plus/m/6bf1ffb5a48382cb63046ede193339edaa49bd9132430b700e9aa1913809269f
- Outcamp — Mini vs Gen2 vs Gen3 vs HP:https://outcamp.com.au/blogs/starlink-education-guide/starlink-mini-vs-gen-2-vs-gen-3-vs-high-performance-a-which-dish-is-right-for-you
- 官方 Mini 規格書:https://starlink.com/public-files/specification_sheet_mini.pdf
- 官方 Flat High Performance 規格書:https://api.starlink.com/public-files/specification_sheet_flat_high_performance.pdf
- 官方 Gen 3 Router 規格書:https://starlink.com/public-files/Gen3RouterSpecificationsStandard.pdf

**拆解**
- iFixit — Starlink Round Dish Teardown:https://www.ifixit.com/Teardown/Starlink+Round+Dish+Teardown/148806
- iFixit — Starlink Rectangle Dish Teardown:https://www.ifixit.com/Teardown/Starlink+Rectangle+Dish+Teardown/149892
- Hackaday — Literally Tearing Apart A SpaceX Starlink Antenna:https://hackaday.com/2020/11/25/literally-tearing-apart-a-spacex-starlink-antenna/
- Teslarati — Dishy McFlatface teardown:https://www.teslarati.com/starlink-dishy-mcflatface-teardown-video/
- Dan Murray — Dishy V3 Teardown:https://danmurray.net/2022/03/19/dishy-v3-teardown/
- Oleg Kutkov — Terminal Revision 4 overview:https://olegkutkov.me/2024/02/12/starlink-terminal-revision-4-overview-and-tests/
- Oleg Kutkov — REV1/REV2 (Gen1) teardown(StarMesh Forum):https://olegkutkov.me/forum/index.php?topic=11.0
- Oleg Kutkov — Mini teardown(X/Twitter):https://x.com/olegkutkov/status/1817929594902585421
- Oleg Kutkov — Rev3 (V2) power architecture:https://olegkutkov.me/2024/12/31/starlink-rev-3-v2-power-architecture/

**RF / 天線 / 晶片架構**
- Abhishek Goyal — Inside the Starlink Dish(RF deep dive):https://abgoyal.com/posts/starlink-dish-rf-deep-dive/
- DARKNAVY — A First Glimpse of the Starlink User Terminal:https://www.darknavy.org/blog/a_first_glimpse_of_the_starlink_user_ternimal/
- wccftech — Starlink UT uses same supplier as Apple(ST):https://wccftech.com/starlink-user-terminal-apple-supplier-teardown/
- TechInsights — Deep Dive Teardown UTA-212/UTR-211:https://www.techinsights.com/products/ddt-2206-815
- Yole — Technical & cost analysis of Starlink Gen 2 Chipset:https://www.yolegroup.com/product/report/starlink-gen-2-chipset/
- PatSnap Eureka — Starlink UT Phased Array Antenna Technology:https://eureka.patsnap.com/article/starlink-user-terminals-phased-array-antenna-technology

**MCU / SoC / 韌體 / 安全**
- KU Leuven COSIC — Dumping and extracting the Starlink UT firmware:https://www.esat.kuleuven.be/cosic/blog/dumping-and-extracting-the-spacex-starlink-user-terminal-firmware/
- DEF CON 30 — Lennert Wouters, Black Box Security Evaluation of SpaceX Starlink(影片/講稿)

**供應鏈**
- ST Newsroom — ST & SpaceX 十年合作:https://newsroom.st.com/media-center/press-item.html/t4741.html
- iotinsider — ST & SpaceX decade-long partnership:https://www.iotinsider.com/industries/communications/stmicroelectronics-and-spacex-mark-decade-long-partnership-behind-starlinks-global-rise/

**專利**
- Google Patents — US20190253125A1 Beamformer Lattice for Phased Array Antennas:https://patents.google.com/patent/US20190253125A1/en
- Google Patents — US20190252801A1 Antenna Aperture in Phased Array Antenna Systems:https://patents.google.com/patent/US20190252801A1/en
- MaxVal — Featured Technologies: Starlink Constellation:https://www.maxval.com/blog/featured-technologies-starlink-constellation/
- Teslarati — SpaceX custom-built Starlink antenna patent:https://www.teslarati.com/spacex-custom-built-starlink-satellite-antenna-patent-grant/

---

## 12. 拆解影片清單

| 主題 / 世代 | 作者 | 內容重點 | 連結 |
|---|---|---|---|
| **Gen1 圓盤破壞式拆解**(經典) | Kenneth Keiter | 55 分鐘完整拆解 + 相位陣列與機構/電子逐段解說,iFixit 亦引用 | https://youtu.be/iOmdQnIlnRo |
| **相位陣列 RF 深度分析** | The Signal Path(TSP #181/#183) | 相位陣列架構、RF 訊號鏈、X 光透視分析 | https://www.youtube.com/watch?v=h6MfM8EFkGg |
| **Gen1 圖文拆解** | iFixit | SoC/波束成形/FEM/馬達/膠合、可維修性評分 | https://www.ifixit.com/Teardown/Starlink+Round+Dish+Teardown/148806 |
| **Gen2 矩形圖文拆解** | iFixit | 矩形版更薄更輕的內部結構 | https://www.ifixit.com/Teardown/Starlink+Rectangle+Dish+Teardown/149892 |
| **Gen2/矩形詳細拆解** | YouTube(RECTANGLE Teardown Details) | 內部高清照片、修剪成低功耗面板 | https://www.youtube.com/watch?v=AlvIWF0AXI0 |
| **非破壞式拆解** | YouTube(Non Destructive Way) | 不切割拆開 Dishy 的方法 | https://www.youtube.com/watch?v=iqzim4wR7eE |
| **Gen3 拆解系列 ep.03** | YouTube | REV4/Gen3 逐集拆解 | https://www.youtube.com/watch?v=samgbxEcXiQ |
| **底座拆解** | YouTube(Disassemble Base) | 致動器/底座機構 | https://www.youtube.com/watch?v=ahIQXHqK3AA |
| **Starlink Mini 拆解速覽** | Oleg Kutkov(X) | Catapult SoC、8 Gb RAM、2 數位波束成形器、GNSS;最低可維修性 | https://x.com/olegkutkov/status/1817929594902585421 |
| **REV4 拆解與測試(圖文)** | Oleg Kutkov | SoC/RAM/eMMC 同 REV3、6 顆新 Shiraz、新 patch 天線 | https://olegkutkov.me/2024/02/12/starlink-terminal-revision-4-overview-and-tests/ |
| **Dishy V3 拆解(圖文)** | Dan Murray | 與 Lennert Wouters 合作做 eMMC dump | https://danmurray.net/2022/03/19/dishy-v3-teardown/ |
| **安全評估拆解(DEF CON 30)** | Lennert Wouters (KU Leuven) | 「Glitched on Earth by Humans」電壓毛刺 + $25 modchip 破解、韌體 dump | https://forum.defcon.org/node/241928 |

> 提示:文字類拆解(iFixit / Oleg Kutkov / Dan Murray)含大量高清內部照片與晶片標記,
> 是核對晶片型號最好的一手來源;影片類(Keiter / TSP)適合理解機構與 RF 鏈路全貌。

---

## 13. 專利清單(SpaceX / Space Exploration Technologies Corp.)

> 背景:SpaceX 自 **2016 年**起針對 Starlink 天線佈局專利。截至 2020-09-24,已有
> **28 件公開**(3 件美國核發、9 件美國待審、9 件 PCT、7 件台灣申請)。以下為與
> **使用者終端相位陣列**最相關的代表項目。

**核心專利族:相位陣列 / 波束成形**

| 專利號 | 類型 | 標題 | 重點 |
|---|---|---|---|
| **US2019/0253125 A1** | 申請 | Beamformer Lattice for Phased Array Antennas | 多層結構:beamformer cell 陣列(第一層)+ 多工饋電網路 H-network(第二層)+ 天線單元(第三層);22 個 INPADOC 同族,涵蓋波束成形、self-multiplexing、訊號路由 |
| **US 11,146,323 B2** | 核發 | Beamformer Lattice for Phased Array Antennas | 上案之核發專利 |
| **US 11,606,134 B2** | 核發 | Beamformer Lattice for Phased Array Antennas | 同族後續核發 |
| **US2019/0252801 A1** | 申請 | Antenna Aperture in Phased Array Antenna Systems | 天線 lattice 採**空間漸縮(space-tapered)**排列 + beamformer lattice |
| **US 11,695,222 B2** | 核發 | Antenna Aperture in Phased Array Antenna Systems | 上案之核發專利 |
| **US2019/0252796 A1** | 申請 | Antenna Modules for Phased Array Antennas | 相位陣列的天線模組化設計 |
| **WO2017/123677 A1** | PCT | Methods and Apparatus for Manufacture and In-Space Assembly of Antennas | 天線製造與太空組裝方法 |

**主張的技術優勢**:能效、頻寬、輕量化、**製造簡化**;對應「同時追蹤星座衛星與地面
單元」的工程挑戰(陣列結構、訊號路由、波束成形/定向)。

**相關但非 SpaceX 本體**
- **US2024/0405420 A1**(Justia)— "Mechanism Type Antenna for Tracking Starlink Satellite":
  第三方的**追星機構**申請,非 SpaceX。

**查詢原文入口**
- Google Patents(可看全文/圖式/同族/引用):
  - https://patents.google.com/patent/US20190253125A1/en
  - https://patents.google.com/patent/US20190252801A1/en
  - https://patents.google.com/patent/US20190252796A1/en
- USPTO 全文 PDF:
  - US 11,146,323:https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11146323
  - US 11,606,134:https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11606134
  - US 11,695,222:https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11695222
- 專利組合概覽:
  - MaxVal — Featured Technologies: Starlink Constellation:https://www.maxval.com/blog/featured-technologies-starlink-constellation/
  - GreyB — SpaceX Patents Insights & Stats:https://insights.greyb.com/spacex-patent/
  - PatentPC — Role of Patents in SpaceX's Satellite Network:https://patentpc.com/blog/the-role-of-patents-in-spacexs-satellite-network-technology-success
  - Justia Patents(依 assignee 搜尋 "Space Exploration Technologies")

> 提醒:專利族持續更新,且「申請公開號」與「核發號」需分辨;精確權利範圍與最新
> 法律狀態,請以 Google Patents / USPTO / 各國專利局原文為準。

---

*本文件為公開資料彙整,含第三方拆解之推定值;精確規格請以 SpaceX 官方與原始拆解/專利文件為準。*
