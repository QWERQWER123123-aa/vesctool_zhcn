#!/usr/bin/env python3
"""
fix_info_xml_html_issues.py
修复 info.xml 中的 HTML 问题:
1. 合并 <li> 元素上的重复 style 属性
2. 将 font-weight:600 替换为 font-weight:bold (提高 QML 兼容性)
3. 去除 style 属性值中的前导空格
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INFO_FILES = sorted(BASE_DIR.glob("res/config/*/info.xml"))
INFO_FILES += sorted(BASE_DIR.glob("res/config_*.xml"))

PATTERNS = [
    # 1. 合并 <li> 的 double style: style="A" style="B" → style="A B"
    (
        r'(<li\s+style=")([^"]*)("\s+style=")([^"]*)(")',
        lambda m: f'<li style="{m.group(2).rstrip(";")}; {m.group(4)}"'
    ),
    # 2. font-weight:600 → font-weight:bold (QML RichText 不支持数字字重)
    (r'font-weight:600;?', 'font-weight:bold;'),
    # 3. font-weight:400 → font-weight:normal
    (r'font-weight:400;?', 'font-weight:normal;'),
    # 4. 清理双分号 (残留)
    (r';\s*;\s*', '; '),
]

def fix_html_in_xml(content):
    for pattern, replacement in PATTERNS:
        content = re.sub(pattern, replacement, content)
    return content

fixed = 0
for f in INFO_FILES:
    if not f.exists():
        continue
    with open(f, "r", encoding="utf-8") as fh:
        original = fh.read()
    fixed_content = fix_html_in_xml(original)
    if fixed_content != original:
        bak = f.with_suffix(f.suffix + ".bak2")
        with open(bak, "w", encoding="utf-8") as fh:
            fh.write(original)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(fixed_content)
        fixed += 1
        print(f"  ✓ 已修复: {f.name}")
    else:
        print(f"  - 无需修复: {f.name}")

print(f"\n修复了 {fixed} 个文件。")