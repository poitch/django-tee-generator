import io
import re
import os
import logging

from django.conf import settings
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponse

from django.views.generic.base import View
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

logger = logging.getLogger(__name__)

class GeneratorView(View):
    def get(self, request, shape, color, text_color, font, sentence, filename):
        BASE_DIR = Path(__file__).resolve().parent

        regex = "([A-Fa-f0-9]{2})([A-Fa-f0-9]{2})([A-Fa-f0-9]{2})"
        p = re.compile(regex)

        # Color
        result = re.search(p, color)
        if result is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid color'})
        c = (int(result.group(1), 16), int(result.group(2), 16), int(result.group(3), 16))
        logger.debug(f'Using color {c}')


        # Text Color
        result = re.search(p, text_color)
        if result is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid text color'})
        tc = (int(result.group(1), 16), int(result.group(2), 16), int(result.group(3), 16))
        logger.debug(f'Using text color {tc}')

        # Fonts
        fonts = {
            'avenir': (os.path.join(BASE_DIR, 'assets', 'Avenir Next.ttc'), 8),
            'helvetica': (os.path.join(BASE_DIR, 'assets', 'Helvetica.ttc'), 1),
        }
        font_file = fonts['avenir']
        if font.lower() in fonts:
            font_file = fonts[font.lower()]

        logger.debug(f'Using font {font_file}')
        lines = sentence.split('/')
        font = ImageFont.truetype(font_file[0], size=108, index=font_file[1])

        # Find the longest line first, to figure out the best font size
        longest = None
        for line in lines:
            if longest is None or len(line) > len(longest):
                longest = line

        for size in range(108, 300):
            font = ImageFont.truetype(font_file[0], size=size, index=font_file[1])
            dimensions = font.getsize(longest)
            if dimensions[0] > 700:
                break

        #
        # DRAW
        #
        output = Image.open(os.path.join(BASE_DIR, 'assets', 'crew_background_lg.png'))
        mask = Image.open(os.path.join(BASE_DIR, 'assets', 'crew_mask_lg.png')).convert('L')

        colorized = Image.new("RGBA", mask.size, color=c)
        output.paste(colorized, (0, 0), mask)

        wrinkles = Image.open(os.path.join(BASE_DIR, 'assets', 'crew_wrinkles_lg.png'))

        # Recompute wrinkle colors
        w = wrinkles.size[0]
        h = wrinkles.size[1]
        for i in range(0, w):
            for j in range(0, h):
                data = wrinkles.getpixel((i, j))
                if data[3] != 0:
                    r = int(c[0] * 237 / data[0])
                    g = int(c[1] * 237 / data[1])
                    b = int(c[2] * 237 / data[2])
                    alpha = data[3]
                    wrinkles.putpixel((i, j), (r, g, b, alpha))

        output.paste(wrinkles, (128,297), wrinkles)

        # Draw text
        d = ImageDraw.Draw(output)
        x = 375
        y = 450
        for line in lines:
            dimensions = font.getsize(line)
            d.text((x, y), line, font=font, fill=tc)
            y = y + dimensions[1]

        buffer = io.BytesIO()
        output.save(buffer, format='PNG')

        return HttpResponse(buffer.getvalue(), content_type='image/png')

