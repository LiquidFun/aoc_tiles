# AoC Tiles

This script creates a graphic for each day for each year of the Advent of Code. 
A tile is an image which represents both parts of a day, it looks like this:

![AoC Tiles](examples/basic.png)

It uses the personal [AoC Leaderboard](https://adventofcode.com/2023/leaderboard/self) to get the data for each day using your cookie. 


## Installation

For this year (2023) I have rewritten this script to make it a lot easier to use. 
Now you **only** need to install `pre-commit`, add a pre-commit hook and add two HTML comments to your README.

### Install `pre-commit`:

```bash
pip install pre-commit
```

or the more modern way below (either is fine, modern pip in Python 3.11+ 
will [not allow the above command to run though](https://veronneau.org/python-311-pip-and-breaking-system-packages.html)):

```bash
# if you don't have pipx, install it with pip install pipx, or with your package manager
pipx install pre-commit  
```

### Add pre-commit hook to your repository

Add this pre-commit hook to your `.pre-commit-config.yaml` (create it, if you don't have it):

```yaml
repos:
    - repo: https://github.com/LiquidFun/aoc_tiles
      rev: 0.4.0
      hooks:
          - id: aoc-tiles
            args:
                - --auto-add-tiles-to-git
```

There are a lot more flags, see [config.py](./aoc_tiles/config.py) for all of them.
Auto add tiles is recommended as it will automatically add the tiles to your git repository, otherwise you might
forget it and the tiles will not be updated.

### Set-up

Now add `<!-- AOC TILES BEGIN -->` and `<!-- AOC TILES END -->` in your README, everything between these 2 tags
will always be replaced by the script, so do not add additional information there. Note that these are HTML comments,
so they will not be visible in the rendered README.

### Configuration

If you care about your submit-time and rank, you need to add your session cookie to the script. 
By default, if no session cookie is found, checkmarks will be used instead of the time and rank.
Add it either in the root of the repository as `session.cookie` or in the `.aoc_tiles` directory as `session.cookie`.
Make sure that this file is in your `.gitignore`!
It should contain a single line, the "session" cookie from https://adventofcode.com when you are logged in. 
No prefix is needed, only the string of length 128.



## Customization

There are various flags which can be set to change the look of your tiles. Some of them are listed here
with examples showing how it changes the look.

<!-- **Note that in order to regenerate images you have to either delete the images or delete the .aoc-tiles-cache!** -->

* `--what-to-show-on-right-side=`:

| `auto` (default)                                         | `checkmark`               | `time_and_rank`                |
|----------------------------------------------------------|---------------------------|--------------------------------|
| `time_and_rank` if cookie is available, else `checkmark` | ![](examples/01basic.png) | ![](examples/01checkmarks.png) |

* `--contrast_improvement_type=`:

| `outline` (default)          | `dark`                 | `none`                 |
|-----------------------------|--------------------------|--------------------------|
| ![](examples/05outline.png) | ![](examples/05dark.png) | ![](examples/05none.png) |
