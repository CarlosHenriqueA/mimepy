#!/usr/bin/env python3
"""
MimePy v0.4 — security.py (sanitização de HTML por parser real)
================================================================
Substitui a antiga `sanitize_html` baseada em regex por um sanitizador
que usa `html.parser` (stdlib — zero dependência extra).

Por que "parser real" em vez de regex:
- regex não entende DOM; quebra em markup malformado / atributos com aspas
  aninhadas, e pode deixar vetores passar.
- `html.parser` reconstrói a árvore e permite decidir TAG a TAG e ATRIBUTO a
  atributo — muito mais robusto e testável.

Modelo de segurança (alinhado a docs/SEGURANCA.md):
- Entrada: Markdown do próprio autor (confiável por padrão). O sanitize é
  OPCIONAL — ativado via config `sanitize: true` quando o conteúdo NÃO é 100%
  do autor (ex.: conteúdo comentado/terceiros).
- Saída: HTML literal, autocontido, offline.

Vetores cobertos:
  - tags <script>, <style>, <iframe>, <object>, <embed>, <link>, <meta>
  - atributos on* (onclick, onerror, onload, onmouseover, ...)
  - protocolos perigosos em href/src: javascript:, data:, vbscript:, file:
  - atributo style com expressões perigosas (url(...)) dentro de <img> etc.
"""
import html as _html
from html.parser import HTMLParser

# Tags que são de execução/injeção — SEMPRE removidas (com conteúdo)
_BLOCKED_TAGS = {
    "script", "style", "iframe", "object", "embed", "link", "meta", "base",
    "form", "input", "textarea", "select", "button", "svg", "math", "template",
}

# Tags VOID (sem tag de fechamento em HTML). Não incrementam o contador de
# bloqueio (não têm conteúdo a suprimir), apenas são descartadas quando perigosas.
_VOID_TAGS = {
    "input", "img", "br", "hr", "meta", "link", "source", "embed", "area",
    "base", "wbr", "track", "col",
}

# Protocolos de URL que nunca devem ser abertos
_DANGEROUS_SCHEMES = ("javascript:", "data:", "vbscript:", "file:")


def _is_safe_scheme(url):
    """True se a URL não usa protocolo perigoso (aceita http/https/mailto/Ã¢ncoras)."""
    u = (url or "").strip().lower()
    if not u:
        return True
    # remove espaços/controle que permitem obfuscação: java\tscript:
    u = "".join(ch for ch in u if not ch.isspace())
    return not u.startswith(_DANGEROUS_SCHEMES)


def _is_safe_style(style):
    """True se o atributo style não contém url(...) nem import (vetores CSS)."""
    s = (style or "").lower()
    return ("url(" not in s) and ("@import" not in s) and ("expression(" not in s)


class _Sanitizer(HTMLParser):
    """Reconstrói HTML deixando só tags/atributos seguros, escapando texto."""

    # atributos permitidos por tag (allowlist por tag == defense in depth)
    _ALLOWED = {
        # padrão aplicado a qualquer tag
        "common": {"id", "class", "title", "lang", "dir", "role", "tabindex",
                   "aria-label", "aria-hidden"},
        "a": {"href", "name", "target", "rel"},
        "img": {"src", "alt", "width", "height", "loading", "title"},
        "td": {"colspan", "rowspan"},
        "th": {"colspan", "rowspan"},
        "code": {"class"},       # p/ linguagem do highlight (ex.: language-python)
        "span": {"class"},
        "input": {},             # não permitimos input (evita form/estados)
    }
    # protocolos permitidos por atributo
    _URL_ATTRS = {"href", "src"}

    def __init__(self):
        super().__init__()
        self.out = []
        self._in_blocked = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in _BLOCKED_TAGS:
            if tag not in _VOID_TAGS:
                self._in_blocked += 1        # tag com conteúdo: suprime até fechar
            return
        if self._in_blocked:
            return
        allow = self._ALLOWED.get("common", set()) | self._ALLOWED.get(tag, set())
        safe_attrs = []
        src_rejected = False                  # img/<src> perigoso -> descarta tag
        for k, v in attrs:
            k = k.lower()
            if k not in allow:
                continue
            if k in self._URL_ATTRS:
                if k == "href" and tag == "a" and v.lower().startswith("#"):
                    safe_attrs.append((k, v))   # âncora interna
                    continue
                if not _is_safe_scheme(v):
                    if k == "src":
                        src_rejected = True      # img/... sem recurso seguro
                    continue                     # descarta javascript:/data:/...
            if k == "style" and not _is_safe_style(v):
                continue                         # descarta url(...)/@import
            safe_attrs.append((k, v or ""))
        # <img>/src vazios são inofensivos mas sem src é imagem quebrada: descarta
        if tag == "img" and src_rejected:
            return
        attr_str = "".join(' %s="%s"' % (k, _html.escape(v, quote=True))
                           for k, v in safe_attrs)
        self.out.append("<%s%s>" % (tag, attr_str))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in _BLOCKED_TAGS:
            if tag not in _VOID_TAGS and self._in_blocked:
                self._in_blocked -= 1
            return
        if self._in_blocked:
            return
        self.out.append("</%s>" % tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if not self._in_blocked:
            self.out.append(_html.escape(data))

    def handle_entityref(self, name):
        if not self._in_blocked:
            self.out.append("&%s;" % name)

    def handle_charref(self, name):
        if not self._in_blocked:
            self.out.append("&#%s;" % name)


def sanitize_html(html_doc):
    """Sanitiza HTML bruto (de Markdown possivelmente não confiável).

    Mantém tags semânticas e texto; remove vetores XSS comuns. É o ponto de
    entrada único — compatível com a API antiga (recebe str, devolve str).
    """
    p = _Sanitizer()
    p.feed(html_doc or "")
    p.close()
    return "".join(p.out)