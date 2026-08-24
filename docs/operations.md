# Operations

## Prerequisites

- Node.js >= 22
- npm >= 10.9.2
- [Task](https://taskfile.dev/) (optional, for shortcuts)
- Python 3.9+ (for scripts)

## Taskfile Commands

All shortcuts are defined in `Taskfile.yml` at the project root.

| Command | Description |
|---------|-------------|
| `task install` | Install npm dependencies in `webapp/` |
| `task dev` | Build and serve with hot reload (localhost:8080) |
| `task build` | Build the static site to `webapp/public/` |
| `task clean` | Remove build artifacts, cache, and node_modules |
| `task service-install` | Install and enable the systemd user service |
| `task service-status` | Check if the service is running |
| `task service-logs` | Tail the service logs |
| `task service-restart` | Restart after content changes |

## Running Manually

Without Task installed, the equivalent commands are:

```sh
cd webapp
npm install
npx quartz build --serve        # dev server on localhost:8080
npx quartz build -d ../content  # explicit content directory
```

## systemd Service

The file `webapp/scifi-database.service` defines a user-level systemd unit for running the site persistently on the local machine. It auto-restarts on failure.

```sh
# Install
ln -sf $(pwd)/webapp/scifi-database.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now scifi-database.service

# Check
systemctl --user status scifi-database.service
journalctl --user -u scifi-database.service -f
```

## CI/CD

A GitHub Actions workflow (`.github/workflows/readme_generator.yml`) runs on every push:

1. Runs `scripts/readme-generator.py` — regenerates `README.md` with current page counts, tag frequencies, and link usage stats
2. Runs `scripts/smallest-files.py` — updates `analysis/smallest-files.md` listing entries by file size (useful for finding sparse entries that need more content)
3. Commits the changes back to the repo if anything changed

## Quartz Configuration

The two main config files:

- **`webapp/quartz.config.ts`** — Plugins (markdown parsing, tag pages, search index, RSS, sitemap), theme colors/fonts, ignored patterns, locale
- **`webapp/quartz.layout.ts`** — Which components appear on each page type (content pages vs. list pages), sidebar contents, header/footer

### Enabled Plugins

**Transformers** (process markdown): FrontMatter, CreatedModifiedDate, SyntaxHighlighting, ObsidianFlavoredMarkdown, GitHubFlavoredMarkdown, TableOfContents, CrawlLinks, Description, Latex

**Filters**: RemoveDrafts

**Emitters** (generate output): AliasRedirects, ComponentResources, ContentPage, FolderPage, TagPage, ContentIndex (search + sitemap + RSS), Assets, Static, Favicon, NotFoundPage

### Page Components

Content pages (individual entries) have: breadcrumbs, title, metadata, tag list, file explorer, search, dark mode toggle, reader mode, knowledge graph, table of contents, backlinks.

List pages (tag/folder listings) have: breadcrumbs, title, metadata, file explorer, search, dark mode toggle, knowledge graph, backlinks.
