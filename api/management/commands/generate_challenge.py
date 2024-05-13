import logging

from django.core.management.base import BaseCommand
from django_seed import Seed
from django.conf import settings
from api.models import Challenge, Round
from PIL import Image, ImageFont, ImageDraw


class Command(BaseCommand):
    help = "Create 10 challenges for playing"
    seeder = Seed.seeder()

    def create_number_image(self, number, output_path):
        img = Image.new("RGB", (512, 512), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        # Font
        font = ImageFont.load_default(45)
        d.text((10, 10), str(number), fill=(255, 255, 0), font=font)
        img.save(output_path)

    def handle(self, *args, **options):
        for i in range(1, 11):  # 生成10個 Challenge
            image_output_path = f"./media/generate/{i}.png"
            self.create_number_image(i, image_output_path)
            round_id = i // 3 + 1
            # with open(image_output_path, "rb") as f:
            # content = f.read()
            challenge = Challenge(
                description=f"請畫出一個{i}的圖形",
                image_url=image_output_path[1:],
                round_id=Round.objects.get(id=round_id),
                is_valid=True,
            )
            challenge.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created challenge {challenge}")
            )
