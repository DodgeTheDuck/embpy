
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
        self.stages[self.active_stage].bind_fbo()
        self.active_stage += 1
        return True

    # TODO: create a pipeline input/output system to avoid this
    def get_last_stage(self: Self) -> PipelineStage:
        if self.active_stage <= 0:
            raise Exception("Unable to get last stage, active stage is zero")
        return self.stages[self.active_stage - 2]

    def get_active_stage_index(self: Self) -> int:
        return self.active_stage

    def get_active_stage(self: Self) -> PipelineStage:
        return self.stages[self.active_stage - 1]

    def add_stage(self: Self, stage: PipelineStage) -> Self:
        self.stages.append(stage)
        return self

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
