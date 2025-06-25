# Yu Xi Chau - Professional Blog

This is a Jekyll-based blog and professional website for Yu Xi Chau, hosted on GitHub Pages. The site uses the Minimal Mistakes theme and focuses on MLOps, AI Governance, and data science topics.

## Project Structure

```
yuxichau/
├── _config.yml           # Jekyll configuration file
├── index.md              # Homepage content
├── Gemfile               # Ruby dependencies
├── _data/
│   └── navigation.yml    # Site navigation configuration
├── _pages/
│   ├── about.md          # About page
│   └── posts.md          # Posts listing page
├── _posts/               # Blog posts (Markdown files)
│   └── YYYY-MM-DD-post-title.md  # Blog post files
├── assets/
│   └── images/           # Site images and assets
│       ├── bio-photo.png
│       ├── logo.png
│       └── [other images]
├── .github/
│   └── workflows/
│       └── jekyll.yml    # GitHub Actions workflow for deployment
├── .gitignore            # Files to ignore by Git
└── README.md             # Project documentation
```

## Technology Stack

- **Jekyll**: Static site generator
- **Minimal Mistakes**: Jekyll theme
- **Ruby**: Required for Jekyll
- **GitHub Pages**: Hosting platform
- **GitHub Actions**: Automated deployment

## Setup Instructions

### Prerequisites
- Ruby (version 3.1 or higher)
- Bundler gem

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yuxichau/yuxichau.git
   cd yuxichau
   ```

2. Install dependencies:
   ```bash
   bundle install
   ```

3. Serve the site locally:
   ```bash
   bundle exec jekyll serve
   ```

4. Open your browser to `http://localhost:4000` to view the site.

## Content Management

### Adding Blog Posts
Create new Markdown files in the `_posts/` directory following the naming convention:
```
YYYY-MM-DD-title-of-post.md
```

Each post should include front matter:
```yaml
---
title: "Your Post Title"
date: YYYY-MM-DD
categories: [category1, category2]
tags: [tag1, tag2]
---
```

### Updating Site Configuration
- Edit `_config.yml` for site-wide settings
- Modify `_data/navigation.yml` for navigation menu
- Update author information and social links in `_config.yml`

### Managing Pages
- Add new pages in the `_pages/` directory
- Include appropriate front matter for layout and permalink

## Deployment

This site uses GitHub Actions for automated deployment to GitHub Pages. The workflow is defined in `.github/workflows/jekyll.yml` and triggers on pushes to the main branch.

### Manual Deployment
If needed, you can build the site manually:
```bash
bundle exec jekyll build
```

## Theme Customization

The site uses the Minimal Mistakes theme with the "air" skin. To customize:
- Theme settings are in `_config.yml`
- Custom CSS can be added via theme overrides
- Layout modifications should follow Jekyll/Minimal Mistakes documentation

## License

This project is licensed under the MIT License.