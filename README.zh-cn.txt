# Stardew Valley Letter Generator

[English](./README_EN.md) | 简体中文

<div style="text-align:center">
  <img src="./example_output/result.png" alt="Stardew Valley Letter Generator" />
</div>

<p style="text-align:center">
  Custom generate Stardew Valley letter images
</p>

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
mail_generator/
├── config/
│   ├── generate_setting.json  # Generator configuration file
│   └── mail_content.json      # Mail content configuration file
├── fonts/
│   └── Kingnammm-Maiyuan.ttf  # Default font file
├── images/
│   └── mail.png               # Background image
├── src/
│   ├── generator.py           # Main program
│   └── loader.py              # Configuration loader
├── output/                    # Output directory
│   └── result.png             # Generated image
├── requirements.txt           # Project dependencies
└── README.md                  # Documentation
```

## Usage

### Configuration Files

#### generate_setting.json
```text
{
    "background_path": "mail.png",      // Background image name, stored in images/
    "use_system_font": false,           // Whether to use system font
    "font_path": "path/to/font",        // Custom font path
    "font_size": 27,                    // Font size
    "margin_left": 7,                   // Left margin (percentage)
    "margin_top": 7,                    // Top margin (percentage)
    "margin_right": 7,                  // Right margin (percentage)
    "paragraph_spacing": 10,            // Paragraph spacing (pixels)
    "line_spacing": 8,                  // Line spacing (pixels)
    "text_color": [108, 79, 45]         // Text color
}
```

Note that text color supports both RGB and Hexadecimal representations:
```text
{
    "text_color": [108, 79, 45],     // ok
    "text_color": "#6C4F2D"          // ok
}
```

#### mail_content.json
```json
{
    "title": "Title",
    "paragraph": "Body content\nUse \\n for line breaks",
    "sign": "Signature"
}
```

### Running the Program

```bash
python src/generator.py
```

The generated image will be saved as `output/result.png`.

## Roadmap
- Add PC GUI version
- Add "Attached xxx" content found in original Stardew Valley letters
- Rewrite using React Native and release an Android mobile app
