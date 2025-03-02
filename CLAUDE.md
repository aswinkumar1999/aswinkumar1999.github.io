# CLAUDE.md - Reference for AI Agents

## Build Commands
- Start dev server: `docker compose up`
- Build site: `docker compose run jekyll bundle exec jekyll build`
- Check for broken links: `docker compose run jekyll bundle exec jekyll build --trace`
- Purge unused CSS: `docker compose run jekyll purgecss -c purgecss.config.js`

## Testing Commands
- Validate HTML: View site locally at http://localhost:8080 and inspect console for errors

## Code Style Guidelines
- Markdown: Use GitHub-flavored markdown syntax
- HTML/Liquid: Follow existing template patterns in _layouts and _includes
- YAML: Use 2-space indentation in _config.yml and other YAML files
- Front Matter: Include required fields (layout, title, permalink) on all pages
- Images: Place in assets/img/ directory with descriptive filenames
- CSS: Modify _sass files rather than adding inline styles
- JavaScript: Follow the patterns in assets/js/

## Repository Structure
- Website content: _pages/, _posts/, _projects/
- Configuration: _config.yml
- Styling: _sass/ directory
- Layouts: _layouts/ and _includes/ directories

## Common Tasks
- Add a blog post: Create new file in _posts/ following YYYY-MM-DD-title.md format
- Add project: Create new file in _projects/ directory with front matter
- Edit site config: Modify _config.yml (requires restart of Jekyll server)