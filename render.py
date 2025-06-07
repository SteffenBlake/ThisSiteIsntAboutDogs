from PIL import Image, ImageDraw, ImageFont
import re
import os
import markdown
import textwrap
import time

# === Step 1: Parse README.md and render images ===
with open("README.md") as f:
    content = f.read()

sections = re.findall(r"# (.*?)\n(.*?)(?=\n#|\Z)", content, re.DOTALL)

output_dir = "site/images"
os.makedirs(output_dir, exist_ok=True)
font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=28)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=28)

nonce = int(time.time())

ascent, descent = font.getmetrics()
line_height = ascent + descent

img_tags = []
for i, (title, body) in enumerate(sections):
    img_path = f"images/section_{i+1}.png"
    full_path = os.path.join("site", img_path)

    # Preserve paragraph breaks, wrap each paragraph at 50 chars
    paragraphs = body.strip().split('\n\n')
    wrapped_paragraphs = [textwrap.fill(p.replace('\n', ' '), width=50) for p in paragraphs]

    # Count total lines to calculate height
    total_lines = sum(len(p.split('\n')) for p in wrapped_paragraphs)
    # Add spacing between paragraphs (1 extra line per paragraph except last)
    total_lines += len(wrapped_paragraphs) - 1

    # Title is 1 line, plus body lines, plus padding
    img_height = 20 + line_height * (1 + total_lines) + 20

    img = Image.new("RGB", (800, img_height), color="#171717")
    draw = ImageDraw.Draw(img)

    draw.text((20, 20), title, fill="white", font=font_bold)

    y = 20 + line_height  # start below title
    for p in wrapped_paragraphs:
        for line in p.split('\n'):
            draw.text((20, y), line, fill="white", font=font)
            y += line_height
        y += line_height  # extra space between paragraphs

    img.save(full_path)
    # Cache busting images when we re-render new builds
    img_tags.append(f'<img src="{img_path}?v={nonce}" class="img-content" alt="A picture of a dog! Sorry screen readers">')

# === Step 2: Convert DogContent.md to HTML ===
with open("DogContent.md") as f:
    dog_md = f.read()
dog_html = markdown.markdown(dog_md)

# === Step 3: Write index.html ===
index_path = "site/index.html"
with open(index_path, "w") as f:
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('  <meta charset="UTF-8">\n')
    f.write('  <meta name="viewport" content="width=device-width, initial-scale=1">\n')
    f.write('  <meta name="description" content="Awesome dog facts with images generated from markdown.">\n')
    f.write('  <meta name="author" content="Steffen Blake">\n')
    f.write('  <meta property="og:title" content="Pawfactual — Awesome Totally Real Dog Facts" />\n')
    f.write('  <meta property="og:description" content="Explore amazing totally real dog facts here! This definitely isnt something else!" />\n')
    f.write('  <meta property="og:type" content="website" />\n')
    f.write('  <meta property="og:url" content="https://pawfactual.com/" />\n')
    f.write('  <title>Pawfactual — Awesome Dog Facts</title>\n')
    f.write(f'  <link rel="stylesheet" href="site.css?v={nonce}">\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<a href="https://github.com/SteffenBlake/ThisSiteIsntAboutDogs">\n')
    f.write(f'<img src="images/GithubLink.png?v={nonce}" class="github-link" alt="Check this project out on github!">\n')
    f.write('</a>\n')
    f.write('\n'.join(img_tags) + '\n')
    f.write('<hr>\n')
    f.write(dog_html + '\n')
    f.write('</body>\n')
    f.write('</html>\n')
