from pathlib import Path
import math, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,SECONDS=1920,1080,24,8
root=Path('/home/ubuntu/RTM')
frames=root/'assets'/'vimax'/'fight_frames'
out=root/'assets'/'vimax'/'rtm_fight_scene.mp4'
frames.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def lerp(a,b,t): return a+(b-a)*t

def draw_fighter(d,x,y,scale,coat,accent,flip=False,pose=0):
    s=scale; sign=-1 if flip else 1
    # head, hair, torso
    d.ellipse((x-28*s,y-150*s,x+28*s,y-94*s),fill=(218,160,128,255),outline=(20,23,35,255),width=max(2,int(4*s)))
    d.polygon([(x-35*s,y-145*s),(x+30*s,y-143*s),(x+12*s,y-174*s),(x-20*s,y-170*s)],fill=(22,25,38,255))
    d.polygon([(x-58*s,y-90*s),(x+45*s,y-90*s),(x+72*s,y+95*s),(x-70*s,y+95*s)],fill=coat,outline=(18,24,39,255))
    # legs in grounded stance
    d.line((x-28*s,y+78*s,x-95*s,y+235*s),fill=(18,24,37,255),width=max(10,int(22*s)))
    d.line((x+25*s,y+78*s,x+92*s,y+225*s),fill=(18,24,37,255),width=max(10,int(22*s)))
    d.ellipse((x-122*s,y+220*s,x-55*s,y+244*s),fill=(10,14,25,255))
    d.ellipse((x+58*s,y+210*s,x+128*s,y+236*s),fill=(10,14,25,255))
    # arms vary with pose, kept non-graphic
    if pose==0: arms=[(-52,-45,-125,-5),(42,-40,112,18)]
    elif pose==1: arms=[(-48,-40,-128,-92),(38,-42,125,-72)]
    elif pose==2: arms=[(-45,-10,-125,30),(42,-32,142,-15)]
    else: arms=[(-40,-30,-100,70),(45,-35,100,60)]
    for ax,ay,bx,by in arms:
        d.line((x+ax*s,y+ay*s,x+bx*s,y+by*s),fill=coat,width=max(9,int(24*s)))
        d.ellipse((x+(bx-12)*s,y+(by-12)*s,x+(bx+12)*s,y+(by+12)*s),fill=(218,160,128,255))
    d.line((x-sign*44*s,y+15*s,x+sign*48*s,y+15*s),fill=accent,width=max(3,int(8*s)))

def make(i):
    t=i/(FPS*SECONDS-1)
    im=Image.new('RGB',(W,H),(8,10,25)); p=im.load()
    for yy in range(H):
        q=yy/H
        c=(int(9+26*q),int(12+18*q),int(35+28*q))
        for xx in range(W): p[xx,yy]=c
    d=ImageDraw.Draw(im,'RGBA')
    # neon arena
    d.rectangle((0,700,W,H),fill=(8,12,22,255))
    for xx in range(-400,2400,240):
        d.line((W//2,700,xx,1080),fill=(46,83,125,110),width=3)
    d.line((0,700,W,700),fill=(91,206,220,120),width=4)
    # backlights
    for x,col in [(310,(40,160,255,170)),(1600,(255,72,132,170))]:
        glow=Image.new('RGBA',(W,H));g=ImageDraw.Draw(glow)
        for r in range(280,30,-20): g.ellipse((x-r,360-r,x+r,360+r),fill=col[:-1]+(max(2,int(col[3]*(1-r/300))),))
        im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(25))); d=ImageDraw.Draw(im,'RGBA')
    # beat-based choreography: advance, strike, evade, reset
    phase=t*4
    cycle=int(phase)%4; local=phase%1
    if cycle==0: # face off
        ax, bx=575+40*local,1345-40*local; ap,bp=0,0
    elif cycle==1: # blue fighter lunges
        ax,bx=615+140*local,1305-35*local; ap,bp=2,1
    elif cycle==2: # red dodges with kinetic streak
        ax,bx=760-90*local,1200+100*local; ap,bp=1,3
        d.line((780,650,1180,560),fill=(255,118,152,180),width=12)
        d.line((780,660,1180,570),fill=(255,204,105,130),width=5)
    else: # reset
        ax,bx=670-95*local,1270+75*local; ap,bp=3,0
    draw_fighter(d,ax,700,1.25,(26,100,194,255),(80,216,255,255),False,ap)
    draw_fighter(d,bx,700,1.25,(164,34,75,255),(255,135,163,255),True,bp)
    # impact spark at middle on strike beat
    if cycle==1 and .45<local<.75:
        cx,cy=1040,620
        for k in range(14):
            a=k*math.pi/7; rr=60+20*math.sin(k)
            d.line((cx,cy,cx+math.cos(a)*rr,cy+math.sin(a)*rr),fill=(255,221,129,220),width=5)
        d.ellipse((cx-20,cy-20,cx+20,cy+20),fill=(255,246,192,240))
    # title cards
    d.rounded_rectangle((75,70,670,205),radius=25,fill=(4,8,21,185),outline=(87,192,255,140),width=2)
    d.text((112,94),'NEON DUEL',font=ImageFont.truetype(font,52),fill=(235,248,255,255))
    d.text((115,158),'CINEMATIC ACTION / NO GORE',font=ImageFont.truetype(font,22),fill=(132,214,255,255))
    d.text((78,1015),'ViMax-style local choreography preview',font=ImageFont.truetype(font,20),fill=(216,231,244,180))
    im.convert('RGB').save(frames/f'frame_{i:04d}.jpg',quality=94)

for i in range(FPS*SECONDS): make(i)
subprocess.run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(frames/'frame_%04d.jpg'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
shutil.rmtree(frames)
print(out)
