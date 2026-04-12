from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import sass

TEMPLATES_DIR = Path("templates")
NOTE_TYPES_DIR = TEMPLATES_DIR / "note_types"
COMPONENTS_DIR = TEMPLATES_DIR / "components"
BUILD_DIR = Path("build")


def create_env():
    return Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        variable_start_string="[[",
        variable_end_string="]]",
        block_start_string="[%",
        block_end_string="%]",
        comment_start_string="[#",
        comment_end_string="#]",
    )


def build_html():
    env = create_env()

    for note_type in NOTE_TYPES_DIR.iterdir():
        if not note_type.is_dir():
            continue

        cards_dir = note_type / "cards"

        for card_type in cards_dir.iterdir():
            if not card_type.is_dir():
                continue

            for template_file in card_type.glob("*.html"):
                template = env.get_template(str(template_file.relative_to(TEMPLATES_DIR)))
                rendered = template.render()

                output = (
                    BUILD_DIR
                    / note_type.name
                    / "cards"
                    / card_type.name
                    / template_file.name
                )

                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(rendered)

                print("built", output)


def build_css():
    for note_type in NOTE_TYPES_DIR.iterdir():
        if not note_type.is_dir():
            continue

        scss_file = note_type / "style.scss"

        if not scss_file.exists():
            continue

        css = sass.compile(
            filename=str(scss_file),
            include_paths=[str(COMPONENTS_DIR)],
        )

        output = BUILD_DIR / note_type.name / "style.css"

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(css)

        print("built", output)


def main():
    build_html()
    build_css()


if __name__ == "__main__":
    main()
