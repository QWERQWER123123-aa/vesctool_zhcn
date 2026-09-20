#!/usr/bin/env python3
# fix_menu_translations.py
# 放在 vesc_tool-master 目录下运行

import os

# 简单字符串替换：把 type="unfinished" 的条目改为已完成翻译
# 注意：文件中用的是 <translation type="unfinished"></translation> 双标签格式

REPLACEMENTS = [
    # ===== 页面级 Tab/菜单 =====
    # ===== PageAppAdc (line 3087) =====
    ('<source>Mapping</source>\n        <translation type="unfinished"></translation>',
     '<source>Mapping</source>\n        <translation>映射</translation>'),
    ('<source>Throttle Curve</source>\n        <translation type="unfinished"></translation>',
     '<source>Throttle Curve</source>\n        <translation>油门曲线</translation>'),

    # ===== PageAppGeneral (line 3106) =====
    ('<source>Tools</source>\n        <translation type="unfinished"></translation>',
     '<source>Tools</source>\n        <translation>工具</translation>'),
    ('<source>Servo Output</source>\n        <translation type="unfinished"></translation>',
     '<source>Servo Output</source>\n        <translation>舵机输出</translation>'),
    ('<source>Center</source>\n        <translation type="unfinished"></translation>',
     '<source>Center</source>\n        <translation>居中</translation>'),

    # ===== PageAppImu =====
    ('<source>RPY</source>\n        <translation type="unfinished"></translation>',
     '<source>RPY</source>\n        <translation>横滚/俯仰/偏航</translation>'),
    ('<source>Accel</source>\n        <translation type="unfinished"></translation>',
     '<source>Accel</source>\n        <translation>加速度计</translation>'),
    ('<source>Gyro</source>\n        <translation type="unfinished"></translation>',
     '<source>Gyro</source>\n        <translation>陀螺仪</translation>'),

    # ===== PageAppSettings =====
    ('<source>Input Setup Wizard</source>\n        <translation type="unfinished"></translation>',
     '<source>Input Setup Wizard</source>\n        <translation>输入设置向导</translation>'),

    # ===== PageBldc =====
    ('<source>Sensorless</source>\n        <translation type="unfinished"></translation>',
     '<source>Sensorless</source>\n        <translation>无传感器</translation>'),
    ('<source>Sensors</source>\n        <translation type="unfinished"></translation>',
     '<source>Sensors</source>\n        <translation>传感器</translation>'),

    # ===== PageMotor =====
    ('<source>Wattage</source>\n        <translation type="unfinished"></translation>',
     '<source>Wattage</source>\n        <translation>功率</translation>'),

    # ===== PageMotorInfo =====
    ('<source>Setup</source>\n        <translation type="unfinished"></translation>',
     '<source>Setup</source>\n        <translation>设置</translation>'),
    ('<source>Motor General</source>\n        <translation type="unfinished"></translation>',
     '<source>Motor General</source>\n        <translation>电机概要</translation>'),
    ('<source>Description</source>\n        <translation type="unfinished"></translation>',
     '<source>Description</source>\n        <translation>描述</translation>'),
    ('<source>Quality</source>\n        <translation type="unfinished"></translation>',
     '<source>Quality</source>\n        <translation>质量</translation>'),

    # ===== PageBms =====
    ('<source>Voltages</source>\n        <translation type="unfinished"></translation>',
     '<source>Voltages</source>\n        <translation>电压</translation>'),
    ('<source>Temperatures</source>\n        <translation type="unfinished"></translation>',
     '<source>Temperatures</source>\n        <translation>温度</translation>'),
    ('<source>Temp Plot</source>\n        <translation type="unfinished"></translation>',
     '<source>Temp Plot</source>\n        <translation>温度图表</translation>'),
    ('<source>Total Voltage</source>\n        <translation type="unfinished"></translation>',
     '<source>Total Voltage</source>\n        <translation>总电压</translation>'),
    ('<source>Cell Min</source>\n        <translation type="unfinished"></translation>',
     '<source>Cell Min</source>\n        <translation>最低电芯</translation>'),
    ('<source>Cell Max</source>\n        <translation type="unfinished"></translation>',
     '<source>Cell Max</source>\n        <translation>最高电芯</translation>'),
    ('<source>Cell Diff</source>\n        <translation type="unfinished"></translation>',
     '<source>Cell Diff</source>\n        <translation>电芯压差</translation>'),
    ('<source>Input Current</source>\n        <translation type="unfinished"></translation>',
     '<source>Input Current</source>\n        <translation>输入电流</translation>'),
    ('<source>Ah Counter</source>\n        <translation type="unfinished"></translation>',
     '<source>Ah Counter</source>\n        <translation>安时计数</translation>'),
    ('<source>Wh Counter</source>\n        <translation type="unfinished"></translation>',
     '<source>Wh Counter</source>\n        <translation>瓦时计数</translation>'),
    ('<source>Temp Cell Max</source>\n        <translation type="unfinished"></translation>',
     '<source>Temp Cell Max</source>\n        <translation>电芯最高温</translation>'),
    ('<source>Temp PCB Max</source>\n        <translation type="unfinished"></translation>',
     '<source>Temp PCB Max</source>\n        <translation>PCB 最高温</translation>'),
    ('<source>Humidity</source>\n        <translation type="unfinished"></translation>',
     '<source>Humidity</source>\n        <translation>湿度</translation>'),
    ('<source>Pressure</source>\n        <translation type="unfinished"></translation>',
     '<source>Pressure</source>\n        <translation>气压</translation>'),

    # ===== PageRtData =====
    ('<source>Obs vs Hall</source>\n        <translation type="unfinished"></translation>',
     '<source>Obs vs Hall</source>\n        <translation>观测器vs霍尔</translation>'),
    ('<source>PID Error</source>\n        <translation type="unfinished"></translation>',
     '<source>PID Error</source>\n        <translation>PID 误差</translation>'),

    # ===== PageScripting =====
    ('<source>Run in panel.</source>\n        <translation type="unfinished"></translation>',
     '<source>Run in panel.</source>\n        <translation>在面板中运行。</translation>'),
    ('<source>Run in Window</source>\n        <translation type="unfinished"></translation>',
     '<source>Run in Window</source>\n        <translation>在窗口中运行</translation>'),
    ('<source>Window</source>\n        <translation type="unfinished"></translation>',
     '<source>Window</source>\n        <translation>窗口</translation>'),
    ('<source>Fullscreen</source>\n        <translation type="unfinished"></translation>',
     '<source>Fullscreen</source>\n        <translation>全屏</translation>'),
    ('<source>Recent</source>\n        <translation type="unfinished"></translation>',
     '<source>Recent</source>\n        <translation>最近</translation>'),
    ('<source>Clear Filter Text</source>\n        <translation type="unfinished"></translation>',
     '<source>Clear Filter Text</source>\n        <translation>清除过滤文本</translation>'),
    ('<source>Remove</source>\n        <translation type="unfinished"></translation>',
     '<source>Remove</source>\n        <translation>移除</translation>'),
    ('<source>Examples</source>\n        <translation type="unfinished"></translation>',
     '<source>Examples</source>\n        <translation>示例</translation>'),
    ('<source>Tools</source>\n        <translation type="unfinished"></translation>',
     '<source>Tools</source>\n        <translation>工具</translation>'),
    ('<source>Export C Array</source>\n        <translation type="unfinished"></translation>',
     '<source>Export C Array</source>\n        <translation>导出 C 数组</translation>'),
    ('<source>Export Array HW</source>\n        <translation type="unfinished"></translation>',
     '<source>Export Array HW</source>\n        <translation>导出硬件数组</translation>'),
    ('<source>Export Array App</source>\n        <translation type="unfinished"></translation>',
     '<source>Export Array App</source>\n        <translation>导出应用数组</translation>'),
    ('<source>Calculate Size</source>\n        <translation type="unfinished"></translation>',
     '<source>Calculate Size</source>\n        <translation>计算大小</translation>'),
    ('<source>Connected VESC</source>\n        <translation type="unfinished"></translation>',
     '<source>Connected VESC</source>\n        <translation>已连接的 VESC</translation>'),
    ('<source>Open Qmlui HW</source>\n        <translation type="unfinished"></translation>',
     '<source>Open Qmlui HW</source>\n        <translation>打开 QML 硬件 UI</translation>'),
    ('<source>Open Qmlui App</source>\n        <translation type="unfinished"></translation>',
     '<source>Open Qmlui App</source>\n        <translation>打开 QML 应用 UI</translation>'),
    ('<source>QML Upload</source>\n        <translation type="unfinished"></translation>',
     '<source>QML Upload</source>\n        <translation>QML 上传</translation>'),
    ('<source>Clear text below</source>\n        <translation type="unfinished"></translation>',
     '<source>Clear text below</source>\n        <translation>清除下方文本</translation>'),
    ('<source>main</source>\n        <translation type="unfinished"></translation>',
     '<source>main</source>\n        <translation>main</translation>'),

    # ===== PageSetupCalculators =====
    ('<source>Add Setup</source>\n        <translation type="unfinished"></translation>',
     '<source>Add Setup</source>\n        <translation>添加设置</translation>'),
    ('<source>Remove Setup</source>\n        <translation type="unfinished"></translation>',
     '<source>Remove Setup</source>\n        <translation>移除设置</translation>'),

    # ===== PageSwdProg =====
    ('<source>Included Firmwares</source>\n        <translation type="unfinished"></translation>',
     '<source>Included Firmwares</source>\n        <translation>内置固件</translation>'),

    # ===== NrfPair =====
    ('<source>NRF Pairing</source>\n        <translation type="unfinished"></translation>',
     '<source>NRF Pairing</source>\n        <translation>NRF 配对</translation>'),
    ('<source>Start Pairing</source>\n        <translation type="unfinished"></translation>',
     '<source>Start Pairing</source>\n        <translation>开始配对</translation>'),

    # ===== MotorTypePage =====
    ('<source>Choose Motor Type</source>\n        <translation type="unfinished"></translation>',
     '<source>Choose Motor Type</source>\n        <translation>选择电机类型</translation>'),

    # ===== MainWindow =====
    ('<source>Warning</source>\n        <translation type="unfinished"></translation>',
     '<source>Warning</source>\n        <translation>警告</translation>'),
    ('<source>Error</source>\n        <translation type="unfinished"></translation>',
     '<source>Error</source>\n        <translation>错误</translation>'),
    ('<source>Xml files (*.xml)</source>\n        <translation type="unfinished"></translation>',
     '<source>Xml files (*.xml)</source>\n        <translation>XML 文件 (*.xml)</translation>'),
    ('<source>h files (*.h)</source>\n        <translation type="unfinished"></translation>',
     '<source>h files (*.h)</source>\n        <translation>头文件 (*.h)</translation>'),
    ('<source>Save header</source>\n        <translation type="unfinished"></translation>',
     '<source>Save header</source>\n        <translation>保存头文件</translation>'),
    ('<source>Modemmanager</source>\n        <translation type="unfinished"></translation>',
     '<source>Modemmanager</source>\n        <translation>调制解调器管理器</translation>'),
    ('<source>Create File Error</source>\n        <translation type="unfinished"></translation>',
     '<source>Create File Error</source>\n        <translation>创建文件错误</translation>'),
]

if __name__ == "__main__":
    ts_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vesc_tool_zh_CN.ts")
    
    with open(ts_file, "r", encoding="utf-8") as f:
        content = f.read()

    translated = 0
    for old, new in REPLACEMENTS:
        if old in content:
            cnt = content.count(old)
            content = content.replace(old, new)
            translated += cnt
            print(f"  ✅ [{cnt}x] {new.split('</translation>')[0].rsplit('>', 1)[-1]}")
        else:
            print(f"  ❌ NOT FOUND: {old.split('</source>')[0].rsplit('>', 1)[-1]}")

    with open(ts_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n{'='*50}")
    print(f"完成! 成功翻译 {translated}/{len(REPLACEMENTS)} 条")
    print(f"下一步: 运行 lrelease vesc_tool_zh_CN.ts 编译 .qm 文件")