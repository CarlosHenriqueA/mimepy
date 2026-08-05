---
version: alpha
name: MimePy
description: >-
  Design system autoral do MimePy — framework de documentação e landing pages
  para devs e agentes. Paleta esmeralda/teal técnico + âmbar de apoio (CTA),
  fugindo do índigo/roxo genérico de "vibe coding".
colors:
  primary: "#0d9488"
  primary-strong: "#0f766e"
  primary-light: "#2dd4bf"
  cta: "#f59e0b"
  ink: "#0f172a"
  muted: "#64748b"
  border: "#e2e8f0"
  surface: "#ffffff"
  surface-muted: "#f8fafc"
  surface-dark: "#0f172a"
  surface-dark-soft: "#111827"
  accent-text: "#0d9488"
  success: "#16a34a"
  danger: "#dc2626"
typography:
  body:
    fontFamily: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
    fontSize: 1rem
    lineHeight: 1.7
  h1:
    fontFamily: inherit
    fontSize: 1.9rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  h2:
    fontFamily: inherit
    fontSize: 1.4rem
    fontWeight: 600
    lineHeight: 1.3
  h3:
    fontFamily: inherit
    fontSize: 1.15rem
    fontWeight: 600
  code:
    fontFamily: ui-monospace, SFMono-Regular, Menlo, monospace
    fontSize: 0.85em
rounded:
  sm: 6px
  md: 10px
  lg: 16px
  full: 999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
elevation:
  sm: "0 1px 2px rgba(15,23,42,.06)"
  md: "0 4px 12px rgba(15,23,42,.10)"
  lg: "0 16px 40px rgba(15,23,42,.15)"
components:
  button-primary:
    backgroundColor: "{colors.cta}"
    textColor: "#111827"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "#d97706"
    textColor: "#111827"
  card:
    backgroundColor: "{colors.surface-dark-soft}"
    textColor: "#e2e8f0"
    rounded: "{rounded.lg}"
  nav-link:
    textColor: "#9ca3af"
---

# MimePy — Design System

## Overview

O MimePy é um framework de documentação e landing pages simples e completo para
**devs e agentes**. O design busca ser **técnico, limpo e autoral** — sem a "cara
de vibe coding" genérica (gradiente índigo/roxo, Inter, 3 cards idênticos).

- **Voz:** precisa, developer-first, sem enfeite fake.
- **Superfície:** "Decide / Learn" (landing + docs) — hero é correto, mas com
  composição intencional, não receita pronta.
- **Identidade:** esmeralda/teal como cor da marca; âmbar reservado a **uma única**
  ação de destaque (CTA). Fundo escuro e profundo nas superfícies de alto impacto.

## Colors

- **Primary (esmeralda/teal)** — a voz da marca; links, realces, código.
- **CTA (âmbar)** — **uma única** ação de conversão por superfície (botão primário).
- **Neutros** — ink/muted/border para legibilidade e hierarquia.
- Não usar índigo/roxo (reserva do mercado de "vibe coding").

## Typography

- **Corpo:** stack de sistema (ui-monospace p/ código) — legível, sem depender de
  webfont (offline). Não é Inter pública.
- **Hierarquia por peso/tamanho/espaçamento**, não por caixa decorativa.

## Layout & Spacing

- Escala de espaçamento fixa (xs→xl) mantém o ritmo.
- Cards **variados**, nunca grade de 3 idênticos (anti-slop tells #3, #7, #8).

## Elevation & Depth

- Sombras suaves e propositais (sm/md/lg); sem "glassmorphism" gratuito.

## Shapes

- Radii consistentes (sm/md/lg/full).

## Components

- `button-primary`: **uma** ação de destaque por página, em âmbar.
- `card`: superfície escura para cards; hover com elevação.
- `nav-link`: sidebar/navbar em tom suave.

## Do's and Don'ts

**Do:**
- Usar a paleta esmeralda/teal para a personalidade da marca.
- Reserve o **âmbar** para o CTA principal (1 por tela).
- Variar a composição dos cards (primeiro card em destaque / layout assimétrico).
- Manter hierarquia por tipografia e espaço.

**Don't:**
- Não usar gradiente índigo/roxo.
- Não fazer 3 cards idênticos com ícone + título + texto.
- Não depender de webfont (público-alvo quer offline).
- Não adicionar decoratividade sem função.
