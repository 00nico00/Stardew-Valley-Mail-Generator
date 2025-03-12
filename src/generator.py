from PIL import Image, ImageDraw, ImageFont
import json
import os

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)

def calculate_margins(bg_width, bg_height, settings):
    left = bg_width * settings["margin_left"] / 100
    top = bg_height * settings["margin_top"] / 100
    right = bg_width * settings["margin_right"] / 100

    return left, top, right

def wrap_text(text, font, max_width):
    """自动换行文本，基于实际像素宽度"""
    lines = []
    words = text.split()
    current_line = []

    for word in words:
        # 检查当前行加上新词后的宽度
        test_line = ' '.join(current_line + [word])
        test_width = font.getlength(test_line)
        if test_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # 单个词超过行宽，强制分割
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_text_element(draw, text, font, position, max_width, line_spacing=10, align='left'):
    """绘制文本元素（自动换行）"""
    x, y = position
    lines = wrap_text(text, font, max_width)
    
    for line in lines:
        line_width = font.getlength(line)
        if align == 'center':
            x_offset = (max_width - line_width) / 2
        elif align == 'right':
            x_offset = max_width - line_width
        else:  # left
            x_offset = 0
        draw.text((x + x_offset, y), line, font=font, fill='black')
        y += font.size + line_spacing
    return y  # 返回最终的y坐标

def main():
    # 加载配置
    generate_settings = load_config('config/generate_setting.json')
    mail_content = load_config('config/mail_content.json')

    # 加载背景图
    bg_path = os.path.join('images', generate_settings['background_path'])
    if not os.path.exists(bg_path):
        raise FileNotFoundError(f"背景图不存在：{bg_path}")
    bg_image = Image.open(bg_path)
    bg_width, bg_height = bg_image.size

    # 计算边距和文本区域
    left_margin, top_margin, right_margin = calculate_margins(bg_width, bg_height, generate_settings)
    text_area_width = bg_width - left_margin - right_margin

    # 加载字体
    font_size = generate_settings['font_size']
    font_name = generate_settings['font_name']
    try:
        font = ImageFont.truetype(font_name, font_size)
    except IOError:
        # 回退到默认字体
        print(f"找不到字体\"{font_name}\", 已更换为默认字体")
        font = ImageFont.load_default(size=font_size)

    draw = ImageDraw.Draw(bg_image)

    # 初始绘制位置
    current_y = top_margin

    # 绘制标题（居中）
    if 'title' in mail_content:
        title = mail_content['title']
        current_y = draw_text_element(
            draw, title, font,
            position=(left_margin, current_y),
            max_width=text_area_width,
            align='center'
        ) + 20  # 增加段落间距

    # 绘制段落（左对齐）
    if 'paragraph' in mail_content:
        paragraph = mail_content['paragraph']
        current_y = draw_text_element(
            draw, paragraph, font,
            position=(left_margin, current_y),
            max_width=text_area_width,
            align='left'
        ) + 20

    # 绘制落款（右对齐）
    if 'sign' in mail_content:
        sign = mail_content['sign']
        # 计算落款位置（从底部向上）
        sign_lines = wrap_text(sign, font, text_area_width)
        sign_height = len(sign_lines) * (font.size + 10)
        sign_y = bg_height - generate_settings.get('bottom_margin', 50) - sign_height
        draw_text_element(
            draw, sign, font,
            position=(left_margin, sign_y),
            max_width=text_area_width,
            align='right'
        )

    # 保存结果
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'result.png')
    bg_image.save(output_path)
    print(f"图片已生成至：{output_path}")

if __name__ == '__main__':
    main()
