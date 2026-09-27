"""Apply Raster's audited files to the pinned MesenCE source tree."""
from pathlib import Path
import argparse, base64, hashlib, json, shutil
parser=argparse.ArgumentParser()
parser.add_argument('source', type=Path)
args=parser.parse_args()
root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text())
def digest(path):
 data=path.read_bytes()
 return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()
for item in manifest['files']:
 target=args.source/item['path']
 if item['base_sha256'] is not None:
  if not target.is_file() or digest(target)!=item['base_sha256']:
   raise SystemExit('Upstream source mismatch: '+item['path'])
 elif target.exists():
  raise SystemExit('New file already exists: '+item['path'])
# Complete preflight before copying anything.
for item in manifest['files']:
 target=args.source/item['path'];target.parent.mkdir(parents=True,exist_ok=True)
 src=root/'overlay'/item['stored_path']
 if item['encoding']=='base64': target.write_bytes(base64.b64decode(src.read_text()))
 else: shutil.copyfile(src,target)
 if digest(target)!=item['sha256']: raise SystemExit('Output digest mismatch: '+item['path'])
print('Applied',len(manifest['files']),'files to MesenCE',manifest['upstream_commit'])
