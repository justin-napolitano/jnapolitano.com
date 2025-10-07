# jnapolitano.com

A Hugo-powered personal site that captures long-form blog posts, a lightweight journal, and a curated project portfolio. Content lives in Markdown and the site can be rebuilt automatically whenever a new entry is pushed to GitHub.

## Local development

1. Install the [Hugo Extended binary](https://gohugo.io/installation/) for your platform.
2. Clone the repo and pull in the theme/content submodules:

   ```bash
   git clone https://github.com/justin-napolitano/jnapolitano.com.git
   cd jnapolitano.com
   git submodule update --init --recursive
   ```

3. Start the development server (includes drafts/future-dated content so you can preview everything):

   ```bash
   hugo server --buildDrafts --buildFuture --disableFastRender
   ```

Visit <http://localhost:1313> and the server will live-reload whenever you change Markdown files, layouts, or assets.

## Docker workflow

Build the production image and serve the pre-rendered site with Nginx:

```bash
docker build -t jnapolitano-site .
docker run --rm -p 8080:80 jnapolitano-site
```

Visit `http://localhost:8080` to preview the generated site.

> **Tip:** Running the Docker commands above does **not** require Hugo to be installed locally—the site is built inside the container.

## Continuous deployment

A GitHub Actions workflow (`.github/workflows/hugo.yaml`) builds the site with the same Hugo version used in the Docker image and deploys the `public/` output to GitHub Pages whenever changes land on the `main` or `gh-pages` branches. Add or update Markdown content, push to GitHub, and the workflow will automatically publish the refreshed site.

## Content structure

- `content/posts/` – long-form blog posts (the main blog feed)
- `content/journal/` – quick-hitting notes and progress updates
- `content/portfolio/` – highlighted projects with optional links and tooling notes

Each section has an archetype under `archetypes/` to quickly scaffold new entries with the correct front matter.
