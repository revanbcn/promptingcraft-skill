# PromptingCraft.com brand system

Approved direction: **C2 — Forged Intelligence** (owner decision, 2026-10-13). A dark
hexagonal tile with a gold rim; the P is one folded gold ribbon (stem in front, bowl folded
behind it), and its counter holds a small cyan intelligence core. The marks are hand-built
SVG; the Higgsfield concept image was only a reference and is not shipped.

| File | Use |
| --- | --- |
| `emblem.svg` | Primary vector master (dark tile, works on light and dark pages); plugin `logo` / `logoDark` |
| `emblem-light.svg` | Light tile variant for pale layouts |
| `emblem-micro.svg` | Simplified mark for 16–48 px (heavier ribbon, larger core, flat colours); plugin `composerIcon` / `composerIconDark`, favicons |
| `emblem-micro-light.svg` | Light micro variant |
| `emblem-mono.svg`, `emblem-micro-mono.svg` | Single colour (`currentColor`) fallbacks |
| `wordmark-light.svg`, `wordmark-dark.svg` | "PromptingCraft.com" with a quieter ".com" |
| `lockup-light.svg`, `lockup-dark.svg` | Horizontal emblem + wordmark |
| `png/` | Transparent exports: emblem 512/128/48, light emblem 512/128/48, micro 48/32/16, lockups at 80 px |

Rules: use `emblem-micro` at 48 px and below; never shrink the master into a favicon. Keep
clear space of at least a quarter of the emblem height. Do not recolour the gold, add effects
or put the mark inside another badge. "Developed by the dondego.com team." belongs in footers
and descriptions, not in the logo.

Typography: Geist (SIL Open Font License 1.1), outlined to paths in the wordmark and lockups
(weights 640 and 430), so the files need no font. Colours: obsidian `#15191F`, gold
`#E3B052`, cyan core `#43E2F7` (light variant `#0B9CBC`); ".com" `#6A665F` on light
(5.1:1 on `#F4F1EA`) and `#A39F96` on dark.

Rebuild: `build/build_emblem.py` writes every emblem variant; `build/build_wordmark.py`
needs fontTools and uharfbuzz and the Geist variable font from the website's
`@fontsource-variable/geist`. Rollback: the previous icon set is `assets/*.svg` at commit
`0023980`.

Developed by the dondego.com team.
