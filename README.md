# Personal Blog

Personal blog built with Jekyll and hosted on GitHub Pages.

**Live site**: https://yuxichau.github.io/yuxichau/

## About

This is a Jekyll-based blog where I write about software development, AI agents, and technical topics.

## Local Development

1. Install dependencies:
   ```bash
   bundle install
   ```

2. Run the development server:
   ```bash
   bundle exec jekyll serve
   ```

3. Open http://localhost:4000/yuxichau/ in your browser.

## Project Structure

- `_posts/` - Blog posts in Markdown format
- `_pages/` - Static pages (about, posts index)
- `_data/` - Site data files (navigation, etc.)
- `_includes/` - Reusable HTML components
- `assets/` - Images and other static assets
- `docs/` - Development workflow documentation

## Writing Posts

Create a new file in `_posts/` with the format `YYYY-MM-DD-title.md` and include front matter:

```markdown
---
title: "Your Post Title"
date: YYYY-MM-DD
---

Your content here.
```

## Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the main branch.
