#!/usr/bin/env python3
"""Render animated, GitHub-README-safe SVG cards for Psychomods666.

Input: data/contributions.json with {"total": int, "days": [{"date":"YYYY-MM-DD","count":int}]}
Run: python render_cards.py [--static]   or STATIC=1 python render_cards.py
"""
from __future__ import annotations
import argparse, base64, datetime as dt, html, json, os, re, shutil, subprocess, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "cards"
DATA = ROOT / "data" / "contributions.json"
BG, PANEL, GREEN, MUTED, LINE = "#0A0A12", "#111522", "#00FF41", "#A7B3A8", "#263344"
WHITE, FONT = "#F3F7F3", "Fira Code"
USER = "Psychomods666"
REPOS = [
    ("NetDefend-AI", "AI-powered network threat detection", "Python", "#3572A5"),
    ("psychomods-forensic-lab", "Digital forensics and investigation lab", "Security Research", GREEN),
    ("testwebsite", "Web development and experiments", "Web", "#8B9CF6"),
]
LINKS = [("GITHUB", f"https://github.com/{USER}"), ("PROJECTS", f"https://github.com/{USER}?tab=repositories"), ("WEBSITE", "https://psychomods.infy.uk")]

def esc(s): return html.escape(str(s), quote=True)
def load_font():
    """Download Fira Code, subset it with pyftsubset, and embed WOFF2 as a data URI."""
    cache = ROOT / ".cache"; cache.mkdir(exist_ok=True)
    source, subset = cache / "FiraCode-Regular.ttf", cache / "FiraCode-subset.woff2"
    if not source.exists():
        url = "https://github.com/tonsky/FiraCode/raw/master/distr/ttf/FiraCode-Regular.ttf"
        try:
            urllib.request.urlretrieve(url, source)
        except Exception as e:
            print(f"Font download skipped ({e}); SVG uses monospace fallback.")
            return ""
    chars = "Ashwin Joyson PSYCHOMODS Cybersecurity Researcher AI Developer Ethical Hacker BREAK IT TO UNDERSTAND IT BUILD IT TO DEFEND IT GITHUB PROJECTS WEBSITE ACTIVITY MONITOR CONTRIBUTIONS CURRENT STREAK ACTIVE DAYS BUSIEST DAY FEATURED REPOSITORIES NetDefend-AI psychomods-forensic-lab testwebsite Python Security Research Web 0123456789+-/.:%()[]_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if shutil.which("pyftsubset"):
        subprocess.run(["pyftsubset", str(source), f"--output-file={subset}", "--flavor=woff2", "--text="+chars, "--layout-features=*", "--no-hinting"], check=True)
        return "data:font/woff2;base64," + base64.b64encode(subset.read_bytes()).decode()
    print("pyftsubset not installed; install fonttools[woff] to embed the subset font.")
    return ""

FONT_URI = load_font()
STATIC = os.getenv("STATIC", "0") == "1"

def svg_start(w, h, delay=0):
    css = f'''<style>
    @font-face{{font-family:'Fira Code';src:url('{FONT_URI}') format('woff2');font-weight:400}}
    text{{font-family:'Fira Code',ui-monospace,monospace}}
    .card{{fill:{BG};stroke:{LINE};stroke-width:1.4}}
    .glow{{filter:url(#glow)}}
    @keyframes enter{{0%{{opacity:0;transform:translateY(18px)}}100%{{opacity:1;transform:translateY(0)}}}}
    @keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
    @keyframes scan{{0%{{transform:translateY(-12px);opacity:0}}15%{{opacity:.24}}85%{{opacity:.12}}100%{{transform:translateY(180px);opacity:0}}}}
    .enter{{animation:enter .85s ease-out {delay}s both}}
    .pulse{{animation:pulse 2.8s ease-in-out {delay+.6}s infinite}}
    .scan{{animation:scan 5s linear {delay}s infinite}}
    @media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important;transition:none!important}}.smil-motion{{display:none!important}}}}
    </style>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" viewBox="0 0 {w} {h}" role="img"><title>Psychomods profile card</title><defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><linearGradient id="edge"><stop stop-color="{GREEN}" stop-opacity=".05"/><stop offset=".5" stop-color="{GREEN}" stop-opacity=".8"/><stop offset="1" stop-color="{GREEN}" stop-opacity=".05"/></linearGradient><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{GREEN}" stroke-opacity=".055" stroke-width=".7"/></pattern></defs>{css}'''

def finish(body): return body + "</svg>\n"
def write(name, body):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(body, encoding="utf-8")

def hero():
    b=svg_start(1000,260,0)+f'''<rect x="1" y="1" width="998" height="258" rx="18" class="card"/><rect x="2" y="2" width="996" height="256" rx="17" fill="url(#grid)"/><rect x="0" y="0" width="1000" height="3" rx="2" fill="url(#edge)"/>
    <g class="enter"><text x="54" y="55" fill="{GREEN}" font-size="15" letter-spacing="4">PSYCHOMODS / PROFILE.SYS</text><text x="52" y="133" fill="{WHITE}" font-size="52" font-weight="700">ASHWIN JOYSON</text><text x="55" y="174" fill="{MUTED}" font-size="18">Cybersecurity Researcher  /  AI Developer  /  Ethical Hacker</text><text x="55" y="220" fill="{GREEN}" font-size="13" letter-spacing="1.5">BREAK IT TO UNDERSTAND IT. BUILD IT TO DEFEND IT.</text></g>
    <g class="pulse"><circle cx="905" cy="77" r="35" fill="none" stroke="{GREEN}" stroke-opacity=".5"/><circle cx="905" cy="77" r="24" fill="none" stroke="{GREEN}"/><path d="M905 45V109M873 77H937" stroke="{GREEN}" stroke-opacity=".45"/><circle cx="905" cy="77" r="5" fill="{GREEN}" class="glow"/><circle cx="905" cy="77" r="35" fill="none" stroke="{GREEN}" stroke-opacity=".35" class="smil-motion"><animate attributeName="r" values="34;42;34" dur="3s" repeatCount="indefinite"/></circle></g><text x="845" y="143" fill="{GREEN}" font-size="10">SECURITY LAB</text><rect class="scan" x="0" y="0" width="1000" height="2" fill="{GREEN}" opacity=".2"/>'''
    return finish(b)

def tiles():
    b=svg_start(1000,150,.8)+f'<rect x="1" y="1" width="998" height="148" rx="16" class="card"/>'
    for i,(label,url) in enumerate(LINKS):
        x=10+i*330
        b+=f'''<a xlink:href="{esc(url)}"><g class="enter" style="animation-delay:{.8+i*.12}s"><rect x="{x}" y="12" width="{324}" height="126" rx="12" fill="{PANEL}" stroke="{LINE}"/><text x="{x+22}" y="51" fill="{GREEN}" font-size="12">0{i+1} / LINK</text><text x="{x+22}" y="91" fill="{WHITE}" font-size="21">{label} ↗</text><path d="M{x+22} 111H{x+290}" stroke="{GREEN}" stroke-opacity=".5"/></g></a>'''
    return finish(b)

def get_data():
    if not DATA.exists():
        print(f"Missing {DATA}; using an empty calendar. Run the workflow to populate it.")
        return {"total":0,"days":[]}
    raw=json.loads(DATA.read_text()); return raw

def metrics(days):
    today=dt.date.today(); counts={dt.date.fromisoformat(x["date"]):int(x.get("count",0)) for x in days}
    active=sum(v>0 for v in counts.values())
    cur=today if counts.get(today,0)>0 else today-dt.timedelta(days=1)
    streak=0
    while counts.get(cur,0)>0: streak+=1; cur-=dt.timedelta(days=1)
    busiest=max(counts.items(),key=lambda kv:kv[1]) if counts else (today,0)
    return active,streak,busiest

def tile_card(index):
    label,url=LINKS[index]; delay=.8+index*.12
    b=svg_start(330,150,delay)+f'''<a xlink:href="{esc(url)}"><rect x="1" y="1" width="328" height="148" rx="14" class="card"/><g class="enter" style="animation-delay:{delay}s"><text x="22" y="48" fill="{GREEN}" font-size="12">0{index+1} / LINK</text><text x="22" y="88" fill="{WHITE}" font-size="20">{label} ↗</text><path d="M22 112H305" stroke="{GREEN}" stroke-opacity=".5"/></g></a>'''
    return finish(b)

def activity(data):
    days=data.get("days",[]); active,streak,busy=metrics(days)
    today=dt.date.today(); months=[]
    for back in range(11,-1,-1):
        month=(today.replace(day=1)-dt.timedelta(days=back*30)).replace(day=1)
        key=month.strftime("%Y-%m"); val=sum(int(x.get("count",0)) for x in days if x["date"].startswith(key))
        months.append((month.strftime("%b"),val))
    maxv=max([v for _,v in months]+[1]); b=svg_start(1000,310,1.6)+f'<rect x="1" y="1" width="998" height="308" rx="16" class="card"/><text x="30" y="40" fill="{GREEN}" font-size="15" letter-spacing="2">02 / CONTRIBUTION INTELLIGENCE</text>'
    stats=[(str(streak),"CURRENT STREAK"),(str(active),"ACTIVE DAYS"),(str(busy[1]),"BUSIEST DAY")]
    for i,(v,l) in enumerate(stats):
        x=35+i*315;b+=f'<g class="enter"><text x="{x}" y="92" fill="{WHITE}" font-size="30">{esc(v)}</text><text x="{x}" y="116" fill="{MUTED}" font-size="10">{l}</text></g>'
    b+=f'<text x="35" y="158" fill="{GREEN}" font-size="11">MONTHLY CONTRIBUTIONS / LAST 12 MONTHS</text>'
    for i,(m,v) in enumerate(months):
        x=38+i*78; h=82*v/maxv; y=263-h
        b+=f'<rect x="{x}" y="{y:.1f}" width="42" height="{h:.1f}" rx="4" fill="{GREEN}" opacity=".78" class="enter" style="animation-delay:{1.8+i*.035}s"/><text x="{x+21}" y="282" text-anchor="middle" fill="{MUTED}" font-size="10">{m}</text>'
    b+=f'<text x="965" y="296" text-anchor="end" fill="{MUTED}" font-size="9">Busiest: {busy[0].strftime("%d %b %Y")}</text>'
    return finish(b)

def repo_card(repo,index):
    name,desc,lang,color=repo; delay=2.7+index*.35
    b=svg_start(1000,174,delay)+f'''<rect x="1" y="1" width="998" height="172" rx="16" class="card"/><a xlink:href="https://github.com/{USER}/{esc(name)}"><g class="enter"><text x="30" y="39" fill="{GREEN}" font-size="12">0{index+1} / FEATURED REPOSITORY</text><text x="30" y="86" fill="{WHITE}" font-size="27">{esc(name)}</text><text x="31" y="119" fill="{MUTED}" font-size="14">{esc(desc)}</text><rect x="30" y="139" width="12" height="12" rx="6" fill="{color}"/><text x="51" y="150" fill="{MUTED}" font-size="11">{esc(lang)}</text><text x="960" y="87" text-anchor="end" fill="{GREEN}" font-size="17">OPEN REPOSITORY</text></g></a>'''
    return finish(b)

def contribution_graph(data):
    days=data.get("days",[]); today=dt.date.today(); bydate={dt.date.fromisoformat(x["date"]):int(x.get("count",0)) for x in days}
    start=today-dt.timedelta(days=363); start-=dt.timedelta(days=(start.weekday()+1)%7)
    maxv=max(bydate.values(),default=1); b=svg_start(1000,190,4.0)+f'<rect x="1" y="1" width="998" height="188" rx="16" class="card"/><text x="28" y="34" fill="{GREEN}" font-size="14" letter-spacing="2">03 / CONTRIBUTION MATRIX</text>'
    for i in range(53):
        for j in range(7):
            d=start+dt.timedelta(days=i*7+j); c=bydate.get(d,0)
            opacity=0 if c==0 else .25+.75*min(c/maxv,1)
            b+=f'<rect x="{28+i*17}" y="{52+j*17}" width="12" height="12" rx="2" fill="{GREEN}" opacity="{opacity:.2f}" class="enter" style="animation-delay:{4+i*.008}s"/>'
    b+=f'<text x="28" y="181" fill="{MUTED}" font-size="9">LESS</text><rect x="70" y="172" width="10" height="10" rx="2" fill="{GREEN}" opacity=".2"/><rect x="86" y="172" width="10" height="10" rx="2" fill="{GREEN}" opacity=".45"/><rect x="102" y="172" width="10" height="10" rx="2" fill="{GREEN}" opacity=".7"/><rect x="118" y="172" width="10" height="10" rx="2" fill="{GREEN}"/><text x="137" y="181" fill="{MUTED}" font-size="9">MORE</text>'
    return finish(b)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--static",action="store_true"); args=parser.parse_args()
    global STATIC
    STATIC=STATIC or args.static
    data=get_data()
    OUT.mkdir(exist_ok=True)
    for p in OUT.glob("*.svg"): p.unlink()
    write("01-hero.svg",hero());
    for i in range(3): write(f"02-link-{i+1}.svg",tile_card(i))
    write("03-activity.svg",activity(data))
    for i,r in enumerate(REPOS,1): write(f"04-repo-{i}.svg",repo_card(r,i))
    write("05-contributions.svg",contribution_graph(data))
    if STATIC:
        # Replace CSS animations with their visible end state for deterministic screenshots.
        for p in OUT.glob("*.svg"):
            s=p.read_text().replace("animation:enter .85s ease-out", "animation:none").replace("animation:pulse 2.8s ease-in-out", "animation:none").replace("animation:scan 5s linear", "animation:none")
            s=s.replace("opacity:0;transform:translateY(18px)","opacity:1;transform:translateY(0)")
            s=re.sub(r"<animate\b[^>]*/>", "", s)
            p.write_text(s)
    print(f"Rendered {len(list(OUT.glob('*.svg')))} SVG cards in {OUT}")

if __name__ == "__main__": main()
