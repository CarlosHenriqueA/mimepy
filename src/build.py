#!/usr/bin/env python3
"""
MimePy v0.2 — build.py (gerador genérico e reutilizável)
==========================================================
Converte um conjunto de arquivos Markdown em UMA página HTML bonita,
no estilo GitBook/ReadTheDocs (sidebar + TOC + tipografia limpa),
com recursos modernos: busca, dark mode, navegação prev/next,
copy de código, back-to-top e impressão/PDF.

USO:
    python src/build.py                  # usa config.py do diretório pai
    python src/build.py /path/config.py  # usa outro config

COMPATIBILIDADE:
    - configs antigos (v0.1) funcionam: todos os novos recursos têm default.
    - Extensões e sidebar idênticas; nada de comportamento antigo foi quebrado.

REQUISITO: pip install markdown
"""
import os
import re
import sys
import html as _html
import importlib.util
from pathlib import Path

# Módulos internos (refactor v0.4 — separados para test/limpieza):
#   - security.py : sanitizador HTML robusto (parser real, stdlib)
#   - themes.py   : temas CSS (light/dark/neon/paper/mono) + get_theme_css
sys.path.insert(0, str(Path(__file__).resolve().parent))
from security import sanitize_html            # noqa: E402
from themes import get_theme_css, THEMES_CSS  # noqa: E402   (reexport para compat)
from render import render_md                  # noqa: E402   (docs/landing/blog)

# ---------------------------------------------------------------- config
def load_config(config_path):
    spec = importlib.util.spec_from_file_location("mimepy_cfg", config_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PROJECT

HERE = Path(__file__).resolve().parent
FRAMEWORK_ROOT = HERE.parent
# Fonte única de versão (v0.4): ver src/_meta.py — evita drift entre módulos.
from _meta import VERSION  # noqa: E402

# ---------------------------------------------------------------- markdown
def _md_escape(text):
    """Escapa um texto para uso seguro em HTML (hereditariedade de _html.escape)."""
    return _html.escape(text, quote=True)


# ---------------------------------------------------------------- JS (inline, offline)
APP_JS = r"""
/* MimePy v0.2 — recursos JS (inline, sem dependências externas) */
(function(){
  // 1. Busca na sidebar — filtra por TÍTULO e por CONTEÚDO de cada seção (M4).
  //    Cada entrada do nav corresponde à .section de mesma ordem. Se o termo
  //    aparece no título OU no texto da seção, o link fica visível.
  var q = document.getElementById('df-search');
  if (q){
    var links = Array.prototype.slice.call(document.querySelectorAll('.sidebar nav a'));
    var secs = Array.prototype.slice.call(document.querySelectorAll('.section'));
    // pré-indexa texto (lowercase p/ busca) e original (p/ snippet) de cada seção
    var secText = secs.map(function(s){ return (s.textContent||'').toLowerCase(); });
    var secOrig = secs.map(function(s){ return (s.textContent||''); });
    q.addEventListener('input', function(){
      var v = q.value.trim().toLowerCase();
      links.forEach(function(a, i){
        var inTitle = a.textContent.toLowerCase().indexOf(v) !== -1;
        var inBody = (i < secText.length) && secText[i].indexOf(v) !== -1;
        var ok = v === '' || inTitle || inBody;
        a.style.display = ok ? '' : 'none';
        // N4: snippet — mostra o trecho do corpo que casou (com destaque)
        if (ok && v !== '' && inBody && !inTitle && i < secOrig.length){
          var pos = secText[i].indexOf(v);
          var start = Math.max(0, pos - 40);
          var snip = secOrig[i].slice(start, pos + v.length + 60).replace(/\s+/g,' ').trim();
          // destaca o termo (escape simples, sem regex complexa)
          var low = snip.toLowerCase();
          var k = low.indexOf(v);
          var part = (start>0?'…':'') + snip.slice(0,k) + '<b>' + snip.slice(k,k+v.length) + '</b>' + snip.slice(k+v.length) + '…';
          var old = a.querySelector('.search-snippet');
          if (old) old.remove();
          var sn = document.createElement('span');
          sn.className = 'search-snippet'; sn.innerHTML = part;
          a.appendChild(sn);
        } else {
          var old2 = a.querySelector('.search-snippet');
          if (old2) old2.remove();
        }
      });
    });
    // 1b. Atalho de teclado '/' (M14) — foca a busca (padrão GitBook/Mintlify).
    //     Evita atrapalhar quando o usuário digita em outro campo.
    document.addEventListener('keydown', function(ev){
      var tag = (ev.target && ev.target.tagName) || '';
      if (ev.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(tag) && !ev.metaKey && !ev.ctrlKey){
        ev.preventDefault();
        var sb = document.getElementById('df-search');
        if (sb){ sb.focus(); sb.select(); }
      }
    });
  }
  // 2. Dark mode (o <head> já definiu o tema inicial — localStorage ou sistema)
  //    M8: se o config tem theme=neon, o botão cicla light→dark→neon.
  var dm = document.getElementById('df-dark');
  var STORE = 'mimepy-theme';
  var NEON = document.documentElement.getAttribute('data-neon') === '1';
  if (dm){
    var root = document.documentElement;
    function apply(t){ root.setAttribute('data-theme', t); }
    dm.addEventListener('click', function(){
      var cur = root.getAttribute('data-theme') || 'light';
      var nxt;
      if (NEON){ nxt = cur==='light' ? 'dark' : cur==='dark' ? 'neon' : 'light'; }
      else { nxt = cur === 'dark' ? 'light' : 'dark'; }
      apply(nxt); localStorage.setItem(STORE, nxt);
    });
  }
  // 3. Copy dos blocos de código
  // Fallback p/ compat: alguns navegadores/contextos (ex.: file://) não expõem
  // navigator.clipboard — usamos uma função de cópia com fallback (execCommand).
  function copyText(txt){
    if (navigator.clipboard && navigator.clipboard.writeText){
      return navigator.clipboard.writeText(txt).then(function(){return true;});
    }
    // fallback (Chrome/Edge/Firefox suportam execCommand de forma ampla)
    var ta = document.createElement('textarea');
    ta.value = txt; ta.style.position='fixed'; ta.style.top='-9999px';
    document.body.appendChild(ta); ta.select();
    try { var ok = document.execCommand('copy'); } catch(e){ ok=false; }
    document.body.removeChild(ta); return Promise.resolve(ok);
  }
  document.querySelectorAll('pre code').forEach(function(blk){
    var pre = blk.parentElement;
    if (pre.querySelector('.df-copy')) return;
    var b = document.createElement('button');
    b.className = 'df-copy'; b.textContent = 'copiar';
    b.addEventListener('click', function(){
      copyText(blk.innerText).then(function(){
        b.textContent = 'copiado!'; setTimeout(function(){ b.textContent = 'copiar'; }, 1500);
      });
    });
    pre.style.position = 'relative'; pre.appendChild(b);
  });
  // 4. Back to top
  var bt = document.getElementById('df-top');
  if (bt) bt.addEventListener('click', function(){ window.scrollTo({top:0, behavior:'smooth'}); });

  // 4b. Compartilhar (M7): copia o link atual da página (sem hash).
  var sh = document.getElementById('df-share');
  if (sh) sh.addEventListener('click', function(){
    var url = location.href.split('#')[0];
    copyText(url).then(function(){ sh.textContent = '✓'; setTimeout(function(){ sh.textContent = '🔗'; }, 1500); });
  });

  // 5. aria-current (2.4.1): destaca a seção visível na sidebar p/ leitores de tela
  var secs = Array.prototype.slice.call(document.querySelectorAll('.section'));
  var navlinks = Array.prototype.slice.call(document.querySelectorAll('.sidebar nav a'));
  function sectionFromHash(h){ return h && h.replace(/^#/, ''); }
  function markCurrent(){
    var cur = null;
    // encontra a seção mais próxima do topo que ainda está acima do meio da tela
    for (var i=0;i<secs.length;i++){
      var r = secs[i].getBoundingClientRect();
      if (r.top <= 120){ cur = secs[i].id; } else break;
    }
    // estado no topo da página: marca a PRIMEIRA seção (senão nenhuma ficaria ativa)
    if (cur === null && secs.length){ cur = secs[0].id; }
    navlinks.forEach(function(a){
      var hit = sectionFromHash(a.getAttribute('href')) === cur;
      if (hit){ a.setAttribute('aria-current', 'page'); a.classList.add('df-active'); }
      else { a.removeAttribute('aria-current'); a.classList.remove('df-active'); }
    });
  }
  if (secs.length && navlinks.length){
    markCurrent();
    window.addEventListener('scroll', markCurrent, {passive:true});
    window.addEventListener('resize', markCurrent);
  }

  // 6. Tamanho de fonte + alto contraste (WAI) — controles no topo da sidebar
  var SIZE_KEY = 'mimepy-fontsize';
  var root = document.documentElement;
  function applySize(level){
    root.style.fontSize = (level===2 ? '112.5%' : level===3 ? '125%' : '100%');
    var btns = document.querySelectorAll('.df-fsize');
    btns.forEach(function(b){ b.classList.toggle('on', +b.getAttribute('data-lv')===level); });
  }
  var curr = parseInt(localStorage.getItem(SIZE_KEY)||'1', 10);
  applySize(curr||1);
  document.querySelectorAll('.df-fsize').forEach(function(b){
    b.addEventListener('click', function(){
      var lv = +b.getAttribute('data-lv'); localStorage.setItem(SIZE_KEY, lv); applySize(lv);
    });
  });
  // alto contraste
  var HC_KEY = 'mimepy-hc';
  function applyHC(on){
    root.classList.toggle('df-hc', on);
    var b = document.getElementById('df-hc');
    if (b) b.setAttribute('aria-pressed', on ? 'true' : 'false');
  }
  if (localStorage.getItem(HC_KEY)==='1') applyHC(true);
  var hcb = document.getElementById('df-hc');
  if (hcb) hcb.addEventListener('click', function(){
    var on = !root.classList.contains('df-hc'); localStorage.setItem(HC_KEY, on?'1':'0'); applyHC(on);
  });

  // 6b. Idioma (M10): botão 🌐 alterna pt⇄en nos textos da interface (data-i18n).
  var LANG_KEY = 'mimepy-lang';
  var langBtn = document.getElementById('df-lang');
  var LANG = {
    pt: { skip:'Pular para o conteúdo', buscar:'Buscar...' },
    en: { skip:'Skip to content', buscar:'Search...' }
  };
  if (langBtn){
    var curLang = localStorage.getItem(LANG_KEY) || 'pt';
    function applyLang(l){
      curLang = l; localStorage.setItem(LANG_KEY, l);
      var pair = LANG[l] || LANG.pt;
      // placeholder da busca usa atributo dedicado
      if (q){ q.placeholder = (l==='en' ? (q.getAttribute('data-i18n-ph-en')||'Search...') : (q.getAttribute('data-i18n-ph')||'Buscar...')); }
      // skip-link pelo data-i18n
      document.querySelectorAll('[data-i18n]').forEach(function(el){
        var key=el.getAttribute('data-i18n'); if (pair[key]) el.textContent=pair[key];
      });
    }
    applyLang(curLang);
    langBtn.addEventListener('click', function(){ applyLang(curLang==='pt'?'en':'pt'); });
  }

  // 7. Highlight de sintaxe leve (M2) — offline, sem biblioteca.
  //    Tokeniza o código em UMA passada (regex mestre) que captura cada token
  //    por vez: strings | comentários | números | keywords. Isso evita que um
  //    replace re-processe o HTML que acabou de inserir (ex.: "class" dentro
  //    de class="..."), que era o bug anterior.
  function highlightBlocks(){
    var MASTER = /("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(#[^\n]*|\/\/[^\n]*|\/\*[\s\S]*?\*\/)|(\b\d[\d_]*\b)|\b(def|class|if|else|elif|for|while|return|import|from|as|with|try|except|finally|lambda|yield|pass|break|continue|and|or|not|in|is|None|True|False|new|var|let|const|function|=>)\b/g;
    document.querySelectorAll('pre code, code[class*=language-]').forEach(function(c){
      if (c.getAttribute('data-hl')) return;   // já processado (idempotente)
      // SEGURANÇA (a11y/defesa em profundidade): escapa HTML primeiro. O
      // textContent devolve tags como texto puro (ex.: "<img>"); sem escapar,
      // colocá-las em innerHTML re-executaria como HTML (XSS latente) quando o
      // código vier de fonte não confiável. Escapamos &, <, > antes de inserir.
      var txt = (c.textContent || '')
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      // UMA passada: cada match é substituído pelo span correspondente.
      txt = txt.replace(MASTER, function(all, str, cmt, num, kw){
        if (str) return '<span class="hl-str">'+str+'</span>';
        if (cmt) return '<span class="hl-cmt">'+cmt+'</span>';
        if (num) return '<span class="hl-num">'+num+'</span>';
        if (kw) return '<span class="hl-kw">'+kw+'</span>';
        return all;
      });
      c.innerHTML = txt;
      c.setAttribute('data-hl', '1');
    });
  }
  // N20: modo "texto simples" — se o config desligou o highlight (features.highlight=false),
  // não tokeniza o código (renderização determinística, sem spans).
  var NO_HL = document.documentElement.getAttribute('data-nohighlight') === '1';
  if (!NO_HL) highlightBlocks();
  if (NO_HL) return;

  // 7b. Segurança de links (N11): todo link externo (http) ganha
  //     rel="noopener noreferrer" (evita tabnabbing/referrer vazado).
  Array.prototype.forEach.call(document.querySelectorAll('a[href^="http"]'), function(a){
    a.setAttribute('rel', 'noopener noreferrer');
  });

  // 7c. Imagens responsivas (N7): loading=lazy + dimensões fluidas.
  Array.prototype.forEach.call(document.querySelectorAll('.main img'), function(im){
    if (!im.hasAttribute('loading')) im.setAttribute('loading', 'lazy');
  });

  // 8. Âncoras com botão de cópia (M6): cada h2/h3 da doc ganha um link
  //    "§" que copia a âncora (URL#id) — compartilhar link exato da seção.
  //    Também habilita o TOC recolhível (botão no topo de docs longas).
  document.querySelectorAll('.section h2, .section h3, .section h4').forEach(function(h){
    if (h.querySelector('.df-anchor')) return;
    var id = h.id || (h.textContent || '').trim().toLowerCase()
        .replace(/[^\w\s-]/g,'').replace(/\s+/g,'-').slice(0,50);
    h.id = id || ('sec-' + Math.random().toString(36).slice(2,7));
    var a = document.createElement('a');
    a.className = 'df-anchor'; a.href = '#' + h.id; a.textContent = '§';
    a.setAttribute('aria-label', 'Copiar link desta seção');
    a.title = 'Copiar link desta seção';
    a.style.float = 'right';
    a.addEventListener('click', function(ev){
      ev.preventDefault();
      var id = h.id;
      var url = location.href.split('#')[0] + '#' + id;
      copyText(url);
      a.textContent = '✓'; setTimeout(function(){ a.textContent = '§'; }, 1200);
      history.replaceState(null, '', '#' + id);
    });
    h.appendChild(a);
  });

  // TOC recolhível: gera um sumário do documento (h2/h3) que pode ser
  // minimizado/expandido por usuários de docs longas.
  var main = document.querySelector('main.main');
  var h2s = main ? main.querySelectorAll('.section h2') : [];
  if (main && h2s.length >= 3){
    var tocBox = document.createElement('details');
    tocBox.className = 'df-toc';
    tocBox.innerHTML = '<summary aria-expanded="false">Índice nesta página</summary><nav class="df-toc-body"></nav>';
    var navToc = tocBox.querySelector('.df-toc-body');
    h2s.forEach(function(h){
      if (!h.id) return;
      var li = document.createElement('a');
      li.href = '#' + h.id; li.textContent = h.textContent.trim();
      navToc.appendChild(li);
      navToc.appendChild(document.createElement('br'));
    });
    var first = main.querySelector('.section');
    if (first){ first.parentNode.insertBefore(tocBox, first); }
  }
})();
"""

# Temas (v0.4): ver src/themes.py — THEMES_CSS y get_theme_css reexportados.
def _side_label(title):
    """Título de link da sidebar com ícone (N18): se o texto começa com um
    emoji/símbolo, separa-o num .side-ic (badge pequeno). Ex.:
    '🚀 Início' -> '<span class="side-ic">🚀</span> Início'.
    Sem emoji: só escapa o título."""
    t = title.strip()
    partes = t.split(None, 1)
    if partes:
        ic = partes[0]
        if not re.search(r'[\w]', ic, re.UNICODE) and len(ic) <= 6:
            resto = partes[1].strip() if len(partes) > 1 else ""
            return ('<span class="side-ic" aria-hidden="true">%s</span> %s' % (ic, _html.escape(resto))).strip()
    return _html.escape(t)


def build(cfg, base_dir):
    docs_dir = (base_dir / cfg["docs_dir"]).resolve()
    css = (HERE / "assets" / "style.css").read_text(encoding="utf-8")
    ext = cfg.get("extensions")

    # recursos (features) — defaults ON para provar; configs antigos seguem com os novos
    feat = cfg.get("features", {})
    F = {k: feat.get(k, True) for k in ["search", "dark", "prev_next",
                                        "copy", "back_top", "print", "share", "lang", "highlight"]}

    # Sidebar: suporta lista PLANA [(arquivo,titulo),...] ou AGRUPADA
    # [("Grupo", [(arquivo,titulo),...]), ...] (N19, padrão Mintlify).
    def _flatten(sidebar):
        out = []
        for it in sidebar:
            if isinstance(it, (list, tuple)) and len(it) == 2 and isinstance(it[1], (list, tuple)):
                out.extend(it[1])          # grupo: ("Nome", [ (f,t), ... ])
            else:
                out.append(it)
        return out

    flat_sidebar = _flatten(cfg["sidebar"])
    entries = [e for e in flat_sidebar if (docs_dir / e[0]).exists()]
    sections, all_titles = [], []
    nav = ""   # nav é STRING (concatenação de <a>); lista faria concatenar char a char
    for i, (fname, title) in enumerate(entries):
        anchor = _html.escape(fname.replace(".md", ""))
        all_titles.append(title)
        prev_link = ""
        next_link = ""
        if F["prev_next"]:
            if i > 0:
                p_idx = _html.escape(entries[i-1][0].replace(".md", ""))
                prev_link = f'<a class="navpn" href="#{p_idx}">← {_html.escape(entries[i-1][1])}</a>'
            if i < len(entries) - 1:
                n_idx = _html.escape(entries[i+1][0].replace(".md", ""))
                next_link = f'<a class="navpn" href="#{n_idx}">{_html.escape(entries[i+1][1])} →</a>'
        navrow = ""
        if F["prev_next"] and (prev_link or next_link):
            navrow = f'<div class="pn">{prev_link}{next_link}</div>'
        body, meta = render_md(docs_dir / fname, ext)   # N22: body + frontmatter meta
        if cfg.get("sanitize"):          # SEGURANÇA: sanitiza HTML bruto (XSS)
            body = sanitize_html(body)
        # N22: o frontmatter pode sobrepor o título da seção/descrição.
        sec_title = meta.get("title") or title
        sec_desc = meta.get("description", "")
        desc_html = f'<p class="doc-desc">{_html.escape(sec_desc)}</p>' if sec_desc else ""
        sections.append(
            f'<section class="section" id="{anchor}">'
            f'<p class="doc-title">{_html.escape(fname)}</p>{desc_html}{body}{navrow}</section>'
        )
        nav += (f'<a href="#{anchor}">{_side_label(sec_title)}</a>')

    # Se a sidebar é AGRUPADA, embrulha os links em grupos (N19).
    # Detectamos se algum item de topo é um grupo (2º elemento é lista).
    def _is_grouped(sidebar):
        return any(isinstance(it, (list, tuple)) and len(it) == 2
                   and isinstance(it[1], (list, tuple)) for it in sidebar)

    if _is_grouped(cfg["sidebar"]):
        grouped_nav = ""
        for it in cfg["sidebar"]:
            if isinstance(it, (list, tuple)) and len(it) == 2 and isinstance(it[1], (list, tuple)):
                gname = _html.escape(str(it[0]))
                glinks = ""
                for (gf, gt) in it[1]:
                    if (docs_dir / gf).exists():
                        ga = _html.escape(gf.replace(".md", ""))
                        glinks += f'<a href="#{ga}">{_side_label(gt)}</a>'
                if glinks:
                    grouped_nav += f'<div class="nav-group" data-label="{gname}">{glinks}</div>'
            else:
                # item solto no topo (já incluso no nav plano)
                pass
        # as seções prev/next usam entries; nav agrupado substitui o plano
        nav = grouped_nav

    n = len(entries)
    # Compartilhar: botão no topo que copia o link da página (M7).
    # (As âncoras § de cada seção — M6 — já copiam o link da seção.)
    share_html = ('<button id="df-share" class="df-share" aria-label="Compartilhar (copiar link)" '
                  'title="Compartilhar (copiar link)">🔗</button>') if F["share"] else ""
    # Logo opcional: se config tem "logo" (caminho de imagem), usa <img> no brand.
    # Senão, usa o emoji/brand textual. (brand_mark vai no topo da sidebar.)
    logo = cfg.get("logo", "")
    if logo:
        brand_mark = (f'<img class="df-logo" src="{_html.escape(logo)}" '
                      f'alt="{_html.escape(cfg.get("name",""))}">')
    else:
        # emoji do brand num badge quadrado (visual profissional, como a landing)
        brand_mark = f'<span class="df-badge">{_html.escape(cfg.get("brand",""))}</span>'
    # busca na sidebar
    search_html = ('<input id="df-search" type="text" placeholder="Buscar..." aria-label="Buscar" '
                   'data-i18n-ph="Buscar..." data-i18n-ph-en="Search...">') if F["search"] else ""
    # dark toggle
    toggle_html = '<button id="df-dark" aria-label="Alternar tema">🌙</button>' if F["dark"] else ""
    # back to top
    top_html = ('<button id="df-top" aria-label="Voltar ao topo">↑</button>') if F["back_top"] else ""
    # meta description
    meta_desc = _html.escape(cfg.get("meta_description", cfg.get("intro", "")).strip())

    # Script de tema automático (separado p/ não conflitar com {} da f-string)
    # Tema default vem do config (theme); depois segue preferência do sistema.
    theme_css, default_theme = get_theme_css(cfg)   # CSS extra do tema — M8/M12
    theme_script = (
        "/* Tema: escolha salva > tema do config > preferencia do sistema */"
        "(function(){try{var s=localStorage.getItem('mimepy-theme');"
        "var dt='%s';"
        "var t=s||dt||(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');"
        "document.documentElement.setAttribute('data-theme',t);}catch(e){}})();" % default_theme
    )

    html_attrs = ''
    if (cfg.get("theme") or "").lower() == "neon": html_attrs += ' data-neon="1"'
    if not F.get("highlight", True): html_attrs += ' data-nohighlight="1"'   # N20
    doc = f"""<!DOCTYPE html>
<html lang="{cfg.get('lang','pt-BR')}" data-theme="light"{html_attrs}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{meta_desc}">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'">
<title>{_html.escape(cfg['page_title'])}</title>
<script>{theme_script}</script>
<style>{css}{theme_css}</style>
</head>
<body>
<a class="skip-link" href="#main-content" data-i18n="skip">Pular para o conteúdo</a>
<input type="checkbox" id="menu-chk">
<label for="menu-chk" class="menu-toggle"></label>
<div class="wrap">
  <aside class="sidebar" aria-label="Navegação do documento">
    <div class="brand-top">
      <a class="brand" href="{_html.escape(cfg.get('home_url','index.html'))}" data-i18n="home">
        {brand_mark} {_html.escape(cfg['name'])}
      </a>
    </div>
    <div class="brand-sub">{_html.escape(cfg.get('subtitle',''))}</div>
    {search_html}
    <nav>{nav}</nav>
  </aside>
  <main class="main" id="main-content" role="main" tabindex="-1">
    <div class="top-tools" role="toolbar" aria-label="Ferramentas de acessibilidade e visualização">
      <span class="tools">
        <button class="df-lang" id="df-lang" aria-label="Idioma / Language" title="Idioma / Language">🌐</button>
        <button class="df-fsize" data-lv="1" aria-label="Tamanho de fonte normal">A</button>
        <button class="df-fsize" data-lv="2" aria-label="Aumentar fonte">A+</button>
        <button class="df-fsize" data-lv="3" aria-label="Fonte grande">A++</button>
        <button id="df-hc" aria-label="Alto contraste" aria-pressed="false" title="Alto contraste">◐</button>
        {toggle_html}
      </span>
    </div>
    {share_html}
    {top_html}
    <h1>{_html.escape(cfg['page_title'])}</h1>
    <p style="color:var(--muted)">{cfg.get('intro','')}</p>
    <p style="color:var(--muted);font-size:.85rem"><b>Docs ({n}):</b>
      {' · '.join(_html.escape(t) for t in all_titles)}</p>
    <hr>
    {''.join(sections)}
    <footer style="margin-top:48px;padding-top:16px;border-top:1px solid var(--border);color:var(--muted);font-size:.8rem;">
      {_html.escape(cfg.get('footer',cfg['name']))} · MimePy {VERSION} · GPL-2.0
    </footer>
  </main>
</div>
<script>{APP_JS}</script>
</body>
</html>"""

    # tabelas ganham wrapper .table-scroll (rolagem horizontal no mobile)
    doc = re.sub(r"(<table>.*?</table>)",
                 lambda m: '<div class="table-scroll">' + m.group(1) + '</div>',
                 doc, flags=re.S)

    out = (base_dir / cfg["out_dir"]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    out_file = out / cfg["out_file"]
    out_file.write_text(doc, encoding="utf-8")
    print(f"[MimePy {VERSION}] OK -> {out_file}  ({n} docs, {out_file.stat().st_size} bytes)")
    return out_file

# ---------------------------------------------------------------- LANDING mode
# Design system autoral do MimePy (ver DESIGN.md):
#   - paleta esmeralda/teal (marca) + âmbar (CTA único)
#   - composição anti-slop: cards variados, hierarquia por tipografia/espaço
# LANDING e BLOG (v0.4): movidos para src/modes.py.
# Reexporta para compat (build_landing, build_blog, _cardize, LANDING_CSS).
from modes import build_landing, build_blog, _cardize, LANDING_CSS  # noqa: E402

if __name__ == "__main__":
    cfg_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (FRAMEWORK_ROOT / "config.py")
    if not cfg_path.exists():
        print("config não encontrado:", cfg_path); sys.exit(1)
    cfg = load_config(cfg_path)
    if cfg.get("mode") == "landing":
        build_landing(cfg, cfg_path.parent)
    elif cfg.get("mode") == "blog":
        build_blog(cfg, cfg_path.parent)
    else:
        build(cfg, cfg_path.parent)
