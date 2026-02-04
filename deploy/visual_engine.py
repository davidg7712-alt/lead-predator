from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

class CarouselGenerator:
    """
    Genera láminas de texto premium y limpias (Estilo Influencer de LinkedIn).
    Sin IA, solo diseño gráfico puro mediante código.
    """
    def __init__(self, width=1080, height=1350):
        self.width = width
        self.height = height
        # Colores premium (Dark Mode de autoridad)
        # Colores de Autoridad Industrial (Hazard Theme)
        self.bg_color = (13, 17, 23)    # Deep Charcoal
        self.accent_color = (255, 232, 31) # Warning Yellow
        self.text_color = (240, 246, 252)  # Ghost White
        
        # Intentar cargar fuentes
        try:
            self.font_title = ImageFont.truetype("arial.ttf", 85)
            self.font_body = ImageFont.truetype("arial.ttf", 50)
            self.font_footer = ImageFont.truetype("arial.ttf", 35)
        except:
            self.font_title = ImageFont.load_default()
            self.font_body = ImageFont.load_default()
            self.font_footer = ImageFont.load_default()

    def create_slide(self, title, body_points, slide_num, total_slides, footer_text="CONFIDENTIAL - DATA LEAK"):
        """
        Industrial High-Authority Layout.
        Feels like a leaked document from a tech hub.
        """
        img = Image.new('RGB', (self.width, self.height), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Hazard Stripe (Top)
        stripe_w = 40
        for x in range(0, self.width + stripe_w, stripe_w * 2):
            draw.polygon([(x, 0), (x + stripe_w, 0), (x, 25), (x - stripe_w, 25)], fill=self.accent_color)
        
        # Confidential Watermark
        try:
            watermark_font = ImageFont.truetype("arial.ttf", 100)
            draw.text((100, 450), "INTERNAL ONLY", fill=(20, 20, 20), font=watermark_font)
        except:
            pass
            
        # Pagination
        draw.text((self.width - 160, 50), f"SYS-{slide_num:02d}", fill=self.accent_color, font=self.font_footer)
        
        # Header Section
        title_lines = textwrap.wrap(title.upper(), width=15)
        y_text = 180
        for line in title_lines:
            draw.text((80, y_text), line, fill=self.accent_color, font=self.font_title)
            y_text += 105
            
        draw.rectangle([80, y_text + 20, 450, y_text + 35], fill=self.accent_color)
        
        # Content Section
        content_y = y_text + 110
        margin = 80
        
        if isinstance(body_points, list):
            for point in body_points:
                # Square Bullet
                draw.rectangle([margin, content_y + 15, margin + 15, content_y + 30], fill=self.accent_color)
                
                wrapped_point = textwrap.wrap(point, width=35)
                for line in wrapped_point:
                    draw.text((margin + 50, content_y), line, fill=self.text_color, font=self.font_body)
                    content_y += 65
                content_y += 55 
        else:
            wrapped_body = textwrap.wrap(body_points, width=32)
            for line in wrapped_body:
                draw.text((margin, content_y), line, fill=self.text_color, font=self.font_body)
                content_y += 75
                
        # Footer
        draw.text((80, self.height - 80), f"© {footer_text} | DATA-LEAK V16.0", fill=(60, 60, 60), font=self.font_footer)
        
        path = f"generated_slide_{slide_num}.png"
        img.save(path)
        return path

if __name__ == "__main__":
    gen = CarouselGenerator()
    gen.create_slide("EL FIN DEL HYPE", "La IA no va a reemplazar tu trabajo. La persona que use IA para tomar decisiones correctas en ArXiv, sí.", 1, 3)
    print("Slide generado con éxito.")
