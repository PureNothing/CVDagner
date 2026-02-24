from PIL import ImageDraw, Image, ImageFont
import io

def draw_box(image: bytes, boxes, labels, scores) -> Image:
    pil_image = Image.open(io.BytesIO(image))
    draw = ImageDraw.Draw(pil_image)

    for box, label, score in zip(boxes, labels, scores):
        x1, y1, x2, y2 = box
        draw.rectangle(xy=[x1, y1, x2, y2], outline="red", width=2)
        draw.text(xy=(x1, y1), text=f"{label} {score:.2f}", fill="red")

    return pil_image
