from pathlib import Path
import base64,hashlib,json
root=Path(__file__).resolve().parents[2]
source=root/'work/MesenCE-master';base=root/'work/MesenCE-base';out=root/'raster-overlay'
def digest(data): return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()
files=[]
for p in sorted(source.rglob('*')):
 if not p.is_file():continue
 relative=p.relative_to(source); prior=base/relative;data=p.read_bytes()
 if prior.is_file() and data==prior.read_bytes():continue
 if p.suffix in {'.o','.exe','.dll','.so','.wav','.zip'}:continue
 stored=str(relative)+('.b64' if p.suffix=='.ttf' else '')
 target=out/'overlay'/stored;target.parent.mkdir(parents=True,exist_ok=True)
 target.write_bytes(base64.b64encode(data) if p.suffix=='.ttf' else data)
 files.append({'path':str(relative),'stored_path':stored,'encoding':'base64' if p.suffix=='.ttf' else 'utf-8','base_sha256':digest(prior.read_bytes()) if prior.exists() else None,'sha256':digest(data)})
(out/'manifest.json').write_text(json.dumps({'version':'0.1.0','upstream_repository':'nesdev-org/MesenCE','upstream_commit':'a60e79feb4d6dcced5922d636f9211837d01e381','files':files},indent=2)+'\n')
print('Overlay files:',len(files))
