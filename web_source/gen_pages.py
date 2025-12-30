import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

### Generate pages for groups ###

env = Environment(loader=FileSystemLoader("templates"))
group_template = env.get_template("group.html")

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

output_subdir = output_dir / "group"
output_subdir.mkdir(exist_ok=True)

for data_file in Path("database/group").glob("*.yaml"):
    print(f"Generating page for {data_file.stem}...")
    with open(data_file) as f:
        data = yaml.safe_load(f)

    html = group_template.render(data)
    output = output_dir / f"{data_file.stem}.html"
    output.write_text(html)
