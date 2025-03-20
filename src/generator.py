from PIL import ImageDraw
import os

class TextGenerator:
    OUTPUT_PATH = 'output/result.png'
    DEFAULT_PARAGRAPH_SPACING = 10      # 默认段落间距
    DEFAULT_LINE_SPACING = 8            # 默认行间距
    DEFAULT_TEXT_COLOR = (108, 79, 45)  # 默认文字颜色

    def __init__(self, settings, content, image, font):
        self.settings = settings
        self.content = content
        self.image = image
        self.font = font
        self.draw = ImageDraw.Draw(image)
        self.width, self.height = image.size
        self.margins = self._calculate_margins()
        self.text_area_width = self.width - self.margins[0] - self.margins[2]
        self.current_y = self.margins[1]  # 从顶部边距开始

        self.paragraph_spacing = settings.get('paragraph_spacing', self.DEFAULT_PARAGRAPH_SPACING)
        self.line_spacing = settings.get('line_spacing', self.DEFAULT_LINE_SPACING)
        self.text_color = self._parse_color(settings.get('text_color', self.DEFAULT_TEXT_COLOR))

    def _calculate_margins(self):
        left = self.width * self.settings["margin_left"] / 100
        top = self.height * self.settings["margin_top"] / 100
        right = self.width * self.settings["margin_right"] / 100
        return left, top, right

    def _wrap_text(self, text, max_width):
        if not text:
            return []

        lines = []
        current_line = ""
        
        # 处理英文单词
        words = []
        temp_word = ""
        
        # 将文本分割成单词（英文）和单字符（中文）
        for char in text:
            if ord(char) < 128:  # ASCII字符
                if char.isspace():
                    if temp_word:
                        words.append(temp_word)
                        temp_word = ""
                    words.append(char)
                else:
                    temp_word += char
            else:  # 非ASCII字符（如中文）
                if temp_word:
                    words.append(temp_word)
                    temp_word = ""
                words.append(char)
        
        if temp_word:
            words.append(temp_word)
        
        # 处理换行
        for word in words:
            test_line = current_line + word
            test_width = self.font.getlength(test_line)
            
            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                    current_line = word
                else:
                    # 单个词超过宽度，需要按字符拆分
                    for char in word:
                        char_width = self.font.getlength(char)
                        if char_width <= max_width:
                            if current_line:
                                test_line = current_line + char
                                test_width = self.font.getlength(test_line)
                                if test_width <= max_width:
                                    current_line = test_line
                                else:
                                    lines.append(current_line.strip())
                                    current_line = char
                            else:
                                current_line = char
                        else:
                            if current_line:
                                lines.append(current_line.strip())
                            lines.append(char)
                            current_line = ""
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines

    def _draw_text_element(self, text, position, max_width, line_spacing=None, align='left'):
        x, y = position
        lines = self._wrap_text(text, max_width)
        
        # 使用传入的行间距或默认值
        line_spacing = line_spacing if line_spacing is not None else self.line_spacing
        
        for line in lines:
            line_width = self.font.getlength(line)
            if align == 'center':
                x_offset = (max_width - line_width) / 2
            elif align == 'right':
                x_offset = max_width - line_width
            else:  # left
                x_offset = 0
            self.draw.text((x + x_offset, y), line, font=self.font, fill=self.text_color)
            y += self.font.size + line_spacing
        return y  # 返回最终的y坐标

    def draw_title(self):
        if 'title' in self.content:
            self.current_y = self._draw_text_element(
                self.content['title'],
                position=(self.margins[0], self.current_y),
                max_width=self.text_area_width,
                align='left'
            ) + self.paragraph_spacing

    def draw_paragraphs(self):
        if 'paragraph' in self.content:
            paragraphs = self.content['paragraph'].split('\n')
            for p in paragraphs:
                if p.strip():
                    self.current_y = self._draw_text_element(
                        p,
                        position=(self.margins[0], self.current_y),
                        max_width=self.text_area_width,
                        align='left'
                    ) + self.paragraph_spacing

    def draw_signature(self):
        if 'sign' in self.content:
            self._draw_text_element(
                self.content['sign'],
                position=(self.margins[0], self.current_y),
                max_width=self.text_area_width,
                align='left'
            )

    def save_image(self, output_path=OUTPUT_PATH):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.image.save(output_path)
        print(f"图片已生成至：{output_path}")

    def _parse_color(self, color):
        if isinstance(color, (tuple, list)) and len(color) >= 3:
            # RGB或RGBA元组
            return tuple(int(c) for c in color[:3])
        elif isinstance(color, str) and color.startswith('#'):
            # 十六进制颜色代码
            color = color.lstrip('#')
            if len(color) == 6:
                return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        # 如果无法解析，返回默认颜色
        return self.DEFAULT_TEXT_COLOR 