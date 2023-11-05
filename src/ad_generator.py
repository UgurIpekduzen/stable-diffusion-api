from PIL import Image, ImageDraw, ImageFont

class AdGenerator:
    def __init__(self, image):
        self.canvas = Image.new('RGB', (image.width + 300, image.height + 300), color="#FFFFFF")
        self.draw = ImageDraw.Draw(self.canvas)
        self.font = "content/DMSerifDisplay-Regular.ttf"

    def draw_border(self, color, frame_thickness=1, border_offset=20, border_thickness=5, corner_radius=40):
        # Define the positions for the rounded rectangle
        top_left = (frame_thickness + border_offset, frame_thickness)
        bottom_right = (self.canvas.width - frame_thickness - border_offset, frame_thickness + border_thickness)

        # Draw the top rounded border line
        self.draw.rounded_rectangle([top_left, bottom_right], fill=color, radius=corner_radius)

        # Adjust the bottom positions for the rounded rectangle
        top_left = (frame_thickness + border_offset, self.canvas.height - frame_thickness - border_thickness)
        bottom_right = (self.canvas.width - frame_thickness - border_offset, self.canvas.height - frame_thickness)

        # Draw the bottom rounded border line
        self.draw.rounded_rectangle([top_left, bottom_right], fill=color, radius=corner_radius)

        self.draw.rectangle([frame_thickness, frame_thickness, self.canvas.width - frame_thickness, self.canvas.height - frame_thickness], outline="#000000", width=frame_thickness*2)
    
    def add_image(self, image_path):
        # Place the logo at the top
        image = Image.open(image_path)
        self.canvas.paste(image, ((self.canvas.width - image.width) // 2, (self.canvas.height - image.width) // 3))
        # self.canvas

    def add_logo(self, logo_path):
        logo = Image.open(logo_path)
        self.canvas.paste(logo, (int((self.canvas.width - logo.width) / 2), 20))

    def add_punchline(self, punchline_text, text_color, font_size=37):
        font_large = ImageFont.truetype(self.font, font_size)

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
                fill= text_color,
            )
            y_offset += lineheight
    
    def add_button(self, button_color, button_text, font_size=15, rectangle_padding = 10, radius=10):
        font_small = ImageFont.truetype(self.font, font_size)

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
        self.draw.rounded_rectangle([x, y, x + rectangle_width, y + rectangle_height], fill=button_color, radius=radius)

        # Calculate the position to center the text within the rectangle
        text_x = x + rectangle_padding
        text_y = y + rectangle_padding

        # Draw the text within the rectangle
        self.draw.text((text_x, text_y), button_text, fill="#FFFFFF", font=font_small)

    def display_ad(self):
        self.canvas.show()