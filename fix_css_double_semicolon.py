#!/usr/bin/env python3
# fix_css_double_semicolon.py
# 修复 info.xml 中 HTML 的 ;; 双分号问题，防止 CSS font-style:italic 解析失败

import glob
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INFO_FILES = list(BASE_DIR.glob("res/config/*/info.xml"))

print(f"找到 {len(INFO_FILES)} 个 info.xml 文件")
fixed_count = 0

for f in INFO_FILES:
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()

    # 修复模式: ; ; → ;
    # 匹配 ;[空格];[空格] → ;[空格]
    new_content = re.sub(r';\s*;\s*font-weight', r'; font-weight', content)
    new_content = re.sub(r';\s*;\s*font-style', r'; font-style', new_content)

    # 更精确的修复: 查找 description 中的 ;; 模式
    # 模式: ; ; font-weight → ; font-weight
    new_content = re.sub(
        r'(&quot;)\s*font-family:.*?;\s*;\s*',
        lambda m: re.sub(r';\s*;\s*', '; ', m.group()),
        new_content
    )

    if new_content != content:
        bak = f.with_suffix(".xml.bak")
        with open(bak, "w", encoding="utf-8") as fh:
            fh.write(content)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(new_content)
        fixed_count += 1
        print(f"  已修复: {f.name}")
    else:
        print(f"  无需修复: {f.name}")

print(f"\n完成! 修复了 {fixed_count} 个文件。")