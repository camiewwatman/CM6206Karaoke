# SPDX-License-Identifier: GPL-3.0-or-later
from flask import Flask,request,jsonify,Response
import glob,subprocess
app=Flask(__name__)
HTML='''<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>CM6206</title><style>:root{color-scheme:dark;font-family:system-ui}body{background:#020617;color:#e2e8f0;margin:0}.w{max-width:760px;margin:auto;padding:24px}.c{background:#0f172a;border:1px solid #1e293b;border-radius:18px;padding:20px;margin:16px 0}.g{display:grid;grid-template-columns:1fr 1fr;gap:14px}button{padding:18px;border:0;border-radius:12px;background:#1e293b;color:white;font-weight:700}.pcm{background:#0891b2}.dolby{background:#7c3aed}input{width:100%}.v{font-size:36px;font-weight:700}.m{color:#94a3b8}@media(max-width:600px){.g{grid-template-columns:1fr}}</style><main class="w"><h1>CM6206 Audio Control</h1><span id="s">Loading...</span><section class="c g"><button id="pcm" onclick="mode('pcm')">PCM + Microphone</button><button id="dolby" onclick="mode('dolby')">Dolby / Encoded</button></section><section class="g"><div class="c"><h2>Line In</h2><div class="v"><span id="ld">100</span>%</div><div class="m">Hardware: <span id="lh">80</span>%</div><input id="line" type="range" min="0" max="100" value="100"></div><div class="c"><h2>Microphone</h2><div class="v"><span id="md">100</span>%</div><div class="m">Hardware: <span id="mh">100</span>%</div><input id="mic" type="range" min="0" max="100" value="100"></div></section><section class="c m" id="r"></section><script>let M='pcm',T={};const S=x=>s.textContent=x;async function P(u,d){let x=await fetch(u,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});if(!x.ok)throw Error(await x.text());return x.json()}function R(){pcm.className=M==='pcm'?'pcm':'';dolby.className=M==='dolby'?'dolby':'';line.disabled=mic.disabled=M!=='pcm';r.textContent=M==='pcm'?'TOSLINK In -> Front Out -> TRS -> Line In + Mic -> Mixer -> SPDIF Out':'Encoded S/PDIF passthrough'}async function mode(m){try{await P('/api/mode',{mode:m});M=m;R();S('Mode: '+m)}catch(e){S(e.message)}}function V(id,d,h,c,k){let x=document.getElementById(id);x.oninput=()=>{document.getElementById(d).textContent=x.value;let p=Math.round(x.value*k);document.getElementById(h).textContent=p;clearTimeout(T[c]);T[c]=setTimeout(()=>P('/api/volume',{channel:c,percent:p}).then(()=>S(c+' '+p+'%')).catch(e=>S(e.message)),80)}}V('line','ld','lh','line',.8);V('mic','md','mh','mic',1);fetch('/api/status').then(x=>x.json()).then(x=>{M=x.mode||'pcm';R();S(x.ok?'Ready - ALSA card '+x.card:'Unavailable')});</script>'''
def card():
 for p in glob.glob('/proc/asound/card*/id'):
  try:
   if open(p).read().strip()=='ICUSBAUDIO7D':return p.split('/card',1)[1].split('/',1)[0]
  except OSError:pass
 raise RuntimeError('CM6206 not found')
def run(a):
 r=subprocess.run(a,capture_output=True,text=True,timeout=10)
 if r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip())
def cur():
 try:return open('/run/cm6206-mode').read().strip()
 except:return 'pcm'
@app.get('/')
def index():return Response(HTML,mimetype='text/html')
@app.get('/api/health')
def health():return jsonify(ok=True)
@app.get('/api/status')
def status():
 try:return jsonify(ok=True,card=int(card()),mode=cur())
 except Exception as e:return jsonify(ok=False,error=str(e),mode=cur()),500
@app.post('/api/mode')
def mode():
 m=(request.get_json(silent=True)or{}).get('mode')
 if m not in ('pcm','dolby'):return jsonify(error='invalid mode'),400
 try:run(['/usr/bin/sudo','/usr/local/sbin/cm6206-mode','encoded' if m=='dolby' else 'pcm']);return jsonify(ok=True,mode=m)
 except Exception as e:return jsonify(ok=False,error=str(e)),500
@app.post('/api/volume')
def volume():
 d=request.get_json(silent=True)or{};ch=d.get('channel')
 if ch not in ('line','mic'):return jsonify(error='invalid channel'),400
 try:p=int(d.get('percent'))
 except:return jsonify(error='invalid percent'),400
 if not 0<=p<=100:return jsonify(error='invalid percent'),400
 p=min(p,80) if ch=='line' else p
 try:c=card();run(['/usr/bin/amixer','-q','-c',c,'sset','Line' if ch=='line' else 'Mic',f'{p}%','cap']);return jsonify(ok=True,percent=p)
 except Exception as e:return jsonify(ok=False,error=str(e)),500
