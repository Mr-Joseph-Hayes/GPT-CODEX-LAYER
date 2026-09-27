"""Build original Raster Display ASCII typeface and the matching native OSD bitmap.
No font downloads. Geometry and glyph source are editable. GPL-3.0-or-later.
"""
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
import json,re
GLYPHS={
' ':['00000']*7,
'A':'01110 10001 10001 11111 10001 10001 10001',
'B':'11110 10001 10001 11110 10001 10001 11110',
'C':'01111 10000 10000 10000 10000 10000 01111',
'D':'11110 10001 10001 10001 10001 10001 11110',
'E':'11111 10000 10000 11110 10000 10000 11111',
'F':'11111 10000 10000 11110 10000 10000 10000',
'G':'01111 10000 10000 10111 10001 10001 01111',
'H':'10001 10001 10001 11111 10001 10001 10001',
'I':'01110 00100 00100 00100 00100 00100 01110',
'J':'00111 00010 00010 00010 10010 10010 01100',
'K':'10001 10010 10100 11000 10100 10010 10001',
'L':'10000 10000 10000 10000 10000 10000 11111',
'M':'10001 11011 10101 10101 10001 10001 10001',
'N':'10001 11001 11001 10101 10011 10011 10001',
'O':'01110 10001 10001 10001 10001 10001 01110',
'P':'11110 10001 10001 11110 10000 10000 10000',
'Q':'01110 10001 10001 10001 10101 10010 01101',
'R':'11110 10001 10001 11110 10100 10010 10001',
'S':'01111 10000 10000 01110 00001 00001 11110',
'T':'11111 00100 00100 00100 00100 00100 00100',
'U':'10001 10001 10001 10001 10001 10001 01110',
'V':'10001 10001 10001 10001 10001 01010 00100',
'W':'10001 10001 10001 10101 10101 11011 10001',
'X':'10001 10001 01010 00100 01010 10001 10001',
'Y':'10001 10001 01010 00100 00100 00100 00100',
'Z':'11111 00001 00010 00100 01000 10000 11111',
'0':'01110 10001 10011 10101 11001 10001 01110',
'1':'00100 01100 00100 00100 00100 00100 01110',
'2':'01110 10001 00001 00110 01000 10000 11111',
'3':'11110 00001 00001 01110 00001 00001 11110',
'4':'00010 00110 01010 10010 11111 00010 00010',
'5':'11111 10000 10000 11110 00001 00001 11110',
'6':'01110 10000 10000 11110 10001 10001 01110',
'7':'11111 00001 00010 00100 01000 01000 01000',
'8':'01110 10001 10001 01110 10001 10001 01110',
'9':'01110 10001 10001 01111 00001 00001 01110',
'a':'00000 00000 01110 00001 01111 10001 01111',
'b':'10000 10000 10110 11001 10001 10001 11110',
'c':'00000 00000 01111 10000 10000 10000 01111',
'd':'00001 00001 01101 10011 10001 10001 01111',
'e':'00000 00000 01110 10001 11111 10000 01111',
'f':'00110 01001 01000 11100 01000 01000 01000',
'g':'00000 01111 10001 10001 01111 00001 01110',
'h':'10000 10000 10110 11001 10001 10001 10001',
'i':'00100 00000 01100 00100 00100 00100 01110',
'j':'00010 00000 00110 00010 00010 10010 01100',
'k':'10000 10000 10001 10010 11100 10010 10001',
'l':'01100 00100 00100 00100 00100 00100 01110',
'm':'00000 00000 11010 10101 10101 10101 10101',
'n':'00000 00000 10110 11001 10001 10001 10001',
'o':'00000 00000 01110 10001 10001 10001 01110',
'p':'00000 11110 10001 10001 11110 10000 10000',
'q':'00000 01111 10001 10001 01111 00001 00001',
'r':'00000 00000 10110 11001 10000 10000 10000',
's':'00000 00000 01111 10000 01110 00001 11110',
't':'01000 01000 11100 01000 01000 01001 00110',
'u':'00000 00000 10001 10001 10001 10011 01101',
'v':'00000 00000 10001 10001 10001 01010 00100',
'w':'00000 00000 10001 10001 10101 10101 01010',
'x':'00000 00000 10001 01010 00100 01010 10001',
'y':'00000 10001 10001 10001 01111 00001 01110',
'z':'00000 00000 11111 00010 00100 01000 11111',
'.':'00000 00000 00000 00000 00000 00110 00110',
',':'00000 00000 00000 00000 00110 00100 01000',
':':'00000 00110 00110 00000 00110 00110 00000',
';':'00000 00110 00110 00000 00110 00100 01000',
'-':'00000 00000 00000 11111 00000 00000 00000',
'_':'00000 00000 00000 00000 00000 00000 11111',
'+':'00000 00100 00100 11111 00100 00100 00000',
'=':'00000 00000 11111 00000 11111 00000 00000',
'/':'00001 00001 00010 00100 01000 10000 10000',
'\\':'10000 10000 01000 00100 00010 00001 00001',
'!':'00100 00100 00100 00100 00100 00000 00100',
'?':'01110 10001 00001 00010 00100 00000 00100',
'%':'11001 11010 00010 00100 01000 01011 10011',
'(':'00010 00100 01000 01000 01000 00100 00010',
')':'01000 00100 00010 00010 00010 00100 01000',
'[':'01110 01000 01000 01000 01000 01000 01110',
']':'01110 00010 00010 00010 00010 00010 01110',
'<':'00010 00100 01000 10000 01000 00100 00010',
'>':'01000 00100 00010 00001 00010 00100 01000',
'\"':'01010 01010 01010 00000 00000 00000 00000',
"'":'00100 00100 00100 00000 00000 00000 00000',
'#':'01010 01010 11111 01010 11111 01010 01010',
'$':'00100 01111 10100 01110 00101 11110 00100',
'&':'01100 10010 10100 01000 10101 10010 01101',
'*':'00000 10101 01110 11111 01110 10101 00000',
'@':'01110 10001 10111 10101 10111 10000 01111',
'^':'00100 01010 10001 00000 00000 00000 00000',
'`':'01000 00100 00010 00000 00000 00000 00000',
'{':'00011 00100 00100 01000 00100 00100 00011',
'}':'11000 00100 00100 00010 00100 00100 11000',
'|':'00100 00100 00100 00100 00100 00100 00100',
'~':'00000 00000 01001 10110 00000 00000 00000',
}
GLYPHS={k:v.split() if isinstance(v,str) else v for k,v in GLYPHS.items()}
assert all(len(v)==7 and all(len(row)==5 for row in v) for v in GLYPHS.values())
root=Path(__file__).resolve().parents[2]
out=root/'work/MesenCE-master/UI/Assets/RasterDisplay.ttf'
out.parent.mkdir(exist_ok=True,parents=True)
fb=FontBuilder(1000,isTTF=True)
chars=list(range(32,127)); names=['.notdef']+['uni%04X'%c for c in chars]
fb.setupGlyphOrder(names)
fb.setupCharacterMap({c:'uni%04X'%c for c in chars})
glyphs={}; metrics={}
for idx,name in enumerate(names):
 c=chr(chars[idx-1]) if idx else '?'
 pen=TTGlyphPen(None)
 # Trace the boundary of the union of all occupied cells. Shared edges are removed,
 # producing continuous stems without anti-aliased seams between adjacent cells.
 edges=set()
 for row,line in enumerate(GLYPHS.get(c,GLYPHS['?'])):
  for col,bit in enumerate(line):
   if bit=='0': continue
   x=col; y=6-row
   points=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
   for a,b in zip(points,points[1:]+points[:1]):
    if (b,a) in edges:edges.remove((b,a))
    else:edges.add((a,b))
 directions={(1,0):0,(0,1):1,(-1,0):2,(0,-1):3}
 while edges:
  first=min(edges);edges.remove(first); contour=[first[0],first[1]]
  while contour[-1]!=contour[0]:
   before,current=contour[-2:]
   direction=directions[(current[0]-before[0],current[1]-before[1])]
   candidates=[e for e in edges if e[0]==current]
   assert candidates
   priority={1:0,0:1,3:2,2:3}
   def rank(e):
    d=directions[(e[1][0]-e[0][0],e[1][1]-e[0][1])]
    return priority[(d-direction)%4]
   nxt=min(candidates,key=rank);edges.remove(nxt);contour.append(nxt[1])
  contour=contour[:-1]
  simplified=[]
  for i,b in enumerate(contour):
   a=contour[i-1];cpt=contour[(i+1)%len(contour)]
   if (b[0]-a[0])*(cpt[1]-b[1])!=(b[1]-a[1])*(cpt[0]-b[0]):simplified.append(b)
  pen.moveTo((simplified[0][0]*100+35,simplified[0][1]*100))
  for x,y in simplified[1:]:pen.lineTo((x*100+35,y*100))
  pen.closePath()
 glyphs[name]=pen.glyph();metrics[name]=(600,35)
fb.setupGlyf(glyphs);fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=850,descent=-150)
fb.setupOS2(sTypoAscender=850,sTypoDescender=-150,usWinAscent=850,usWinDescent=150,sxHeight=500,sCapHeight=700)
fb.setupNameTable({'familyName':'Raster Display','styleName':'Regular','uniqueFontIdentifier':'Raster Display 0.1','fullName':'Raster Display Regular','psName':'RasterDisplay-Regular','version':'Version 0.1','copyright':'Original Raster Display glyphs. Copyright 2026 Joseph Hayes. GPL-3.0-or-later.'})
fb.setupPost(isFixedPitch=1);fb.setupMaxp();fb.font['head'].created=fb.font['head'].modified=3800000000
fb.save(out)
p=root/'work/MesenCE-master/Core/Shared/Video/DrawStringCommand.h'
s=p.read_text()
rows=[]
for c in list(map(chr,chars))+['?']:
 rows.append('        6, '+', '.join(str(int(row,2)<<3) for row in GLYPHS[c])+',')
s=re.sub(r'static constexpr uint8_t _font\[(?:792|768)\] = \{.*?\n\t\};','static constexpr uint8_t _font[768] = {\n'+'\n'.join(rows)+'\n\t};',s,count=1,flags=re.S)
s=s.replace("int rowOffset = (c == 'y' || c == 'g' || c == 'p' || c == 'q') ? 1 : 0;",'int rowOffset = 0; // Raster glyphs contain their complete seven-row design.')
p.write_text(s)
(root/'raster-overlay/docs/raster-glyphs.json').write_text(json.dumps(GLYPHS,indent=2))
print('Built original 95-character Raster Display font and matching OSD glyphs')
