from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ex_simbols = ["_", "*", "`", "["]


def render_template(template_file: str, *args, **kwargs):
    template_path = Path(__file__).resolve().parent.parent.joinpath("templates/")
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_file)
    return template.render(**kwargs)