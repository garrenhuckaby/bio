## Repository configuration

Target repository: https://github.com/garrenhuckaby/bio
Expected project-site URL: https://garrenhuckaby.github.io/bio/

Portrait and project photos are labeled placeholders. GitHub links to the real profile; email and LinkedIn are labeled, non-clickable placeholders. Replace these in `site.json` when ready.

# Garren Huckaby’s personal website

A GitHub Pages-ready static website with a welcome page, project case studies, Markdown blog, personally curated reading list, and contact links. Read `PLAN.md` for the full plan.

## Local preview

Python 3.12 is used by the deployment workflow.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py --preview
python -m http.server 8000 --directory dist
```

Open http://localhost:8000. On Windows, activate with `.venv\Scripts\activate` instead.

For production output (sample drafts excluded):

```sh
python build.py
```

Do not open generated HTML via `file://`; use a web server so root-relative links work.

## Personalize

Edit `site.json`:

- `bio`: paragraphs of your biography.
- `portrait`: filename relative to `assets/`, e.g. `garren.webp`.
- `portrait_alt`: accessible description of the real photo.
- `email`: public email address, or empty to omit it.
- `links`: objects such as `{"label": "GitHub", "url": "https://github.com/YOUR_USERNAME"}`.

Put the photo into `assets/`. Aim for a compressed image around 600–1000 px wide. Verify the crop on mobile. The sample biography/project copy needs your review before launch. Update role labels in `build.py` if desired; the `role` field in `site.json` is reserved for future use.

## Add a blog post

Create `content/blog/my-post.md`. Metadata uses valid JSON (double quotes, `true`/`false`, no trailing commas):

```markdown
---
{"title":"My post","description":"A short description.","date":"2026-10-08","tags":["Electronics"],"draft":true}
---
## The problem

Write your post here. Use normal Markdown, fenced code blocks, tables, and images.
```

Set `draft` to `false` to include the post in production. Filenames become URLs. Changing a filename changes its URL. Dates use YYYY-MM-DD. Drafts are not private if committed to a public repository.

For a project, copy one of the existing files in `content/projects/`; keep `number` unique and use it to order projects.

## Add a curated news entry

Copy `content/news/example.md`. Replace the title, description, source, URL, date, and tags. Write your own commentary in the body. Set `draft` to `false` when ready. The original source link is shown above your commentary.

## Publish to GitHub Pages

1. Create a repository. For a personal root site, name it exactly `YOUR_USERNAME.github.io`. For a project site, any repository name works.
2. Add the source files from this folder, including `.github/workflows/pages.yml`. Do not commit `dist/`, `.venv/`, or private data. Ensure the default branch is `main`, or edit the workflow branch.
3. In repository **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source.
4. Commit/push to `main`, or manually run **Publish personal website** from the Actions tab after enabling Pages.
5. After the workflow completes, open the deployed URL shown in the `github-pages` environment.

GitHub Free Pages uses a public repository. A custom domain is optional: configure it through Pages settings and your domain provider, verify it, and enable HTTPS. The workflow reads the configured origin and base path automatically. A manually maintained `CNAME` file is not necessary for this custom Actions workflow.

For a local subfolder-deployment check:

```sh
python build.py --base /personal-site --site-url https://example.github.io
```

This output is meant to be served under `/personal-site/`. For normal local preview, omit `--base`.

## What works now

- All required page types and project detail pages.
- Light/dark theme with locally saved preference.
- Responsive navigation and editorial reading layouts.
- Markdown content and production draft exclusion.
- Source links on curated entries.
- GitHub Pages workflow, base-path support, 404 page, and sitemap when an origin is configured.

## Still needed before launch

A portrait, approved biography/project copy, actual contact links, and GitHub repository details. Production blog/news intentionally start empty. The development preview includes clearly labeled sample drafts.
