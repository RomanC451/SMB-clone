from collections import defaultdict
import time
from typing import List, Callable, Dict


def check_max_dt(category: str = None) -> Callable[[Callable], Callable]:
    def check_dt(function: Callable):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            function(*args, **kwargs)
            dt = time.time() - start_time
            max_delta_times.set_max_dt(function.__name__, round(dt, 6), category)

        return wrapper

    return check_dt


class MaxDeltaTimes:
    def __init__(self) -> None:

        self.dict = defaultdict(lambda: 0)

    def set_categoryes(self, categories: List[str]) -> None:

        self.dict = {categ: defaultdict(lambda: 0) for categ in categories}

    def set_max_dt(self, func_name: str, dt: float, category: str = None) -> None:
        if category != None:
            if dt > self.dict[category][func_name]:
                self.dict[category][func_name] = dt
            return

        if dt > self.dict[func_name]:
            self.dict[func_name] = dt

    def get_categoty_dict(self, category: str) -> Dict | str:

        if category not in self.dict:
            return "Not found"

        return sorted(self.dict[category].items())

    def get_categ_total_dt(self, category: str) -> float | str:
        if category not in self.dict:
            return "Not found"

        return sum(self.dict[category].values())
    
    def reset_categ(self, category:str)-> None:
        for key in self.dict[category]:
            self.dict[category][key] = 0


max_delta_times = MaxDeltaTimes()
