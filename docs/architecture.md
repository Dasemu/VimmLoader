# Architecture

VimmLoader is a pair of single-file scripts with no package structure.

## `generator.py`

Writes a sequential range of Vimm's Lair vault URLs (`https://vimm.net/vault/<id>`) to `links.txt`, one per line. The `start`/`finish` range is edited directly in the file before running it.

## `run.py`

For each URL still in `links.txt`:

1. Fetches the vault page and scrapes its download form (action URL and hidden fields) with BeautifulSoup.
2. Submits the form and streams the response archive into `downloading/`, rendering a `tqdm` progress bar.
3. Extracts the archive (`.zip` or `.7z`) into `finished/`.
4. Deletes the downloaded archive once extraction succeeds.
5. Removes the URL's line from `links.txt`.

A URL that fails at any step is left in `links.txt`, which makes the file a resumable work queue: re-running `run.py` only retries what's left.

Requests to vimm.net disable TLS verification (`verify=False`). This is intentional, existing behavior — see [LESSONS.md](../LESSONS.md) and the root `CLAUDE.md` before touching it.

## Working directories

- `downloading/`: archives in progress. Gitignored; kept via `.gitkeep`.
- `finished/`: extracted output. Gitignored; kept via `.gitkeep`.

## Configuration

Runtime config is via environment variables, read directly by `run.py` (no `.env` loading). See `.env.example` for the full list, currently just `VIMM_COOKIE` for pages that require a logged-in session.
