from PIL import Image, ImageDraw, ImageFont
import re
import os

with open("README.md") as f:
    content = f.read()

sections = re.findall(r"# (.*?)\n(.*?)(?=\n#|\Z)", content, re.DOTALL)

output_dir = "site/images"
os.makedirs(output_dir, exist_ok=True)
font = ImageFont.load_default()

for i, (title, body) in enumerate(sections):
    img = Image.new("RGB", (800, 400), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), title, fill="black", font=font)
    draw.text((20, 60), body.strip(), fill="black", font=font)
    img.save(f"{output_dir}/section_{i+1}.png")
