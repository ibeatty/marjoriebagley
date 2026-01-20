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

GitHub Pages will automatically use the local `_layouts`, `_includes`, and `_sass` files when it builds the site, since the `theme:` line in `_config.yml` is commented out.

## Recent Changes (January 2026)

- Removed `minima.gemspec` (no longer needed)
- Updated Gemfile to remove gemspec reference
- Fixed deprecated Sass color functions in `_sass/minima/skins/auto.scss`
- Commented out `theme: minima` in `_config.yml` to use local files
