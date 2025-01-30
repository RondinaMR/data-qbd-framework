import re

# Functions
def hex_to_rgb(hex_color):
    # Remove the '#' character if it's present
    hex_color = hex_color.lstrip('#')
    # Convert the hex color to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

def rgb_to_hex(rgb):
    # Convert RGB values to a hex color
    r, g, b = rgb
    return f"{r:02X}{g:02X}{b:02X}"

def interpolate_color(min_color, max_color, value):
    # Convert hex colors to RGB
    min_rgb = hex_to_rgb(min_color)
    max_rgb = hex_to_rgb(max_color)

    # Interpolate the RGB values
    interpolated_rgb = tuple(
        int(min_rgb[i] + (max_rgb[i] - min_rgb[i]) * value) for i in range(3)
    )

    # Convert the interpolated RGB values back to hex
    interpolated_color = rgb_to_hex(interpolated_rgb)
    return interpolated_color

def value_to_str(value):
    return f'{value:.2f}'.replace('.', ',')

def risk_color_or_nothing(value,b_index):
    threshold = 0
    addition = ''

    if b_index == 'gini':
        threshold = 0.4
    elif b_index == 'shannon':
        threshold = 0.5
    elif b_index == 'simpson':
        threshold = 0.3
    elif b_index == 'iir':
        threshold = 0.15

    if value < threshold:
        addition = f'\cellcolor[HTML]{{fc8d59}}'
    return addition

def tex_sanitizer(tex_content):
    # Sanitize the TeX content
    tex_content = tex_content.replace('_', '\_')
    tex_content = tex_content.replace('%', '\%')
    tex_content = tex_content.replace('&', '\&')
    tex_content = tex_content.replace('$', '\$')
    tex_content = tex_content.replace('~', '$\sim$')
    return tex_content

def modify_latex_table(input_tex_file, min_color, max_color, dataquality_rule=False):
    # Read the LaTeX file
    with open(input_tex_file, 'r') as f:
        tex_content = f.read()
    position = 0
    # Define a regular expression pattern to match table cells
    cell_pattern = r'\d,\d{3}\s'
    # Find all matches of the pattern
    matches = re.findall(cell_pattern, tex_content)
    # Loop through the matches and update the table cells
    # Dataset-Name & Com-I-1-DevA & Com-I-5 & Acc-I-4 & Con-I-3 & Con-I-2-DevB & Con-I-4-DevC
    for match in matches:
        value = float(match.replace(',', '.'))
        if value > 1.0:
            value = 1.0
        if dataquality_rule and (((position % 6) == 0) or ((position % 6) == 4)):  # Acc-I-4 & Con-I-3
            value = 1 - value
        color = interpolate_color(min_color, max_color, value)
        replacement = f'{match.strip()}\cellcolor[HTML]{{{color}}}'
        tex_content = tex_content.replace(match, replacement, 1)
        position += 1
    # Write the modified content back to the file
    with open(input_tex_file, 'w') as f:
        f.write(tex_content)
    return