from PIL import Image, ImageDraw, ImageFont
import json

with open("config.json") as f:
    cfg = json.loads(f.read())

def hex_to_rgb(hexcode):
    try:
        # Hex renk kodundan gereksiz karakterleri kaldırın ve doğrudan RGB'ye çevirin
        hexcode = hexcode.replace('"', '').lstrip("#") 
        rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
        return rgb
    except ValueError:
        # Hata durumunda varsayılan bir değer döndürün (örneğin siyah renk: (0, 0, 0))
        return (0, 0, 0)

class AdGenerator:
    def __init__(self, image):
        self.canvas = Image.new('RGB', (image.width + 300, image.height + 300), color=(255,255,255))
        self.draw = ImageDraw.Draw(self.canvas)
        self.font = cfg["font"]

    def draw_border(self, hex_color, frame_thickness=1, border_offset=20, border_thickness=5, corner_radius=40):
        rgb_color = hex_to_rgb(hex_color)
        # Define the positions for the rounded rectangle
        top_left = (frame_thickness + border_offset, frame_thickness)
        bottom_right = (self.canvas.width - frame_thickness - border_offset, frame_thickness + border_thickness)

        # Draw the top rounded border line
        self.draw.rounded_rectangle([top_left, bottom_right], fill=rgb_color, radius=corner_radius)

        # Adjust the bottom positions for the rounded rectangle
        top_left = (frame_thickness + border_offset, self.canvas.height - frame_thickness - border_thickness)
        bottom_right = (self.canvas.width - frame_thickness - border_offset, self.canvas.height - frame_thickness)

        # Draw the bottom rounded border line
        self.draw.rounded_rectangle([top_left, bottom_right], fill=rgb_color, radius=corner_radius)

        self.draw.rectangle([frame_thickness, frame_thickness, self.canvas.width - frame_thickness, self.canvas.height - frame_thickness], outline=(0,0,0), width=frame_thickness*2)
    
    def add_image(self, image):
        # Place the logo at the top
        # image = Image.open(image_path)
        self.canvas.paste(image, ((self.canvas.width - image.width) // 2, (self.canvas.height - image.width) // 3))
    def add_logo(self, logo_path):
        logo = Image.open(logo_path)
        self.canvas.paste(logo, (int((self.canvas.width - logo.width) / 2), 20))

    def add_punchline(self, punchline_text, hex_color, font_size=37):
        try:
            print(punchline_text)
            font_large = ImageFont.truetype(self.font, font_size)
            rgb_color = hex_to_rgb(hex_color)
            x = 0
            y = 150
            width = self.canvas.width - 20
            height = self.canvas.height - 20
            
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
    
    def add_button(self, hex_color, button_text, font_size=15, rectangle_padding = 10, radius=10):
        try:
            font_small = ImageFont.truetype(self.font, font_size)
            rgb_color = hex_to_rgb(hex_color)
            # Calculate the size of the text
            text_width, text_height = self.draw.textsize(button_text, font=font_small)

            # Define the rectangle's dimensions
            # Inner padding between rectangle and text
            rectangle_width = text_width + 2 * rectangle_padding
            rectangle_height = text_height + 2 * rectangle_padding

            # Calculate the position to center the rectangle in the image
            x = (self.canvas.width - rectangle_width) // 2
            y = (self.canvas.height - rectangle_height * 2)

            # Draw the rectangle with the calculated position
            self.draw.rounded_rectangle([x, y, x + rectangle_width, y + rectangle_height], fill=rgb_color, radius=radius)

            # Calculate the position to center the text within the rectangle
            text_x = x + rectangle_padding
            text_y = y + rectangle_padding

            # Draw the text within the rectangle
            self.draw.text((text_x, text_y), button_text, fill=(255, 255, 255), font=font_small)
        except Exception as e:
            print(e)   

    def get_canvas(self):
        return self.canvas

    def display_ad(self):
        self.canvas.show()

# class AdGenerator:
#     def __init__(self, image):
#         self.image = image
#         self.canvas = Image.new('RGB', (image.width + 300, image.height + 300), color=(255, 255, 255))
#         self.draw = ImageDraw.Draw(self.canvas)
#         self.font = cfg["font"]
#         self.logo_width, self.logo_height = 87, 51
#         self.photo_width, self.photo_height = 348, 208

#     def adjust_proportions(self, component_width, component_height):
#         image_ratio = self.image.width / self.image.height
#         canvas_ratio = self.canvas.width / self.canvas.height

#         # Determine the scaling factor based on image and canvas ratios
#         if image_ratio > canvas_ratio:  # Scale based on height
#             scale_factor = self.canvas.height / self.image.height
#         else:  # Scale based on width
#             scale_factor = self.canvas.width / self.image.width

#         # Adjust component sizes according to the scale factor
#         adjusted_width = int(component_width * scale_factor)
#         adjusted_height = int(component_height * scale_factor)

#         return adjusted_width, adjusted_height

#     def draw_border(self, hex_color, frame_thickness=1, border_offset=20, border_thickness=5, corner_radius=40):
#         rgb_color = hex_to_rgb(hex_color)
#         # Define the positions for the rounded rectangle
#         top_left = (frame_thickness + border_offset, frame_thickness)
#         bottom_right = (self.canvas.width - frame_thickness - border_offset, frame_thickness + border_thickness)

#         # Draw the top rounded border line
#         self.draw.rounded_rectangle([top_left, bottom_right], fill=rgb_color, radius=corner_radius)

#         # Adjust the bottom positions for the rounded rectangle
#         top_left = (frame_thickness + border_offset, self.canvas.height - frame_thickness - border_thickness)
#         bottom_right = (self.canvas.width - frame_thickness - border_offset, self.canvas.height - frame_thickness)

#         # Draw the bottom rounded border line
#         self.draw.rounded_rectangle([top_left, bottom_right], fill=rgb_color, radius=corner_radius)

#         self.draw.rectangle([frame_thickness, frame_thickness, self.canvas.width - frame_thickness, self.canvas.height - frame_thickness], outline=(0, 0, 0), width=frame_thickness * 2)

#     def add_logo(self, logo_path):
#         logo = Image.open(logo_path)
#         adjusted_width, adjusted_height = self.adjust_proportions(self.logo_width, self.logo_height)
#         logo = logo.resize((adjusted_width, adjusted_height))
#         self.canvas.paste(logo, ((self.canvas.width - adjusted_width) // 2, 20))

#     def add_image(self, image_path):
#         image = Image.open(image_path)
#         adjusted_width, adjusted_height = self.adjust_proportions(self.photo_width, self.photo_height)
#         image = image.resize((adjusted_width, adjusted_height))
#         self.canvas.paste(image, ((self.canvas.width - adjusted_width) // 2, (self.canvas.height - adjusted_height) // 3))

#     def add_punchline(self, punchline_text, hex_color, font_size=37):
#         try:
#             font_large = ImageFont.truetype(self.font, font_size)
#             rgb_color = hex_to_rgb(hex_color)
#             x = 0
#             y = int(self.canvas.height * 0.4)
#             width = self.canvas.width - int(self.canvas.width * 0.05)
#             height = self.canvas.height - int(self.canvas.height * 0.05)

#             lines = punchline_text.split('\n')
#             true_lines = []
#             for line in lines:
#                 if font_large.getsize(line)[0] <= width:
#                     true_lines.append(line)
#                 else:
#                     current_line = ''
#                     for word in line.split(' '):
#                         if font_large.getsize(current_line + word)[0] <= width:
#                             current_line += ' ' + word
#                         else:
#                             true_lines.append(current_line)
#                             current_line = word
#                     true_lines.append(current_line)

#             lineheight = font_large.getsize(true_lines[0])[1]
#             y_offset = - (len(true_lines) * lineheight) / 2

#             for line in true_lines:
#                 linewidth = font_large.getsize(line)[0]
#                 x_offset = (width - linewidth) / 2

#                 self.draw.text(
#                     (int(x + x_offset), int(y + y_offset)),
#                     line,
#                     font=font_large,
#                     fill=rgb_color
#                 )
#                 y_offset += lineheight
#         except Exception as e:
#             print(e)

#     def add_button(self, hex_color, button_text, font_size=15, rectangle_padding=10, radius=10):
#         try:
#             font_small = ImageFont.truetype(self.font, font_size)
#             rgb_color = hex_to_rgb(hex_color)

#             # Calculate the size of the text
#             text_width, text_height = self.draw.textsize(button_text, font=font_small)

#             # Define the rectangle's dimensions
#             # Inner padding between rectangle and text
#             rectangle_width = text_width + 2 * rectangle_padding
#             rectangle_height = text_height + 2 * rectangle_padding

#             # Calculate the position to center the rectangle in the image
#             x = (self.canvas.width - rectangle_width) // 2
#             y = int(self.canvas.height * 0.7)

#             # Draw the rectangle with the calculated position
#             self.draw.rounded_rectangle([x, y, x + rectangle_width, y + rectangle_height], fill=rgb_color, radius=radius)

#             # Calculate the position to center the text within the rectangle
#             text_x = x + rectangle_padding
#             text_y = y + rectangle_padding

#             # Draw the text within the rectangle
#             self.draw.text((text_x, text_y), button_text, fill=(255, 255, 255), font=font_small)
#         except Exception as e:
#             print(e)

#     def get_canvas(self):
#         return self.canvas

#     def display_ad(self):
#         self.canvas.show()
