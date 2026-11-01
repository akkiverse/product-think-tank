# catalog/

What the think tank knows about every product.

| File | Written by | Content |
|---|---|---|
| `catalog/<name>/PROFILE.md` | inspector (`/inspect`), engineer (release) | What, who, status, stack, features, docs map, open work, risks, next ideas |
| `catalog/<name>.json` | inspector, engineer (release) | `name, slug, repo, live_url, version, stack, last_inspected` |

Product code itself lives in its own repo, cloned locally into `products/<name>/` (git-ignored).
