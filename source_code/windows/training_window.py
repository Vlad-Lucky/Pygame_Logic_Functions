import pygame
from typing import Type
from source_code.block_scheme.blocks.input_block import InputBlock
from source_code.block_scheme.blocks.not_block import NotBlock
from source_code.block_scheme.blocks.output_block import OutputBlock
from source_code.constants import TRAINING_INSTRUCTIONS, \
    TRAINING_STARTING_DRAWING_STAGE, TRAINING_UPPER_TEXT_SIZE, \
    TRAINING_UPPER_TEXT_MAX_SYMBOLS, TRAINING_TEXT_LINES_INDENT, \
    TRAINING_ARROW_SIZE, SCORE_GAME_RECT, TRAINING_TEXT_COLOR, \
    TRAINING_TEXT_LINES_HEIGHT, FONT_NAME
from source_code.middlewares.screen_ration import get_current_rect_ration
from source_code.middlewares.splitting_line import split_line
from source_code.middlewares.window_transition_actions import \
    to_main_menu_action
from source_code.ui.training_arrow import TrainingArrow
from source_code.windows.base_window import mouse_down_check_message, \
    disable_if_message
from source_code.windows.play_window import PlayWindow


class TrainingWindow(PlayWindow):
    def __init__(self):
        super().__init__(0)
        self._stage = 0
        self.training_arrow = TrainingArrow(self.stage)

    def check_solution_action(self):
        super().check_solution_action()
        if self.stage == 14:
            self.stage += 1

    def save_action(self):
        self.show_message('You cannot save training level')

    @disable_if_message
    def mouse_wheel(self, koof: int) -> None:
        if koof > 0 and self.stage == 6:
            self.stage += 1
        super().mouse_wheel(koof)

    @mouse_down_check_message
    def mouse_down(self, mouse_button: int) -> None:
        if self.stage == 12:
            len_not_blocks = len([block for block in self.all_blocks
                                  if isinstance(block, NotBlock)])
        if mouse_button == 1 and self.stage in \
                [0, 1, 2, 3, 4, 9, 11, 15, 16, 17]:
            self.stage += 1
            if self.stage == 18:
                to_main_menu_action()
            super().mouse_down(mouse_button)
        elif mouse_button == 3 and self.stage == 12:
            super().mouse_down(mouse_button)
            now_len_not_blocks = len([block for block in self.all_blocks
                                      if isinstance(block, NotBlock)])
            if now_len_not_blocks != len_not_blocks:
                self.stage += 1
        else:
            super().mouse_down(mouse_button)

    @disable_if_message
    def mouse_up(self) -> None:
        super().mouse_up()
        if self.stage == 5:
            if any([isinstance(block, NotBlock) for block in self.all_blocks]):
                self.stage += 1
        elif self.stage == 7:
            for block in self.all_blocks:
                if isinstance(block, NotBlock) and \
                        len(block.inputs[0].attached_connections) == 1 and \
                        isinstance(block.inputs[0].attached_connections
                                   [0].parent_block, InputBlock):
                    self.stage += 1
        elif self.stage == 8:
            for block in self.all_blocks:
                if isinstance(block, NotBlock) and \
                        len(block.outputs[0].attached_connections) == 1 and \
                        isinstance(block.outputs[0].attached_connections
                                   [0].parent_block, OutputBlock):
                    self.stage += 1
        elif self.stage == 13:
            all_ans = self.get_all_test_answers()
            score_value = self.get_score_from_test_answers(all_ans)
            if score_value == 1:
                self.stage += 1

    @disable_if_message
    def double_mouse_click(self) -> None:
        super().double_mouse_click()
        if self.stage == 10:
            if any(block.outputs[0].signal == 1
                   for block in self.all_blocks
                   if isinstance(block, InputBlock)):
                self.stage += 1

    def tick(self, screen: pygame.Surface) -> None:
        rect = screen.get_rect().copy()
        rect.h = TRAINING_TEXT_LINES_HEIGHT
        for line in split_line(TRAINING_INSTRUCTIONS[self.stage],
                               TRAINING_UPPER_TEXT_MAX_SYMBOLS):
            rect.y += TRAINING_TEXT_LINES_INDENT
            widget = pygame.font.Font(FONT_NAME, TRAINING_UPPER_TEXT_SIZE).render(
                line, True, TRAINING_TEXT_COLOR)
            font_rect = widget.get_rect()
            font_rect.center = (rect.w // 2, font_rect.h // 2 + rect.y)
            screen.blit(widget, font_rect)

        def arrow_to_block_class(block_class: Type):
            nonlocal rect, rotating
            try:
                rect = [block for block in self.all_blocks
                        if isinstance(block, block_class)][0].rect.copy()
                rect.x -= TRAINING_ARROW_SIZE[0]
                rect.y += TRAINING_ARROW_SIZE[1] // 2
            except IndexError:
                rect = None
            rotating = 0

        if self.stage in [3, 10]:
            arrow_to_block_class(InputBlock)
        elif self.stage == 4:
            arrow_to_block_class(OutputBlock)
        elif self.stage == 5:
            cell_not_block = [
                cell for cell in self.choose_block_list.cells
                if isinstance(cell.copy_block, NotBlock)][0]
            rect = cell_not_block.copy_block.rect.copy()
            rect.x += self.choose_block_list.rect.x - TRAINING_ARROW_SIZE[0]
            rect.y += \
                self.choose_block_list.rect.y + \
                self.choose_block_list.cells.index(cell_not_block) * \
                cell_not_block.size[1] + TRAINING_ARROW_SIZE[1]
            rotating = 0
        elif self.stage == 12:
            arrow_to_block_class(NotBlock)
        elif self.stage == 14:
            rect = self.check_btn.rect.copy()
            rect.x += rect.w
            rotating = 180
        elif self.stage == 15:
            rect = self.table_results.rect.copy()
            rect.x += rect.w * 1.2
            rotating = 180
        elif self.stage == 16:
            rect = get_current_rect_ration(SCORE_GAME_RECT).copy()
            rect.x += rect.w
            rotating = 180
        if self.stage in [3, 4, 5, 10, 12, 14, 15, 16] and rect is not None:
            rect.size = TRAINING_ARROW_SIZE
            self.training_arrow.rect = rect
            self.training_arrow.rotating = rotating
            self.training_arrow.render(screen)

        if self.stage >= TRAINING_STARTING_DRAWING_STAGE:
            super().tick(screen)

    @property
    def stage(self) -> int:
        return self._stage

    @stage.setter
    def stage(self, value: int):
        self._stage = value
        self.training_arrow.training_stage = self._stage
