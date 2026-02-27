from PIL import ImageDraw, Image, ImageFont
import io

def draw_box(image: bytes, boxes, labels, scores) -> bytes:
    pil_image = Image.open(io.BytesIO(image))
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype("arial.ttf", size=25)

    for box, label, score in zip(boxes, labels, scores):
        x1, y1, x2, y2 = box
        draw.rectangle(xy=[x1, y1, x2, y2], outline="red", width=2)
        draw.text(xy=(x1, y1), text=f"{label} {score:.2f}", fill="red", font=font)
    
    bytes_image = io.BytesIO()
    pil_image.save(bytes_image, format="JPEG")

    return bytes_image.getvalue()
