from loader import load_config, load_content, load_image, load_font
from generator import TextGenerator

def generate_mail_image():
    settings = load_config()
    content = load_content()
    bg_image = load_image(settings['background_path'])
    font = load_font(settings)

    generator = TextGenerator(settings, content, bg_image, font)
    generator.draw_title()
    generator.draw_paragraphs()
    generator.draw_signature()
    generator.save_image()

if __name__ == '__main__':
    generate_mail_image()
