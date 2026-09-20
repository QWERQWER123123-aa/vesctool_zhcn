# extract_xml_strings_for_translation.py
# 运行方式: python extract_xml_strings_for_translation.py
# 用于从 res/config/*/parameters_mcconf.xml 和 parameters_appconf.xml 以及 info.xml 中提取所有 longName, description, enumNames

import os
import xml.etree.ElementTree as ET
import re
from pathlib import Path

translations = {}
config_dir = Path(r"f:\VESC\vesc_tool-master\vesc_tool-master\res\config")

for xml_file in config_dir.rglob("*.xml"):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    for params_elem in root.findall(".//Params"):
        for param in params_elem:
            long_name = param.find("longName")
            if long_name is not None and long_name.text:
                translations[long_name.text] = ""
            
            description = param.find("description")
            if description is not None and description.text:
                translations[description.text] = ""
            
            for enum in param.findall("enumNames"):
                if enum.text:
                    translations[enum.text] = ""

# Also add separator texts
separators = set()
for xml_file in config_dir.rglob("*.xml"):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for pg in root.findall(".//ParamGrouping"):
        for group in pg:
            for entry in group:
                if entry.tag == "param" and entry.text and entry.text.startswith("::sep::"):
                    sep_text = entry.text[7:]
                    translations[sep_text] = ""

print(f"Total unique strings to translate: {len(translations)}")
print("\nFormat for .ts file (copy into vesc_tool_zh_CN.ts within <context name=\"ConfigParams\">):")
for source, _ in sorted(translations.items()):
    escaped = source.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    print(f'        <message>\n            <source>{escaped}</source>\n            <translation type="unfinished"></translation>\n        </message>')