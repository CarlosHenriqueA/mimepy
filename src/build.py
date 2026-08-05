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

# ---------------------------------------------------------------- config
def load_config(config_path):
    spec = importlib.util.spec_from_file_location("mimepy_cfg", config_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PROJECT

HERE = Path(__file__).resolve().parent
FRAMEWORK_ROOT = HERE.parent
VERSION = "0.2"

# ---------------------------------------------------------------- markdown
def sanitize_html(html):
    """Sanitização básica de segurança (opcional, ligada via config `sanitize`).

    Remove vetores XSS comuns que o autor de Markdown (possivelmente não
    confiável, ex.: conteúdo de terceiros comentado) poderia injetar:
      - tags <script> e <style> (com conteúdo)
      - atributos on* (onclick, onerror, onload, ...)
      - URLs javascript:, data: em links
    PS: MimePy por padrão perm.rel HTML bruto no Markdown (flexibilidade).
    Ative `sanitize: true` no config quando o Markdown NÃO for 100% confiável.
    """
    import re as _re
    # remove <script ...>...</script> e <style>...</style>
    html = _re.sub(r"<\s*script\b[^>]*>.*?<\s*/\s*script\s*>", "", html, flags=_re.S | _re.I)
    html = _re.sub(r"<\s*style\b[^>]*>.*?<\s*/\s*style\s*>", "", html, flags=_re.S | _re.I)
    html = _re.sub(r"<\s*script\b[^>]*>", "", html, flags=_re.I)
    # remove atributos on*
    html = _re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", "", html, flags=_re.I)
    # remove javascript:/data: em href e src
    html = _re.sub(r'\s(href|src)\s*=\s*(["\'])\s*javascript:[^"\']*\2', "", html, flags=_re.I)
    html = _re.sub(r'\s(href|src)\s*=\s*(["\'])\s*data:[^"\']*\2', "", html, flags=_re.I)
    return html


def render_md(path, extensions):
    import markdown
    with open(path, encoding="utf-8") as f:
        md = f.read()
    # strip yaml/frontmatter
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)
    # robust tables: garante linha em branco antes do separador de tabela
    # SOMENTE quando uma linha separador (|---|) vem logo após um PARÁGRAFO
    # SOLTO (linha sem "|"), e não logo após outro header de tabela.
    md = re.sub(
        r"(?m)^(?P<prev>[^\n|][^\n]*)\n(?P<sep>\|[^\n]*\|[\s:|:-]*\|\s*)$",
        lambda m: m.group("prev") + "\n\n" + m.group("sep"),
        md,
    )
    return markdown.markdown(
        md,
        extensions=extensions or ["tables", "fenced_code", "sane_lists",
                                  "md_in_html", "attr_list", "def_list"],
    )

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
    // pré-indexa o texto de cada seção (uma vez, p/ performance)
    var secText = secs.map(function(s){ return (s.textContent||'').toLowerCase(); });
    q.addEventListener('input', function(){
      var v = q.value.trim().toLowerCase();
      links.forEach(function(a, i){
        var inTitle = a.textContent.toLowerCase().indexOf(v) !== -1;
        var inBody = (i < secText.length) && secText[i].indexOf(v) !== -1;
        var ok = v === '' || inTitle || inBody;
        a.style.display = ok ? '' : 'none';
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
  highlightBlocks();

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

# ---------------------------------------------------------------- build
# Temas alternativos (M8): cada tema redefine as CSS variables do :root.
# "light" (padrão), "dark" e "neon" (estilo retrô/fosforescente autoral).
THEMES_CSS = {
 "dark": """
 [data-theme="dark"]{
   --bg:#0f172a; --fg:#e2e8f0; --muted:#94a3b8;
   --accent:#2dd4bf; --accent2:#5eead4; --cta:#fbbf24; --cta-strong:#f59e0b;
   --border:#1e293b; --code-bg:#1e293b; --note-bg:#134e4a; --note-border:#2dd4bf;
   --sidebar-bg:#020617; --sidebar-fg:#cbd5e1; --pre-bg:#0b1220; --pre-fg:#e2e8f0;
   --tool-bg:#0f172a; --input-bg:#0f172a;
 }
 """,
 "neon": """
 [data-theme="neon"]{
   --bg:#0a0a0f; --fg:#f0f0ff; --muted:#a5a5c0;
   --accent:#00ffd5; --accent2:#00e0ff; --cta:#ff2e88; --cta-strong:#ff1177;
   --border:#2a2a4a; --code-bg:#12122a; --note-bg:#0f0f24; --note-border:#ff2e88;
   --sidebar-bg:#05050a; --sidebar-fg:#d5d5ff; --pre-bg:#0a0a1e; --pre-fg:#e0e0ff;
   --tool-bg:#12122a; --input-bg:#0a0a1e;
 }
 a{color:#7df9ff;}
 """,
 # "paper": tema claro estilo impresso (marca esverdeada suave). Base CLARA.
 "paper": """
 html[data-theme="paper"]{
   --bg:#fdfcf7; --fg:#2b2b2b; --muted:#6b7280;
   --accent:#15803d; --accent2:#166534; --cta:#b45309; --cta-strong:#92400e;
   --border:#e5e4db; --code-bg:#f4f3ec; --note-bg:#eef7ee; --note-border:#86c79a;
   --sidebar-bg:#f4f3ec; --sidebar-fg:#333; --pre-bg:#f4f3ec; --pre-fg:#2b2b2b;
   --tool-bg:#eceae0; --input-bg:#fff;
 }
 [data-theme="paper"] .sidebar{color:#333;}
 [data-theme="paper"] .brand{color:#166534;}
 """,
 # "mono": monocromático (tons de cinza/preto), visual técnico/minimalista. Base CLARA.
 "mono": """
 html[data-theme="mono"]{
   --bg:#fafafa; --fg:#111; --muted:#525252;
   --accent:#111; --accent2:#333; --cta:#111; --cta-strong:#000;
   --border:#d4d4d4; --code-bg:#f2f2f2; --note-bg:#f2f2f2; --note-border:#a3a3a3;
   --sidebar-bg:#111; --sidebar-fg:#e5e5e5; --pre-bg:#111; --pre-fg:#e5e5e5;
   --tool-bg:#262626; --input-bg:#e5e5e5;
 }
 [data-theme="mono"] .sidebar nav a{color:#a3a3a3;}
 [data-theme="mono"] h1{border-bottom-color:#111;}
 """,
}
def get_theme_css(cfg):
    """Retorna o CSS de tema (dark/neon/paper/mono) com base em cfg.get('theme').

    dark/neon modificam a base ESCURA (são alternativas ao light).
    paper/mono são temas de fundo próprios (claro/escuro na sidebar) e
    substituem completamente o :root — por isso voltam a aplicar o CSS básico
    que já está no style.css (só redefinem as variáveis)."""
    theme = (cfg.get("theme") or "light").lower()
    extra = []
    if theme == "dark":
        extra.append(THEMES_CSS["dark"])
        default_theme = "dark"
    elif theme == "neon":
        extra.append(THEMES_CSS["dark"])     # neon tb força dark base
        extra.append(THEMES_CSS["neon"])
        default_theme = "dark"
    elif theme == "paper":
        extra.append(THEMES_CSS["paper"])
        default_theme = "paper"
    elif theme == "mono":
        extra.append(THEMES_CSS["mono"])
        default_theme = "mono"
    else:
        default_theme = "light"
    return "\n".join(extra), default_theme

def build(cfg, base_dir):
    docs_dir = (base_dir / cfg["docs_dir"]).resolve()
    css = (HERE / "assets" / "style.css").read_text(encoding="utf-8")
    ext = cfg.get("extensions")

    # recursos (features) — defaults ON para provar; configs antigos seguem com os novos
    feat = cfg.get("features", {})
    F = {k: feat.get(k, True) for k in ["search", "dark", "prev_next",
                                        "copy", "back_top", "print", "share", "lang"]}

    entries = [e for e in cfg["sidebar"] if (docs_dir / e[0]).exists()]
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
        body = render_md(docs_dir / fname, ext)
        if cfg.get("sanitize"):          # SEGURANÇA: sanitiza HTML bruto (XSS)
            body = sanitize_html(body)
        sections.append(
            f'<section class="section" id="{anchor}">'
            f'<p class="doc-title">{_html.escape(fname)}</p>{body}{navrow}</section>'
        )
        nav += (f'<a href="#{anchor}">{_html.escape(title)}</a>')

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

    doc = f"""<!DOCTYPE html>
<html lang="{cfg.get('lang','pt-BR')}" data-theme="light"{' data-neon="1"' if (cfg.get("theme") or "").lower()=="neon" else ""}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{meta_desc}">
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
      <span class="brand">{brand_mark} {_html.escape(cfg['name'])}</span>
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
LANDING_CSS = r"""
/* MimePy — landing page (design system autoral) */
.land{min-height:100vh;background:#0b1220;color:#e2e8f0;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased;transition:background .2s,color .2s;}
/* Tema CLARO na landing (p/ o botão 🌙 funcionar): quando data-theme=light,
   inverte o fundo e os textos. Mantém a paleta autoral esmeralda/âmbar. */
[data-theme="light"] .land{background:#f7f9fc;color:#1f2937;}
[data-theme="light"] .land-nav{background:rgba(255,255,255,.88);border-bottom-color:#e5e7eb;}
[data-theme="light"] .land .hero h1,[data-theme="light"] .land section h2,
[data-theme="light"] .land .card h3,[data-theme="light"] .land .brand{color:#0f172a;}
[data-theme="light"] .land .hero .tagline,[data-theme="light"] .land .card p,
[data-theme="light"] .land section > p,[data-theme="light"] .land footer,
[data-theme="light"] .land .form-note{color:#475569;}
[data-theme="light"] .land .card,[data-theme="light"] .land .contact-form,[data-theme="light"] .land blockquote{background:#ffffff;border-color:#e5e7eb;}
[data-theme="light"] .land .card .ic,[data-theme="light"] .land .card h3{background:none;}
[data-theme="light"] .land blockquote{color:#334155;}
[data-theme="light"] .land table{background:#fff;box-shadow:0 8px 24px rgba(15,23,42,.08);}
[data-theme="light"] .land th{background:rgba(13,148,136,.10);color:#0f766e;}
[data-theme="light"] .land td{color:#334155;}
[data-theme="light"] .land th,[data-theme="light"] .land td{border-color:#e2e8f0;}
[data-theme="light"] .land .form-f input,.land .form-f textarea{background:#fff;border-color:#cbd5e1;color:#1f2937;}
[data-theme="light"] .land footer{background:#f1f5f9;border-top-color:#e5e7eb;}
/* Acessibilidade (WCAG 2.2 AA): skip link + foco visível + reduced motion */
.land .skip-link{position:absolute;top:-60px;left:16px;z-index:200;background:#0d9488;
  color:#fff;padding:10px 16px;border-radius:0 0 8px 8px;text-decoration:none;font-weight:600;transition:top .2s;}
.land .skip-link:focus{top:0;}
.land a:focus-visible,.land button:focus-visible,.land input:focus-visible{
  outline:3px solid #2dd4bf;outline-offset:2px;}
@media (prefers-reduced-motion:reduce){
  .land *, .land *::before, .land *::after{animation:none !important;transition:none !important;scroll-behavior:auto !important;}
}

/* ---------- Navbar fixa (blur) ---------- */
.land-nav{position:fixed;top:0;left:0;right:0;z-index:100;
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 28px;background:rgba(11,18,32,.72);backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.06);}
.land-nav .brand{display:flex;align-items:center;gap:10px;font-weight:800;color:#fff;
  font-size:1.05rem;letter-spacing:.02em;}
.land-nav .brand .badge{font-size:1.3rem;}
.land-nav .links{display:flex;gap:6px;}
.land-nav .links a{color:#9ca3af;text-decoration:none;font-size:.9rem;padding:8px 12px;
  border-radius:8px;transition:color .2s,background .2s;}
.land-nav .links a:hover{color:#fff;background:rgba(255,255,255,.08);}
.land-nav .cta-nav{margin-left:8px;display:flex;align-items:center;gap:8px;}
/* Botão de tema na navbar da landing (dark/light) */
.land-theme{background:rgba(255,255,255,.05);border:1px solid #334155;color:#fff;
  width:38px;height:38px;border-radius:10px;cursor:pointer;font-size:1.05rem;line-height:1;
  transition:background .15s,border-color .15s;}
.land-theme:hover{background:rgba(255,255,255,.12);border-color:#2dd4bf;}
[data-theme="light"] .land-theme{background:rgba(15,23,42,.05);border-color:#cbd5e1;}
[data-theme="light"] .land-theme:hover{border-color:#0d9488;}

/* ---------- Hero (Decide/Learn: uma ideia por vez) ---------- */
.land .hero{text-align:center;padding:130px 24px 70px;position:relative;overflow:hidden;}
.land .hero::before{content:'';position:absolute;top:-220px;left:50%;transform:translateX(-50%);
  width:720px;height:520px;background:radial-gradient(circle,rgba(13,148,136,.28),transparent 62%);
  pointer-events:none;}
.land .hero .content{position:relative;z-index:1;}
.land .hero .emoji{font-size:3.4rem;display:inline-block;margin-bottom:8px;
  animation:float 4s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.land .hero h1{font-size:3rem;font-weight:800;letter-spacing:-.03em;color:#fff;
  border:none;margin:10px 0 6px;line-height:1.12;}
/* Título com cor da marca (esmeralda) + reflexo claro — sem roxo;
   fallback sólido p/ nunca ficar invisível. */
.land .hero h1 span{color:#2dd4bf;}
@supports (-webkit-background-clip:text) or (background-clip:text){
  .land .hero h1 span{background:linear-gradient(90deg,#5eead4,#2dd4bf);
    -webkit-background-clip:text;background-clip:text;color:transparent;}
}
.land .hero .tagline{color:#98a2b3;font-size:1.2rem;max-width:640px;margin:0 auto 16px;
  line-height:1.6;}
.land .hero .cta{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:28px;}
.land .btn{display:inline-block;padding:14px 30px;border-radius:12px;text-decoration:none;
  font-weight:700;font-size:1rem;transition:transform .2s,box-shadow .2s,background .2s,border-color .2s;}
/* CTA ÚNICO em âmbar — uma ação de destaque por tela */
.land .btn-p{background:linear-gradient(90deg,#f59e0b,#fbbf24);color:#111827;
  box-shadow:0 8px 24px rgba(245,158,11,.30);}
.land .btn-p:hover{transform:translateY(-2px);box-shadow:0 12px 32px rgba(245,158,11,.45);}
.land .btn-g{border:1px solid #2dd4bf;color:#e2e8f0;background:rgba(45,212,191,.06);}
.land .btn-g:hover{border-color:#5eead4;color:#fff;transform:translateY(-2px);}

/* Botão dentro de card (ex.: links de exemplos) — vira CTA discreto e
   alinhado, em vez de link de texto "cru". */
.land .card a.btn-card, .land .card p a[href$=".html"], .land .card p a{
  display:inline-flex;align-items:center;gap:6px;margin-top:14px;padding:10px 18px;
  border-radius:10px;font-weight:600;font-size:.9rem;text-decoration:none;
  color:#0d9488;border:1px solid rgba(13,148,136,.4);background:rgba(13,148,136,.08);
  transition:all .18s;}
.land .card a.btn-card:hover, .land .card p a:hover{background:var(--cta, #0d9488);color:#fff;
  border-color:var(--cta, #0d9488);transform:translateY(-2px);box-shadow:0 8px 20px rgba(13,148,136,.25);}

/* ---------- Seções ---------- */
.land section{padding:64px 24px;max-width:1080px;margin:0 auto;}
.land section h2{font-size:2rem;color:#fff;text-align:center;margin:0 0 12px;border:none;
  letter-spacing:-.02em;line-height:1.25;}
.land section h2:after{content:'';display:block;width:56px;height:4px;margin:14px auto 0;
  background:linear-gradient(90deg,#2dd4bf,#fbbf24);border-radius:2px;}
.land section > ul{max-width:720px;margin:20px auto;}
.land section > p{max-width:720px;margin:16px auto;color:#98a2b3;text-align:center;font-size:1.02rem;}

/* ---------- Cards (variados, não 3 idênticos) ----------
   Grid com no MÁXIMO 3 colunas (a landing tem tipicamente 3 cards de seção;
   4+ colunas deixaria coluna vazia = desbalanceado). Em telas menores,
   o auto-fit reduz para 2/1 coluna. */
.land .cards{display:grid;
  grid-template-columns:repeat(auto-fit,minmax(240px,255px));
  gap:22px;margin-top:34px;align-items:stretch;
  justify-content:center;max-width:820px;margin-left:auto;margin-right:auto;}
.land .card{background:#101826;border:1px solid #1e293b;border-radius:16px;padding:28px 24px;
  transition:transform .25s,border-color .25s,box-shadow .25s;position:relative;overflow:hidden;}
.land .card:hover{transform:translateY(-6px);border-color:#2dd4bf;box-shadow:0 16px 40px rgba(13,148,136,.18);}
.land .card .ic{font-size:2rem;line-height:1;
  /* ícone em "badge" circular para visual profissional */
  display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;
  border-radius:14px;background:rgba(13,148,136,.10);border:1px solid rgba(45,212,191,.22);}
.land .card h3{color:#fff;margin:14px 0 8px;font-size:1.15rem;background:none;border:none;line-height:1.3;}
.land .card p{color:#98a2b3;font-size:.95rem;line-height:1.55;}
/* Variação: primeiros 2 cards (destaque por posição) ocupam mais largura */
.land .cards .card:nth-child(1){grid-column:span 1;}
.land .cards .card:nth-child(2){border-top:3px solid #2dd4bf;}
/* Variação: cada card alterna uma borda superior sutil de cor (esmeralda/âmbar) */
.land .cards .card:nth-child(3n){border-top:3px solid #fbbf24;}
.land .cards .card:nth-child(3n+1){border-top:3px solid #2dd4bf;}
.land .cards .card:nth-child(3n+2){border-top:3px solid #f59e0b;}

/* ---------- Tabela (diferenciais) ---------- */
.land table{max-width:760px;margin:26px auto;background:rgba(255,255,255,.02);
  border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.3);}
.land th,.land td{border:1px solid #1f2937;padding:14px 18px;}
.land th{background:rgba(13,148,136,.16);color:#5eead4;font-weight:700;}
.land td{color:#cbd5e1;}
.land table tr:nth-child(even){background:rgba(255,255,255,.02);}

/* ---------- Depoimentos (blockquote) ---------- */
.land blockquote{background:#101826;border-left:4px solid #2dd4bf;color:#d1d5db;
  padding:20px 24px;border-radius:0 12px 12px 0;margin:18px auto;max-width:720px;
  box-shadow:0 6px 20px rgba(0,0,0,.25);}
.land blockquote p{margin:0 0 4px;}
.land blockquote p:last-child{margin-bottom:0;}

/* ---------- Footer ---------- */
.land footer{text-align:center;padding:44px 24px;border-top:1px solid #1f2937;
  color:#64748b;font-size:.9rem;background:#090e1a;}

/* ---------- Formulário de contato (M9) ---------- */
.land .contact-form{max-width:520px;margin:26px auto;background:#101826;
  border:1px solid #1e293b;border-radius:14px;padding:28px 26px;}
.land .form-f{margin-bottom:16px;display:flex;flex-direction:column;gap:6px;}
.land .form-f label{color:#cbd5e1;font-size:.9rem;font-weight:600;}
.land .form-f input,.land .form-f textarea{background:#0b1220;border:1px solid #2a3a50;
  color:#e2e8f0;border-radius:8px;padding:10px 12px;font:inherit;width:100%;}
.land .form-f input:focus,.land .form-f textarea:focus{outline:2px solid #2dd4bf;border-color:#2dd4bf;}
.land .form-btn{background:linear-gradient(90deg,#f59e0b,#fbbf24);color:#111827;border:none;
  border-radius:10px;padding:12px 22px;font-weight:700;cursor:pointer;font:inherit;}
.land .form-btn:hover{filter:brightness(1.05);}
.land .form-note{color:#64748b;font-size:.78rem;margin:12px 0 0;}

/* corrige elementos claros que podem vazar como "retângulos brancos" */
.land pre,.land code{background:#0b1220 !important;color:#e2e8f0 !important;}
.land code{background:#101826 !important;}
.land a{color:#5eead4;word-break:break-word;}
.land .table-scroll{margin:14px 0;}

/* ================================================================
   RESPONSIVO — landing se adapta a TODAS as telas
   - <600px: celular (menu 1 coluna, navbar compacta)
   - 600–900px: tablet (2 colunas de cards, navbar encurtada)
   - >900px: desktop (3 colunas, navbar completa)
   ================================================================ */

/* Tablet pequeno / celular grande */
@media (max-width:900px){
  .land-nav{flex-wrap:wrap;padding:12px 18px;row-gap:8px;}
  .land .hero{padding:115px 20px 50px;}
  .land .hero h1{font-size:2.4rem;}
  .land section{padding:52px 20px;}
}

/* Celular */
@media (max-width:600px){
  .land-nav{padding:10px 14px;gap:6px;}
  .land-nav .brand{font-size:.95rem;flex:1 1 auto;}
  /* links de seção somem; CTA e tema permanecem (compacto) */
  .land .land-nav .links .hide-m{display:none;}
  .land .cta-nav{margin-left:0;}
  .land .cta-nav .btn-p{padding:10px 14px;font-size:.85rem;}
  .land .cta-nav .land-theme{width:34px;height:34px;font-size:.95rem;}

  .land .hero{padding:100px 16px 44px;}
  .land .hero h1{font-size:1.9rem;line-height:1.15;}
  .land .hero .emoji{font-size:2.6rem;}
  .land .hero .tagline{font-size:1rem;}
  .land .hero .cta{flex-direction:column;align-items:center;gap:10px;}
  .land .hero .cta .btn{width:100%;max-width:280px;text-align:center;}

  .land section{padding:40px 16px;}
  .land section h2{font-size:1.5rem;}
  .land .cards{grid-template-columns:1fr;max-width:100%;}  /* 1 coluna no celular */
  .land .cards .card:nth-child(1),.land .cards .card:nth-child(3n),
  .land .cards .card:nth-child(3n+1),.land .cards .card:nth-child(3n+2){grid-column:auto;border-top-width:3px;}

  .land table{display:block;overflow-x:auto;}  /* tabela com rolagem no celular */
  .land blockquote{padding:16px 18px;}
}

/* Celular muito pequeno (<360px): fonte hero menor */
@media (max-width:360px){
  .land .hero h1{font-size:1.6rem;}
  .land .land-nav .brand span[class=badge]{display:none;}
  .land section h2{font-size:1.3rem;}
}
"""

def _cardize(block):
    """Melhora um bloco de card: extrai o emoji do <h3> e o coloca num .ic
    (badge), deixando o card com ícone destacado (visual profissional).
    Ex.: '<h3>📄 Markdown</h3><p>...' -> '<div class="ic">📄</div><h3>Markdown</h3><p>...'
    Robusto: captura SOMENTE o símbolo inicial (evita '/', '%', '100' etc.)."""
    m = re.match(r'<h3[^>]*>\s*([^<]*?)\s*</h3>', block, re.S)
    if not m:
        return block
    texto = m.group(1).strip()
    # a 1ª "palavra" é o emoji/símbolo se ela terminar em símbolo e for curta
    partes = texto.split(None, 1)
    possivel_emoji = partes[0] if partes else ""
    # símbolo: não tem letras/dígitos (só caracteres não-alfanuméricos ou emoji)
    so_simbolo = bool(possivel_emoji) and not re.search(r'[\w]', possivel_emoji, re.UNICODE)
    # emoji pode ter comprimento de variados pontos de código; aceita até ~4 símbolos
    if so_simbolo and len(possivel_emoji) <= 6:
        resto = partes[1].strip() if len(partes) > 1 else ""
        ic = '<div class="ic">%s</div>' % possivel_emoji
        novo_h3 = '<h3>%s</h3>' % resto if resto else ''
        block = re.sub(r'^\s*<h3[^>]*>.*?</h3>', ic + novo_h3, block, count=1, flags=re.S)
    return block


def build_landing(cfg, base_dir):
    """Gera um site de 1 página (landing) a partir de UM arquivo Markdown.

    - O .md de entrada usa as seções por título (##) para dividir a página.
    - A PRIMEIRA seção (h1) vira o hero; as demais (##) viram seções.
    - Blocos consecutivos de ### (h3) dentro de uma seção viram uma grade de CARDS.
    - Uma navbar fixa é gerada com links para as seções (##).
    """
    css = (HERE / "assets" / "style.css").read_text(encoding="utf-8")
    ext = cfg.get("extensions")
    md_file = cfg.get("landing_md", "LANDING.md")
    md_path = (base_dir / cfg["docs_dir"] / md_file)
    if not md_path.exists():
        print(f"[MimePy] ERRO: landing_md não encontrado: {md_path}"); sys.exit(1)

    import markdown
    md = md_path.read_text(encoding="utf-8")
    raw = markdown.markdown(md, extensions=ext or ["tables","fenced_code","sane_lists"])

    # Formulário de contato (M9): se o LANDING.md contém um bloco com o
    # marcador `:::form` (num fence), substitui por um <form> HTML real.
    # Uso no .md:
    #   ```form
    #   Nome, Email, Mensagem
    #   ```
    # O form é funcional apenas se hospedado com backend; por padrão abre
    # um mailto preenchido (offline) — sem enviar dados a lugar nenhum.
    m_form = re.search(r'```form\s*\n(.*?)\n```', md, re.S | re.I)
    if m_form:
        labels = [l.strip() for l in m_form.group(1).split(",") if l.strip()]
        fields = ""
        for lab in labels:
            low = lab.lower()
            name = "email" if "email" in low else ("mensagem" if "mensag" in low or "mess" in low else "nome")
            if name == "mensagem":
                fields += (f'<div class="form-f"><label for="fm-ms">{_html.escape(lab)}</label>'
                           f'<textarea id="fm-ms" name="mensagem" rows="4"></textarea></div>')
            elif name == "email":
                fields += (f'<div class="form-f"><label for="fm-em">{_html.escape(lab)}</label>'
                           f'<input id="fm-em" type="email" name="email"></div>')
            else:
                fields += (f'<div class="form-f"><label for="fm-{_html.escape(name)}">{_html.escape(lab)}</label>'
                           f'<input id="fm-{_html.escape(name)}" type="text" name="{_html.escape(name)}"></div>')
        form_html = (
            '<form class="contact-form" action="mailto:" method="post" enctype="text/plain">'
            + fields +
            '<button type="submit" class="form-btn">Enviar</button>'
            '<p class="form-note">Contato offline: o envio abre seu app de e-mail.</p>'
            '</form>'
        )
        # o form substitui o bloco fenced no markdown; depois re-renderiza
        md_clean = md.replace(m_form.group(0), form_html)
        raw = markdown.markdown(md_clean, extensions=ext or ["tables","fenced_code","sane_lists"])
    else:
        md_clean = md

    hero = cfg.get("hero", {})
    emoji = str(hero.get("emoji", "🚀"))          # string; escapado abaixo no HTML
    emoji_esc = _html.escape(emoji)                # SEGURANÇA: evita XSS via emoji

    # H1 -> título do hero (sai do corpo). Fallback: page_title.
    title = ""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    if m:
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        raw = re.sub(r"<h1[^>]*>.*?</h1>", "", raw, count=1, flags=re.S)
    if not title:
        title = cfg.get("page_title", "")

    # Hero: título todo no span com gradiente (fallback sólido)
    hero_html_title = _html.escape(title)

    tagline = hero.get("tagline", cfg.get("intro", ""))
    cta_text = hero.get("cta_text", "Começar")
    cta_link = hero.get("cta_link", "#secoes")
    # SEGURANÇA: bloqueia javascript:/data: em link de CTA (evita XSS)
    if str(cta_link).strip().lower().startswith(("javascript:", "data:")):
        cta_link = "#secoes"
    meta_desc = _html.escape(cfg.get("meta_description", tagline).strip())

    # ----- constrói navbar + processa corpo -----
    # 1) colhe as seções (h2) para os links da navbar.
    #    Uso <h2[^>]*> p/ aceitar atributos (ex.: id da extensão toc).
    nav_links = re.findall(r'<h2[^>]*>(.*?)</h2>', raw, re.S)
    nav_items = ""
    for i, h in enumerate(nav_links):
        # label: remove tags E desescapa HTML (evita "&amp;amp;" duplo)
        label = re.sub(r"<[^>]+>", "", h).strip()
        label = _html.unescape(label)
        anchor = "sec%d" % i
        nav_items += f'<a class="hide-m" href="#{anchor}">{_html.escape(label)}</a>'

    # 2) agrupando seções: cada <h2>...</h2> + seu conteúdo vira <section id=secN>...</section>
    #    converte blocos de ### (h3) em uma grade de cards.
    #    Se não houver ###, uma lista de itens com <strong> (ex.: "- **Título**: desc")
    #    também vira cards (M5) — um item = um card.
    sections_html = []
    m = re.finditer(r'<h2[^>]*>(.*?)</h2>(.*?)(?=<h2[^>]*>|$)', raw, flags=re.S)
    for i, match in enumerate(m):
        h2 = match.group(1)
        inner = match.group(2)
        # (a) grupos de <h3> em cards. Aceita <h3 ...> (extensão toc adiciona id)
        block_split = re.split(r'(?=<h3[^>]*>)', inner)
        if len(block_split) > 1:
            cards = []
            for b in block_split:
                b = b.strip()
                if not b:
                    continue
                b = _cardize(b)   # extrai emoji do h3 p/ badge .ic (profissional)
                cards.append('<div class="card">' + b + '</div>')
            inner = '<div class="cards">' + ''.join(cards) + '</div>'
        # (b) lista <ul> de itens com <strong> vira cards (um item = um card)
        ul = re.search(r'<ul>(.*?)</ul>', inner, re.S)
        if ul:
            items = re.findall(r'<li>(.*?)</li>', ul.group(1), re.S)
            if len(items) >= 2:
                cards = []
                for it in items:
                    cards.append('<div class="card">' + it.strip() + '</div>')
                lista_cards = '<div class="cards">' + ''.join(cards) + '</div>'
                inner = inner.replace(ul.group(0), lista_cards)
        sections_html.append(f'<section id="sec{i}">{h2}{inner}</section>')
    body = ''.join(sections_html)

    # JS do formulário de contato (M9) — separado para não quebrar a f-string
    form_js = (
        '<script>\n'
        '/* M9: formulario de contato offline. No submit, monta mailto com os\n'
        '   campos preenchidos (nao envia dado a nenhum servidor). */\n'
        "document.querySelectorAll('.contact-form').forEach(function(f){\n"
        "  f.addEventListener('submit', function(ev){\n"
        "    ev.preventDefault();\n"
        "    var nome=(f.querySelector('[name=nome]')||{}).value||'';\n"
        "    var email=(f.querySelector('[name=email]')||{}).value||'';\n"
        "    var msg=(f.querySelector('[name=mensagem]')||{}).value||'';\n"
        "    var body=encodeURIComponent('De: '+nome+'\\nEmail: '+email+'\\n\\n'+msg);\n"
        "    window.location.href='mailto:?subject=Contato&body='+body;\n"
        "  });\n"
        "});\n"
        "</script>\n"
    )
    # ----- monta o <head> com tema opcional (dark/neon/paper/mono) -----
    theme_css, default_theme = get_theme_css(cfg)
    theme_script = (
        "(function(){try{var s=localStorage.getItem('mimepy-theme');"
        "var dt='%s';"
        "var t=s||dt||(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');"
        "document.documentElement.setAttribute('data-theme',t);}catch(e){}})();" % default_theme
    )
    # botão de tema/dark na navbar da landing
    theme_btn = ''
    if cfg.get("theme") in ("dark", "neon") or cfg.get("features", {}).get("dark", True):
        theme_btn = '<button id="df-dark" class="land-theme" aria-label="Alternar tema" title="Alternar tema">🌙</button>'
    # script que liga o botão de tema (landing não tem o APP_JS de docs)
    theme_toggle_js = (
        '<script>'
        "var b=document.getElementById('df-dark');var r=document.documentElement;var K='mimepy-theme';"
        "if(b){b.addEventListener('click',function(){"
        "var c=r.getAttribute('data-theme')||'light';"
        "var n=(c==='light'?'dark':c==='dark'?'light':'light');"
        "r.setAttribute('data-theme',n);try{localStorage.setItem(K,n);}catch(e){}});}"
        "</script>"
    ) if theme_btn else ""

    doc = f"""<!DOCTYPE html>
<html lang="{cfg.get('lang','pt-BR')}"{' data-neon="1"' if (cfg.get("theme") or "").lower()=="neon" else ""}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{meta_desc}">
<title>{_html.escape(cfg['page_title'])}</title>
<script>{theme_script}</script>
<style>{css}{LANDING_CSS}{theme_css}</style>
</head>
<body class="land">
  <a class="skip-link" href="#secoes">Pular para o conteúdo</a>
  <nav class="land-nav" aria-label="Navegação principal">
    <div class="brand"><span class="badge">{emoji_esc}</span>{_html.escape(cfg['name'])}</div>
    <div class="links">{nav_items}</div>
    <div class="cta-nav">{theme_btn}<a class="btn btn-p" href="#secoes">{_html.escape(cta_text)}</a></div>
  </nav>

  <header class="hero">
    <div class="content">
      <div class="emoji">{emoji_esc}</div>
      <h1><span>{hero_html_title}</span></h1>
      <p class="tagline">{_html.escape(tagline)}</p>
      <div class="cta">
        <a class="btn btn-p" href="{_html.escape(cta_link)}">{_html.escape(cta_text)}</a>
        <a class="btn btn-g" href="#secoes">Conhecer</a>
      </div>
    </div>
  </header>

  <main id="secoes" role="main" tabindex="-1">
    {body}
  </main>
  <footer>
    {_html.escape(cfg.get('footer', cfg['name']))} · MimePy {VERSION} · GPL-2.0
  </footer>
{theme_toggle_js}
{form_js}</body>
</html>"""

    out = (base_dir / cfg["out_dir"]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    out_file = out / cfg["out_file"]
    out_file.write_text(doc, encoding="utf-8")
    print(f"[MimePy {VERSION}] LANDING OK -> {out_file} ({out_file.stat().st_size} bytes)")
    return out_file

if __name__ == "__main__":
    cfg_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (FRAMEWORK_ROOT / "config.py")
    if not cfg_path.exists():
        print("config não encontrado:", cfg_path); sys.exit(1)
    cfg = load_config(cfg_path)
    if cfg.get("mode") == "landing":
        build_landing(cfg, cfg_path.parent)
    else:
        build(cfg, cfg_path.parent)
