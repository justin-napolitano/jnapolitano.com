# Retain and align legacy writing site — jnapolitano.com

Approved visual authority: littlelink commit ae3e9062d8e06a1158af74a29cbd8b549d82b3e2, docs/branding/2026-10-22/brand-contract.md. Preserve all writing, media, URLs, feed behavior and access boundaries. No redirect, retirement, DNS, content rewrite, workflow change or dependency migration.

Scope: additive local template hook and static CSS/font assets with OFL licenses. Text-only site title; 22px identity, 28px reading titles, 16px body, paper/ink/stone, restrained dark slate. Existing social/menu/theme/toc controls retained. No decorative images added; meaningful article media preserved.

GitHub Pages evidence 2026-10-22: Pages API confirms project URL https://justin-napolitano.github.io/jnapolitano.com/, no custom domain, latest deployment main92886e21caeb722877fdd05e41ebe336c58eafa4 on 2024-08-09. Config still claims jnapolitano.com; preserve that divergence and existing canonical URLs for separate reviewed routing decision. Exact workflow Hugo0.124.0 baseline builds129pages; newer installed Hugo0.147.9 rejects legacy invalid frontmatter date. Use pinned toolchain, no writing edits. Rollback focused CSS/hook commit.

Validation after implementation: exact pinned toolchain build passes. Before/after HTML route sets identical (80 HTML output files); rendered text identical across all outputs; XML feed outputs unchanged. Only additive CSS/font assets and template hook change. Browser QA remains blocked pending authorized fallback.
