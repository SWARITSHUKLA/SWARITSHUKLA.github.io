import os
from datetime import datetime
from zoneinfo import ZoneInfo

date = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")
title = input("Enter the title of the note: ").strip()
sanitized_title = title.replace(" ", "-").replace("/", "-").replace("?", "").replace(":", "")
modified_title = f"{date}-{sanitized_title}"

categories = ['deep-learning', 'machine-learning', 'mathematics', 'systems']
print("\nSelect a category:")
for idx, cat in enumerate(categories):
    print(f"  [{idx}] {cat}")

category_idx = int(input(f"Choose category index [0-{len(categories)-1}]: ").strip())
category = categories[category_idx]

pdf_input = input("\nEnter PDF filename or relative path (e.g. 'transformer_notes.pdf'): ").strip()
if not pdf_input.startswith("/") and not pdf_input.startswith("assets/notes/"):
    pdf_path = f"/assets/notes/{pdf_input}"
elif not pdf_input.startswith("/"):
    pdf_path = f"/{pdf_input}"
else:
    pdf_path = pdf_input

description = input("\nEnter a short 1-line description of the note: ").strip()

file_content = f"""---
layout: note
title: "{title}"
date: {date}
category: {category}
pdf: "{pdf_path}"
description: "{description}"
---

<!-- Optional: You can write additional text, key formulas, or takeaways here below the PDF -->
"""

os.makedirs("_notes", exist_ok=True)
os.makedirs("assets/notes", exist_ok=True)

file_path = f"_notes/{modified_title}.md"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(file_content)

print(f"\n✓ Created note scaffold: {file_path}")
print(f"✓ Make sure your PDF is placed at: .{pdf_path}")
