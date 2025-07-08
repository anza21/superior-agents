import os
import requests
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image
# Monkey-patch PIL.Image.ANTIALIAS for MoviePy compatibility
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

if hasattr(Image, 'Resampling'):
    RESAMPLE = Image.Resampling.LANCZOS
else:
    RESAMPLE = Image.ANTIALIAS

def download_images(image_urls, output_folder="downloaded_images"):
    os.makedirs(output_folder, exist_ok=True)
    local_paths = []
    for i, url in enumerate(image_urls):
        try:
            ext = url.split('.')[-1].split('?')[0]
            if ext.lower() not in ["jpg", "jpeg", "png", "webp", "avif"]:
                ext = "jpg"
            local_path = os.path.join(output_folder, f"img_{i}.{ext}")
            r = requests.get(url, timeout=10)
            with open(local_path, "wb") as f:
                f.write(r.content)
            # Convert AVIF to PNG for MoviePy compatibility
            if ext.lower() == "avif":
                try:
                    im = Image.open(local_path)
                    png_path = os.path.splitext(local_path)[0] + ".png"
                    im.save(png_path)
                    local_paths.append(png_path)
                    print(f"Converted {local_path} to {png_path}")
                except Exception as e:
                    print(f"Error converting {local_path} to PNG: {e}")
            else:
                local_paths.append(local_path)
            print(f"Downloaded: {local_path}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
    return local_paths

def make_slideshow(image_paths, output_path="ali_product_video.mp4", duration_per_image=2.5):
    clips = [ImageClip(img).set_duration(duration_per_image).resize(width=720) for img in image_paths]
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"Slideshow video saved as {output_path}")

# Εικόνες από AliExpress
image_urls = [
    "https://ae-pic-a1.aliexpress-media.com/kf/A31f1610de31b46b78cfd17a26d297ad7S.png_220x220.png_.avif",
    "https://ae-pic-a1.aliexpress-media.com/kf/A328ebaa18cc04f6f94f7412e7cbe33f4r.png_220x220.png_.avif",
    "https://ae-pic-a1.aliexpress-media.com/kf/Aeac96766008d4474b833506a33a67cf82.png_220x220.png_.avif",
    "https://ae-pic-a1.aliexpress-media.com/kf/A61ae96ea0a774d0ca1af2c946e2d1913B.png_220x220.png_.avif",
    "https://ae-pic-a1.aliexpress-media.com/kf/Ad88cea5d1ce54c878b0baadf52dcfd4aw.png_220x220.png_.avif",
    "https://ae-pic-a1.aliexpress-media.com/kf/Ac22cd85005584351af0e0fe1d51b53bbV.png_220x220.png_.avif"
]

# 1. Κατέβασε τις εικόνες
downloaded_images = download_images(image_urls)

# 2. Φτιάξε το video
make_slideshow(downloaded_images, output_path="ali_product_video.mp4", duration_per_image=2.5) 