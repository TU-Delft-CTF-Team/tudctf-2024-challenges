from PIL import Image

img = Image.open('ew_orig.png')
password = Image.open('inner_password.png').convert('1')

for y in range(img.height):
    for x in range(img.width):
        (r, g, b, a) = img.getpixel((x, y))
        lsb = password.getpixel((x, y)) & 1
        b2 = (b & 0xfe) | lsb
        img.putpixel((x, y), (r, g, b2, a))

img.save('ew.png')
