#!/usr/bin/env python3
# fix_configparams_translations.py
# 用法: python fix_configparams_translations.py
# 功能: 扫描 res/config 下所有 XML 文件，提取 longName/enumNames/分隔符，
#       并替换 vesc_tool_zh_CN.ts 中空的 ConfigParams 上下文

import xml.etree.ElementTree as ET
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "res" / "config"
TS_FILE = BASE_DIR / "vesc_tool_zh_CN.ts"

# ========== 翻译字典 (与 gen_ts_entries.py 保持一致) ==========
TR_DICT = {
    "PWM Mode": "PWM 模式", "Commutation Mode": "换向模式",
    "Motor Type": "电机类型", "Sensor Mode": "传感器模式",
    "Motor Current Max": "电机最大电流",
    "Motor Current Max Brake": "电机制动最大电流",
    "Battery Current Max": "电池最大电流",
    "Battery Current Max Regen": "电池最大回充电流",
    "Input Current Limit Map Start": "输入电流限制映射起点",
    "Input Current Map Filter": "输入电流映射滤波器",
    "Absolute Maximum Current": "绝对最大电流",
    "Max ERPM Reverse": "最大反向 ERPM", "Max ERPM": "最大 ERPM",
    "ERPM Limit Start": "ERPM 限制起点",
    "Max ERPM Full Brake": "最大 ERPM 全制动",
    "Max ERPM Full Brake Current Control": "最大 ERPM 全制动电流控制",
    "Minimum Input Voltage": "最低输入电压",
    "Maximum Input Voltage": "最高输入电压",
    "Battery Voltage Cutoff Start": "电池电压截止起点",
    "Battery Voltage Cutoff End": "电池电压截止终点",
    "Battery Voltage Regen Cutoff Start": "电池回充电压截止起点",
    "Battery Voltage Regen Cutoff End": "电池回充电压截止终点",
    "Slow ABS Current Limit": "慢速 ABS 电流限制",
    "MOSFET Temp Cutoff Start": "MOSFET 温度截止起点",
    "MOSFET Temp Cutoff End": "MOSFET 温度截止终点",
    "Motor Temp Cutoff Start": "电机温度截止起点",
    "Motor Temp Cutoff End": "电机温度截止终点",
    "Acceleration Temperature Decrease": "加速温度降低",
    "Minimum Duty Cycle": "最小占空比", "Maximum Duty Cycle": "最大占空比",
    "Maximum Wattage": "最大功率", "Maximum Braking Wattage": "最大制动功率",
    "Max Current Scale": "最大电流比例", "Min Current Scale": "最小电流比例",
    "Duty Cycle Current Limit Start": "占空比电流限制起点",
    "Additional Faults": "附加故障", "Minimum ERPM": "最小 ERPM",
    "Minimum ERPM Integrator": "最小 ERPM 积分器",
    "Max Brake Current at Direction Change": "换向最大制动电流",
    "Cycle Integrator Limit": "周期积分器限制",
    "Phase Advance at BR ERPM": "BR ERPM 处相位超前",
    "BR ERPM": "BR ERPM", "BEMF Coupling": "BEMF 耦合",
    "Hall Table [0]": "霍尔表 [0]", "Hall Table [1]": "霍尔表 [1]",
    "Hall Table [2]": "霍尔表 [2]", "Hall Table [3]": "霍尔表 [3]",
    "Hall Table [4]": "霍尔表 [4]", "Hall Table [5]": "霍尔表 [5]",
    "Hall Table [6]": "霍尔表 [6]", "Hall Table [7]": "霍尔表 [7]",
    "Sensorless ERPM Hybrid": "无传感器 ERPM 混合",
    "Current KP": "电流 KP", "Current KI": "电流 KI",
    "Zero Vector Frequency": "零矢量频率",
    "Dead Time Compensation": "死区时间补偿",
    "Encoder Inverted": "编码器反转", "Encoder Offset": "编码器偏移",
    "Encoder Ratio": "编码器比例",
    "Speed Tracker Kp": "速度跟踪器 Kp",
    "Speed Tracker Ki": "速度跟踪器 Ki",
    "Motor Inductance (L)": "电机电感 (L)",
    "Motor Inductance Difference (Lq - Ld)": "电机电感差 (Lq - Ld)",
    "Motor Resistance (R)": "电机电阻 (R)",
    "Motor Flux Linkage (λ)": "电机磁链 (λ)",
    "Observer Gain (x1M)": "观测器增益 (x1M)",
    "Observer Gain At Minimum Duty": "最小占空比观测器增益",
    "Observer Offset": "观测器偏移",
    "Duty Downramp Kp": "占空比下降斜率 Kp",
    "Duty Downramp Ki": "占空比下降斜率 Ki",
    "Start Current Decrease": "启动电流降低",
    "Start Current Decrease ERPM": "启动电流降低 ERPM",
    "Openloop ERPM": "开环 ERPM",
    "Openloop ERPM at Min Current": "最小电流时开环 ERPM",
    "Openloop Hysteresis": "开环滞后",
    "Openloop Lock Time": "开环锁定时间",
    "Openloop Ramp Time": "开环斜坡时间", "Openloop Time": "开环时间",
    "Openloop Current Boost": "开环电流增强",
    "Openloop Current Max": "开环最大电流",
    "Hall Interpolation ERPM": "霍尔插值 ERPM",
    "Sensored ERPM Start": "有传感器 ERPM 起点",
    "Sensorless ERPM": "无传感器 ERPM",
    "Control Sample Mode": "控制采样模式",
    "Current Sample Mode": "电流采样模式",
    "Saturation Compensation Mode": "饱和补偿模式",
    "Saturation Compensation Factor": "饱和补偿系数",
    "Temp Comp": "温度补偿",
    "Temp Comp Base Temp": "温度补偿基准温度",
    "Current Filter Constant": "电流滤波常数",
    "Current Controller Decoupling": "电流控制器解耦",
    "Observer Type": "观测器类型",
    "HFI Ambiguity Resolve Mode": "HFI 极性分辨模式",
    "HFI Ambiguity Resolve Current": "HFI 极性分辨电流",
    "HFI Ambiguity Resolve Threshold": "HFI 极性分辨阈值",
    "HFI Start Voltage": "HFI 启动电压",
    "HFI Run Voltage": "HFI 运行电压",
    "HFI Max Voltage": "HFI 最大电压",
    "HFI Gain": "HFI 增益", "HFI Max Error": "HFI 最大误差",
    "HFI Current Hysteresis": "HFI 电流滞回",
    "Sensorless ERPM HFI": "无传感器 ERPM HFI",
    "HFI Reset ERPM": "HFI 重置 ERPM",
    "HFI Start Samples": "HFI 启动采样数",
    "HFI Observer Override Time": "HFI 观测器覆盖时间",
    "HFI Samples": "HFI 采样数",
    "Offset Calibration Mode": "偏移校准模式",
    "Current Offset 0": "电流偏移 0", "Current Offset 1": "电流偏移 1",
    "Current Offset 2": "电流偏移 2",
    "Voltage Offset 0": "电压偏移 0", "Voltage Offset 1": "电压偏移 1",
    "Voltage Offset 2": "电压偏移 2",
    "Voltage Offset Undriven 0": "未驱动电压偏移 0",
    "Voltage Offset Undriven 1": "未驱动电压偏移 1",
    "Voltage Offset Undriven 2": "未驱动电压偏移 2",
    "Enable Phase Filters": "启用相位滤波器",
    "Disable Phase Filter Fault Code": "禁用相位滤波故障码",
    "Maximum ERPM for phase filters": "相位滤波器最大 ERPM",
    "MTPA Algorithm Mode": "MTPA 算法模式",
    "Field Weakening Current Max": "弱磁最大电流",
    "Field Weakening Duty Start": "弱磁占空比起始",
    "Q Axis Current Factor": "Q 轴电流系数",
    "Backoff Gain": "回退增益",
    "Field Weakening Ramp Time": "弱磁斜坡时间",
    "Speed Tracker Position Source": "速度跟踪位置源",
    "Short Low-Side FETs on Zero Duty": "零占空比时短接低侧 FET",
    "Overmodulation Factor": "过调制系数",
    "Maximum VD Magnitude": "最大 VD 幅度",
    "PID Loop Rate": "PID 循环频率",
    "Speed PID Kp": "速度 PID Kp", "Speed PID Ki": "速度 PID Ki",
    "Speed PID Kd": "速度 PID Kd",
    "Speed PID Kd Filter": "速度 PID Kd 滤波器",
    "Allow Braking": "允许制动",
    "Ramp eRPMs per second": "每秒 ERPM 斜坡",
    "Speed Source": "速度源",
    "Position PID Kp": "位置 PID Kp", "Position PID Ki": "位置 PID Ki",
    "Position PID Kd": "位置 PID Kd",
    "Position PID Offset Angle": "位置 PID 偏移角度",
    "Position PID Kd Process": "位置 PID Kd 处理",
    "Position PID Kd Filter": "位置 PID Kd 滤波器",
    "Position Angle Division": "位置角度分频",
    "Gain Decrease Angle": "增益衰减角度",
    "Startup boost": "启动增强", "Minimum Current": "最小电流",
    "Current Controller Gain": "电流控制器增益",
    "Current Control Ramp Step Max": "电流控制最大斜坡步长",
    "Fault Stop Time": "故障停机时间",
    "Duty Ramp Step Max": "占空比最大斜坡步长",
    "Current Backoff Gain": "电流回退增益",
    "Encoder counts": "编码器计数",
    "Sine Amplitude": "正弦幅度", "Cosine Amplitude": "余弦幅度",
    "Sine Offset": "正弦偏移", "Cosine Offset": "余弦偏移",
    "Sin/Cos Filter Constant": "Sin/Cos 滤波常数",
    "Sin/Cos Phase Correction": "Sin/Cos 相位校正",
    "Sensor Port Mode": "传感器端口模式",
    "Invert Motor Direction": "反转电机方向",
    "DRV8301 OC Mode": "DRV8301 过流模式",
    "DRV8301 OC Adjustment": "DRV8301 过流调整",
    "Minimum Switching Frequency": "最低开关频率",
    "Maximum Switching Frequency": "最高开关频率",
    "Switching Frequency": "开关频率",
    "Beta Value for Motor Thermistor": "电机热敏电阻 Beta 值",
    "Auxiliary Output Mode": "辅助输出模式",
    "Motor Temperature Sensor Type": "电机温度传感器类型",
    "Coefficient for PTC Motor Thermistor": "PTC 电机热敏电阻系数",
    "Custom NTC/PTC Resistance": "自定义 NTC/PTC 电阻",
    "Custom NTC/PTC Base Temperature": "自定义 NTC/PTC 基准温度",
    "Hall Sensor Extra Samples": "霍尔传感器额外采样",
    "Battery Filter Constant": "电池滤波常数",
    "Motor Poles": "电机极对数", "Gear Ratio": "齿轮比",
    "Wheel Diameter": "轮径", "Battery Type": "电池类型",
    "Battery Cells Series": "电池串联数",
    "Battery Capacity": "电池容量",
    "Motor No Load Current": "电机空载电流",
    "Motor Brand": "电机品牌", "Motor Model": "电机型号",
    "Motor Weight": "电机重量", "Position Sensor": "位置传感器",
    "Motor Description": "电机描述",
    "Bearing Quality": "轴承质量", "Magnet Quality": "磁铁质量",
    "Construction Quality": "制造质量",
    "Quality Description": "质量描述",
    "IMU Type": "IMU 类型", "IMU AHRS Mode": "IMU AHRS 模式",
    "Accel/Gyro Filter": "加速度计/陀螺仪滤波器",
    "Accel lowpass filter X": "加速度计低通滤波 X",
    "Accel lowpass filter Y": "加速度计低通滤波 Y",
    "Accel lowpass filter Z": "加速度计低通滤波 Z",
    "Gyro lowpass filter": "陀螺仪低通滤波器",
    "Sample Rate": "采样率", "Use magnetometer": "使用磁力计",
    "Accelerometer Confidence Decay": "加速度计置信衰减",
    "Mahony KP": "Mahony KP", "Mahony KI": "Mahony KI",
    "Madgwick Beta": "Madgwick Beta",
    "Imu Rotation Roll": "IMU 旋转横滚",
    "Imu Rotation Pitch": "IMU 旋转俯仰",
    "Imu Rotation Yaw": "IMU 旋转偏航",
    "Accel Offset X": "加速度计偏移 X",
    "Accel Offset Y": "加速度计偏移 Y",
    "Accel Offset Z": "加速度计偏移 Z",
    "Gyro Offset X": "陀螺仪偏移 X",
    "Gyro Offset Y": "陀螺仪偏移 Y",
    "Gyro Offset Z": "陀螺仪偏移 Z",
    "VESC ID": "VESC ID", "Timeout": "超时",
    "Timeout Brake Current": "超时制动电流",
    "Can Status Rate 1": "CAN 状态频率 1",
    "Can Status Rate 2": "CAN 状态频率 2",
    "Can Messages Rate 1": "CAN 消息频率 1",
    "Can Messages Rate 2": "CAN 消息频率 2",
    "CAN Baud Rate": "CAN 波特率",
    "Pairing Done": "已完成配对",
    "Enable Permanent UART": "启用永久 UART",
    "Shutdown Mode": "关机模式", "CAN Mode": "CAN 模式",
    "UAVCAN ESC Index": "UAVCAN ESC 索引",
    "UAVCAN Raw Throttle Mode": "UAVCAN 原始油门模式",
    "UAVCAN Raw RPM Max": "UAVCAN 原始 RPM 最大值",
    "UAVCAN Status Current Mode": "UAVCAN 状态电流模式",
    "Enable Servo Output": "启用舵机输出",
    "Kill Switch Mode": "急停开关模式",
    "APP to Use": "使用的 APP", "Control Type": "控制类型",
    "PID Max ERPM": "PID 最大 ERPM",
    "Input Deadband": "输入死区",
    "Pulselength Start": "脉冲长度起点",
    "Pulselength End": "脉冲长度终点",
    "Pulselength Center": "脉冲长度中点",
    "Median Filter": "中值滤波器", "Safe Start": "安全启动",
    "Throttle Expo": "油门曲线",
    "Throttle Expo Brake": "制动油门曲线",
    "Throttle Expo Mode": "油门曲线模式",
    "Positive Ramping Time": "正向斜坡时间",
    "Negative Ramping Time": "反向斜坡时间",
    "Multiple VESCs Over CAN": "CAN 多 VESC",
    "Traction Control": "牵引力控制",
    "TC Max ERPM Difference": "牵引力控制最大 ERPM 差",
    "Max ERPM for direction switch": "换向最大 ERPM",
    "Smart Reverse Max Duty Cycle": "智能倒车最大占空比",
    "Smart Reverse Ramp Time": "智能倒车斜坡时间",
    "ADC1 Start Voltage": "ADC1 起始电压",
    "ADC1 End Voltage": "ADC1 终止电压",
    "ADC1 Abs Min Voltage": "ADC1 绝对最小电压",
    "ADC1 Abs Max Voltage": "ADC1 绝对最大电压",
    "ADC1 Center Voltage": "ADC1 中点电压",
    "ADC2 Start Voltage": "ADC2 起始电压",
    "ADC2 End Voltage": "ADC2 终止电压",
    "Use Filter": "使用滤波器", "Button Inputs": "按钮输入",
    "Invert ADC1 Voltage": "反转 ADC1 电压",
    "Invert ADC2 Voltage": "反转 ADC2 电压",
    "Update Rate": "更新频率", "Baudrate": "波特率",
    "ERPM Per Second Cruise Control": "定速巡航每秒 ERPM",
    "Use Smart Reverse": "使用智能倒车",
    "Coasting Brake Level": "滑行制动级别",
    "Coasting Brake Ramp Time": "滑行制动斜坡时间",
    "Speed": "速率", "TX Power": "发射功率",
    "CRC": "CRC 校验", "Retry Delay": "重试延迟",
    "Retries": "重试次数", "Radio Channel": "无线电信道",
    "Address 0": "地址 0", "Address 1": "地址 1",
    "Address 2": "地址 2", "Send ACK": "发送 ACK",
    "Sensor Type": "传感器类型",
    "Pedal RPM Start": "踏板 RPM 起点",
    "Pedal RPM End": "踏板 RPM 终点",
    "Invert Pedal Direction": "反转踏板方向",
    "Sensor Magnets": "传感器磁铁数",
    "PAS Max Current": "PAS 最大电流",
    "ABI Encoder": "ABI 编码器",
    "Sin/Cos Encoder": "Sin/Cos 编码器",
    "Motor": "电机", "Battery": "电池",
    "DRV8301": "DRV8301",
    "General": "通用", "MOSFET": "MOSFET",
    "Encoder": "编码器", "Current": "电流",
    "Voltage": "电压", "Voltage Undriven": "未驱动电压",
    "Common": "通用", "Speed Controller": "速度控制器",
    "Position Controller": "位置控制器",
    "CAN Messages Rate 1": "CAN 消息频率 1",
    "CAN Messages Rate 2": "CAN 消息频率 2",
    "Multiple VESCs over CAN": "CAN 多 VESC",
    "Multiple VESCs over CAN-bus": "CAN 总线多 VESC",
    "ADC 1": "ADC 1", "ADC 2": "ADC 2",
    "Smart Reverse": "智能倒车",
    "Coasting Brake": "滑行制动",
    "Multiple ESCs over CAN-bus": "CAN 总线多 ESC",
    "Radio": "无线电", "Integrity": "完整性",
    "Address": "地址", "AHRS": "AHRS",
    "Rotation": "旋转", "Offsets": "偏移",
    "Six Vectors": "六矢量法",
    "Id Single Pulse": "Id 单脉冲",
    "Id Double Pulse": "Id 双脉冲",
    "Status 1": "状态 1", "Status 2": "状态 2",
    "Status 3": "状态 3", "Status 4": "状态 4",
    "Status 5": "状态 5", "Status 6": "状态 6",
    "Unused": "未使用",
    "CAN_BAUD_125K": "CAN 125K",
    "CAN_BAUD_250K": "CAN 250K",
    "CAN_BAUD_500K": "CAN 500K",
    "CAN_BAUD_1M": "CAN 1M",
    "CAN_BAUD_10K": "CAN 10K",
    "CAN_BAUD_20K": "CAN 20K",
    "CAN_BAUD_50K": "CAN 50K",
    "CAN_BAUD_75K": "CAN 75K",
    "CAN_BAUD_100K": "CAN 100K",
    "Firmware Version": "固件版本",
    "Soft Battery Cutoff Calculator": "软电池截止计算器",
    "Detect BLDC Parameters": "检测 BLDC 参数",
    "Detect FOC Parameters": "检测 FOC 参数",
    "Detect FOC Encoder Parameters": "检测 FOC 编码器参数",
    "Detect FOC Hall Sensor Parameters": "检测 FOC 霍尔传感器参数",
    "NRF Pairing": "NRF 配对", "CAN Forwarding": "CAN 转发",
    "RT data logging": "实时数据记录",
    "Motor Setting Description": "电机设置说明",
    "App Setting Description": "应用设置说明",
    "Development Tool Description": "开发工具说明",
    "Data Analysis Description": "数据分析说明",
    "App ADC Information": "App ADC 信息",
    "Chuk Info": "Chuk 信息",
    "PPM Pulselength Mapping": "PPM 脉冲长度映射",
    "ADC Voltage Mapping": "ADC 电压映射",
    "Welcome to VESC Tool": "欢迎使用 VESC Tool",
    "Usage": "使用说明", "Warranty": "保修",
    "Conclusion": "总结", "License": "许可证",
    "Firmware Not Included": "固件未包含",
    "Firmware Not Downloaded": "固件未下载",
}

def escape_xml(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def collect_all_translations():
    translations = {}

    for xml_file in sorted(CONFIG_DIR.rglob("*.xml")):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for elem in root.iter("longName"):
                if elem.text and elem.text.strip() and elem.text.strip() != "none":
                    key = elem.text.strip()
                    translations[key] = TR_DICT.get(key, "")

            for elem in root.iter("enumNames"):
                if elem.text and elem.text.strip():
                    key = elem.text.strip()
                    translations[key] = TR_DICT.get(key, "")

            for pg in root.iter("ParamGrouping"):
                for group in pg:
                    for entry in group:
                        if entry.tag == "param" and entry.text and entry.text.startswith("::sep::"):
                            sep_text = entry.text[7:].strip()
                            if sep_text:
                                translations[sep_text] = TR_DICT.get(sep_text, "")
        except ET.ParseError as e:
            print(f"  警告: 解析失败 {xml_file}: {e}")
            continue

    return translations

def build_configparams_context(translations):
    lines = []
    lines.append("    <context>")
    lines.append("        <name>ConfigParams</name>")

    for source in sorted(translations.keys()):
        trans = translations[source]
        src_esc = escape_xml(source)
        if trans:
            trans_esc = escape_xml(trans)
            lines.append("        <message>")
            lines.append(f"            <source>{src_esc}</source>")
            lines.append(f"            <translation>{trans_esc}</translation>")
            lines.append("        </message>")
        else:
            lines.append("        <message>")
            lines.append(f"            <source>{src_esc}</source>")
            lines.append('            <translation type="unfinished"></translation>')
            lines.append("        </message>")

    lines.append("    </context>")
    return "\n".join(lines)

def main():
    print("=" * 60)
    print("VESC Tool ConfigParams 翻译修补工具")
    print("=" * 60)

    if not TS_FILE.exists():
        print(f"错误: 找不到 {TS_FILE}")
        return

    if not CONFIG_DIR.exists():
        print(f"错误: 找不到 {CONFIG_DIR}")
        return

    print(f"\n[1/4] 扫描 XML 配置文件...")
    translations = collect_all_translations()

    finished = sum(1 for v in translations.values() if v)
    unfinished = len(translations) - finished
    print(f"  找到 {len(translations)} 个唯一字符串")
    print(f"  已翻译: {finished}, 待翻译: {unfinished}")

    print(f"\n[2/4] 读取当前 .ts 文件...")
    with open(TS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"\n[3/4] 构建新的 ConfigParams 上下文...")
    new_context = build_configparams_context(translations)

    old_pattern = r'<context>\s*\n\s*<name>ConfigParams</name>.*?</context>'
    if re.search(old_pattern, content, re.DOTALL):
        new_content = re.sub(old_pattern, new_context.replace("\\", "\\\\"), content, flags=re.DOTALL)
        print("  已匹配到旧的 ConfigParams 上下文")
    else:
        print("  错误: 未找到 ConfigParams 上下文!")
        return

    print(f"\n[4/4] 写入更新后的 .ts 文件...")
    bak_path = TS_FILE.with_suffix(".ts.bak")
    with open(bak_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  备份已保存到: {bak_path}")

    with open(TS_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  已更新: {TS_FILE}")

    print(f"\n完成! 新增 {len(translations)} 条 ConfigParams 翻译条目。")
    print(f"待手动翻译: {unfinished} 条 (标记为 type=\"unfinished\")")
    print(f"\n下一步: 运行 lrelease vesc_tool_zh_CN.ts 生成 .qm 文件")

if __name__ == "__main__":
    main()