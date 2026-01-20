# Jekyll Site Setup Notes

## Theme Configuration

This site uses **Minima 3.0** theme files stored locally in the repository:
- `_layouts/` - Page templates
- `_includes/` - Reusable components
- `_sass/` - Stylesheets with modern Sass

### Why Local Theme Files?

1. **Deprecation Warnings Fixed**: Updated Sass files use modern `color.adjust()` instead of deprecated `lighten()`/`darken()` functions
2. **Customizations Preserved**: Your maroon background, navbar styling, and other customizations
3. **GitHub Pages Compatible**: Works without needing a theme gem

### Configuration Files

- **_config.yml**: Theme line is commented out - uses local files instead
- **Gemfile**: Specifies Jekyll 4.3+ for local development
- **_sass/minima/skins/auto.scss**: Updated with modern Sass color module

## Local Development

Run with Docker:
```bash
docker run --rm -v "$(pwd):/site" -p 4000:4000 -e JEKYLL_INCREMENTAL=false bretfisher/jekyll-serve jekyll serve --host 0.0.0.0 --watch --force_polling
```

## GitHub Pages Deployment

This site uses a **GitHub Actions workflow** (`.github/workflows/jekyll.yml`) to build and deploy with Jekyll 4.x.

### Required GitHub Settings

In your repository settings, you need to configure GitHub Pages to use GitHub Actions:

1. Go to **Settings** → **Pages**
2. Under "Build and deployment" → "Source"
3. Select **GitHub Actions** (not "Deploy from a branch")

This allows the site to use Jekyll 4.3+ with the modern Sass features, instead of the legacy GitHub Pages builder which only supports Jekyll 3.x.

## Recent Changes (January 2026)

- Added GitHub Actions workflow (`.github/workflows/jekyll.yml`) for Jekyll 4.x deployment
- Removed `minima.gemspec` (no longer needed)
- Updated Gemfile to use Jekyll 4.3+ instead of gemspec reference
- Fixed deprecated Sass color functions in `_sass/minima/skins/auto.scss`
- Commented out `theme: minima` in `_config.yml` to use local files
- **ACTION REQUIRED**: Change GitHub Pages source to "GitHub Actions" in repo settings
