import os
import requests
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, TextClip, AudioFileClip
from PIL import Image
from gtts import gTTS
import argparse

# Monkey-patch for Pillow >= 10 compatibility with MoviePy
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

def download_images_from_products(products, output_folder="downloaded_images"):
    os.makedirs(output_folder, exist_ok=True)
    local_paths = []
    for i, product in enumerate(products):
        image_url = None
        if 'image_urls' in product and product['image_urls']:
            image_url = product['image_urls'][0]
        elif 'image' in product and product['image']:
            image_url = product['image']
        if image_url:
            ext = image_url.split('.')[-1].split('?')[0]
            if ext.lower() not in ["jpg", "jpeg", "png", "webp", "avif"]:
                ext = "jpg"
            local_path = os.path.join(output_folder, f"img_{i}.{ext}")
            try:
                r = requests.get(image_url, timeout=10)
                with open(local_path, "wb") as f:
                    f.write(r.content)
                if ext.lower() == "avif":
                    im = Image.open(local_path)
                    png_path = os.path.splitext(local_path)[0] + ".png"
                    im.save(png_path)
                    local_paths.append(png_path)
                    print(f"Converted {local_path} to {png_path}")
                else:
                    local_paths.append(local_path)
                print(f"Downloaded: {local_path}")
            except Exception as e:
                print(f"Error downloading {image_url}: {e}")
    return local_paths

def make_collage_video_with_captions_logo(image_paths, products, logo_path="logo.png", output_path="products_collage.mp4", duration_per_image=2.5, tts_path="narration.mp3"):
    logo = (ImageClip(logo_path).resize(width=120).set_pos(("right", "bottom")).set_duration(duration_per_image)
            if os.path.exists(logo_path) else None)
    clips = []
    narration_texts = []
    for i, img in enumerate(image_paths):
        product = products[i] if i < len(products) else {}
        title = product.get('title', '')
        price = product.get('price', '')
        source = product.get('source', '').capitalize()
        caption = f"{title}\n${price} | {source}"
        base_clip = ImageClip(img).set_duration(duration_per_image).resize(width=720)
        txt_clip = TextClip(caption, fontsize=36, color='white', font='DejaVu-Sans', bg_color='rgba(0,0,0,0.5)').set_position(('center', 'bottom')).set_duration(duration_per_image)
        layers = [base_clip, txt_clip]
        if logo:
            layers.append(logo)
        final_clip = CompositeVideoClip(layers)
        clips.append(final_clip)
        narration_texts.append(f"{title}, price {price} dollars, from {source}.")
    video = concatenate_videoclips(clips, method="compose")
    narration_text = " ".join(narration_texts)
    tts = gTTS(narration_text, lang='en')
    tts.save(tts_path)
    audio = AudioFileClip(tts_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"Collage video with captions, logo, and narration saved as {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a collage video with captions, logo, and TTS narration from products.json.")
    parser.add_argument("--logo_path", type=str, default="logo.png", help="Path to logo image (default: logo.png)")
    parser.add_argument("--output", type=str, default="products_collage.mp4", help="Output video filename")
    parser.add_argument("--duration", type=float, default=2.5, help="Duration per image (seconds)")
    parser.add_argument("--tts_path", type=str, default="narration.mp3", help="TTS narration filename")
    args = parser.parse_args()
    import json
    with open("products.json", "r") as f:
        products = json.load(f)
    image_paths = download_images_from_products(products)
    make_collage_video_with_captions_logo(
        image_paths, products,
        logo_path=args.logo_path,
        output_path=args.output,
        duration_per_image=args.duration,
        tts_path=args.tts_path
    )
    print("\nTo run with SuggestoAI logo:")
    print("python image_video_collage.py --logo_path logo.png")
    print("To run with AI agent logo:")
    print("python image_video_collage.py --logo_path logo_agent.png") 