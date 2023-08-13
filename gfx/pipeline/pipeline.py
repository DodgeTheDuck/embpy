
from abc import abstractmethod
from typing import Self

from gfx.pipeline.pipeline_stage import PipelineStage
import imgui


class Pipeline:
    def __init__(self: Self) -> None:
        self.stages = list[PipelineStage]()
        self.active_stage = -1

    def next(self: Self) -> bool:
        if self.active_stage >= len(self.stages):
            self.active_stage = 0
            return False
        self.stages[self.active_stage].bind()
        self.active_stage += 1
        return True

    def get_active_stage(self: Self) -> int:
        return self.active_stage

    def add_stage(self: Self, stage: PipelineStage) -> None:
        self.stages.append(stage)

    def draw_gui(self: Self) -> None:
        imgui.begin("Pipeline")
        for stage in self.stages:
            if imgui.collapsing_header(stage.name)[0]:
                stage.draw_gui()
        imgui.end()

    @abstractmethod
    def begin(self: Self) -> None:
        pass

    @abstractmethod
    def end(self: Self) -> None:
        pass
