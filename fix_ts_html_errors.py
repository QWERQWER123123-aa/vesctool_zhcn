# fix_ts_html_errors.py
# 修复 vesc_tool_zh_CN.ts 中 PageWelcome 翻译的 HTML 语法错误

import re

TS_PATH = r"f:\VESC\vesc_tool-master\vesc_tool-master\vesc_tool_zh_CN.ts"

with open(TS_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 错误1: <palign=  →  <p align=  (全局替换，两处都会修复)
content = content.replace("&lt;palign=&quot;", "&lt;p align=&quot;")

# 错误2: font-style:italic; 在标签内容区 → 移入 style 属性
old_span = '&lt;span style=&quot;font-size:14pt;&quot;&gt; font-style:italic;&quot;&gt;设置向导'
new_span = '&lt;span style=&quot;font-size:14pt; font-style:italic;&quot;&gt;设置向导'
content = content.replace(old_span, new_span)

with open(TS_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. Fixed:")
print("  1. &lt;palign= → &lt;p align=  (2 occurrences)")
print("  2. font-style:italic; moved into style attribute")