# import posixpath, ntpath, json
# from pathlib import Path

# with open("config.json") as f:
#     cfg = json.loads(f.read())

# prompt = "A fantasy landscape, realistic"
# image_name = f'{prompt}.png'
# dirpath = Path(cfg["image_path"])
# save_path = (dirpath / image_name).as_posix().replace(ntpath.sep, posixpath.sep)

# print(save_path)

def hex_to_rgb(hexcode):
    try:
        # Hex renk kodundan gereksiz karakterleri kaldırın ve doğrudan RGB'ye çevirin
        hexcode = hexcode.replace('"', '').lstrip("#") 
        if len(hexcode) == 6:  # Renk kodu 6 karakter uzunluğunda olmalıdır
            rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
            return rgb
        else:
            raise ValueError("Geçersiz renk kodu uzunluğu")
    except ValueError as e:
        # Hata durumunda hatayı görüntüleyin
        print("Hata:", str(e))
        return (0, 0, 0)

text_color ='"#2D573B"'
print(text_color)
print(hex_to_rgb(text_color))