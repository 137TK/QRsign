import qrcode
import PIL
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import datetime
import re
# import argparse


# parser = argparse.ArgumentParser()
# parser.add_argument("name", help="your name. recommended length >3, <8")
# args = parser.parse_args()

# # 名前と日付を設定
# name = args.name
date = datetime.datetime.now().strftime("%Y/%m/%d")

def arrange_name_scale(name):
    if(re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+', name)):
        if(len(name) < 2):
            name_scale = 0.3
        elif(len(name) == 2):
            name_scale = 0.7
        else:
            name_scale = 0.9
    else:
        if(len(name) < 5):
            name_scale = 1
        elif(len(name) == 5):
            name_scale = 1.3
        else:
            name_scale = 1.6
    
    return name_scale



def make_name_date(name, date):
    size = 256

    name_scale = arrange_name_scale(name)
    date_scale = 1.5
    distance = 0.1 # scale
    height_scale = 0.6
    date_pos_correction = 0.15
    name_pos_correction = 0.05
    
    # 画像サイズの設定
    width, height = size, int(size*height_scale)
    
    # 画像の生成
    image = Image.new("L", (width, height), color=255)  # 白黒画像として生成
    
    # フォントとサイズの設定
    date_font_size = int(int(size*date_scale)/len(date)) 
    date_font = ImageFont.truetype("meiryo.ttc", date_font_size)  
    
    name_font_size = int(int(size*name_scale)/len(name))
    name_font = ImageFont.truetype("meiryo.ttc", name_font_size)  
    
    
    # テキストの描画
    draw = ImageDraw.Draw(image)
    
    # 名前の描画
    name_bbox = draw.multiline_textbbox((0, 0), name, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_height = name_bbox[3] - name_bbox[1] 
    name_position = ((width - name_width) // 2, ((height - name_height ) // 2 - name_height // 2 ) + int(name_pos_correction*size)- int(size*distance) )
    draw.text(name_position, name, fill=0, font=name_font)
    
    # 日付の描画
    date_bbox = draw.multiline_textbbox((0, 0), date, font=date_font)
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1] + int(size*distance)
    date_position = ((width - date_width) // 2, ((height - date_height ) // 2 + date_height // 2 ) + int(date_pos_correction*size)- int(size*distance) )
    draw.text(date_position, date, fill=0, font=date_font)

    return image

def make_qr(image, name, date):
    qr_big = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    rsa_pub = "xxxxx"
    qr_big.add_data("name={}:date={}:rsa_pub:{}".format(name, date, rsa_pub).encode("shift-jis"))
    qr_big.make()
    img_qr_big = qr_big.make_image().convert('RGB')
    
    pos = ((img_qr_big.size[0] - image.size[0]) // 2, (img_qr_big.size[1] - image.size[1]) // 2)
    
    img_qr_big.paste(image, pos)
    print(r'.\{}:{}.png'.format(name, date.replace("/", "-")) + "is created.")
    date = date.replace("/", "-")
    img_qr_big.save(r'.\{}_{}.png'.format(name, date))

    return img_qr_big

# image = make_name_date(name, date)
# image = make_qr(image, name, date)
# plt.imshow(image)

def main():
    print("名前を入力してください（３文字以上８文字以内推奨）")
    name = input()
    image = make_name_date(name, date)
    image = make_qr(image, name, date)
    plt.imshow(image)


if __name__ =="__main__":
    main()