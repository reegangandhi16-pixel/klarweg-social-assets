"""LearnWithReegan A1 PREMIUM LOCKED DESIGN v2. 
One fixed visual system for every slot; only words, topic and icons change.
Inspired by the account's approved green/gold Cologne illustrated educational posters.
No photo of the teacher. Built entirely with Pillow + open-source system emoji glyphs.
"""
from __future__ import annotations
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=1080,1350
NAVY=(1,40,29)
GREEN="#053E2A"
GOLD="#FFE334"
CREAM="#FFFBEF"
RED="#DE1B29"
FONT_REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
EMOJI="/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

CATEGORIES={
"Zuhause":"🏠","Küche":"🍳","Essen":"🍎","Getränke":"🥤",
"Stadt":"🏙️","Verkehr":"🚍","Schule":"📚","Familie":"👨‍👩‍👧",
"Kleidung":"👕","Körper":"🦵","Natur":"🌳","Freizeit":"🎾",
"Arbeit":"💻","Badezimmer":"🛀","Einkaufen":"🛍️","Zeit":"⏰",
"Restaurant":"🍽️","Reisen":"✈️","Haushalt":"🧹","Tiere":"🐈",
"Wetter":"🌦️","Musik":"🎶",
}
# Illustrations are fixed per word and never supplied by an unconstrained AI.
OBJECTS={
"Bett":"🛏️","Tisch":"🪑","Stuhl":"🪑","Lampe":"💡","Tür":"🚪",
"Fenster":"🪟","Sofa":"🛋️","Schrank":"🗄️","Spiegel":"🪞",
"Teppich":"🧶","Uhr":"🕒","Regal":"📚","Kühlschrank":"🧊",
"Herd":"🍳","Teller":"🍽️","Tasse":"☕","Glas":"🥛","Löffel":"🥄",
"Gabel":"🍴","Messer":"🔪","Topf":"🍲","Pfanne":"🍳","Geschirr":"🍽️",
"Küche":"🍳","Apfel":"🍎","Banane":"🍌","Orange":"🍊",
"Kartoffel":"🥔","Tomate":"🍅","Gurke":"🥒","Käse":"🧀","Ei":"🥚",
"Reis":"🍚","Suppe":"🥣","Fleisch":"🥩","Fisch":"🐟",
"Wasser":"💧","Kaffee":"☕","Tee":"🍵","Milch":"🥛",
"Saft":"🧃","Limonade":"🍋","Cola":"🥤","Flasche":"🍼",
"Becher":"🥛","Getränk":"🥤","Kakao":"🍫","Durst":"💧",
"Straße":"🛣️","Park":"🌳","Brücke":"🌉","Ampel":"🚦","Platz":"🏙️",
"Rathaus":"🏛️","Post":"📮","Bank":"🏦","Apotheke":"💊",
"Krankenhaus":"🏥","Geschäft":"🏬","Bahnhof":"🚉",
"Bus":"🚌","Zug":"🚆","Fahrrad":"🚲","Auto":"🚗",
"Taxi":"🚕","U-Bahn":"🚇","Straßenbahn":"🚊","Flugzeug":"✈️",
"Schiff":"🚢","Haltestelle":"🚏","Fahrkarte":"🎟️","Koffer":"🧳",
"Schule":"🏫","Lehrer":"👨‍🏫","Lehrerin":"👩‍🏫","Schüler":"👨‍🎓",
"Schülerin":"👩‍🎓","Buch":"📚","Heft":"📓","Stift":"🖊️",
"Bleistift":"✏️","Radiergummi":"🧽","Tafel":"📝","Rucksack":"🎒",
"Mutter":"👩","Vater":"👨","Schwester":"👧","Bruder":"👦",
"Oma":"👵","Opa":"👴","Kind":"🧒","Sohn":"👦","Tochter":"👧",
"Tante":"👩","Onkel":"👨","Baby":"👶",
"Hose":"👖","Hemd":"👔","Kleid":"👗","Rock":"👗","Jacke":"🧥",
"Mantel":"🧥","Pullover":"🧶","Schuh":"👞","Socke":"🧦",
"Mütze":"🧢","Hut":"🎩","Gürtel":"👖",
"Kopf":"🗣️","Hand":"✋","Arm":"💪","Bein":"🦵","Fuß":"🦶",
"Auge":"👁️","Ohr":"👂","Nase":"👃","Mund":"👄",
"Bauch":"🧍","Rücken":"🧍","Haar":"💇",
"Baum":"🌳","Blume":"🌼","Sonne":"☀️","Mond":"🌙","Stern":"⭐",
"Himmel":"🌤️","Wolke":"☁️","Regen":"🌧️","Schnee":"❄️",
"Wind":"🌬️","Berg":"🏔️","See":"🏞️",
"Kino":"🎬","Museum":"🏛️","Schwimmbad":"🏊","Spiel":"🎲",
"Musik":"🎵","Lied":"🎶","Foto":"📷","Kamera":"📸",
"Ball":"⚽","Film":"🎞️","Hobby":"🎨","Konzert":"🎤",
"Arbeit":"💼","Büro":"🏢","Chef":"👔","Chefin":"👩‍💼",
"Kollege":"👨‍💼","Kollegin":"👩‍💼","Computer":"💻",
"Bildschirm":"🖥️","Drucker":"🖨️","Kalender":"📅",
"Telefon":"☎️","Beruf":"💼",
"Badezimmer":"🛁","Dusche":"🚿","Seife":"🧼",
"Handtuch":"🧻","Zahnbürste":"🪥","Zahnpasta":"🦷",
"Toilette":"🚽","Waschbecken":"🚰","Badewanne":"🛀",
"Kamm":"💇","Föhn":"💨",
"Supermarkt":"🛒","Laden":"🏪","Kasse":"💶","Geld":"💶",
"Preis":"🏷️","Angebot":"🏷️","Rechnung":"🧾","Tasche":"👜",
"Einkaufswagen":"🛒","Obst":"🍎","Gemüse":"🥕","Korb":"🧺",
"Morgen":"🌅","Abend":"🌆","Nacht":"🌙","Stunde":"🕑",
"Minute":"⏱️","Woche":"🗓️","Monat":"📆","Jahr":"🗓️",
"Tag":"🌞","Montag":"📅","Sonntag":"☀️","Wochenende":"🏖️",
"Restaurant":"🍽️","Speisekarte":"📋","Kellner":"👨‍🍳",
"Kellnerin":"👩‍🍳","Bestellung":"🧾","Essen":"🍲",
"Salat":"🥗","Serviette":"🧻","Besteck":"🍴",
"Hotel":"🏨","Zimmer":"🛏️","Rezeption":"🛎️","Schlüssel":"🔑",
"Reise":"🧳","Urlaub":"🏝️","Reisepass":"🛂",
"Karte":"🗺️","Strand":"🏖️","Meer":"🌊","Flughafen":"🛫",
"Waschmaschine":"🧺","Staubsauger":"🧹","Besen":"🧹",
"Eimer":"🪣","Boden":"🧹","Wand":"🧱","Decke":"🏠",
"Müll":"🗑️","Treppe":"🪜","Wohnung":"🏠",
"Hund":"🐕","Katze":"🐈","Vogel":"🐦","Pferd":"🐎",
"Kuh":"🐄","Schaf":"🐑","Schwein":"🐖","Maus":"🐁",
"Hase":"🐇","Ente":"🦆","Löwe":"🦁",
"Gewitter":"⛈️","Sänger":"🎤","Sängerin":"🎤","Gitarre":"🎸",
"Klavier":"🎹","Trommel":"🥁","Mikrofon":"🎙️"
}
# A sample house, furniture or animal must have its own relevant emoji.
ARTICLES={"der":"#1466C0","die":"#D3182E","das":"#1E8F4B"}
def font(sz,bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,sz)
def boxtext(d,text,maxwidth,maxsize,minsize=22,bold=True):
    for sz in range(maxsize,minsize-1,-1):
        f=font(sz,bold)
        b=d.textbbox((0,0),text,font=f)
        if b[2]-b[0]<=maxwidth:
            return f
    raise ValueError("Visual text overflow: "+text)
def center(d,text,x,y,f,colour,shadow=None):
    bb=d.textbbox((0,0),text,font=f)
    tw=bb[2]-bb[0]
    if shadow:
        d.text((x-tw/2+2,y+3),text,font=f,fill=shadow)
    d.text((x-tw/2,y),text,font=f,fill=colour)
def gradient():
    im=Image.new("RGB",(W,H))
    d=ImageDraw.Draw(im)
    for y in range(H):
        if y<550:
            r=y/550
            a=(0,54,39);b=(10,78,60)
        else:
            r=(y-550)/800
            a=(9,77,57);b=(0,56,42)
        d.line((0,y,W,y),fill=tuple(round(a[i]*(1-r)+b[i]*r) for i in range(3)))
    return im
def cologne(im):
    """Stylized cathedral, arched bridge and warm Rhine skyline—all slots identical."""
    d=ImageDraw.Draw(im,"RGBA")
    for k in range(10,0,-1):
        d.ellipse((710-k*22,286-k*20,1180+k*20,610+k*16),fill=(244,158,112,round(2.4*k)))
    d.rectangle((0,390,W,585),fill=(120,124,120,40))
    # sunset river visible behind the panel
    d.polygon([(0,515),(1080,470),(1080,645),(0,650)],fill=(27,89,90,115))
    for x in range(0,W,70):
        d.line((x,540,x+37,544),fill=(238,185,116,75),width=3)
    # Hohenzollern bridge silhouette
    d.line((0,480,600,470),fill=(0,37,40,220),width=13)
    for x in range(20,590,65):
        d.arc((x,420,x+110,522),180,360,fill=(0,37,40,230),width=5)
        for dx in range(0,80,18):
            d.line((x+dx,448,x+dx+20,497),fill=(5,45,45,200),width=2)
    # Gothic twin cathedral spires at right
    for x in (908,998):
        d.polygon([(x,237),(x-27,365),(x+27,365)],fill=(13,36,37,245))
        d.line((x,213,x,247),fill=(18,39,40,255),width=4)
        d.rectangle((x-22,366,x+24,482),fill=(14,42,40,244))
        for y in range(320,455,32):
            d.line((x-13,y,x+13,y),fill=(187,149,107,160),width=2)
    d.rectangle((895,402,1035,488),fill=(12,40,42,225))
    d.polygon([(894,405),(965,360),(1034,405)],fill=(15,39,43,235))
    for x in range(911,1030,29):
        d.arc((x,424,x+21,472),180,360,fill=(204,165,112,180),width=2)
    # Top-left German tricolor flag with cloth polygon and pole
    d.line((31,134,31,448),fill="#F4F7F0",width=6)
    for i,c in enumerate(("#141414","#DC2025","#F1C920")):
        y=137+38*i
        d.polygon([(35,y),(122,y+9),(185,y+21),(176,y+51),(98,y+38),(35,y+38)],fill=c)
    # Decorative leaves at upper-left, drawn fixed, not varying per item
    for x,y,r in [(42,10,37),(89,5,30),(130,19,24),(10,65,34),(65,77,24),(17,115,25)]:
        d.ellipse((x-r,y-r/2,x+r,y+r/2),fill=(142,169,39,205))
        d.line((x,y-r//2,x+18,y+r//3),fill=(49,104,44,175),width=3)
    # brand top-right light rays
    for i in range(5):
        a=(i-2)*math.pi/13
        xx=190+math.cos(a)*83
        yy=159+math.sin(a)*83
        d.line((xx,yy,xx+math.cos(a)*28,yy+math.sin(a)*28),fill="#FFE22D",width=10)
def banner(im,german,english):
    d=ImageDraw.Draw(im)
    # Fixed masthead
    d.rounded_rectangle((338,23,736,81),radius=15,fill="#073527")
    d.polygon([(344,30),(370,11),(400,29),(371,46)],fill=GOLD)
    d.rectangle((363,41,379,62),fill=GOLD)
    center(d,"LearnWithReegan",572,27,font(39,True),CREAM,shadow="#00120C")
    center(d,"GERMAN",505,96,font(112,True),CREAM,shadow="#001A13")
    # A1 starburst badge
    for r,col in ((98,"#FEDC31"),(91,"#0C4D34")):
        d.ellipse((877-r,111-r/2,877+r,111+1.5*r),fill=col)
    center(d,"A1",877,104,font(76,True),CREAM)
    # Slanted golden ribbon approx identical for each
    d.polygon([(157,230),(975,212),(1000,313),(163,330)],fill="#FFDC21")
    center(d,"VOCABULARY",574,218,font(82,True),GREEN)
    # subtitle with brush banner
    d.rounded_rectangle((130,346,1030,444),radius=30,fill="#FFF9EC")
    heading=german.upper()
    title_f=boxtext(d,heading,686,56,28,True)
    center(d,heading,627,349,title_f,GREEN)
    center(d,english.upper(),631,412,boxtext(d,english.upper(),650,25,19), "#284F3E")
    d.line((386,412,875,412),fill="#DB2C2A",width=4)
    # Mini category icon inside white card
    emoji=CATEGORIES.get(german,"📚")
    draw_icon(im,emoji,(169,353),scale=0.7)
def draw_icon(im,s,xy,scale=1):
    try:
        e=ImageFont.truetype(EMOJI,109)
        sprite=Image.new("RGBA",(145,145),(0,0,0,0))
        ed=ImageDraw.Draw(sprite)
        ed.text((15,10),s,font=e,embedded_color=True)
        if scale!=1:
            sprite=sprite.resize((int(145*scale),int(145*scale)),Image.Resampling.LANCZOS)
        im.paste(sprite,(int(xy[0]),int(xy[1])),sprite)
        return True
    except Exception:
        return False
def vocabulary(im,german,words):
    d=ImageDraw.Draw(im)
    # Cream grid matches the personally approved illustrated post
    d.rounded_rectangle((44,464,1039,1158),radius=46,fill="#0A6945")
    d.rounded_rectangle((51,472,1032,1151),radius=42,fill="#FFF9EB",outline="#E3EDD8",width=5)
    # fixed 3x2 columns, scalable to every word in catalogue
    for x in (376,704):d.line((x,491,x,1132),fill="#9DAF9B",width=2)
    d.line((70,808,1015,808),fill="#9DAF9B",width=2)
    for i,(article,word,english) in enumerate(words):
        col,row=i%3,i//3
        x=58+col*328
        y=487+row*338
        # white icon badge with gentle yellow pedestal, accessible contrast
        d.rounded_rectangle((x+74,y+7,x+244,y+175),radius=28,fill="#FFFDF5",outline="#F3E6BF",width=2)
        d.ellipse((x+109,y+152,x+204,y+167),fill="#E7D8AD")
        sym=OBJECTS.get(word,CATEGORIES.get(german,"📚"))
        draw_icon(im,sym,(x+87,y+20),scale=1)
        # text labels in one continuous professional pill
        pill_top=y+194
        d.rounded_rectangle((x+17,pill_top,x+303,pill_top+65),radius=33,fill="#F8F5DF",outline="#26593E",width=2)
        label=f"{article} {word}"
        f=boxtext(d,label,274,41,21,True)
        bb=d.textbbox((0,0),label,font=f);tw=bb[2]-bb[0]
        start=x+162-tw/2
        d.text((start,pill_top+8),article,font=f,fill=ARTICLES[article])
        wa=d.textbbox((0,0),article,font=f)[2]
        d.text((start+wa+13,pill_top+8),word,font=f,fill="#121C1A")
        d.rounded_rectangle((x+49,y+270,x+269,y+312),radius=22,fill="#E1F6BF")
        ef=boxtext(d,english,206,26,18,True)
        center(d,english,x+162,y+274,ef,"#142C20")
def footer(im):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((48,1185,1030,1300),radius=51,fill=GOLD,outline="#FFF8D5",width=4)
    d.ellipse((68,1204,146,1279),fill="#075037",outline="#FFFFFF",width=5)
    for i in range(3):d.ellipse((88+i*16,1235,97+i*16,1244),fill="#FFFFFF")
    center(d,"WIE VIELE WÖRTER KENNST DU?",565,1199,font(43,True),GREEN)
    center(d,"How many words do you know?  •  Comment below!",555,1256,boxtext(d,"How many words do you know?  •  Comment below!",843,25,19,True),GREEN)
    d.arc((740,1320,1205,1440),180,330,fill="#F8FFF3",width=12)
def poster_v2(german,english,words,slot):
    im=gradient()
    cologne(im)
    banner(im,german,english)
    vocabulary(im,german,words)
    footer(im)
    assert im.size==(W,H)
    return im.convert("RGB")
