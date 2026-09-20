# batch_translate.py
# 使用方法：将此脚本放在 vesc_tool-master 目录下运行
# python batch_translate.py

import xml.etree.ElementTree as ET
import re
import os

# 翻译字典 - 常用 UI 和技术术语
TRANSLATIONS = {
    # 通用 UI
    "Form": "窗体",
    "Dialog": "对话框",
    "Ok": "确定",
    "Cancel": "取消",
    "Reset": "重置",
    "Apply": "应用",
    "Close": "关闭",
    "Save": "保存",
    "Delete": "删除",
    "Edit": "编辑",
    "Copy": "复制",
    "Cut": "剪切",
    "Paste": "粘贴",
    "Undo": "撤销",
    "Redo": "重做",
    "Help": "帮助",
    "Show help": "显示帮助",
    "Menu": "菜单",
    "Grid": "网格",
    "Follow": "跟随",
    "AutoZoom": "自动缩放",
    "Search": "搜索",
    "Filter": "过滤",
    "Refresh": "刷新",
    "Clear": "清除",
    "Enable": "启用",
    "Disable": "禁用",
    "Enabled": "已启用",
    "Disabled": "已禁用",
    "Start": "启动",
    "Stop": "停止",
    "Play": "播放",
    "Pause": "暂停",
    "Export": "导出",
    "Import": "导入",
    "Browse": "浏览",
    "Select": "选择",
    "Open": "打开",
    "File": "文件",
    "Folder": "文件夹",
    "Path": "路径",
    "Name": "名称",
    "Type": "类型",
    "Size": "大小",
    "Date": "日期",
    "Time": "时间",
    "Value": "值",
    "Unit": "单位",
    "Range": "范围",
    "Min": "最小",
    "Max": "最大",
    "Average": "平均",
    "Total": "总计",
    "Current": "当前",
    "Voltage": "电压",
    "Power": "功率",
    "Speed": "速度",
    "Position": "位置",
    "Temperature": "温度",
    "Status": "状态",
    "Mode": "模式",
    "Config": "配置",
    "Settings": "设置",
    "Advanced": "高级",
    "Basic": "基本",
    "General": "通用",
    "Custom": "自定义",
    "Default": "默认",
    "Auto": "自动",
    "Manual": "手动",
    "None": "无",
    "All": "全部",
    "Yes": "是",
    "No": "否",
    "On": "开",
    "Off": "关",
    "Error": "错误",
    "Warning": "警告",
    "Info": "信息",
    "Question": "问题",
    "Confirm": "确认",
    "Are you sure?": "您确定吗？",
    "OK": "确定",
    "Next": "下一步",
    "Previous": "上一步",
    "Back": "返回",
    "Forward": "前进",
    "Finish": "完成",
    "Exit": "退出",
    "Quit": "退出",
    "About": "关于",
    "Version": "版本",
    "License": "许可证",
    "Loading...": "加载中...",
    "Please wait...": "请稍候...",
    "Connecting...": "连接中...",
    "Connected": "已连接",
    "Disconnected": "已断开",

    # 编辑器相关
    "Undo (CTRL+Z)": "撤销 (CTRL+Z)",
    "Cut (CTRL+X)": "剪切 (CTRL+X)",
    "Copy (CTRL+C)": "复制 (CTRL+C)",
    "Paste (CTRL+V)": "粘贴 (CTRL+V)",
    "Link (CTRL+L)": "链接 (CTRL+L)",
    "Italic (CTRL+I)": "斜体 (CTRL+I)",
    "Underline (CTRL+U)": "下划线 (CTRL+U)",
    "Font size": "字体大小",
    "Insert image...": "插入图片...",
    "Paragraph formatting": "段落格式",
    "...": "...",

    # VESC 电机相关
    "Motor": "电机",
    "MOSFET": "MOSFET",
    "RPM": "转速",
    "FOC": "FOC",
    "BLDC": "BLDC",
    "PID Pos": "PID位置",
    "Obs vs Enc": "观测器vs编码器",
    "Observer": "观测器",
    "Encoder": "编码器",
    "Inductance": "电感",
    "Rotor Position": "转子位置",
    "%v Degrees": "%v 度",
    "Duty Cycle": "占空比",
    "Battery": "电池",
    "BMS": "电池管理系统",
    "BMS On": "BMS开",
    "BMS Off": "BMS关",
    "ESC": "电调",
    "VESC": "VESC",
    "CAN Bus": "CAN总线",
    "UART": "UART",
    "I2C": "I2C",
    "SPI": "SPI",
    "PWM": "PWM",
    "PPM": "PPM",
    "ADC": "ADC",
    "NTC": "NTC",
    "Hall Sensor": "霍尔传感器",
    "Encoder Index": "编码器索引",
    "Flux Linkage": "磁链",
    "Resistance": "电阻",
    "Bandwidth": "带宽",
    "Observer Gain": "观测器增益",
    "KP": "KP",
    "KI": "KI",
    "KD": "KD",

    # 页面/功能相关
    "ADC Mapping": "ADC映射",
    "ADC Voltage Mapping": "ADC电压映射",
    "Apply Voltages": "应用电压",
    "Poll GNSS": "轮询GNSS",
    "No log opened": "未打开日志",
    "No tab is open": "未打开选项卡",
    "Reading Code...": "读取代码中...",
    "Streaming...": "流传输中...",
    "Erasing...": "擦除中...",
    "Start/Stop LispBM": "启动/停止 LispBM",
    "Delete the tab": "删除选项卡",
    "Firmware": "固件",
    "Bootloader": "引导程序",
    "Flash": "烧录",
    "Read": "读取",
    "Write": "写入",
    "Upload": "上传",
    "Download": "下载",
    "Firmware Update": "固件更新",
    "Motor Detection": "电机检测",
    "Motor Setup": "电机设置",
    "Input Setup": "输入设置",
    "App Settings": "应用设置",
    "Realtime Data": "实时数据",
    "RT Data": "实时数据",
    "Sampling": "采样",
    "Logging": "日志记录",
    "Analysis": "分析",
    "Comparison": "比较",
    "Terminal": "终端",
    "Console": "控制台",
    "Lisp": "Lisp",
    "Script": "脚本",
    "Code": "代码",
    "Run": "运行",
    "Stop": "停止",
    "Compile": "编译",
    "Step Into": "单步进入",
    "Step Over": "单步跳过",
    "Breakpoint": "断点",

    # 蓝牙/无线
    "Bluetooth": "蓝牙",
    "BLE": "BLE",
    "Scan": "扫描",
    "Pair": "配对",
    "Unpair": "取消配对",
    "Connect": "连接",
    "Disconnect": "断开连接",
    "Reconnect": "重新连接",
    "Signal Strength": "信号强度",
    "RSSI": "RSSI",

    # 向导/对话框标题
    "Connection": "连接",
    "Connection Failed": "连接失败",
    "Connection Lost": "连接丢失",
    "Timeout": "超时",
    "Retry": "重试",
    "Ignore": "忽略",
    "Abort": "中止",
    "Continue": "继续",
    "Skip": "跳过",
    "Details": "详情",
    "Summary": "摘要",
    "Report": "报告",
    "Log": "日志",

    # CH1/CH2
    "CH1 ": "CH1 ",
    "CH2 ": "CH2 ",
    "Center: ": "中心: ",
    "Max: ": "最大: ",
    "Min: ": "最小: ",

    # %1 格式化字符串
    "%1 V (%2 %)": "%1 V (%2 %)",
}

def translate_ts_file(ts_path):
    """翻译 TS 文件中所有未完成的条目"""
    tree = ET.parse(ts_path)
    root = tree.getroot()
    
    translated_count = 0
    not_found = []

    for context in root.findall('context'):
        context_name = context.get('name', '')
        for message in context.findall('message'):
            source_elem = message.find('source')
            translation_elem = message.find('translation')

            if source_elem is None or translation_elem is None:
                continue

            source_text = source_elem.text or ''
            
            # 只处理未完成的条目
            if translation_elem.get('type') == 'unfinished':
                if source_text in TRANSLATIONS:
                    translation_elem.text = TRANSLATIONS[source_text]
                    del translation_elem.attrib['type']
                    translated_count += 1
                else:
                    not_found.append((context_name, source_text))

    # 写回文件
    tree.write(ts_path, encoding='utf-8', xml_declaration=True)
    
    return translated_count, not_found

if __name__ == '__main__':
    ts_file = os.path.join(os.path.dirname(__file__), 'vesc_tool_zh_CN.ts')
    
    print(f"正在处理: {ts_file}")
    count, not_found = translate_ts_file(ts_file)
    print(f"\n✅ 已翻译: {count} 条")
    print(f"❌ 未找到翻译: {len(not_found)} 条")
    
    if not_found:
        print("\n--- 以下条目需要手动翻译 ---")
        for ctx, src in not_found:
            print(f"  [{ctx}] {src}")
    
    print("\n注意: 翻译完成后请运行 lrelease vesc_tool_zh_CN.ts 来编译 .qm 文件")