# VimmLoader

## Overview
Command-line tool that batch-downloads archives from Vimm's Lair vault pages, extracts them, and tracks progress through `links.txt` as a resumable queue.

## Commands
- Install deps: `pip install -r requirements.txt`
- Generate a range of vault URLs: `python3 generator.py` (edit `start`/`finish` in the file first)
- Run the downloader: `python3 run.py`
- Lint: none configured
- Tests: none configured — `python -m py_compile *.py` is the only automated check (syntax only)

## Architecture
- `run.py`: scrapes each vault page for its download form, downloads the archive with a progress bar, extracts `.zip`/`.7z` into `finished/`, deletes the archive, and drops successfully processed lines from `links.txt`.
- `generator.py`: writes a sequential range of vault URLs to `links.txt`.
- `downloading/`, `finished/`: working directories; contents are gitignored, directories kept via `.gitkeep`.

## Conventions
- Single-file scripts, no package structure; keep it that way unless the tool grows.
- Runtime config via environment variables (e.g. `VIMM_COOKIE`), never hardcoded.

## Workflow quirks
- `links.txt` is the resumable work queue: failed/unresolved URLs stay in the file, successful ones are removed.
- TLS verification is disabled (`verify=False`) in requests to vimm.net; this is existing intentional behavior, not a bug to silently fix.

## Deployment
- Not a deployed service; run locally/ad hoc as a CLI script.

## Gotchas
- No linter or test suite exists yet; CI and the Stop hook only run a syntax check (`py_compile`).
- `VIMM_COOKIE` may be required for some downloads (403/redirect) — see README.
