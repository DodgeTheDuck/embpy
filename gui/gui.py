
import sys
from imgui.integrations.opengl import ProgrammablePipelineRenderer
import imgui
import config
import pygame as pg
from scene.scene_graph import SceneGraph
from scene.scene_object import SceneObject

_impl: ProgrammablePipelineRenderer = None
_selected_obj: SceneObject = None
_key_map = None
_custom_key_map = {}

# TODO:
# - move the application specific stuff in to it's own class


def init() -> None:
    global _impl, _key_map

    imgui.create_context()
    _impl = ProgrammablePipelineRenderer()
    _impl.io.display_size = (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

    _key_map = _impl.io.key_map

    _key_map[imgui.KEY_TAB] = _custom_key(pg.K_TAB)
    _key_map[imgui.KEY_LEFT_ARROW] = _custom_key(pg.K_LEFT)
    _key_map[imgui.KEY_RIGHT_ARROW] = _custom_key(pg.K_RIGHT)
    _key_map[imgui.KEY_UP_ARROW] = _custom_key(pg.K_UP)
    _key_map[imgui.KEY_DOWN_ARROW] = _custom_key(pg.K_DOWN)
    _key_map[imgui.KEY_PAGE_UP] = _custom_key(pg.K_PAGEUP)
    _key_map[imgui.KEY_PAGE_DOWN] = _custom_key(pg.K_PAGEDOWN)
    _key_map[imgui.KEY_HOME] = _custom_key(pg.K_HOME)
    _key_map[imgui.KEY_END] = _custom_key(pg.K_END)
    _key_map[imgui.KEY_DELETE] = _custom_key(pg.K_DELETE)
    _key_map[imgui.KEY_SPACE] = _custom_key(pg.K_SPACE)
    _key_map[imgui.KEY_BACKSPACE] = _custom_key(pg.K_BACKSPACE)
    _key_map[imgui.KEY_ENTER] = _custom_key(pg.K_RETURN)
    _key_map[imgui.KEY_ESCAPE] = _custom_key(pg.K_ESCAPE)
    _key_map[imgui.KEY_A] = _custom_key(pg.K_a)
    _key_map[imgui.KEY_C] = _custom_key(pg.K_c)
    _key_map[imgui.KEY_V] = _custom_key(pg.K_v)
    _key_map[imgui.KEY_X] = _custom_key(pg.K_x)
    _key_map[imgui.KEY_Y] = _custom_key(pg.K_y)
    _key_map[imgui.KEY_Z] = _custom_key(pg.K_z)


def start_frame() -> None:
    imgui.new_frame()


def object_properties() -> None:
    imgui.set_next_window_size(400, config.WINDOW_HEIGHT)
    imgui.set_next_window_position(config.WINDOW_WIDTH - 400, 0)
    imgui.begin(f"Properties: {_selected_obj.name if _selected_obj else 'None'}",
                flags=imgui.WINDOW_NO_COLLAPSE
                | imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR)

    if _selected_obj is not None:
        for component in _selected_obj.components:
            imgui.text(component.name)
            component.gui()

    imgui.end()


def _traverse_graph_node(obj: SceneObject) -> SceneObject:
    global _selected_obj
    if imgui.tree_node(obj.name, flags=imgui.TREE_NODE_DEFAULT_OPEN):
        if imgui.is_item_clicked(0):
            _selected_obj = obj
        for child in obj.children:
            _traverse_graph_node(child)
        imgui.tree_pop()


def scene_graph(graph: SceneGraph) -> SceneObject:
    imgui.begin("Scene Graph")
    _traverse_graph_node(graph.root)
    imgui.end()


def pipeline() -> None:
    # imgui.begin("Pipeline")
    # for stage in engine_pg.gl().pipeline.stages.values():
    #     if imgui.collapsing_header(stage.name)[0]:
    #         for tex in stage.fbo.textures:
    #             imgui.image(tex, 128 * config.ASPECT_RATIO, 128, (1, 1), (0, 0))
    #         pass

    # imgui.end()
    pass


def menu() -> None:

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):

            clicked_quit, selected_quit = imgui.menu_item(
                "Quit", "Cmd+Q", False, True
            )

            if clicked_quit or selected_quit:
                sys.exit(0)

            imgui.end_menu()
        imgui.end_main_menu_bar()


def render() -> None:
    imgui.render()
    _impl.render(imgui.get_draw_data())


def handle_event(event: pg.Event) -> None:
    match event.type:
        case pg.MOUSEMOTION:
            _impl.io.mouse_pos = event.pos[0], event.pos[1]
        case pg.MOUSEBUTTONDOWN:
            _impl.io.mouse_down[event.button - 1] = 1
        case pg.MOUSEBUTTONUP:
            _impl.io.mouse_down[event.button - 1] = 0
        case pg.KEYDOWN:
            for char in event.unicode:
                code = ord(char)
                if 0 < code < 0x10000:
                    _impl.io.add_input_character(code)
            _impl.io.keys_down[_custom_key(event.key)] = True
        case pg.KEYUP:
            # if event.scancode in _impl.io.keys_down:
            _impl.io.keys_down[_custom_key(event.key)] = False


def _custom_key(key: int) -> int:
    if key not in _custom_key_map:
        _custom_key_map[key] = len(_custom_key_map)
    return _custom_key_map[key]
