# Garren Huckaby — personal website plan

## Decisions from discovery

- Hosting: GitHub Pages.
- Homepage: a welcome page with Garren’s portrait and bio.
- Sections: projects, blog, personally curated news, and contact/profile links.
- Authoring: Markdown files committed through GitHub.
- News selection: manual curation; no automatic scraping, AI service, or scheduled publishing required.

## 1. Visitor experience and information architecture

| Route | Purpose | Content |
| --- | --- | --- |
| `/` | Introduce Garren | Portrait, short bio, and navigation |
| `/projects/` | Browse engineering work | Project summaries, discipline, and status |
| `/projects/<slug>/` | Understand a project | Problem, architecture, constraints, evidence, lessons |
| `/blog/` | Browse original writing | Titles, descriptions, dates, and topic labels |
| `/blog/<slug>/` | Read a post | Comfortable reading column; Markdown headings, code, tables, and images |
| `/news/` | Browse Garren’s selected reading | Article selection and short descriptions |
| `/news/<slug>/` | Read Garren’s perspective | Link to original source and personal commentary |
| `/contact/` | Find ways to contact Garren | Email and approved profile links |
| `/404.html` | Recover from a missing page | Link back to the homepage |

The homepage introduces the person before the work. Project and writing pages use an editorial layout, with secondary context in a desktop sidebar. Mobile layouts collapse into a single reading column.

## 2. Design direction

Use Josh Comeau’s readable, article-oriented structure as a layout reference and Wodniack’s confident typography and contrast as stylistic references. Develop an original design rather than copying their assets or implementation.

- Large, compact headings paired with readable body text.
- Neutral light surfaces, deep green dark surfaces, and a bright lime accent.
- Portrait as the main visual on the homepage.
- Text-led project cards until real project photos are supplied.
- Clear navigation, restrained hover motion, and an optional light/dark theme.
- Respect reduced-motion preferences and support keyboard navigation.
- No scroll hijacking, animated cursor, or heavyweight introduction sequence.

The ellis.tennis URL could not be accessed through the research tool. It is treated as the user's hosting example; its technical implementation is unverified.

## 3. Technical architecture

The initial implementation uses a small Python static publisher and Python-Markdown. Templates, styles, and content remain repository-owned and portable. The generated site is ordinary HTML, CSS, and a small theme-toggle script.

Inputs → static build → `dist/` → GitHub Actions artifact → GitHub Pages.

- `site.json`: name, role, biography, portrait, email, and profile links.
- `content/projects/*.md`: project case studies.
- `content/blog/*.md`: original posts.
- `content/news/*.md`: curated source links and commentary.
- `assets/`: CSS, script, favicon, portrait, and project images.
- `templates/page.html`: shared document and navigation layout.
- `build.py`: content rendering, routing, metadata, and draft exclusion.
- `.github/workflows/pages.yml`: build and deploy after commits to `main`.

This avoids a frontend framework for the first version. Tradeoff: the publisher is small custom code to maintain rather than a large ecosystem such as Astro. If later requirements include interactive articles, complex taxonomies, or a CMS, reassess the stack before extending it substantially.

## 4. Authoring workflow

1. Copy an existing Markdown entry in the relevant content folder.
2. Edit the JSON metadata between the `---` delimiters, then write the body in Markdown.
3. Keep `draft: true` while preparing the entry.
4. Preview locally with `python build.py --preview`.
5. Set `draft: false` and commit to `main` to publish.

News metadata includes a source name and article URL. Use original commentary, attribution, and a link to the publisher rather than copying full articles. The feed remains static between commits and continues to work if external APIs are unavailable.

Drafts are excluded from production output. In a public repository, however, draft source files are publicly readable. Keep confidential drafts and private data outside that repository.

## 5. GitHub Pages constraints and decisions

- Static hosting has no server-side database, secrets, or contact-form processor.
- Contact begins with an email link and external profile links. A form would require a separate service.
- Free GitHub Pages supports public repositories. Private-repository Pages requires an eligible paid plan.
- A custom domain is optional and has a separate registration cost.
- User sites use `<username>.github.io`; project sites use `<username>.github.io/<repository>/`.
- The workflow obtains the actual deployment origin and base path from GitHub’s Pages configuration. Links and assets use that path.
- Real page files are generated for each route, so direct article links do not depend on single-page-app routing fallbacks.
- Portraits and project images should be compressed before committing; avoid large raw videos or laboratory datasets.
- A public repository and website must contain only information intended for public sharing. Exclude credentials and employer or participant data.

Sources checked October 8, 2026:
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- https://www.joshwcomeau.com/
- https://wodniack.dev/

## 6. Development phases and acceptance criteria

### Phase A — foundation (implemented)

Build shared navigation, footer, themes, responsive styles, welcome page, portrait slot, and content pipeline. Accept when every page renders without a runtime dependency on JavaScript and links resolve under root and repository paths.

### Phase B — content surfaces (implemented as first drafts)

Add project summaries and detail pages, blog index and article layouts, curated-news index and commentary pages, and configurable contact links. Production excludes sample blog/news drafts and uses honest empty states.

### Phase C — personalization (needs Garren’s input)

Replace the portrait placeholder, approve or rewrite the biography, supply email/GitHub/LinkedIn links, and add actual project photos, results, and original writing. No invented measurements or fabricated news are needed to fill the site.

### Phase D — validation and launch

Check all generated internal links, asset references, draft exclusion, deployment base paths, mobile overflow, theme controls, keyboard focus, and reduced-motion handling. Supply the source package and preview for review. Then connect the chosen GitHub repository, enable Pages with GitHub Actions, deploy, and verify the live URL.

### Phase E — maintain

Publish by committing content. Keep build dependencies and workflow actions reviewed periodically. Add more features only as concrete needs arise.

## 7. Remaining inputs

- A portrait image and confirmation of the bio wording.
- Public email and profile URLs.
- GitHub username, repository URL/name, and whether to use a custom domain.
- Project images and details approved for publication.
- First original blog post and first curated article.

## Initial scope boundaries

The first version includes neither a CMS nor comments, subscriptions, analytics, automatic news collection, or a server-side form. These were not requested and would introduce services or maintenance. Topic labels are shown; filtering/search can be added later if the content volume makes them useful.
