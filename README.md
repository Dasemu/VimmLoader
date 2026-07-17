# VimmLoader

A simple command-line tool to batch-download files from [Vimm's Lair](https://vimm.net). It scrapes the download form on each vault page with `requests` and `BeautifulSoup`, downloads the resulting archive, and extracts it automatically.

## Features

- Downloads a list of Vimm's Lair vault pages in sequence
- Shows a progress bar for each download (`tqdm`)
- Extracts `.zip` and `.7z` archives and deletes the archive afterward
- Skips lines it already processed, so `links.txt` doubles as a resumable queue

## Requirements

- Python 3.x

## Installation

```bash
git clone https://git.zenvairo.es/dasemu/VimmLoader
cd VimmLoader
pip install -r requirements.txt
```

## Usage

Create a file named `links.txt` in the project root with one vault page URL per line:

```text
https://vimm.net/vault/7836
https://vimm.net/vault/7970
https://vimm.net/vault/8000
```

You can generate a range of sequential vault URLs instead of typing them by hand with `generator.py` (edit the `start`/`finish` values at the top of the file first):

```bash
python3 generator.py
```

Then run the downloader:

```bash
python3 run.py
```

The `downloading/` and `finished/` folders are created automatically. Downloads are saved to `downloading/`, then extracted into `finished/`, and the original archive is deleted once extraction succeeds. Any URL that fails to resolve is kept in `links.txt` so you can retry later.

### Optional: session cookie

Some pages may require a logged-in session to allow the download. If you hit repeated errors, log in to vimm.net in your browser, copy the `Cookie` header from a request, and export it before running the script:

```bash
export VIMM_COOKIE="paste your cookie header here"
python3 run.py
```

## Disclaimer

This tool only automates requests to publicly reachable pages on vimm.net; it does not bypass any access control. You are responsible for complying with Vimm's Lair's terms of service and the copyright laws that apply to you.

## License

Released under the [GNU General Public License v3.0](LICENSE).
