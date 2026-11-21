#!/usr/bin/env python3
"""Deterministic, original A1 vocabulary images. No AI API, no personal photographs."""
from __future__ import annotations
import hashlib
import json
import math
import os
from datetime import datetime, date, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from style_v2 import poster_v2

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "germanwithreegan" / "auto"
BASE = "https://raw.githubusercontent.com/reegangandhi16-pixel/klarweg-social-assets/main"
FIRST_DAY = date(2026, 11, 21)
SLOTS = (0, 4, 8, 12, 16, 20)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GREEN = "#073A2A"
CREAM = "#FFF8E9"
YELLOW = "#FBE436"
MINT = "#B7E6C3"
THEMES = [
 ("Zuhause","At home",[("das","Bett","bed"),("der","Tisch","table"),("der","Stuhl","chair"),("die","Lampe","lamp"),("die","Tür","door"),("das","Fenster","window"),("das","Sofa","sofa"),("der","Schrank","wardrobe"),("der","Spiegel","mirror"),("der","Teppich","carpet"),("die","Uhr","clock"),("das","Regal","shelf")]),
 ("Küche","In the kitchen",[("der","Kühlschrank","refrigerator"),("der","Herd","stove"),("der","Teller","plate"),("die","Tasse","cup"),("das","Glas","glass"),("der","Löffel","spoon"),("die","Gabel","fork"),("das","Messer","knife"),("der","Topf","pot"),("die","Pfanne","pan"),("das","Geschirr","dishes"),("die","Küche","kitchen")]),
 ("Essen","Food",[("der","Apfel","apple"),("die","Banane","banana"),("die","Orange","orange"),("die","Kartoffel","potato"),("die","Tomate","tomato"),("die","Gurke","cucumber"),("der","Käse","cheese"),("das","Ei","egg"),("der","Reis","rice"),("die","Suppe","soup"),("das","Fleisch","meat"),("der","Fisch","fish")]),
 ("Getränke","Drinks",[("das","Wasser","water"),("der","Kaffee","coffee"),("der","Tee","tea"),("die","Milch","milk"),("der","Saft","juice"),("die","Limonade","lemonade"),("die","Cola","cola"),("die","Flasche","bottle"),("der","Becher","cup"),("das","Getränk","drink"),("der","Kakao","cocoa"),("der","Durst","thirst")]),
 ("Stadt","Around the city",[("die","Straße","street"),("der","Park","park"),("die","Brücke","bridge"),("die","Ampel","traffic light"),("der","Platz","square"),("das","Rathaus","town hall"),("die","Post","post office"),("die","Bank","bank"),("die","Apotheke","pharmacy"),("das","Krankenhaus","hospital"),("das","Geschäft","shop"),("der","Bahnhof","train station")]),
 ("Verkehr","Transport",[("der","Bus","bus"),("der","Zug","train"),("das","Fahrrad","bicycle"),("das","Auto","car"),("das","Taxi","taxi"),("die","U-Bahn","subway"),("die","Straßenbahn","tram"),("das","Flugzeug","airplane"),("das","Schiff","ship"),("die","Haltestelle","stop"),("die","Fahrkarte","ticket"),("der","Koffer","suitcase")]),
 ("Schule","At school",[("die","Schule","school"),("der","Lehrer","teacher (m)"),("die","Lehrerin","teacher (f)"),("der","Schüler","pupil (m)"),("die","Schülerin","pupil (f)"),("das","Buch","book"),("das","Heft","notebook"),("der","Stift","pen"),("der","Bleistift","pencil"),("der","Radiergummi","eraser"),("die","Tafel","board"),("der","Rucksack","backpack")]),
 ("Familie","Family",[("die","Mutter","mother"),("der","Vater","father"),("die","Schwester","sister"),("der","Bruder","brother"),("die","Oma","grandma"),("der","Opa","grandpa"),("das","Kind","child"),("der","Sohn","son"),("die","Tochter","daughter"),("die","Tante","aunt"),("der","Onkel","uncle"),("das","Baby","baby")]),
 ("Kleidung","Clothes",[("die","Hose","trousers"),("das","Hemd","shirt"),("das","Kleid","dress"),("der","Rock","skirt"),("die","Jacke","jacket"),("der","Mantel","coat"),("der","Pullover","sweater"),("der","Schuh","shoe"),("die","Socke","sock"),("die","Mütze","hat/cap"),("der","Hut","hat"),("der","Gürtel","belt")]),
 ("Körper","Body parts",[("der","Kopf","head"),("die","Hand","hand"),("der","Arm","arm"),("das","Bein","leg"),("der","Fuß","foot"),("das","Auge","eye"),("das","Ohr","ear"),("die","Nase","nose"),("der","Mund","mouth"),("der","Bauch","stomach"),("der","Rücken","back"),("das","Haar","hair")]),
 ("Natur","Nature",[("der","Baum","tree"),("die","Blume","flower"),("die","Sonne","sun"),("der","Mond","moon"),("der","Stern","star"),("der","Himmel","sky"),("die","Wolke","cloud"),("der","Regen","rain"),("der","Schnee","snow"),("der","Wind","wind"),("der","Berg","mountain"),("der","See","lake")]),
 ("Freizeit","Free time",[("das","Kino","cinema"),("das","Museum","museum"),("das","Schwimmbad","pool"),("das","Spiel","game"),("die","Musik","music"),("das","Lied","song"),("das","Foto","photo"),("die","Kamera","camera"),("der","Ball","ball"),("der","Film","film"),("das","Hobby","hobby"),("das","Konzert","concert")]),
 ("Arbeit","At work",[("die","Arbeit","work"),("das","Büro","office"),("der","Chef","boss (m)"),("die","Chefin","boss (f)"),("der","Kollege","colleague (m)"),("die","Kollegin","colleague (f)"),("der","Computer","computer"),("der","Bildschirm","screen"),("der","Drucker","printer"),("der","Kalender","calendar"),("das","Telefon","telephone"),("der","Beruf","profession")]),
 ("Badezimmer","Bathroom",[("das","Badezimmer","bathroom"),("die","Dusche","shower"),("die","Seife","soap"),("das","Handtuch","towel"),("die","Zahnbürste","toothbrush"),("die","Zahnpasta","toothpaste"),("der","Spiegel","mirror"),("die","Toilette","toilet"),("das","Waschbecken","sink"),("die","Badewanne","bathtub"),("der","Kamm","comb"),("der","Föhn","hairdryer")]),
 ("Einkaufen","Shopping",[("der","Supermarkt","supermarket"),("der","Laden","shop"),("die","Kasse","checkout"),("das","Geld","money"),("der","Preis","price"),("das","Angebot","offer"),("die","Rechnung","bill"),("die","Tasche","bag"),("der","Einkaufswagen","shopping cart"),("das","Obst","fruit"),("das","Gemüse","vegetables"),("der","Korb","basket")]),
 ("Zeit","Time",[("der","Morgen","morning"),("der","Abend","evening"),("die","Nacht","night"),("die","Stunde","hour"),("die","Minute","minute"),("die","Woche","week"),("der","Monat","month"),("das","Jahr","year"),("der","Tag","day"),("der","Montag","Monday"),("der","Sonntag","Sunday"),("das","Wochenende","weekend")]),
 ("Restaurant","At a restaurant",[("das","Restaurant","restaurant"),("die","Speisekarte","menu"),("der","Kellner","waiter"),("die","Kellnerin","waitress"),("die","Bestellung","order"),("das","Essen","food"),("die","Rechnung","bill"),("der","Salat","salad"),("das","Getränk","drink"),("die","Serviette","napkin"),("das","Besteck","cutlery"),("der","Tisch","table")]),
 ("Reisen","Travel",[("das","Hotel","hotel"),("das","Zimmer","room"),("die","Rezeption","reception"),("der","Schlüssel","key"),("die","Reise","trip"),("der","Urlaub","holiday"),("der","Reisepass","passport"),("der","Koffer","suitcase"),("die","Karte","map"),("der","Strand","beach"),("das","Meer","sea"),("der","Flughafen","airport")]),
 ("Haushalt","Household",[("die","Waschmaschine","washing machine"),("der","Staubsauger","vacuum cleaner"),("der","Besen","broom"),("der","Eimer","bucket"),("das","Fenster","window"),("der","Boden","floor"),("die","Wand","wall"),("die","Decke","ceiling"),("der","Müll","rubbish"),("die","Treppe","stairs"),("der","Schlüssel","key"),("die","Wohnung","apartment")]),
 ("Tiere","Animals",[("der","Hund","dog"),("die","Katze","cat"),("der","Vogel","bird"),("der","Fisch","fish"),("das","Pferd","horse"),("die","Kuh","cow"),("das","Schaf","sheep"),("das","Schwein","pig"),("die","Maus","mouse"),("der","Hase","rabbit"),("die","Ente","duck"),("der","Löwe","lion")])
]


# Explicitly scheduled editorial posts; normal curated rotation remains unchanged.
# No previously approved dated JPEG or manifest is overwritten.
SPECIAL_POSTS = {
    (date(2026, 11, 26), 0): ("Wetter", "Weather", [
        ("die", "Sonne", "sun"),
        ("der", "Regen", "rain"),
        ("der", "Schnee", "snow"),
        ("der", "Wind", "wind"),
        ("die", "Wolke", "cloud"),
        ("das", "Gewitter", "thunderstorm"),
    ]),
    (date(2026, 11, 26), 4): ("Musik", "Music", [
        ("der", "Sänger", "male singer"),
        ("die", "Sängerin", "female singer"),
        ("die", "Gitarre", "guitar"),
        ("das", "Klavier", "piano"),
        ("die", "Trommel", "drum"),
        ("das", "Mikrofon", "microphone"),
    ]),
}

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def fit(d, text, max_width, start=52, min_size=28, bold=True):
    for size in range(start, min_size-1, -1):
        f=font(size,bold)
        if d.textbbox((0,0),text,font=f)[2] <= max_width:
            return f
    raise ValueError("Too long to render: " + text)

def centered(d,xy,text,f,fill):
    b=d.textbbox((0,0),text,font=f)
    d.text((xy[0]-(b[2]-b[0])//2,xy[1]),text,font=f,fill=fill)

def poster(german, english, words, slot):
    img=Image.new('RGB',(1080,1350),GREEN)
    d=ImageDraw.Draw(img)
    for y in range(1350):
        t=y/1350
        d.line([(0,y),(1080,y)],fill=(round(5+8*t),round(55-17*t),round(39-9*t)))
    d.ellipse((770,-280,1320,310),outline="#206650",width=6)
    d.ellipse((840,-210,1250,240),outline="#2B795F",width=4)
    d.ellipse((-270,1030,520,1820),outline="#1A634C",width=5)
    d.rectangle((52,68,133,88),fill="#111111")
    d.rectangle((52,88,133,108),fill="#D71E2A")
    d.rectangle((52,108,133,128),fill="#FFD028")
    d.text((159,74),"LearnWithReegan",font=font(42,True),fill="#FFFFFF")
    d.text((52,160),"GERMAN",font=font(102,True),fill="#FFFDF4",stroke_width=2,stroke_fill="#FFFDF4")
    d.rounded_rectangle((817,159,1021,265),radius=36,fill="#FFDE3A",outline="#FFEC9C",width=4)
    centered(d,(918,174),"A1",font(70,True),GREEN)
    d.rounded_rectangle((54,285,1026,386),radius=24,fill="#FFDC31")
    centered(d,(540,296),"VOCABULARY",font(69,True),GREEN)
    centered(d,(540,406),f"{german.upper()}  /  {english.upper()}",fit(d,f"{german.upper()}  /  {english.upper()}",970,45,26),CREAM)
    colours={"der":("#CDEAFF","#154A9B"),"die":("#FFD9D6","#B12A30"),"das":("#D8F5C3","#19653C")}
    for i,(article,word,meaning) in enumerate(words):
        col=i%2
        row=i//2
        x=54+col*496
        y=489+row*214
        shadow=Image.new("RGBA",img.size,(0,0,0,0))
        sd=ImageDraw.Draw(shadow)
        sd.rounded_rectangle((x+7,y+9,x+480+7,y+195+9),radius=26,fill=(0,0,0,95))
        shadow=shadow.filter(ImageFilter.GaussianBlur(10))
        img=Image.alpha_composite(img.convert("RGBA"),shadow).convert("RGB")
        d=ImageDraw.Draw(img)
        d.rounded_rectangle((x,y,x+480,y+195),radius=29,fill="#FFFBEF",outline="#B1D7BA",width=3)
        badge,c=colours[article]
        d.rounded_rectangle((x+18,y+21,x+135,y+73),radius=17,fill=badge)
        centered(d,(x+76,y+27),article.upper(),font(32,True),c)
        d.text((x+151,y+20),f"{i+1:02d}",font=font(24,True),fill="#A0A997")
        wfont=fit(d,word,442,51,30)
        d.text((x+22,y+79),word,font=wfont,fill=GREEN)
        d.rounded_rectangle((x+20,y+147,x+459,y+179),radius=10,fill="#E7F4DE")
        mfont=fit(d,meaning,420,27,19,bold=False)
        d.text((x+30,y+146),meaning,font=mfont,fill="#24573F")
    d=ImageDraw.Draw(img)
    d.rounded_rectangle((53,1149,1026,1286),radius=35,fill="#FFE13E",outline="#FFF2B2",width=4)
    centered(d,(540,1160),"HOW MANY WORDS DID YOU KNOW?",fit(d,"HOW MANY WORDS DID YOU KNOW?",924,45,30),GREEN)
    centered(d,(540,1220),"Comment your score  /  Save for A1 revision",font(27,True),GREEN)
    d.text((66,1314),"DER  •  DIE  •  DAS   |   Learn nouns with their articles",font=font(23),fill="#EDF4E7")
    return img

def build_one(day,slot):
    n=(day-FIRST_DAY).days
    index=(n*6+SLOTS.index(slot))%len(THEMES)
    german,english,all_words=THEMES[index]
    start=(n*7+SLOTS.index(slot)*3)%len(all_words)
    words=[all_words[(start+i)%len(all_words)] for i in range(6)]
    if (day, slot) in SPECIAL_POSTS:
        german, english, words = SPECIAL_POSTS[(day, slot)]
    assert len(words)==6 and len({a+" "+b for a,b,_ in words})==6
    assert all(a in ("der","die","das") for a,b,c in words)
    path=OUT/day.isoformat()/f"{slot:02d}00"
    dest=path/"01.jpg"
    manifest=path/"post.json"
    if dest.exists() and manifest.exists():
        previous=json.loads(manifest.read_text('utf8'))
        if previous.get('generator_version')=='a1-v2':
            print("V2 ALREADY APPROVED",day,slot)
            return
    path.mkdir(parents=True,exist_ok=True)
    image=poster_v2(german,english,words,slot)
    image.save(dest,format="JPEG",quality=90,optimize=True,subsampling=0)
    img_hash=hashlib.sha256(dest.read_bytes()).hexdigest()
    identifier=f"gwr-auto-{day:%Y%m%d}-{slot:02d}"
    scheduled=f"{day.isoformat()}T{slot:02d}:00:00+05:30"
    media_url=f"{BASE}/germanwithreegan/auto/{day.isoformat()}/{slot:02d}00/01.jpg"
    word_lines="\n".join(f"{a} {b} = {c}" for a,b,c in words)
    common=f"🇩🇪 A1 GERMAN VOCABULARY: {german} ({english})\n\n{word_lines}\n\n💡 Tip: Learn der/die/das with every noun.\n💬 Which word was new for you?\n🌐 https://klarweg.in\n#LearnGerman #GermanA1 #DeutschLernen #LearnWithReegan"
    threads=f"🇩🇪 A1 Vocabulary — {german} ({english})\n{word_lines}\n\n💬 Which one did you know?\n🌐 https://klarweg.in\n#LearnGerman #GermanA1"
    assert len(common)<=2200 and len(threads)<=500,(len(common),len(threads))
    p={
        "id":identifier,"status":"approved","level":"A1",
        "topic":german,"generator_version":"a1-v2","scheduled_at":scheduled,
        "image_url":media_url,"image_sha256":img_hash,
        "words":[{"article":a,"german":w,"english":e} for a,w,e in words],
        "facebook":{"approved":True,"scheduled_at":scheduled,"image_url":media_url,"caption":common},
        "threads":{"approved":True,"scheduled_at":scheduled,"image_url":media_url,"text":threads},
        "instagram":{"approved":True,"mode":"image","scheduled_at":scheduled,"image_url":media_url,"caption":common},
    }
    manifest.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("BUILT",day.isoformat(),f"{slot:02d}:00",german,dest, len(dest.read_bytes()))

def build_contact_sheet(day):
    """Actual output previews, not separately generated imagery."""
    folder=OUT/day.isoformat()
    images=[]
    for slot in SLOTS:
        jpg=folder/f"{slot:02d}00"/"01.jpg"
        manifest=folder/f"{slot:02d}00"/"post.json"
        if not (jpg.exists() and manifest.exists()):
            raise FileNotFoundError("Missing poster/manifest for "+str(day)+" "+str(slot))
        post=json.loads(manifest.read_text('utf8'))
        if post.get("generator_version")!="a1-v2":
            raise ValueError("Old visual style found in "+str(jpg))
        with Image.open(jpg) as im:
            images.append(im.convert('RGB').copy())
    cw,ch=352,440
    review=Image.new("RGB",(1080,990),"#093F2D")
    dr=ImageDraw.Draw(review)
    dr.text((38,16),"LearnWithReegan  |  SIX PREMIUM A1 POSTS",font=font(28,True),fill="#FFFBEF")
    dr.text((39,56),day.isoformat()+"   •   same locked layout • 00 / 04 / 08 / 12 / 16 / 20 IST",font=font(18,True),fill="#FFE23C")
    for index,(im,slot) in enumerate(zip(images,SLOTS)):
        x=10+(index%3)*358
        y=96+(index//3)*443
        im.thumbnail((cw,ch),Image.Resampling.LANCZOS)
        review.paste(im,(x,y))
        dr.rectangle((x,y,x+cw-1,y+ch-1),outline="#E7F5D4",width=2)
    target=folder/"six-post-contact-sheet.jpg"
    review.save(target,format="JPEG",quality=87,optimize=True)
    print("REVIEW SHEET",target, target.stat().st_size)


def main():
    today=datetime.now(ZoneInfo("Asia/Kolkata")).date()
    # Publish is separately gated by date, media hash, account identity and ledger.
    # Prebuild two explicitly requested first-free slots, leaving older approved posts untouched.
    if today < date(2026, 11, 26):
        for special_slot in (0, 4):
            build_one(date(2026, 11, 26), special_slot)
    # Build today + next two days; each dated file is immutable after creation.
    for n in range(1,4):
        day=today+timedelta(days=n)
        for slot in SLOTS:
            build_one(day,slot)
        build_contact_sheet(day)

if __name__=="__main__":
    main()
