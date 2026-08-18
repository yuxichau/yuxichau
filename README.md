# Personal Blog

Personal blog built with Jekyll and hosted on Cloudflare Pages.

**Live site**: https://yuxichau.com

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

3. Open http://localhost:4000/ in your browser.

## Project Structure

- `_posts/` - Blog posts in Markdown format
- `_pages/` - Static pages (about, posts index)
- `_data/` - Site data files (navigation, etc.)
- `_includes/` - Reusable HTML components
- `assets/` - Images and other static assets
- `_redirects` - Cloudflare Pages redirect rules (legacy /yuxichau/* URLs)

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

The site automatically deploys to Cloudflare Pages (project: `yuxichau`) when changes are pushed to the main branch.