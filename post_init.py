import subprocess, os
from datetime import datetime
from zoneinfo import ZoneInfo

date = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")
title = input("Enter the title of the post: ")
modified_title =  date + " " +title.replace(" ", "-")

print(modified_title)
category = ['ai-hype', "deep-ai", 'life']
enumerated_category = list(enumerate(category))
category_selected = int(input(f"enter the category for the post choose: {enumerated_category} : "))
category = category[category_selected]

file_content = f"""---
layout: post
title: "{title}"
date: {date}
categories: {category}
---
Write here!!
"""

file_path = f"_posts/{modified_title}.md"
command = ["touch", file_path]
subprocess.run(command)
with open(file_path, "w") as file:
    file.write(file_content)
