import os
import math
import threading
import time

from PIL import Image, ImageFont, ImageDraw, ImageChops

#img1 = Image.open('images/testimg.png')
#img1.save('images/testimg2.png')
#img1.show()

imgs_fp = 'resources' + os.sep
saves_folder = 'images' + os.sep
imgs = {
    'bg_img': 'Background.png',
    'circle': 'Circle.png',
    'rad': 'RadiusLine.png',
    'edot': 'DotEmpty.png'
}

bg_img = Image.open(imgs_fp + imgs['bg_img'])
circle = Image.open(imgs_fp + imgs['circle'])
rad = Image.open(imgs_fp + imgs['rad'])
edot = Image.open(imgs_fp + imgs['edot'])

def draw_line(pos, t_pos, dot, img, seq_index): #Pos and Target Pos should be tuples.
    #iterate from x to tx
    #increase y by the slope
    x1, y1 = pos
    x2, y2 = t_pos
    #dot = dot.copy
    dot = Image.open(imgs_fp + dot.lower() +'dot.png')
    dotW, dotH = dot.size
    
    x1 -= round(dotW/2)
    x2 -= round(dotW/2)
    y1 -= round(dotH/2)
    y2 -= round(dotH/2)
    
    rise = y2 - y1
    run = x2-x1
    
    if run == 0:
        if y2 < y1:
            y1, y2 = (y2, y1)
        for y in range(y1, y2+1):
            img.paste(dot, (x1, y+seq_index*2, x1+dotW, y+dotH+seq_index*2), dot)
    else:
        m = float(rise)/run
        adjust = 1 if m >= 0 else -1
        offset = 0
        threshold = 0.5
        if m <= 1 and m >= -1:
            delta = abs(m)
            y = y1
            if x2 < x1:
                x1, x2 = (x2, x1)
                y=y2
            for x in range(x1, x2+1):
                img.paste(dot, (x, y+seq_index*2, x+dotW, y+dotH+seq_index*2), dot)
                offset += delta
                if offset >= threshold:
                    y += adjust
                    threshold += 1
        else:
            delta = abs(float(run)/rise)
            x = x1
            if y2<y1:
                y1, y2 = (y2, y1)
                x = x2
            for y in range(y1, y2+1):
                img.paste(dot, (x, y+seq_index*2, x+dotW, y+dotH+seq_index*2), dot)
                offset += delta
                if offset >= threshold:
                    x += adjust
                    threshold += 1


def make_picture(base, sequences, sequence_colors):
    new_image = Image.new("RGBA", bg_img.size)
                    
    new_image.paste(bg_img, (0, 0), bg_img)

    degrees = 360/(base-1)

    #opposite, adjacent = y, y (y should be 350 or 349)

    #hypotenuse_squared = math.pow(opposite) + math.pow(adjacent)
    #hypotenuse = math.sqrt(hypotenuse_squared)

    #sin = opposite/hypotenuse
    #inverse_sin = sin/sin

    #cos = adjacent/hypotenuse
    #inverse_cos = cos/cos

    #tan = opposite/adjacent
    #inverse_tan = tan/tan

    #target_x = [ degrees.cos, -degrees.sin ] * origin_x
    #target_y = [ degrees.sin,  degrees.cos ] * origin_y

    new_image.paste(circle, (0, 0), circle)

    for i in range(1, base):
        rdcp = rad.copy()
        rdDraw = ImageDraw.Draw(rdcp)
        rdDraw.text(((bg_img.width/2)-10, 5), str(i), font=ImageFont.truetype("arial.ttf", 40))
        rdcp.putpixel((round(bg_img.width/2), round(bg_img.height/2)-350), (i,128,128))
        rdcp.putpixel((round(bg_img.width/2), round(1+bg_img.height/2)-350), (i,128,128))
        rdcp.putpixel((round(1+bg_img.width/2), round(bg_img.height/2)-350), (i,128,128))
        rdcp = rdcp.rotate( -degrees*i, Image.NEAREST )
        new_image.paste(rdcp, (0, 0), rdcp)
        
    number_locations = {}#[0]*base
    for y in range(new_image.width):
        for x in range(new_image.height):
            r, g, b, a = new_image.getpixel((x, y))
            if (g, b, a) == (128, 128, 255):
                if r >= 10:
                    r = chr(r+55)
                number_locations[r] = (x, y)
                
    for i in range(1, base):
        rdotcp = edot.copy()
        rdotcp = ImageChops.offset(rdotcp, 0, -350)
        rdotcp = rdotcp.rotate( -degrees*i, Image.NEAREST )
        new_image.paste(rdotcp, (0, 0), rdotcp)    
    
    #draw_line(number_locations[1], number_locations[3], rdot, new_image)
    
    for seq_index, sequence in enumerate(sequences):
        for num_index, num in enumerate(sequence):
            if num_index <= len(sequence)-2 and len(sequence) > 2:
                if type( num ) != type( '' ):
                    base_converted_num = num if num < 10 else chr(num+55)
                else:
                    base_converted_num = num
                if type( sequence[num_index+1] ) != type( '' ):
                    base_converted_seq_num = sequence[num_index+1] if sequence[num_index+1] < 10 else chr( sequence[num_index+1] + 55 )
                else:
                    base_converted_seq_num = sequence[num_index+1]
                draw_line(number_locations[base_converted_num], number_locations[base_converted_seq_num], sequence_colors[seq_index], new_image, seq_index)
        
    threading.Thread(target=new_image.show).start()

    new_image.save(saves_folder + 'Base '+ str(base) + '.png')