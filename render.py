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
font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=28)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=28)

ascent, descent = font.getmetrics()
line_height = ascent + descent

img_tags = []
for i, (title, body) in enumerate(sections):
    img_path = f"images/section_{i+1}.png"
    full_path = os.path.join("site", img_path)

    wrapped_body = textwrap.fill(body.strip(), width=50)
    lines = wrapped_body.count('\n') + 1

    # title counts as 1 line, plus body lines, plus padding
    img_height = 20 + line_height * (1 + lines) + 20

    img = Image.new("RGB", (800, img_height), color="#171717")
    draw = ImageDraw.Draw(img)

    draw.text((20, 20), title, fill="white", font=font_bold)
    draw.text((20, 20 + line_height), wrapped_body, fill="white", font=font)

    img.save(full_path)
    img_tags.append(f'<img src="{img_path}" alt="A picture of a dog! Sorry screen readers">')

# === Step 2: Convert DogContent.md to HTML ===
with open("DogContent.md") as f:
    dog_md = f.read()
dog_html = markdown.markdown(dog_md)

# === Step 3: Write index.html ===
index_path = "site/index.html"
with open(index_path, "w") as f:
    f.write("<html>\n")
    f.write("<head>\n")
    f.write('  <meta charset="UTF-8">\n')
    f.write('  <meta name="viewport" content="width=device-width, initial-scale=1">\n')
    f.write('  <meta name="description" content="Awesome dog facts with images generated from markdown.">\n')
    f.write('  <meta name="author" content="Steffen Blake">\n')
    f.write('  <meta property="og:title" content="Pawfactual — Awesome Totally Real Dog Facts" />\n')
    f.write('  <meta property="og:description" content="Explore amazing totally real dog facts here! This definitely isn't something else!" />\n')
    f.write('  <meta property="og:type" content="website" />\n')
    f.write('  <meta property="og:url" content="https://pawfactual.com/" />\n')
    f.write('  <title>Pawfactual — Awesome Dog Facts</title>\n')
    f.write('  <link rel="stylesheet" href="site.css">\n')
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("\n".join(img_tags) + "\n")
    f.write("<hr>\n")
    f.write(dog_html + "\n")
    f.write("</body>\n")
    f.write("</html>\n")

