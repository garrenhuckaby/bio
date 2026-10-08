"""Small static publisher. Markdown content is trusted repository-owned input."""
import argparse, json, shutil, os, re
from pathlib import Path
from datetime import date
from html import escape as e
from string import Template
from urllib.parse import urlparse
import markdown
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--base',default=os.environ.get('BASE_PATH',''))
parser.add_argument('--site-url',default=os.environ.get('SITE_URL',''))
parser.add_argument('--preview',action='store_true')
a=parser.parse_args(); base='/' + a.base.strip('/') if a.base.strip('/') else ''
if base and not re.fullmatch(r'/[a-zA-Z0-9_./-]+',base): raise ValueError('Invalid base path')
origin=a.site_url.rstrip('/')
if origin and (urlparse(origin).scheme not in ('http','https') or not urlparse(origin).netloc): raise ValueError('Invalid site URL')
config=json.loads((ROOT/'site.json').read_text()); out=ROOT/'dist'
if out.exists(): shutil.rmtree(out)
out.mkdir(); shutil.copytree(ROOT/'assets',out/'assets'); (out/'.nojekyll').touch()
template=Template((ROOT/'templates/page.html').read_text()); routes=[]
def url(path): return base+'/'+path.strip('/')+('/' if path.strip('/') else '')
def external(value):
 if urlparse(value).scheme not in ('http','https'): raise ValueError('Only HTTPS/HTTP profile and source links are supported')
 return e(value,quote=True)
def load(collection):
 items=[]
 for f in sorted((ROOT/'content'/collection).glob('*.md')):
  raw=f.read_text(); _,front,body=raw.split('---',2); data=json.loads(front)
  if data.get('draft') and not a.preview: continue
  if data.get('date'): date.fromisoformat(data['date'])
  data.update(slug=f.stem,html=markdown.markdown(body,extensions=['fenced_code','tables','toc']))
  items.append(data)
 return sorted(items,key=lambda d:d.get('date',d.get('number','')),reverse=collection!='projects')
def page(path,title,description,body,active=''):
 nav=''.join(f'<a href="{url(p)}"'+(' aria-current="page"' if active==p else '')+f'>{label}</a>' for p,label in [('', 'Home'),('projects','Projects'),('blog','Blog'),('news','News'),('contact','Contact')])
 target=out/(path.strip('/')+'/index.html' if path.strip('/') else 'index.html'); target.parent.mkdir(parents=True,exist_ok=True)
 canonical=f'<link rel="canonical" href="{e(origin+url(path),quote=True)}">' if origin else ''
 preview='<div class="wrap preview-note">Development preview · Draft bio and project copy awaiting your review.</div>' if a.preview else ''
 target.write_text(template.substitute(title=e(title+' | Garren Huckaby'),description=e(description,quote=True),canonical=canonical,base=base,body=body,navigation=nav,preview=preview,year=date.today().year)); routes.append(path)
def heading(kicker,title,description): return f'<section class="page-heading"><div class="eyebrow">{e(kicker)}</div><h1>{e(title)}</h1><p>{e(description)}</p></section>'
def tags(values): return ''.join(f'<span class="tag">{e(t)}</span>' for t in values)
portrait=config.get('portrait','')
if portrait:
 path=ROOT/'assets'/portrait
 if not path.is_file() or not path.resolve().is_relative_to((ROOT/'assets').resolve()): raise ValueError('Portrait must be a file inside assets/')
 photo=f'<img class="portrait" src="{base}/assets/{e(portrait,quote=True)}" alt="{e(config["portrait_alt"],quote=True)}" width="600" height="750" fetchpriority="high">'
else: photo='<div class="portrait-placeholder" role="img" aria-label="Portrait placeholder; a photo of Garren will be added"><strong>GH</strong><span>PORTRAIT TO COME</span></div>'
bio=''.join(f'<p>{e(p)}</p>' for p in config['bio'])
page('','Home','Garren Huckaby’s projects, writing, and curated reading.',f'<section class="welcome"><div><div class="eyebrow">Welcome. I’m Garren.</div><h1>Hi, I’m<span>Garren.</span></h1><div class="bio">{bio}</div><div class="intro-links"><a class="button primary" href="{url("projects")}">Explore my projects</a><a class="button" href="{url("contact")}">Get in touch</a></div></div><div><div class="portrait-frame">{photo}</div><div class="portrait-caption"><span>Garren Huckaby</span><span>Electrical engineering</span></div></div></section><section class="home-bottom" aria-label="Explore the site"><div><a href="{url("projects")}">01 / Projects</a><p>Hardware, software, and experiments.</p></div><div><a href="{url("blog")}">02 / Build notes</a><p>Ideas and lessons along the way.</p></div><div><a href="{url("news")}">03 / Worth reading</a><p>News and research, selected by me.</p></div></section>')
projects=load('projects'); cards=[]
for d in projects:
 cards.append(f'<article class="project-card"><div class="project-top"><strong>{e(d["title"])}</strong><span>{e(d["number"])}</span></div><div class="project-photo-placeholder" role="img" aria-label="Project photo placeholder">Project photo placeholder</div><div class="project-copy"><div class="meta">{e(d["category"])}</div><h2><a href="{url("projects/"+d["slug"])}">{e(d["title"])}</a></h2><p>{e(d["description"])}</p><span class="tag">{e(d["status"])}</span></div></article>')
 page('projects/'+d['slug'],d['title'],d['description'],f'<article class="article"><a href="{url("projects")}">All projects</a><h1>{e(d["title"])}</h1><p class="dek">{e(d["description"])}</p><div class="prose">{d["html"]}</div></article>','projects')
page('projects','Projects','Hardware, software, and engineering experiments.',heading('Selected work','Things I’m building.','Projects at the intersection of hardware, software, and practical problems.')+'<div class="project-grid">'+''.join(cards)+'</div>','projects')
for collection,title,intro in [('blog','Build notes.','A place for engineering, experiments, and ideas.'),('news','Worth reading.','News and research I’ve selected, with a few thoughts on why they matter.')]:
 entries=load(collection); cards=[]
 for d in entries:
  draft='<span class="tag">Sample draft</span>' if d.get('draft') else ''
  label=d.get('source','')
  extra=f'<p><a href="{external(d["url"])}">Read original at {e(label)}</a></p>' if collection=='news' else ''
  cards.append(f'<article class="card"><div class="meta"><time datetime="{d["date"]}">{date.fromisoformat(d["date"]).strftime("%b %d, %Y")}</time>{draft}</div><h2><a href="{url(collection+"/"+d["slug"])}">{e(d["title"])}</a></h2><p>{e(d["description"])}</p><div class="meta">{tags(d.get("tags",[]))}</div></article>')
  notice='<div class="draft">Sample draft · This entry is excluded from production builds.</div>' if d.get('draft') else ''
  page(collection+'/'+d['slug'],d['title'],d['description'],f'<article class="article"><a href="{url(collection)}">All {"posts" if collection=="blog" else "reading"}</a><h1>{e(d["title"])}</h1><div class="meta"><time datetime="{d["date"]}">{d["date"]}</time>{tags(d.get("tags",[]))}</div><p class="dek">{e(d["description"])}</p>{notice}{extra}<div class="prose">{d["html"]}</div></article>',collection)
 empty='<div class="empty"><h2>'+('The first post is on its way.' if collection=='blog' else 'The reading list starts here.')+'</h2><p>'+('New posts will appear here as I publish them.' if collection=='blog' else 'Selected articles and my commentary will appear here.')+'</p></div>'
 aside='<h2>About these notes</h2><p>Design decisions, experiments, and what I learn while building.</p><h2>Areas of interest</h2><ul><li>Embedded systems</li><li>Sensors and electronics</li><li>Software and startups</li></ul>' if collection=='blog' else '<h2>Through my lens</h2><p>This is a personally curated reading list. Each entry links to its source and includes my own commentary.</p><h2>What catches my eye</h2><ul><li>Robotics and sensors</li><li>Batteries and energy</li><li>AI and engineering</li></ul>'
 page(collection,'Blog' if collection=='blog' else 'Curated news',intro,heading('Writing' if collection=='blog' else 'Garren’s reading list',title,intro)+f'<div class="editorial"><div class="cards">'+(''.join(cards) or empty)+f'</div><aside class="sidebar">{aside}</aside></div>',collection)
links=''.join(f'<span class="button placeholder-link" aria-disabled="true">{e(x["label"])} · placeholder</span>' if x.get('placeholder') else f'<a class="button" href="{external(x["url"])}">{e(x["label"])}</a>' for x in config.get('links',[]))
email=config.get('email','')
if email:
 if not re.fullmatch(r'[^\s@?]+@[^\s@?]+\.[^\s@?]+',email): raise ValueError('Invalid email')
 links=f'<a class="button primary" href="mailto:{e(email,quote=True)}">{e(email)}</a>'+links
contact=f'<p>I’d enjoy hearing about interesting projects, engineering problems, or opportunities to collaborate.</p><div class="contact-links">{links}</div>' if links else '<div class="empty"><h2>Contact details coming soon.</h2><p>Email and profile links will appear here once they’re ready to share.</p></div>'
page('contact','Contact','Contact Garren Huckaby.',heading('Say hello','Let’s connect.','Engineering, projects, and good conversations.')+f'<section class="contact-box">{contact}</section>','contact')
page('404','Page not found','The requested page could not be found.',heading('404','A loose connection.','This page doesn’t exist, or the address has changed.')+f'<p><a class="button primary" href="{url("")}">Back to home</a></p>')
shutil.move(out/'404/index.html',out/'404.html'); (out/'404').rmdir(); routes.remove('404')
if origin:
 (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+e(origin+url(p))+'</loc></url>' for p in routes)+'</urlset>')
 (out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+origin+base+'/sitemap.xml\n')
print(f'Built {len(routes)+1} pages into {out}; base={base or "/"}; preview={a.preview}')
