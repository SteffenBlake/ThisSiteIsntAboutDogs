from PIL import Image, ImageDraw, ImageFont
import re
import os
import markdown
import textwrap

# === Step 1: Parse README.md and render images ===
with open("README.md") as f:
    content = f.read()

sections = re.findall(r"# (.*?)\n(.*?)(?=\n#|\Z)", content, re.DOTALL)

output_dir = "site/images"
os.makedirs(output_dir, exist_ok=True)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=28)

img_tags = []
for i, (title, body) in enumerate(sections):
    img_path = f"images/section_{i+1}.png"
    full_path = os.path.join("site", img_path)

    wrapped_body = textwrap.fill(body.strip(), width=80)
    text = f"{title}\n{wrapped_body}"

    # Measure text height for dynamic image sizing
    dummy_img = Image.new("RGB", (800, 10))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.multiline_textbbox((20, 20), text, font=font)
    img_height = bbox[3] + 20  # add some padding

    img = Image.new("RGB", (800, img_height), color="#171717")
    draw = ImageDraw.Draw(img)
    draw.multiline_text((20, 20), text, fill="white", font=font)

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
