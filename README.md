# SSBU-Dump-Scripts
Script to dump and parse character game animcmd scripts programatically using r2pipe (3.0.0 - 5.0.0 only)

## Requirements
* Python 3
* Recent version of radare2 (online)
* Recent version of r2pipe (`pip install r2pipe`)

## Usage

```
python main.py ".elf path" (-p)
python main.py "directory with .elf files" (-p)
```

use the `-c` arg to specify a script category, such as `-c effect`
