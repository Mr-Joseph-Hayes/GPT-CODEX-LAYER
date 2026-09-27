from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import sys
source=Path(sys.argv[1]);out=Path(sys.argv[2])
with ZipFile(out,'w',ZIP_DEFLATED) as z:
 for p in source.rglob('*'):
  rel=p.relative_to(source)
  if p.is_file() and not any(x in {'.git','bin','obj','build','.vs','__pycache__'} for x in rel.parts) and p.name!='Dependencies.zip':
   z.write(p,Path('Raster-MesenCE')/rel)
