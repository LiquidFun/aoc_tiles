This project is currently being reworked in order to make it easier to use! Things might change in the next few days.

# AoC Tiles

This script creates a graphic for each day for each year of the Advent of Code. 
A tile is an image which represents both parts of a day, it looks like this:

![AoC Tiles](examples/basic.png)

It uses the personal [AoC Leaderboard](https://adventofcode.com/2021/leaderboard/self) to get the data for each day using your cookie. 


## Installation

Feel free to use it, here is a short description of how to get it working:

Copy this entire folder into your AoC repository. Then install the requirements.

### Requirements

Install at least Python 3.10 (because of the new typing union `|`, if you cannot do so you can
change the `type1 | type2` annotations to `Union[type1, type2]`).

Install the requirements (`pillow` for creating images, `requests` for the leaderboard data and `pyyaml` to parse the language config):

```
pip install -r requirements.txt
```

### Configuration

To use this script, you need to have a file named "session.cookie" in the same folder as this script.
It should contain a single line, the "session" cookie from https://adventofcode.com when you are logged in. 
No prefix is needed, only the string of length 128.

Now add `<!-- AOC TILES BEGIN -->
<h1 align="center">
  2015 - 0 ⭐
</h1>
<h1 align="center">
  2016 - 0 ⭐
</h1>
<h1 align="center">
  2017 - 0 ⭐
</h1>
<h1 align="center">
  2018 - 0 ⭐
</h1>
<h1 align="center">
  2019 - 0 ⭐
</h1>
<h1 align="center">
  2020 - 0 ⭐
</h1>
<h1 align="center">
  2021 - 0 ⭐
</h1>
<h1 align="center">
  2022 - 0 ⭐
</h1>
<a href="tests/samples/adventofcode/2016/puzzle01.py">
  <img src=".aoc_tiles/tiles/2016/01.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 01.ipynb">
  <img src=".aoc_tiles/tiles/2017/01.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 01.ipynb">
  <img src=".aoc_tiles/tiles/2022/01.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 01.ipynb">
  <img src=".aoc_tiles/tiles/2018/01.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 01.ipynb">
  <img src=".aoc_tiles/tiles/2021/01.png" width="161px">
</a>
<a href="None">
  <img src=".aoc_tiles/tiles/2015/01.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 01.ipynb">
  <img src=".aoc_tiles/tiles/2019/01.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle02.py">
  <img src=".aoc_tiles/tiles/2016/02.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 01.ipynb">
  <img src=".aoc_tiles/tiles/2020/01.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 02.ipynb">
  <img src=".aoc_tiles/tiles/2018/02.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 02.ipynb">
  <img src=".aoc_tiles/tiles/2017/02.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 02.ipynb">
  <img src=".aoc_tiles/tiles/2022/02.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 02.ipynb">
  <img src=".aoc_tiles/tiles/2021/02.png" width="161px">
</a>
<a href="None">
  <img src=".aoc_tiles/tiles/2015/02.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle03.py">
  <img src=".aoc_tiles/tiles/2016/03.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 02.ipynb">
  <img src=".aoc_tiles/tiles/2019/02.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 02.ipynb">
  <img src=".aoc_tiles/tiles/2020/02.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 03.ipynb">
  <img src=".aoc_tiles/tiles/2018/03.png" width="161px">
</a>
<a href="None">
  <img src=".aoc_tiles/tiles/2015/03.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 03.ipynb">
  <img src=".aoc_tiles/tiles/2021/03.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 03.ipynb">
  <img src=".aoc_tiles/tiles/2022/03.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 03.ipynb">
  <img src=".aoc_tiles/tiles/2017/03.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle04.py">
  <img src=".aoc_tiles/tiles/2016/04.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 03.ipynb">
  <img src=".aoc_tiles/tiles/2019/03.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 03.ipynb">
  <img src=".aoc_tiles/tiles/2020/03.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 04.ipynb">
  <img src=".aoc_tiles/tiles/2018/04.png" width="161px">
</a>
<a href="None">
  <img src=".aoc_tiles/tiles/2015/04.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 04.ipynb">
  <img src=".aoc_tiles/tiles/2021/04.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 04.ipynb">
  <img src=".aoc_tiles/tiles/2017/04.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 04.ipynb">
  <img src=".aoc_tiles/tiles/2022/04.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle05.py">
  <img src=".aoc_tiles/tiles/2016/05.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 04.ipynb">
  <img src=".aoc_tiles/tiles/2019/04.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 05.ipynb">
  <img src=".aoc_tiles/tiles/2017/05.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 04.ipynb">
  <img src=".aoc_tiles/tiles/2020/04.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 05.ipynb">
  <img src=".aoc_tiles/tiles/2021/05.png" width="161px">
</a>
<a href="None">
  <img src=".aoc_tiles/tiles/2015/05.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 05.ipynb">
  <img src=".aoc_tiles/tiles/2018/05.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle06.py">
  <img src=".aoc_tiles/tiles/2016/06.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 05.ipynb">
  <img src=".aoc_tiles/tiles/2019/05.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 06.ipynb">
  <img src=".aoc_tiles/tiles/2017/06.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 05.ipynb">
  <img src=".aoc_tiles/tiles/2022/05.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent6.py">
  <img src=".aoc_tiles/tiles/2015/06.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 06.ipynb">
  <img src=".aoc_tiles/tiles/2018/06.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 06.ipynb">
  <img src=".aoc_tiles/tiles/2021/06.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 05.ipynb">
  <img src=".aoc_tiles/tiles/2020/05.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle07.py">
  <img src=".aoc_tiles/tiles/2016/07.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 06.ipynb">
  <img src=".aoc_tiles/tiles/2019/06.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 07.ipynb">
  <img src=".aoc_tiles/tiles/2017/07.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent7.py">
  <img src=".aoc_tiles/tiles/2015/07.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 06.ipynb">
  <img src=".aoc_tiles/tiles/2022/06.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 07.ipynb">
  <img src=".aoc_tiles/tiles/2018/07.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 07.ipynb">
  <img src=".aoc_tiles/tiles/2019/07.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 06.ipynb">
  <img src=".aoc_tiles/tiles/2020/06.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent8.py">
  <img src=".aoc_tiles/tiles/2015/08.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 08.ipynb">
  <img src=".aoc_tiles/tiles/2017/08.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 07.ipynb">
  <img src=".aoc_tiles/tiles/2021/07.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle08.py">
  <img src=".aoc_tiles/tiles/2016/08.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 08.ipynb">
  <img src=".aoc_tiles/tiles/2018/08.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 07.ipynb">
  <img src=".aoc_tiles/tiles/2020/07.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 08.ipynb">
  <img src=".aoc_tiles/tiles/2019/08.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 09.ipynb">
  <img src=".aoc_tiles/tiles/2017/09.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent9.py">
  <img src=".aoc_tiles/tiles/2015/09.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 08.ipynb">
  <img src=".aoc_tiles/tiles/2021/08.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 07.ipynb">
  <img src=".aoc_tiles/tiles/2022/07.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle09.py">
  <img src=".aoc_tiles/tiles/2016/09.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 09.ipynb">
  <img src=".aoc_tiles/tiles/2018/09.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 09.ipynb">
  <img src=".aoc_tiles/tiles/2019/09.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent10.py">
  <img src=".aoc_tiles/tiles/2015/10.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 08.ipynb">
  <img src=".aoc_tiles/tiles/2020/08.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 10.ipynb">
  <img src=".aoc_tiles/tiles/2017/10.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 08.ipynb">
  <img src=".aoc_tiles/tiles/2022/08.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 09.ipynb">
  <img src=".aoc_tiles/tiles/2021/09.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent11.py">
  <img src=".aoc_tiles/tiles/2015/11.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle10.py">
  <img src=".aoc_tiles/tiles/2016/10.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 10.ipynb">
  <img src=".aoc_tiles/tiles/2018/10.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 10.ipynb">
  <img src=".aoc_tiles/tiles/2019/10.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle11.py">
  <img src=".aoc_tiles/tiles/2016/11.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 11.ipynb">
  <img src=".aoc_tiles/tiles/2017/11.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 10.ipynb">
  <img src=".aoc_tiles/tiles/2021/10.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 09.ipynb">
  <img src=".aoc_tiles/tiles/2022/09.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 09.ipynb">
  <img src=".aoc_tiles/tiles/2020/09.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent12.py">
  <img src=".aoc_tiles/tiles/2015/12.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 11.ipynb">
  <img src=".aoc_tiles/tiles/2019/11.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 11.ipynb">
  <img src=".aoc_tiles/tiles/2018/11.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 11.ipynb">
  <img src=".aoc_tiles/tiles/2021/11.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 10.ipynb">
  <img src=".aoc_tiles/tiles/2022/10.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 10.ipynb">
  <img src=".aoc_tiles/tiles/2020/10.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle12.py">
  <img src=".aoc_tiles/tiles/2016/12.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 12.ipynb">
  <img src=".aoc_tiles/tiles/2019/12.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent13.py">
  <img src=".aoc_tiles/tiles/2015/13.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 12.ipynb">
  <img src=".aoc_tiles/tiles/2018/12.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle13.py">
  <img src=".aoc_tiles/tiles/2016/13.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 12.ipynb">
  <img src=".aoc_tiles/tiles/2021/12.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 12.ipynb">
  <img src=".aoc_tiles/tiles/2017/12.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 11.ipynb">
  <img src=".aoc_tiles/tiles/2022/11.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 11.ipynb">
  <img src=".aoc_tiles/tiles/2020/11.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 13.ipynb">
  <img src=".aoc_tiles/tiles/2019/13.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent14.py">
  <img src=".aoc_tiles/tiles/2015/14.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 13.ipynb">
  <img src=".aoc_tiles/tiles/2021/13.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 12.ipynb">
  <img src=".aoc_tiles/tiles/2022/12.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle14.py">
  <img src=".aoc_tiles/tiles/2016/14.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 13.ipynb">
  <img src=".aoc_tiles/tiles/2017/13.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 13.ipynb">
  <img src=".aoc_tiles/tiles/2018/13.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 12.ipynb">
  <img src=".aoc_tiles/tiles/2020/12.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 14.ipynb">
  <img src=".aoc_tiles/tiles/2021/14.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent15.py">
  <img src=".aoc_tiles/tiles/2015/15.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 14.ipynb">
  <img src=".aoc_tiles/tiles/2019/14.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 13.ipynb">
  <img src=".aoc_tiles/tiles/2020/13.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 13.ipynb">
  <img src=".aoc_tiles/tiles/2022/13.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 15.ipynb">
  <img src=".aoc_tiles/tiles/2019/15.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 14.ipynb">
  <img src=".aoc_tiles/tiles/2017/14.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle15.py">
  <img src=".aoc_tiles/tiles/2016/15.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 14.ipynb">
  <img src=".aoc_tiles/tiles/2018/14.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 15.ipynb">
  <img src=".aoc_tiles/tiles/2021/15.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 14.ipynb">
  <img src=".aoc_tiles/tiles/2020/14.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent16.py">
  <img src=".aoc_tiles/tiles/2015/16.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 14.ipynb">
  <img src=".aoc_tiles/tiles/2022/14.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 15.ipynb">
  <img src=".aoc_tiles/tiles/2017/15.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 16.ipynb">
  <img src=".aoc_tiles/tiles/2019/16.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 16.ipynb">
  <img src=".aoc_tiles/tiles/2021/16.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle16.py">
  <img src=".aoc_tiles/tiles/2016/16.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 15.ipynb">
  <img src=".aoc_tiles/tiles/2018/15.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 15.ipynb">
  <img src=".aoc_tiles/tiles/2020/15.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent17.py">
  <img src=".aoc_tiles/tiles/2015/17.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 15.ipynb">
  <img src=".aoc_tiles/tiles/2022/15.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 16.ipynb">
  <img src=".aoc_tiles/tiles/2017/16.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle17.py">
  <img src=".aoc_tiles/tiles/2016/17.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 17.ipynb">
  <img src=".aoc_tiles/tiles/2021/17.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 17.ipynb">
  <img src=".aoc_tiles/tiles/2019/17.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 16.ipynb">
  <img src=".aoc_tiles/tiles/2018/16.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 16.ipynb">
  <img src=".aoc_tiles/tiles/2020/16.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 16.ipynb">
  <img src=".aoc_tiles/tiles/2022/16.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 17.ipynb">
  <img src=".aoc_tiles/tiles/2017/17.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent18.py">
  <img src=".aoc_tiles/tiles/2015/18.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 17.ipynb">
  <img src=".aoc_tiles/tiles/2018/17.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 18.ipynb">
  <img src=".aoc_tiles/tiles/2019/18.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 18.ipynb">
  <img src=".aoc_tiles/tiles/2021/18.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 17.ipynb">
  <img src=".aoc_tiles/tiles/2020/17.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle18.py">
  <img src=".aoc_tiles/tiles/2016/18.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent19.py">
  <img src=".aoc_tiles/tiles/2015/19.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle19.py">
  <img src=".aoc_tiles/tiles/2016/19.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 17.ipynb">
  <img src=".aoc_tiles/tiles/2022/17.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 18.ipynb">
  <img src=".aoc_tiles/tiles/2020/18.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 18.ipynb">
  <img src=".aoc_tiles/tiles/2017/18.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 19.ipynb">
  <img src=".aoc_tiles/tiles/2021/19.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 19.ipynb">
  <img src=".aoc_tiles/tiles/2019/19.png" width="161px">
</a>
<a href="None">
  <img src=".aoc_tiles/tiles/2015/20.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 18.ipynb">
  <img src=".aoc_tiles/tiles/2018/18.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle20.py">
  <img src=".aoc_tiles/tiles/2016/20.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 19.ipynb">
  <img src=".aoc_tiles/tiles/2017/19.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 19.ipynb">
  <img src=".aoc_tiles/tiles/2020/19.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 20.ipynb">
  <img src=".aoc_tiles/tiles/2021/20.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 18.ipynb">
  <img src=".aoc_tiles/tiles/2022/18.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent21.py">
  <img src=".aoc_tiles/tiles/2015/21.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 20.ipynb">
  <img src=".aoc_tiles/tiles/2019/20.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 19.ipynb">
  <img src=".aoc_tiles/tiles/2018/19.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 20.ipynb">
  <img src=".aoc_tiles/tiles/2020/20.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle21.py">
  <img src=".aoc_tiles/tiles/2016/21.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent22.py">
  <img src=".aoc_tiles/tiles/2015/22.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 19.ipynb">
  <img src=".aoc_tiles/tiles/2022/19.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 21.ipynb">
  <img src=".aoc_tiles/tiles/2019/21.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 21.ipynb">
  <img src=".aoc_tiles/tiles/2021/21.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 20.ipynb">
  <img src=".aoc_tiles/tiles/2017/20.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 20.ipynb">
  <img src=".aoc_tiles/tiles/2018/20.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 21.ipynb">
  <img src=".aoc_tiles/tiles/2020/21.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 21.ipynb">
  <img src=".aoc_tiles/tiles/2017/21.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle22.py">
  <img src=".aoc_tiles/tiles/2016/22.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 22.ipynb">
  <img src=".aoc_tiles/tiles/2021/22.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent23.py">
  <img src=".aoc_tiles/tiles/2015/23.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 21.ipynb">
  <img src=".aoc_tiles/tiles/2018/21.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 20.ipynb">
  <img src=".aoc_tiles/tiles/2022/20.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 22.ipynb">
  <img src=".aoc_tiles/tiles/2017/22.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle23.py">
  <img src=".aoc_tiles/tiles/2016/23.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 22.ipynb">
  <img src=".aoc_tiles/tiles/2020/22.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 22.ipynb">
  <img src=".aoc_tiles/tiles/2019/22.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 21.ipynb">
  <img src=".aoc_tiles/tiles/2022/21.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 23.ipynb">
  <img src=".aoc_tiles/tiles/2021/23.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent24.py">
  <img src=".aoc_tiles/tiles/2015/24.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 22.ipynb">
  <img src=".aoc_tiles/tiles/2018/22.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 23.ipynb">
  <img src=".aoc_tiles/tiles/2017/23.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 23.ipynb">
  <img src=".aoc_tiles/tiles/2020/23.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle24.py">
  <img src=".aoc_tiles/tiles/2016/24.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 23.ipynb">
  <img src=".aoc_tiles/tiles/2019/23.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2015/advent25.py">
  <img src=".aoc_tiles/tiles/2015/25.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 24.ipynb">
  <img src=".aoc_tiles/tiles/2021/24.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 22.ipynb">
  <img src=".aoc_tiles/tiles/2022/22.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2016/puzzle25.py">
  <img src=".aoc_tiles/tiles/2016/25.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 23.ipynb">
  <img src=".aoc_tiles/tiles/2018/23.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 24.ipynb">
  <img src=".aoc_tiles/tiles/2020/24.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 24.ipynb">
  <img src=".aoc_tiles/tiles/2017/24.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 24.ipynb">
  <img src=".aoc_tiles/tiles/2019/24.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 24.ipynb">
  <img src=".aoc_tiles/tiles/2018/24.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2020/Day 25.ipynb">
  <img src=".aoc_tiles/tiles/2020/25.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2021/Day 25.ipynb">
  <img src=".aoc_tiles/tiles/2021/25.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 23.ipynb">
  <img src=".aoc_tiles/tiles/2022/23.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2017/Day 25.ipynb">
  <img src=".aoc_tiles/tiles/2017/25.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2019/Day 25.ipynb">
  <img src=".aoc_tiles/tiles/2019/25.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2018/Day 25.ipynb">
  <img src=".aoc_tiles/tiles/2018/25.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 24.ipynb">
  <img src=".aoc_tiles/tiles/2022/24.png" width="161px">
</a>
<a href="tests/samples/adventofcode/2022/Day 25.ipynb">
  <img src=".aoc_tiles/tiles/2022/25.png" width="161px">
</a>
<!-- AOC TILES END -->` in your README, everything between these 2 tags
will always be replaced by the script, so do not add additional information there. Note that these are HTML comments, 
so they will not be visible in the rendered README.

Your year/day script structure likely looks different. You can change the patterns for years and days in the 
[create_aoc_tiles.py](create_aoc_tiles.py) file.

The variables at the top of the script have comments to explain what they do.

To try whether it works you can run the script directly:

```
python3 create_aoc_tiles.py
```

### Pre-commit hook

Add [.pre-commit-config.yaml](/.pre-commit-config.yaml) to your repository and run `pre-commit install` to install the hook.


## Customization

There are various flags and variables which can be set to change the look of your tiles. Some of them are listed here
with examples showing how it changes the look.

**Note that in order to regenerate images you have to either delete the images or delete the .aoc-tiles-cache!**

* `SHOW_CHECKMARK_INSTEAD_OF_TIME_RANK`:

| `False` (default)           | `True`                         |
|---------------------------|--------------------------------|
| ![](examples/01basic.png) | ![](examples/01checkmarks.png) |

* `CONTRAST_IMPROVEMENT_TYPE`:

| `"outline"` (default)          | `"dark"`                 | `"none"`                 |
|-----------------------------|--------------------------|--------------------------|
| ![](examples/05outline.png) | ![](examples/05dark.png) | ![](examples/05none.png) |
---|--------------------------|
| ![](examples/05outline.png) | ![](examples/05dark.png) | ![](examples/05none.png) |
