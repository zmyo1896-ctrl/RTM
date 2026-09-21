from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

W, H, FPS, SECONDS = 1920, 1080, 24, 8
root = Path(__file__).parent
frames = root / "assets" / "vimax" / "frames"
out = root / "assets" / "vimax" / "rtm_vimax_demo.mp4"
frames.mkdir(parents=True, exist_ok=True)
font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def mix(a, b, t): return int(a + (b-a)*t)
def gradient(im, top, bottom):
    p = im.load()
    for y in range(H):
        t = y/(H-1)
        c = tuple(mix(top[i], bottom[i], t) for i in range(3))
        for x in range(W): p[x,y] = c

def frame(i):
    t = i/(FPS*SECONDS-1)
    im = Image.new("RGB", (W,H)); gradient(im, (9,18,45), (246,152,72))
    d = ImageDraw.Draw(im, "RGBA")
    # cinematic sun bloom
    sx, sy = int(320 + 90*t), int(260 - 25*t)
    glow = Image.new("RGBA", (W,H)); gd = ImageDraw.Draw(glow)
    for r in range(300, 40, -12): gd.ellipse((sx-r,sy-r,sx+r,sy+r), fill=(255,190,72,max(2,int(55*(1-r/320)))))
    glow = glow.filter(ImageFilter.GaussianBlur(18)); im = Image.alpha_composite(im.convert("RGBA"), glow); d = ImageDraw.Draw(im, "RGBA")
    d.ellipse((sx-54,sy-54,sx+54,sy+54), fill=(255,235,152,255))
    # distant hills and foreground
    d.polygon([(0,650),(240,510),(470,640),(760,450),(1050,650),(1360,470),(1700,620),(1920,500),(1920,1080),(0,1080)], fill=(11,39,53,255))
    d.polygon([(0,810),(350,700),(700,820),(1050,660),(1450,800),(1760,680),(1920,760),(1920,1080),(0,1080)], fill=(5,23,34,255))
    # workshop
    bx, by = 760, 545
    d.rectangle((bx,by,bx+640,930), fill=(20,34,46,255), outline=(85,177,187,255), width=4)
    d.polygon([(bx-45,by),(bx+320,by-165),(bx+700,by),(bx+700,by+30),(bx-45,by+30)], fill=(27,67,76,255), outline=(111,223,218,255))
    # solar panels with moving shimmer
    for px in range(bx+35, bx+590, 125):
        d.polygon([(px,by-12),(px+100,by-57),(px+100,by+10),(px,by+35)], fill=(11,63,91,255), outline=(91,199,221,255))
        for k in range(1,4): d.line((px+25*k,by-23,px+25*k,by+22), fill=(98,190,211,150), width=2)
    d.rectangle((bx+55,by+100,bx+235,by+330), fill=(7,17,25,255), outline=(71,138,148,255), width=4)
    d.rectangle((bx+360,by+150,bx+560,by+310), fill=(255,193,89,160), outline=(255,222,155,220), width=4)
    # technician silhouette and periodic arm motion
    tx, ty = 620, 650
    d.ellipse((tx-35,ty-120,tx+35,ty-50), fill=(9,18,29,255))
    d.rectangle((tx-48,ty-55,tx+48,ty+170), fill=(12,42,66,255))
    d.line((tx-20,ty+160,tx-70,ty+330), fill=(8,18,28,255), width=28)
    d.line((tx+20,ty+160,tx+75,ty+330), fill=(8,18,28,255), width=28)
    arm = int(70*math.sin(t*math.pi*2))
    d.line((tx+35,ty-25,tx+145,ty+35+arm), fill=(8,18,28,255), width=22)
    d.line((tx-35,ty-25,tx-100,ty+45), fill=(8,18,28,255), width=22)
    # foreground grass strokes
    for x in range(0,W,34):
        h = 22 + int(12*math.sin(x*.09+t*8))
        d.line((x,980,x+8,980-h), fill=(38,111,78,180), width=4)
    # tasteful title overlay
    d.rounded_rectangle((90,82,710,240), radius=28, fill=(3,12,25,170), outline=(102,226,223,130), width=2)
    d.text((130,108), "RTM SOLAR", font=ImageFont.truetype(font_bold, 54), fill=(227,255,251,255))
    d.text((133,176), "CLEAN ENERGY / LOCAL DEMO", font=ImageFont.truetype(font_reg, 24), fill=(142,231,227,255))
    d.text((90,1000), "ViMax pipeline preview • local fallback render", font=ImageFont.truetype(font_reg, 22), fill=(220,238,239,190))
    im.convert("RGB").save(frames / f"frame_{i:04d}.jpg", quality=94)

for i in range(FPS*SECONDS): frame(i)
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(frames/"frame_%04d.jpg"),"-c:v","libx264","-pix_fmt","yuv420p","-crf","19","-movflags","+faststart",str(out)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(out)
print(out.stat().st_size)
