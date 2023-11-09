from PIL import Image, ImageDraw, ImageFont
import json
from .editing import convert_to_rgb

with open("config.json") as f:
    cfg = json.loads(f.read())

class AdGenerator:
    def __init__(self):
        self.canvas = Image.new('RGB', (cfg['gen_image_size'][0] + 350, cfg['gen_image_size'][1] + 350), color=(255,255,255))
        self.draw = ImageDraw.Draw(self.canvas)
        self.font = cfg["font"]
        self.logo_width, self.logo_height = cfg['logo_image_size'][0], cfg['logo_image_size'][1]
        self.image_width, self.image_height = cfg['gen_image_size'][0], cfg['gen_image_size'][1]
        
    def adjust_proportions(self, component_width, component_height):
        image_ratio = self.image_width / self.image_height
        canvas_ratio = self.canvas.width / self.canvas.height

        if image_ratio > canvas_ratio: 
            scale_factor = self.canvas.height / self.image_height
        else: 
            scale_factor = self.canvas.width / self.image_width

        adjusted_width = int(component_width * scale_factor)
        adjusted_height = int(component_height * scale_factor)

        return adjusted_width, adjusted_height
        
    def draw_border(self, hex_color, frame_thickness=1, border_offset=20, border_thickness=5, corner_radius=40):
        rgb_color = convert_to_rgb(hex_color)

        top_left = (frame_thickness + border_offset, frame_thickness)
        bottom_right = (self.canvas.width - frame_thickness - border_offset, frame_thickness + border_thickness)

        self.draw.rounded_rectangle([top_left, bottom_right], fill=rgb_color, radius=corner_radius)

        top_left = (frame_thickness + border_offset, self.canvas.height - frame_thickness - border_thickness)
        bottom_right = (self.canvas.width - frame_thickness - border_offset, self.canvas.height - frame_thickness)

        self.draw.rounded_rectangle([top_left, bottom_right], fill=rgb_color, radius=corner_radius)

        self.draw.rectangle([frame_thickness, frame_thickness, self.canvas.width - frame_thickness, self.canvas.height - frame_thickness], outline=(0,0,0), width=frame_thickness*2)
    
    def add_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((self.image_width, self.image_height))
        self.canvas.paste(image, ((self.canvas.width - image.width) // 2, (self.canvas.height - image.width) // 3))
    
    def add_logo(self, logo_path):
        logo = Image.open(logo_path)
        logo = logo.resize((self.logo_width, self.logo_height))
        self.canvas.paste(logo, ((self.canvas.width - logo.width) // 2, int(self.canvas.height * 0.057)))
    
    def add_punchline(self, punchline_text, hex_color, font_size=37):
        try:
            font_large = ImageFont.truetype(self.font, font_size)
            rgb_color = convert_to_rgb(hex_color)
            
            width = self.canvas.width - int(self.canvas.width * 0.05)
            height = self.canvas.height - int(self.canvas.height * 0.05)
            x = 0
            y = int(self.canvas.height * 0.3)
            
            lines = punchline_text.split('\n')
            true_lines = []
            for line in lines:
                if font_large.getsize(line)[0] <= width:
                    true_lines.append(line) 
                else:
                    current_line = ''
                    for word in line.split(' '):
                        if font_large.getsize(current_line + word)[0] <= width:
                            current_line += ' ' + word 
                        else:
                            true_lines.append(current_line)
                            current_line = word 
                    true_lines.append(current_line)
            
            lineheight = font_large.getsize(true_lines[0])[1] 
            y = int(y + height / 2)
            y_offset = - (len(true_lines) * lineheight) / 2
            
            for line in true_lines:
                linewidth = font_large.getsize(line)[0]
                x_offset = (width - linewidth) / 2
                
                self.draw.text(
                    (int(x + x_offset), int(y + y_offset)),
                    line,
                    font=font_large,
                    fill=rgb_color
                )
                y_offset += lineheight
        except Exception as e:
            print(e)
    
    def add_button(self, hex_color, button_text, font_size=15, rectangle_padding=10, radius=10):
        try:
            font_small = ImageFont.truetype(self.font, font_size)
            rgb_color = convert_to_rgb(hex_color)
            
            text_width, text_height = self.draw.textsize(button_text, font=font_small)

            rectangle_width = text_width + 2 * rectangle_padding
            rectangle_height = text_height + 2 * rectangle_padding

            x = (self.canvas.width - rectangle_width) // 2
            y = (self.canvas.height - rectangle_height * 2)

            self.draw.rounded_rectangle([x, y, x + rectangle_width, y + rectangle_height], fill=rgb_color, radius=radius)

            text_x = x + rectangle_padding
            text_y = y + rectangle_padding

            self.draw.text((text_x, text_y), button_text, fill=(255, 255, 255), font=font_small)
        except Exception as e:
            print(e)   

    def get_canvas(self):
        return self.canvas

    def display_ad(self):
        self.canvas.show()

