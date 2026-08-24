# Content Format

## File Structure

Each entry is a markdown file in the appropriate category folder (`Movies/`, `Novels/`, `Stories/`, `Comics/`, `TV/`, `People/`).

### Frontmatter (optional)

Some entries include YAML frontmatter for metadata:

```yaml
---
rate: 9
author: Troy Nixley
read: 12/6/2022
---
```

Frontmatter fields are not standardized across all entries — most entries omit it entirely.

### Inline Tags

Tags go at the top of the file body (after any frontmatter), as Obsidian-style inline hashtags:

```
#space/space-settling #space #children #action #time/time-gap
```

Tags use hyphens for multi-word names and `/` for hierarchy.

### Body Content

Entries are freeform bullet-point notes. Tags can also appear inline within the body text to annotate specific observations:

```
- Love TARS's design and character, great #robots
- #megastructures/oneill-cylinder referenced at the end
```

### Wikilinks

Cross-references use Obsidian `[[wikilink]]` syntax:

```
- Another collaboration between [[Christopher Nolan]] and [[Hanz Zimmer]]
- Lots of homages to [[2001 A Space Odyssey (Movie)]]
```

Quartz resolves these using shortest-path matching, so `[[Interstellar]]` links to `Movies/Interstellar.md`.

## Tag Taxonomy

Tags are hierarchical. A tag like `#space/mars` creates two tag pages:
- `tags/space` — aggregates all entries with any `#space/*` tag
- `tags/space/mars` — entries specifically tagged `#space/mars`

### Top-level tag categories with subtags:

| Parent | Children |
|--------|----------|
| `#aliens` | `superior-aliens`, `inferior-aliens`, `ancestor-aliens` |
| `#biology` | `alien-biology` |
| `#children` | `post-humans` |
| `#megastructures` | `dyson-spheres`, `oneill-cylinder`, `orbital-ring`, `space-elevator`, `topopolis` |
| `#minds` | `hive-minds`, `omnipotence` |
| `#space` | `asteroids`, `black-holes`, `mars`, `moon`, `space-settling` |
| `#time` | `beyond-time`, `time-gap`, `time-loop`, `time-reversal`, `time-trap`, `time-travel` |

Most tags are flat (non-hierarchical), like `#action`, `#comedy`, `#cyberpunk`, etc.
