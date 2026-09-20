# VESC Tool 中文版

这是 **VESC Tool** 的中文版源码仓库。VESC Tool 是一套功能强大的 **VESC（Vedder Electronic Speed Controller）电机控制器配置与调试工具**，由 Benjamin Vedder 开发并维护。

VESC 是目前世界上最流行的开源无刷直流电机（BLDC）控制器之一，广泛应用于：

- 🛹 电动滑板 / 电动长板
- 🚲 电动自行车 / 电动山地车
- 🤖 机器人 / 伺服系统
- 🚁 无人机 / 多旋翼
- ⚡ 各类电动交通工具与自动化设备

VESC Tool 是连接 VESC 硬件与控制器的桥梁，提供图形化界面让你轻松完成参数配置、实时监控和固件管理。

**本中文版**包含完整的中文本地化文件（`vesc_tool_zh_CN.ts`），界面、菜单、参数说明等均已汉化，极大降低了国内用户的使用门槛。

---

## 目录

- [版本信息](#版本信息)
- [功能概览](#功能概览)
- [多平台支持](#多平台支持)
- [开源协议](#开源协议)
- [项目结构](#项目结构)
  - [核心模块](#核心模块)
  - [页面模块（Pages）](#页面模块pages)
  - [控件模块（Widgets）](#控件模块widgets)
  - [移动端模块（Mobile UI）](#移动端模块mobile-ui)
  - [第三方库](#第三方库)
- [开发指南](#开发指南)
- [命令行参数](#命令行参数)
- [命令行使用示例](#命令行使用示例)
- [添加自定义硬件](#添加自定义硬件)
- [相关链接](#相关链接)

---

## 版本信息

| 字段             | 值          |
|------------------|-------------|
| 当前版本         | **7.01**    |
| 介绍版本         | 1           |
| 配置版本         | 4           |
| 是否为测试版     | 是（1）     |
| Android ARMv7    | 221         |
| Android ARM64    | 222         |
| Android x86      | 223         |

## 功能概览

VESC Tool 提供了以下核心功能：

### 🔌 多协议连接
- **USB 串口**：通过 USB 线直接连接 VESC 控制器
- **蓝牙（BLE）**：无线连接，方便移动设备和远程调试
- **CAN 总线**：支持多设备链式连接与 CAN 转发
- **TCP 服务器/集线器**：支持网络远程访问与控制
- **UDP**：轻量级网络通信

### 📊 实时数据监控
- 电压、电流、功率实时显示
- 转速（ERPM）、温度监控
- 实时数据图表绘制（基于 QCustomPlot 的富交互式图表）
- 姿态数据（IMU）实时 3D 可视化
- 采样数据记录与分析
- 日志分析与回放

### ⚙️ 参数配置
- **电机参数配置**：PID 控制参数、电流限制、电压限制、转速限制
- **应用参数配置**：PPM / ADC / Nunchuk / PAS / UART 等输入源设置
- **FOC（磁场定向控制）参数**：FOC 检测向导、编码器/霍尔传感器配置
- **BLDC（六步换向）参数**：BLDC 检测向导
- **电池管理系统（BMS）**：电池参数与保护设置
- **自定义配置**：支持自定义 XML 配置

### 🔧 固件管理
- 固件上传与升级（支持所有官方硬件）
- 内置 Bootloader 上传
- ESP32 固件编程
- SWD 编程器支持
- **VESC 包**：将固件、LispBM、QML 打包分发
- 固件打包与解包工具

### 💻 编程与脚本
- **LispBM** 脚本编辑器（含语法高亮和代码补全）
- 脚本上传、擦除、打包
- 终端模式：直接与 VESC 进行指令交互
- 调试输出查看器

### 🧪 实验与高级功能
- 电机对比分析
- 实验模式（自定义实验曲线）
- 电机检测向导（电阻、电感、磁链自动测量）
- 设置计算器（电池计算器等）
- **Display Tool**：VESC 显示屏编辑器

### 🗺️ GPS 与地图
- GPS 轨迹记录与地图显示（OSM 瓦片地图）
- 车辆信息/无人机信息展示
- 定位点管理与路径回放

---

## 多平台支持

| 平台       | 稳定版 | 开发版（每几天更新一次） | 备注                                  |
|------------|:------:|:------------------------:|---------------------------------------|
| Linux      |   ✓    |            ✓             | 支持 x86 和 ARM（树莓派等）           |
| Windows    |   ✓    |            ✓             | MSVC 或 MinGW 编译                    |
| macOS      |   ✓    |            -             | Homebrew 安装 Qt                      |
| Android    |   ✓    |            ✓             | 支持 ARMv7 / ARM64 / x86              |
| iOS        |   ✓*   |            -             | \*仅通过 Apple App Store 分发         |

> **所有平台的二进制文件均可在 [http://vesc-project.com/](http://vesc-project.com/) 免费下载**（iOS 除外）。

---

## 开源协议

VESC Tool 基于 **GNU General Public License v3.0（GPLv3）** 发布。核心条款：

- ✅ 自由使用、修改和分发
- ✅ 可商用，但衍生作品必须同样以 GPLv3 开源
- ⚠️ 不提供任何担保
- ⚠️ "VESC" 是 Benjamin Vedder 的注册商标，使用需遵循商标政策

完整协议文本见 [LICENSE](LICENSE) 文件。

---

## 项目结构

### 核心模块

| 文件/模块              | 说明                                                         |
|------------------------|--------------------------------------------------------------|
| `main.cpp`             | 程序入口，命令行参数解析，主题/字体/DPI 初始化               |
| `mainwindow.cpp/h/ui`  | 主窗口框架，页面切换，菜单栏，工具栏                         |
| `boardsetupwindow.*`   | 开发板设置向导窗口                                           |
| `vescinterface.cpp/h`  | VESC 通信核心接口，封装所有与 VESC 的命令交互                |
| `commands.cpp/h`       | VESC 命令定义，发送/接收协议实现                             |
| `packet.cpp/h`         | 数据包编解码，CRC 校验                                       |
| `configparams.cpp/h`   | 配置参数统一管理，XML 导入导出                               |
| `configparam.cpp/h`    | 单个配置参数的封装                                           |
| `datatypes.h`          | 全局数据类型定义                                             |
| `utility.cpp/h`        | 通用工具函数（颜色管理、单位转换、文件操作等）               |
| `codeloader.cpp/h`     | 代码加载器（LispBM 等）                                      |
| `hexfile.cpp/h`        | Intel HEX 文件解析与生成                                     |
| `digitalfiltering.*`   | 数字滤波器实现                                               |
| `tcpserversimple.*`    | 简易 TCP 服务器                                              |
| `tcphub.cpp/h`         | TCP Hub：多客户端共享 VESC 连接                              |
| `udpserversimple.*`    | 简易 UDP 服务器                                              |
| `vbytearray.cpp/h`     | 字节数组扩展工具                                             |
| `preferences.cpp/h`    | 用户偏好设置管理                                             |
| `bleuart.cpp/h`        | 蓝牙 BLE UART 通信（真实现）                                 |
| `bleuartdummy.cpp/h`   | 蓝牙 BLE UART 通信（空实现/兜底）                            |
| `setupwizardapp.*`     | 应用设置向导                                                 |
| `setupwizardmotor.*`   | 电机设置向导                                                 |
| `startupwizard.cpp/h`  | 首次启动向导                                                 |
| `parametereditor.*`    | 参数编辑器                                                   |

### 页面模块（Pages）

VESC Tool 的桌面版采用分页式界面，以下为所有功能页面：

| 页面文件                           | 功能说明                     |
|------------------------------------|------------------------------|
| `pagewelcome.*`                    | 欢迎首页                     |
| `pageconnection.*`                 | 连接管理页面                 |
| `pagertdata.*`                     | 实时数据监控（图表）         |
| `pagesampleddata.*`                | 采样数据查看                 |
| `pagemotorsettings.*`              | 电机参数设置                 |
| `pagemotor.*`                      | 电机通用设置                 |
| `pagemotorinfo.*`                  | 电机信息与检测               |
| `pagemotorcomparison.*`            | 电机对比分析                 |
| `pagefoc.*`                        | FOC 参数配置                 |
| `pagebldc.*`                       | BLDC 参数配置                |
| `pagedc.*`                         | 直流电机参数配置             |
| `pagegpd.*`                        | GPD 参数（通用位置检测）     |
| `pageappgeneral.*`                 | 应用通用设置                 |
| `pageappppm.*`                     | PPM 输入配置                 |
| `pageappadc.*`                     | ADC 输入配置                 |
| `pageappnunchuk.*`                 | Nunchuk（Wii 手柄）配置      |
| `pageapppas.*`                     | PAS（脚踏助力传感器）配置    |
| `pageappnrf.*`                     | NRF 无线配置                 |
| `pageappuart.*`                    | UART 通信配置                |
| `pageappimu.*`                     | IMU 惯性测量单元配置         |
| `pageappsettings.*`                | 应用设置                     |
| `pagebms.*`                        | 电池管理系统配置             |
| `pageimu.*`                        | IMU 数据可视化（3D）         |
| `pagecontrollers.*`                | 控制器列表管理               |
| `pagefirmware.*`                   | 固件上传与升级               |
| `pageespprog.*`                    | ESP32 编程                   |
| `pageswdprog.*`                    | SWD 编程器                   |
| `pagevescpackage.*`                | VESC 包管理                  |
| `pagescripting.*`                  | LispBM 脚本编辑与上传        |
| `pagelisp.*`                       | LispBM 集成环境              |
| `pageterminal.*`                   | 指令终端                     |
| `pagedebugprint.*`                 | 调试输出查看器               |
| `pagedataanalysis.*`               | 数据分析                     |
| `pageloganalysis.*`                | 日志分析                     |
| `pagecananalyzer.*`                | CAN 总线分析器               |
| `pageexperiments.*`                | 实验模式                     |
| `pagesetupcalculators.*`           | 设置计算器                   |
| `pagedisplaytool.*`                | 显示屏编辑工具               |
| `pagecustomconfig.*`               | 自定义配置                   |

### 控件模块（Widgets）

以下为 VESC Tool 中使用的重要自定义控件：

| 控件文件                 | 说明                                 |
|--------------------------|--------------------------------------|
| `paramtable.*`           | 参数表格显示控件                     |
| `paramdialog.*`          | 参数编辑对话框                       |
| `parameditint.*`         | 整数参数编辑器                       |
| `parameditdouble.*`      | 浮点数参数编辑器                     |
| `parameditbool.*`        | 布尔参数编辑器                       |
| `parameditenum.*`        | 枚举参数编辑器                       |
| `parameditstring.*`      | 字符串参数编辑器                     |
| `parameditbitfield.*`    | 位域参数编辑器                       |
| `scripteditor.*`         | LispBM 脚本编辑器（语法高亮、补全）  |
| `rtdatatext.*`           | 实时数据文本显示                     |
| `qcustomplot.cpp/h`      | QCustomPlot 图表库（功能强大的绘库） |
| `experimentplot.*`       | 实验曲线绘制控件                     |
| `detectfoc.*`            | FOC 检测对话框                       |
| `detectfochall.*`        | FOC 霍尔传感器检测                   |
| `detectfocencoder.*`     | FOC 编码器检测                       |
| `detectbldc.*`           | BLDC 检测对话框                      |
| `detectallfocdialog.*`   | 全自动 FOC 检测                      |
| `dirsetup.*`             | 电机方向设置控件                     |
| `ppmmap.*`               | PPM 映射可视化控件                   |
| `adcmap.*`               | ADC 映射可视化控件                   |
| `canlistitem.*`          | CAN 设备列表项                       |
| `pagelistitem.*`         | 页面列表项控件                       |
| `nrfpair.*`              | NRF 配对对话框                       |
| `vesc3dview.*`           | VESC 3D 姿态可视化                   |
| `batterycalculator.*`    | 电池计算器                           |
| `batttempplot.*`         | 电池温度图表                         |
| `helpdialog.*`           | 帮助对话框                           |
| `displaybar.*`           | 显示进度条                           |
| `displaypercentage.*`    | 显示百分比                           |
| `superslider.*`          | 增强滑块控件                         |
| `imagewidget.*`          | 图像显示控件（仪表盘等）             |
| `aspectimglabel.*`       | 等比例缩放图像标签                   |
| `mrichtextedit.*`        | Markdown 富文本编辑器                |
| `mtextedit.*`            | 增强文本编辑器                       |
| `vtextbrowser.*`         | 增强文本浏览器                       |
| `historylineedit.*`      | 带历史记录的输入框                   |

### 移动端模块（Mobile UI）

移动版采用 **Qt Quick / QML** 技术构建，提供与桌面版功能对等的触控优化界面：

| QML 文件                | 对应功能                       |
|-------------------------|--------------------------------|
| `main.qml`              | 移动端主界面框架               |
| `StartPage.qml`         | 启动首页                       |
| `ConnectScreen.qml`     | 连接管理界面                   |
| `RtData.qml`            | 实时数据仪表盘                 |
| `RtDataIMU.qml`         | IMU 实时数据                   |
| `RtDataSetup.qml`       | 实时数据配置                   |
| `ConfigPageMotor.qml`   | 电机参数配置                   |
| `ConfigPageApp.qml`     | 应用参数配置                   |
| `ConfigPageCustom.qml`  | 自定义配置                     |
| `Controls.qml`          | 控制器/输入控制                |
| `FwUpdate.qml`          | 固件更新                       |
| `Lisp.qml`              | LispBM 脚本                    |
| `Terminal.qml`          | 指令终端                       |
| `Packages.qml`          | VESC 包管理                    |
| `CanScreen.qml`         | CAN 总线                       |
| `BMS.qml`               | 电池管理                       |
| `Settings.qml`          | 软件设置                       |
| `DetectFocParam.qml`    | FOC 参数检测                   |
| `DetectFocEncoder.qml`  | FOC 编码器检测                 |
| `DetectFocHall.qml`     | FOC 霍尔传感器检测             |
| `DetectBldc.qml`        | BLDC 检测                      |
| `DirectionSetup.qml`    | 电机方向设置                   |
| `SetupWizardFoc.qml`    | FOC 设置向导                   |
| `SetupWizardIMU.qml`    | IMU 设置向导                   |
| `SetupWizardInput.qml`  | 输入设置向导                   |
| `SetupWizardIntro.qml`  | 设置向导引导页                 |
| `ParamList.qml`         | 参数列表                       |
| `ParamEditors.qml`      | 参数编辑器集合                 |
| `StatPage.qml`          | 统计页面                       |
| `LogBox.qml`            | 日志显示                       |
| `TcpBox.qml`            | TCP 连接                       |
| `TcpHubBox.qml`         | TCP Hub                       |
| `CustomGauge.qml`       | 自定义仪表盘                   |
| `CustomGaugeV2.qml`     | 自定义仪表盘 V2                |
| `Vesc3DView.qml`        | VESC 3D 视图                   |
| `PpmMap.qml`            | PPM 映射                       |
| `AdcMap.qml`            | ADC 映射                       |
| `MultiSettings.qml`     | 多重设置                       |
| `Profiles.qml`          | 配置档案管理                   |
| `ProfileEditor.qml`     | 配置档案编辑器                 |
| `ProfileDisplay.qml`    | 配置档案显示                   |
| `FilePicker.qml`        | 文件选择器                     |
| `DirectoryPicker.qml`   | 目录选择器                     |
| `PairingDialog.qml`     | 蓝牙配对对话框                 |
| `BleSetupDialog.qml`    | BLE 设置对话框                 |
| `NrfPair.qml`           | NRF 配对                       |
| `ImageButton.qml`       | 图像按钮                       |
| `DoubleSpinBox.qml`     | 双精度微调框                   |

> 移动端 C++ 辅助模块：`qmlui.cpp/h`（QML UI 框架）、`fwhelper.cpp/h`（固件助手）、`logwriter.cpp/h`（日志写入）、`logreader.cpp/h`（日志读取）、`vesc3ditem.cpp/h`（3D 渲染项）。

### 第三方库

| 目录          | 库名称          | 说明                                   | 协议  |
|---------------|------------------|----------------------------------------|-------|
| `QCodeEditor/` | QCodeEditor      | Qt 代码编辑器（LispBM/C/Python/Lua 等）| MIT   |
| `esp32/`      | esp32flash       | ESP32 固件刷写工具                     | Apache-2.0 |
| `heatshrink/` | heatshrink       | 嵌入式数据压缩库                       | ISC   |
| `lzokay/`     | lzokay           | LZO 无损压缩算法 C++11 实现            | MIT   |
| `maddy/`      | maddy            | C++ Markdown 解析器                    | MIT   |
| `minimp3/`    | minimp3          | 极简 MP3 解码器                        | CC0   |
| `map/`        | 地图组件         | OSM 瓦片地图渲染组件                   | -     |
| `display_tool/` | 显示编辑器    | VESC 显示屏内容编辑器                   | -     |
| `qmarkdowntextedit/` | QMarkdownTextEdit | Markdown 文本编辑器               | -     |

---

## 开发指南

> **注意：** 以下构建说明默认不包含内置固件包（`exclude_fw`）。如需包含固件，请移除该配置选项并确保已下载匹配的固件文件。

### 环境依赖总览

项目基于 **Qt 5** 和 C++11 构建。主要依赖的 Qt 模块有：
core gui widgets network quick quickcontrols2 quickwidgets svg gui-private 
serialport bluetooth positioning gamepad printsupport androidextras
以及 QML 扩展：
qml-module-qt-labs-folderlistmodel qml-module-qtquick-extras qml-module-qtquick-controls2 qml-module-qt3d qml-module-qt-labs-settings qml-module-qt-labs-platform qt3d5-dev qtdeclarative5-dev


### Linux 构建

#### Ubuntu 18.04 / Debian / Raspbian Buster

```bash
 sudo apt install qml-module-qt-labs-folderlistmodel
qml-module-qtquick-extras qml-module-qtquick-controls2
qt5-default libqt5quickcontrols2-5 qtquickcontrols2-5-dev
qtcreator qtcreator-doc libqt5serialport5-dev build-essential
qml-module-qt3d qt3d5-dev qtdeclarative5-dev qtconnectivity5-dev
qtmultimedia5-dev qtpositioning5-dev libqt5gamepad5-dev
qml-module-qt-labs-settings qml-module-qt-labs-platform
libqt5svg5-dev
```
```bash
构建
qmake -config release "CONFIG += release_lin build_original exclude_fw" make -j$(nproc)

运行
./build/lin/vesc_tool_7.01
```

> 注：`make -j$(nproc)` 会自动使用所有 CPU 核心并行编译。

### Nix 构建（推荐）

如果你使用 Nix，构建将变得极其简单：

```bash 
nix run .

进入开发 Shell（安装所有依赖）
nix develop

在 Nix 环境中启动 Qt Creator
nix develop nix run nixpkgs#qtcreator
```

> ⚠️ 当前 Nix Flake 仅支持 x86 Linux 平台。

### Windows 构建

推荐使用 **MSYS2** 配合 MinGW-w64：
```bash
MSYS2 中安装依赖
pacman -S mingw-w64-x86_64-qt5 mingw-w64-x86_64-gcc mingw-w64-x86_64-make

构建
qmake -config release "CONFIG += release_win exclude_fw" mingw32-make -j8

```




也可以使用 **Visual Studio**（MSVC）：

```bash
qmake -config release "CONFIG += release_win exclude_fw" nmake

```




### macOS 构建

```bash
安装 Qt
brew install qt

构建
qmake -config release "CONFIG += release_macos exclude_fw" make -j8
```
生成的 .app 位于 build/macos/





### Android 构建

需要安装 **Android NDK** 和 **Qt for Android**：

```bash
使用 Qt for Android 的 qmake
/path/to/android-qt/bin/qmake -config release
"CONFIG += release_android exclude_fw" make -j8
```
生成的 APK 位于 build/android/

架构可选配置：
- `ANDROID_TARGET_ARCH=armeabi-v7a` （ARMv7，版本号 221）
- `ANDROID_TARGET_ARCH=arm64-v8a`   （ARM64，版本号 222）
- `ANDROID_TARGET_ARCH=x86`         （x86，版本号 223）

### iOS 构建

iOS 构建需要 macOS + Xcode + Qt for iOS：

```bash
使用 Qt for iOS 的 qmake
/path/to/ios-qt/bin/qmake -config release "CONFIG += release_ios exclude_fw build_mobile" make -j8
```
---

## 命令行参数

VESC Tool 支持强大的命令行模式，可以在无 GUI 环境下完成自动化操作：

### 基础参数

| 参数 | 说明 |
|------|------|
| `-h`, `--help` | 显示帮助信息 |
| `--about` | 显示关于信息 |
| `--version` | 显示版本信息（单行） |

### 网络与连接

| 参数 | 说明 |
|------|------|
| `--tcpServer [port]` | 连接 VESC 并启动 TCP 服务器（指定端口） |
| `--tcpHub [port]` | 启动 TCP Hub 用于远程多客户端访问 |
| `--vescPort [port]` | 指定 VESC 端口（如 `/dev/ttyACM0`、`COM3`），不指定则自动搜索 |
| `--canFwd [canId]` | CAN 总线转发 ID |
| `--retryConn` | 连接失败时持续重试 |
| `--bridgeAppData` | 将应用数据（如 LispBM send-data）输出到 stdout |

### QML 界面

| 参数 | 说明 |
|------|------|
| `--loadQml [file]` | 从指定文件加载 QML UI（替代默认桌面 UI） |
| `--loadQmlVesc` | 从已连接的 VESC 加载 QML UI |
| `--qmlAutoConn` | 加载 QML 前通过 USB 自动连接 |
| `--qmlFullscreen` | QML 全屏模式 |
| `--qmlOtherScreen` | 在副屏上显示 QML UI |
| `--qmlRotation [deg]` | 旋转屏幕指定角度（如 90, 180, 270） |
| `--qmlWindowSize [width:height]` | 指定 QML 窗口大小 |
| `--useMobileUi` | 使用移动端 UI（替代桌面 UI） |

### 配置读写

| 参数 | 说明 |
|------|------|
| `--getMcConf [path]` | 读取电机配置并保存为 XML 文件 |
| `--setMcConf [path]` | 从 XML 文件写入电机配置 |
| `--getAppConf [path]` | 读取应用配置并保存为 XML 文件 |
| `--setAppConf [path]` | 从 XML 文件写入应用配置 |
| `--getCustomConf [path]` | 读取自定义配置 1 并保存为 XML |
| `--setCustomConf [path]` | 从 XML 文件写入自定义配置 1 |

### 固件与脚本

| 参数 | 说明 |
|------|------|
| `--uploadFirmware [path]` | 上传固件文件 |
| `--uploadBootloaderBuiltin` | 上传内置通用 Bootloader |
| `--uploadLisp [path]` | 上传 LispBM 脚本 |
| `--reduceLisp` | 压缩 LispBM 文件（移除注释、空格、导入） |
| `--eraseLisp` | 擦除 LispBM 脚本 |
| `--packFirmware [in:out]` | 打包固件以兼容 Bootloader |
| `--packLisp [in:out]` | 打包 LispBM 文件及其导入 |

### VESC 包

| 参数 | 说明 |
|------|------|
| `--buildPkg [pkgPath:lispPath:qmlPath:isFullscreen:optMd:optName]` | 构建 VESC 包 |
| `--buildPkgFromDesc [qmlDesc]` | 从 QML 描述文件构建 VESC 包 |
| `--testPkgDesc [hwtype:hwname:optfwname]` | 测试包描述的 `isCompatible` 方法 |

### 其他

| 参数 | 说明 |
|------|------|
| `--useBoardSetupWindow` | 直接启动开发板设置窗口 |
| `--xmlConfToCode [xml-file]` | 从 XML 配置文件生成 C 代码 |
| `--debugOutFile [path]` | 将调试输出写入指定文件 |
| `--queryDeviceFwParams` | 查询并打印设备固件参数 |
| `--writeFileToSdCard [local:remote]` | 将本地文件写入 VESC SD 卡 |
| `--offscreen` | 使用离屏 QPA（CLI 模式不需要 X 服务器） |
| `--downloadPackageArchive` | 下载包存档到应用数据目录 |

---

## 命令行使用示例

以下为常见无头（Headless）操作示例，适合自动化与脚本集成：

```bash
=== 读取配置 ===
读取电机配置（无需 GUI，通过 USB 自动连接）
./vesc_tool_7.01 --offscreen --vescPort /dev/ttyACM0 --getMcConf motor_config.xml

读取应用配置
./vesc_tool_7.01 --offscreen --vescPort /dev/ttyACM0 --getAppConf app_config.xml

=== 写入配置 ===
写入电机配置
./vesc_tool_7.01 --offscreen --vescPort /dev/ttyACM0 --setMcConf motor_config.xml

=== 固件操作 ===
上传固件
./vesc_tool_7.01 --offscreen --vescPort /dev/ttyACM0 --uploadFirmware firmware.bin

上传内置 Bootloader
./vesc_tool_7.01 --offscreen --vescPort /dev/ttyACM0 --uploadBootloaderBuiltin

打包固件
./vesc_tool_7.01 --packFirmware input.bin:output_packed.bin

=== LispBM 脚本 ===
上传 LispBM 脚本
./vesc_tool_7.01 --offscreen --vescPort /dev/ttyACM0 --uploadLisp my_script.lisp

压缩 LispBM 脚本体积
./vesc_tool_7.01 --reduceLisp --uploadLisp my_script.lisp

打包 LispBM（含导入文件）
./vesc_tool_7.01 --packLisp main.lisp:packed.lisp

=== 网络远程访问 ===
连接 VESC 并启动 TCP 服务器（端口 65102）
./vesc_tool_7.01 --vescPort /dev/ttyACM0 --tcpServer 65102

仅启动 TCP Hub（不连接自身）
./vesc_tool_7.01 --tcpHub 65103

=== QML 界面 ===
从文件加载自定义 QML UI
./vesc_tool_7.01 --loadQml my_dashboard.qml --qmlFullscreen

从 VESC 加载 QML UI 并使用移动端模式
./vesc_tool_7.01 --loadQmlVesc --useMobileUi
```

---

## 添加自定义硬件

如果你设计了自己的 VESC 兼容硬件并希望其被官方发布支持：

1. Fork [bldc 固件仓库](https://github.com/vedderb/bldc)
2. 进行修改并充分测试
3. 向主仓库提交 **Pull Request**
4. 如果 PR 被接受：
   - 你的硬件将在几天内出现在开发版中
   - 下次发布稳定版时会被包含

---

## 相关链接

| 链接 | 说明 |
|------|------|
| [http://vesc-project.com/](http://vesc-project.com/) | VESC 官方主页，下载预编译版本 |
| [https://github.com/vedderb/vesc_tool](https://github.com/vedderb/vesc_tool) | VESC Tool 源码仓库 |
| [https://github.com/vedderb/bldc](https://github.com/vedderb/bldc) | VESC BLDC 固件源码仓库 |
| [https://vesc-project.com/trademark_policies](https://vesc-project.com/trademark_policies) | VESC 商标政策 |
| [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html) | GPLv3 协议全文 |

---

> **中文版翻译维护**：本项目为 VESC Tool 中文版，包含中文界面本地化支持