# Architecture

## Project Structure

```
scifi-database/
├── content/            # Obsidian vault — all wiki entries (symlinked into webapp)
│   ├── Comics/
│   ├── Movies/
│   ├── Novels/
│   ├── People/
│   │   ├── Artists/
│   │   ├── Authors/
│   │   └── Directors/
│   ├── Stories/
│   ├── TV/
│   └── index.md        # Landing page
├── webapp/             # Quartz v4.5.2 static site generator
│   ├── quartz.config.ts   # Main config (plugins, theme, metadata)
│   ├── quartz.layout.ts   # Page layout (sidebars, components)
│   ├── quartz/            # Quartz framework source (gitignored)
│   ├── package.json
│   └── scifi-database.service  # systemd unit for local hosting
├── scripts/
│   ├── readme-generator.py    # Generates README.md stats from content
│   └── smallest-files.py      # Lists entries by file size (find sparse pages)
├── analysis/
│   └── smallest-files.md      # Output of smallest-files.py
├── .github/workflows/
│   └── readme_generator.yml   # CI: regenerates README on push
├── Taskfile.yml        # Task runner commands (build, dev, service management)
└── README.md           # Auto-generated stats (page counts, tag/link usage)
```

## How It Fits Together

**Content authoring** happens in Obsidian. The `content/` directory is an Obsidian vault with entries organized by media type. Each `.md` file is one work (movie, novel, story, etc.) or person.

**Quartz** (`webapp/`) consumes the content directory and builds a static site. It parses Obsidian-flavored markdown (wikilinks, inline tags, callouts) and generates HTML pages with navigation features like search, graph visualization, backlinks, and tag pages.

**Scripts** analyze the content for stats and maintenance. The README is auto-generated on every push via GitHub Actions.

**Taskfile** provides shortcuts for common operations — see [operations.md](operations.md).
