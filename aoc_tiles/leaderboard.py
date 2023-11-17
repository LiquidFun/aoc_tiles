from dataclasses import dataclass
from typing import Union


@dataclass
class DayScores:
    time1: Union[str, None] = None
    rank1: Union[str, None] = None
    score1: Union[str, None] = None
    time2: Union[str, None] = None
    rank2: Union[str, None] = None
    score2: Union[str, None] = None
