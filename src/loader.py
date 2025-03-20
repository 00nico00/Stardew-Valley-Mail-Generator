import json
import os
from PIL import Image, ImageFont

SETTINGS_PATH = 'config/generate_setting.json'
CONTENT_PATH = 'config/mail_content.json'

def _load_impl(config_path):
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_config():
    return _load_impl(SETTINGS_PATH)

def load_content():
    return _load_impl(CONTENT_PATH)
    
def load_image(image_path):
    bg_path = os.path.join('images', image_path)
    if not os.path.exists(bg_path):
        raise FileNotFoundError(f"背景图不存在：{bg_path}")
    bg_image = Image.open(bg_path)
    return bg_image

def load_font(generate_settings):
    use_system_font = generate_settings.get('use_system_font', True)
    font_size = generate_settings['font_size']
    font_path = generate_settings['font_path']  # 确保配置项名称改为 font_path

    # 字体加载逻辑
    if not use_system_font:
        # 尝试定位字体文件
        original_path = font_path
        
        # 路径校验逻辑
        if not os.path.isfile(font_path):
            # 尝试从 fonts/ 子目录查找
            fallback_path = os.path.join("fonts", os.path.basename(font_path))
            if os.path.isfile(fallback_path):
                font_path = fallback_path
            else:
                # 获取当前工作目录用于错误提示
                cwd = os.getcwd()
                raise FileNotFoundError(
                    f"字体文件未找到！请检查路径配置：\n"
                    f"- 原始配置路径: {original_path}\n"
                    f"- 尝试回退路径: {fallback_path}\n"
                    f"- 当前工作目录: {cwd}\n"
                    f"请确保字体文件存在且路径正确"
                )

        # 加载字体文件
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception as e:
            raise RuntimeError(f"字体加载失败：{font_path}，错误信息：{str(e)}")
    else:
        # 使用系统字体
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"系统字体 {font_path} 不可用，已回退到默认字体")
            font = ImageFont.load_default(size=font_size)
    
    return font