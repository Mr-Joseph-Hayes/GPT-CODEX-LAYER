from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
root=Path(__file__).resolve().parents[2]
font=root/'work/MesenCE-master/UI/Assets/RasterDisplay.ttf'
im=Image.new('RGB',(1280,920),'#101418');d=ImageDraw.Draw(im)
def text(x,y,s,size,color='#DFEBE7'):
 d.text((x,y),s,font=ImageFont.truetype(str(font),size),fill=color)
text(64,48,'RASTER DISPLAY',48,'#AFF2DA')
text(64,112,'Original typeface / Native audio OSD / Design specimen',20,'#92ACAE')
for y,size,label in [(191,32,'REFERENCE  080  SOUND ON'),(258,24,'CRT / LIVING ROOM   HEADPHONES   NIGHT'),(319,18,'Quick volume controls. Simple, readable, immediate.'),(365,16,'ABCDEFGHIJKLMNOPQRSTUVWXYZ  0123456789  +/- %'),(400,16,'abcdefghijklmnopqrstuvwxyz  0 O / 1 I l / 5 S / 8 B')]:
 text(64,y,label,size)
d.rounded_rectangle((64,491,750,733),20,fill='#172127',outline='#4A7069',width=2)
text(98,520,'REFERENCE',30,'#AFF2DA');text(570,518,'080',46,'#C8FBE8')
text(98,581,'VOLUME 80%',24)
for i in range(30):d.rectangle((98+i*20,634,111+i*20,650),fill='#96E4C9' if i<24 else '#31434A')
text(98,681,'CTRL +/-   CTRL M',20,'#91ADB0')
text(815,525,'MUTED',30,'#AFF2DA');text(815,581,'VOLUME 80%',20);text(815,630,'Level remembered',18,'#91ADB0')
text(64,796,'One glyph source. Vector UI + bitmap game overlays.',22,'#AFF2DA')
text(64,843,'Font and layout specimen; the Windows interface has not yet been built.',16,'#92ACAE')
im.save(root/'review/Raster_Display_Specimen.png')
