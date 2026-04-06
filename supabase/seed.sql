-- ============================================================
-- DevPulse — Seed Data
-- ============================================================
-- Run this AFTER schema.sql to populate the tools and
-- processed_updates tables for local development and testing.
--
-- Usage (Supabase CLI):
--   supabase db reset   (runs schema.sql + seed.sql automatically)
--
-- Or apply manually in the Supabase SQL editor.
-- ============================================================

-- ── Tools ────────────────────────────────────────────────────
-- IDs are fixed so processed_updates can reference them by tool_id.
-- Using gen_random_uuid() would produce different IDs each run.

INSERT INTO public.tools (id, name, category, description, website) VALUES
(
    'a1000000-0000-0000-0000-000000000001',
    'React',
    'Frontend Framework',
    'A declarative, component-based JavaScript library for building user interfaces. Maintained by Meta and a massive open-source community.',
    'https://react.dev'
),
(
    'a1000000-0000-0000-0000-000000000002',
    'Bun',
    'Runtime',
    'An all-in-one JavaScript runtime, bundler, transpiler, and package manager designed for speed. Built with Zig.',
    'https://bun.sh'
),
(
    'a1000000-0000-0000-0000-000000000003',
    'Tailwind CSS',
    'CSS Framework',
    'A utility-first CSS framework that lets you build modern designs directly in your markup. No opinionated components.',
    'https://tailwindcss.com'
),
(
    'a1000000-0000-0000-0000-000000000004',
    'Supabase',
    'Backend-as-a-Service',
    'Open-source Firebase alternative offering Postgres, authentication, instant APIs, realtime subscriptions, and storage.',
    'https://supabase.com'
),
(
    'a1000000-0000-0000-0000-000000000005',
    'Vite',
    'Build Tool',
    'A next-generation frontend build tool with instant server start, lightning-fast HMR, and optimized Rollup-based production builds.',
    'https://vitejs.dev'
),
(
    'a1000000-0000-0000-0000-000000000006',
    'Astro',
    'Frontend Framework',
    'The web framework for content-driven websites. Ships zero JavaScript by default and supports any UI framework.',
    'https://astro.build'
),
(
    'a1000000-0000-0000-0000-000000000007',
    'Deno',
    'Runtime',
    'A modern, secure runtime for JavaScript and TypeScript with built-in tooling and web-standard APIs.',
    'https://deno.com'
),
(
    'a1000000-0000-0000-0000-000000000008',
    'SvelteKit',
    'Frontend Framework',
    'The official application framework for Svelte. File-based routing, SSR, and a great developer experience.',
    'https://kit.svelte.dev'
),
(
    'a1000000-0000-0000-0000-000000000009',
    'Next.js',
    'Frontend Framework',
    'The React framework for production. Hybrid static and server rendering, TypeScript support, and smart bundling.',
    'https://nextjs.org'
),
(
    'a1000000-0000-0000-0000-000000000010',
    'LangChain',
    'AI/ML',
    'A framework for building applications powered by language models. Chains, agents, memory, and tool integrations.',
    'https://langchain.com'
),
(
    'a1000000-0000-0000-0000-000000000011',
    'Docker',
    'DevOps',
    'Platform for building, shipping, and running containerized applications across any environment.',
    'https://docker.com'
),
(
    'a1000000-0000-0000-0000-000000000012',
    'FastAPI',
    'Backend Framework',
    'A modern, fast web framework for building APIs with Python 3.8+. Based on standard Python type hints.',
    'https://fastapi.tiangolo.com'
)
ON CONFLICT (id) DO NOTHING;

-- ── Processed Updates ────────────────────────────────────────
-- These match the DEMO_UPDATES in the backend routers.
-- trend_score range: 0-100 (higher = more trending).

INSERT INTO public.processed_updates
    (id, tool_id, tool_name, category, version, summary, source, source_url, trend_score, published_at)
VALUES
(
    'b2000000-0000-0000-0000-000000000001',
    'a1000000-0000-0000-0000-000000000001',
    'React', 'Frontend Framework', '19.1',
    'React 19 introduces Server Actions, an improved compiler, and automatic memoization — significantly reducing boilerplate and improving performance for large-scale apps.',
    'github', 'https://github.com/facebook/react/releases', 98,
    '2026-03-14T10:00:00Z'
),
(
    'b2000000-0000-0000-0000-000000000002',
    'a1000000-0000-0000-0000-000000000002',
    'Bun', 'Runtime', '1.2',
    'Bun 1.2 adds native S3 support, a built-in Postgres driver, and a dramatically faster test runner, positioning it as a serious Node.js alternative.',
    'hackernews', 'https://bun.sh/blog/bun-v1.2', 91,
    '2026-03-13T08:00:00Z'
),
(
    'b2000000-0000-0000-0000-000000000003',
    'a1000000-0000-0000-0000-000000000006',
    'Astro', 'Frontend Framework', '5.0',
    'Astro 5 ships Content Layer for type-safe data loading, Server Islands for hybrid rendering, and a simplified configuration API.',
    'producthunt', 'https://astro.build/blog/astro-5/', 87,
    '2026-03-12T14:00:00Z'
),
(
    'b2000000-0000-0000-0000-000000000004',
    'a1000000-0000-0000-0000-000000000007',
    'Deno', 'Runtime', '2.0',
    'Deno 2.0 brings full Node.js and npm compatibility, a built-in package manager, and stabilized APIs — a drop-in replacement for Node in many projects.',
    'github', 'https://deno.com/blog/v2.0', 85,
    '2026-03-11T09:30:00Z'
),
(
    'b2000000-0000-0000-0000-000000000005',
    'a1000000-0000-0000-0000-000000000003',
    'Tailwind CSS', 'CSS Framework', '4.0',
    'Tailwind CSS v4 introduces a Rust-based engine (10× faster builds), CSS-first configuration, and automatic content detection — no config file needed.',
    'hackernews', 'https://tailwindcss.com/blog/tailwindcss-v4', 93,
    '2026-03-10T11:00:00Z'
),
(
    'b2000000-0000-0000-0000-000000000006',
    'a1000000-0000-0000-0000-000000000008',
    'SvelteKit', 'Frontend Framework', '2.5',
    'SvelteKit 2.5 upgrades to Svelte 5 runes, adds incremental static regeneration, and delivers significantly smaller client bundles.',
    'github', 'https://github.com/sveltejs/kit/releases', 80,
    '2026-03-09T16:00:00Z'
),
(
    'b2000000-0000-0000-0000-000000000007',
    'a1000000-0000-0000-0000-000000000004',
    'Supabase', 'Backend-as-a-Service', '2.0',
    'Supabase launches Branching (git-like database workflows), AI vector embeddings, and queue-based background jobs — expanding beyond its Firebase-alternative roots.',
    'producthunt', 'https://supabase.com/blog', 89,
    '2026-03-08T12:00:00Z'
),
(
    'b2000000-0000-0000-0000-000000000008',
    'a1000000-0000-0000-0000-000000000005',
    'Vite', 'Build Tool', '6.0',
    'Vite 6 introduces the Environment API, allowing frameworks to configure separate dev/build/SSR environments, plus Rolldown-powered production builds.',
    'hackernews', 'https://vitejs.dev/blog/announcing-vite6', 88,
    '2026-03-07T10:30:00Z'
),
(
    'b2000000-0000-0000-0000-000000000009',
    'a1000000-0000-0000-0000-000000000009',
    'Next.js', 'Frontend Framework', '15.0',
    'Next.js 15 ships the stable App Router with improved caching defaults, Turbopack for dev builds, and React 19 as the default renderer.',
    'github', 'https://nextjs.org/blog/next-15', 95,
    '2026-03-06T09:00:00Z'
),
(
    'b2000000-0000-0000-0000-000000000010',
    'a1000000-0000-0000-0000-000000000010',
    'LangChain', 'AI/ML', '0.3',
    'LangChain 0.3 simplifies chain construction, adds structured output support, and improves streaming for real-time AI applications.',
    'github', 'https://github.com/langchain-ai/langchain/releases', 86,
    '2026-03-05T14:00:00Z'
),
(
    'b2000000-0000-0000-0000-000000000011',
    'a1000000-0000-0000-0000-000000000011',
    'Docker', 'DevOps', '27.0',
    'Docker 27 ships Compose Watch for live-reloading containers, improved BuildKit cache mounts, and rootless mode enhancements.',
    'hackernews', 'https://docs.docker.com/engine/release-notes/', 79,
    '2026-03-04T12:00:00Z'
),
(
    'b2000000-0000-0000-0000-000000000012',
    'a1000000-0000-0000-0000-000000000012',
    'FastAPI', 'Backend Framework', '0.115',
    'FastAPI 0.115 adds native support for Pydantic v2 models, improves dependency injection performance, and ships updated OpenAPI 3.1 generation.',
    'github', 'https://github.com/fastapi/fastapi/releases', 83,
    '2026-03-03T11:30:00Z'
)
ON CONFLICT (id) DO NOTHING;
