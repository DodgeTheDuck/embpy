
import time
from typing import Callable, Self


class CallbackInterval:
    def __init__(self: Self,
                 interval_time_s: float,
                 callback: Callable,
                 name: str) -> None:
        self.interval_time_ns: int = interval_time_s * 1e+9
        self.callback: Callable = callback
        self.last_callback_ns: int = time.time_ns()
        self.calls = 0
        self.calls_per_second = 0
        self.name = name


class Timer:

    def __init__(self: Self) -> None:
        self.start_time: int = time.time_ns()
        self.time_last_update: int = self.start_time
        self.intervals: list[CallbackInterval] = []
        self.second_counter: int = 0

    def reset(self: Self) -> None:
        self.start_time = time.time_ns()
        self.time_last_update = self.start_time

    def update(self: Self) -> None:
        now: int = time.time_ns()
        delta_s: int = (now - self.time_last_update) / 1e+9
        self.time_last_update = now

        self.second_counter += delta_s

        if self.second_counter >= 1.0:
            for interval in self.intervals:
                interval.calls_per_second = interval.calls
                print(f"{interval.name}: {interval.calls}")
                interval.calls = 0
            self.second_counter = 0

        for interval in self.intervals:
            if (interval.last_callback_ns + interval.interval_time_ns
                    <= self.time_last_update):
                interval.callback((now - interval.last_callback_ns) / 1e+9)
                interval.last_callback_ns = self.time_last_update
                interval.calls += 1

    def set_interval(self: Self,
                     time_s: float,
                     callback: Callable,
                     name: str) -> CallbackInterval:
        interval: CallbackInterval = CallbackInterval(time_s, callback, name)
        self.intervals.append(interval)
        return interval
