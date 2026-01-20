# Jekyll Site Maintenance Checklist

This document outlines maintenance tasks and items to watch for to keep the site running smoothly.

---

## Regular Maintenance Schedule

### Every 3-6 Months

- [ ] **Test local build** - Run the Docker command to ensure it still works:
  ```bash
  docker run --rm -v "$(pwd):/site" -p 4000:4000 -e JEKYLL_INCREMENTAL=false bretfisher/jekyll-serve jekyll serve --host 0.0.0.0 --watch --force_polling
  ```

- [ ] **Check GitHub Actions** - Visit the Actions tab and verify latest deploy succeeded

- [ ] **Review Dependabot PRs** - If enabled, check for and merge security updates

- [ ] **Test the live site** - Visit the GitHub Pages URL and verify everything looks correct

### Annually

- [ ] **Check Minima theme releases** - Visit https://github.com/jekyll/minima/releases
  - See if there's a stable 3.0 release
  - Review changelog for bug fixes or improvements
  - Consider adopting improvements while keeping your customizations

- [ ] **Review Jekyll changelog** - Check https://jekyllrb.com/news/ for breaking changes in newer versions

- [ ] **Update Ruby version in workflow** - When Ruby 3.2 reaches EOL, update `.github/workflows/jekyll.yml` to use Ruby 3.3+

---

## Items to Watch For

### 1. Sass @import Deprecation (Medium Priority)

**Status:** Currently using deprecated `@import` syntax (still works, just warns)

**Timeline:** Will break when Dart Sass 3.0 is released (1-2 years away, not yet scheduled)

**What to do:**
- Monitor for announcements about Dart Sass 3.0 release date
- When announced, check if Minima theme has been updated to modern Sass syntax
- Options when Dart Sass 3.0 approaches:
  - Wait for updated Minima theme and adopt their changes
  - Convert `@import` to `@use`/`@forward` yourself (complex, see SETUP_NOTES.md)
  - Accept warnings until ecosystem catches up (not recommended long-term)

**Files affected:**
- `assets/css/style.scss`
- `_sass/minima/initialize.scss`
- `_sass/minima/skins/classic.scss`
- `_sass/minima/skins/auto.scss`

### 2. GitHub Actions Workflow Dependencies (Low Priority)

**Status:** Using current stable versions of actions

**What to watch:**
- Dependabot notifications about deprecated action versions
- Warnings in Actions tab during workflow runs

**What to do:**
- Enable Dependabot: Settings → Security → Dependabot → Enable for Actions
- Review and merge auto-created PRs for action version updates

**File affected:**
- `.github/workflows/jekyll.yml`

### 3. Jekyll Version Updates (Low Priority)

**Status:** Locked to Jekyll `~> 4.3` (current stable)

**What to watch:**
- Jekyll 5.x release announcements (not imminent as of Jan 2026)
- Breaking changes in Jekyll changelogs

**What to do:**
- Before updating major versions, test locally in Docker first
- Keep `~> 4.3` constraint until ready to test 5.x
- Review migration guide when Jekyll 5.x is released

**File affected:**
- `Gemfile`

### 4. Minima Theme Updates (Medium Priority)

**Status:** Using local copy of Minima 3.0.dev (unreleased)

**What to watch:**
- Official Minima 3.0 stable release
- Minima's adoption of modern Sass syntax
- Bug fixes in Minima releases

**What to do when Minima 3.0 is released:**
1. Check release notes at https://github.com/jekyll/minima/releases
2. Compare their `_sass/minima/skins/auto.scss` with yours
3. Adopt bug fixes while preserving your `color.adjust()` improvements
4. Consider updating other theme files if beneficial

**Files affected:**
- All files in `_sass/minima/`
- All files in `_layouts/`
- All files in `_includes/`

### 5. GitHub Pages Environment Changes (Low Priority)

**Status:** Using GitHub Actions with explicit Ruby 3.2

**What to watch:**
- GitHub Pages platform announcements
- Ruby version EOL dates: https://endoflife.date/ruby
- Workflow failure notifications

**What to do:**
- GitHub will announce major platform changes in advance
- When Ruby 3.2 reaches EOL (expected ~2026), update workflow to Ruby 3.3+
- Monitor workflow runs for deprecation warnings

**File affected:**
- `.github/workflows/jekyll.yml`

---

## When Warnings or Errors Appear

### If you see deprecation warnings:

1. **Don't panic** - Deprecation warnings are advance notice, not immediate problems
2. **Check the timeline** - Most deprecations have multi-year notice periods
3. **Test locally first** - Use Docker to test any fixes before deploying
4. **Document changes** - Update SETUP_NOTES.md with what you changed and why

### If the build fails:

1. **Check the Actions tab** - Look at the detailed error logs
2. **Test locally** - Try to reproduce the error in Docker
3. **Review recent changes** - Did you or GitHub change something?
4. **Check dependency versions** - Look for breaking changes in Jekyll/gem updates
5. **Consult SETUP_NOTES.md** - Review your setup and recent changes

---

## Proactive Improvements

### Optional enhancements to consider:

- [ ] **Enable Dependabot** - Automate dependency update notifications
  - Go to Settings → Security → Dependabot
  - Enable for "GitHub Actions" and optionally for "bundler"

- [ ] **Set up notifications** - Ensure you receive GitHub Actions failure emails
  - Go to Settings → Notifications
  - Enable "Actions" notifications

- [ ] **Pin Docker image version** - For reproducibility, consider pinning the Docker image in your Docker command to a specific tag instead of using latest

---

## Quick Reference

### Key Files to Understand

- **`_config.yml`** - Main Jekyll configuration
- **`Gemfile`** - Ruby gem dependencies and versions
- **`.github/workflows/jekyll.yml`** - GitHub Actions deployment workflow
- **`_sass/minima/skins/auto.scss`** - Contains your modern Sass color function fixes
- **`SETUP_NOTES.md`** - Detailed explanation of current setup and recent changes

### Useful Commands

**Test locally:**
```bash
docker run --rm -v "$(pwd):/site" -p 4000:4000 -e JEKYLL_INCREMENTAL=false bretfisher/jekyll-serve jekyll serve --host 0.0.0.0 --watch --force_polling
```

**Build locally (no server):**
```bash
docker run --rm -v "$(pwd):/site" -e JEKYLL_INCREMENTAL=false bretfisher/jekyll-serve jekyll build
```

**Check for git changes:**
```bash
git status
```

### Key URLs

- **Live site:** https://ibeatty.github.io/marjoriebagley/
- **Repository:** https://github.com/ibeatty/marjoriebagley
- **Actions tab:** https://github.com/ibeatty/marjoriebagley/actions
- **Jekyll releases:** https://jekyllrb.com/news/
- **Minima releases:** https://github.com/jekyll/minima/releases
- **Ruby EOL dates:** https://endoflife.date/ruby

---

## Notes

- This site uses **Jekyll 4.3** with **GitHub Actions** deployment (not the legacy GitHub Pages builder)
- Local theme files override any gem-based theme
- Modern Sass `color.adjust()` functions are used instead of deprecated `lighten()`/`darken()`
- The `@import` syntax is still used (deprecated but functional) - conversion to `@use` can wait until Dart Sass 3.0 approaches

**Last reviewed:** January 2026
