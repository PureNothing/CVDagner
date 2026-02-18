import pandas as pd
import os
import urllib.parse
from PIL import Image

df = pd.read_csv("BentoService/FineTune/yolo_dataset/csv/war_tech_gont-export.csv")

df['image_decoded'] = df['image'].apply(lambda x: urllib.parse.unquote(x))

label_to_id = {
    'pehota': 0,
    'tank': 1,
    'bmp': 2,
    'btr': 3,
    'bronemashina': 4,
    'artilleriya': 5,
    'rszo': 6,
    'bpla': 7
}

for filename, group in df.groupby('image_decoded'):
    img_path = f"BentoService/FineTune/yolo_dataset/images/train/{filename}"

    if not os.path.exists(img_path):
        print(f"❌ Нет такого файла: {img_path}")
        continue
    
    with Image.open(img_path) as im:
        w, h = im.size

    txt_path = f"BentoService/FineTune/yolo_dataset/labels/train/{filename.replace('.jpg', '.txt')}"
    with open(txt_path, 'w') as f:
        for _, row in group.iterrows():
            x_center = ((row['xmin'] + row['xmax'])/2) / w
            y_center = ((row['ymin'] + row['ymax'])/2) / h
            norm_w_box = (row['xmax'] - row['xmin']) / w
            norm_h_box = (row['ymax'] - row['ymin']) / h

            if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= norm_w_box <=1 and 0 <= norm_h_box <=1):
                print("⚠️ Координаты разметки вне 0 и 1, пропускаю")
                continue

            class_id = label_to_id.get(row['label'], -1)
            if class_id == -1:
                print("⚠️ Неизвестный класс, пропускаю")
                continue

            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_w_box:.6f} {norm_h_box:.6f}\n")
    print(f"Файл {filename} обработан! ✅")
