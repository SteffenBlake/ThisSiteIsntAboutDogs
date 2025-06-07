from PIL import Image, ImageDraw, ImageFont
import re
import os
import markdown

# === Step 1: Parse README.md and render images ===
with open("README.md") as f:
    content = f.read()

sections = re.findall(r"# (.*?)\n(.*?)(?=\n#|\Z)", content, re.DOTALL)

output_dir = "site/images"
os.makedirs(output_dir, exist_ok=True)
font = ImageFont.load_default()

img_tags = []
for i, (title, body) in enumerate(sections):
    img_path = f"images/section_{i+1}.png"
    full_path = os.path.join("site", img_path)
    img = Image.new("RGB", (800, 400), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), title, fill="black", font=font)
    draw.text((20, 60), body.strip(), fill="black", font=font)
    img.save(full_path)
    img_tags.append(f'<img src="{img_path}" alt="Section {i+1}">')

# === Step 2: Convert DogContent.md to HTML ===
with open("DogContent.md") as f:
    dog_md = f.read()
dog_html = markdown.markdown(dog_md)

# === Step 3: Write index.html ===
index_path = "site/index.html"
with open(index_path, "w") as f:
    f.write("<html>\n<body>\n")
    f.write("\n".join(img_tags))
    f.write("<hr>\n")
    f.write(dog_html)
    f.write("\n</body>\n</html>")
