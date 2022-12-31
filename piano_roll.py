import flet as ft
import math

LINE_WITH = 1
LINE_COLOR = ft.colors.BLACK
TOTAL_KEYS = 96
BEATS_PER_GRID = 16

def h_line(length, top = 0, left = 0, line_width = LINE_WITH, line_color = LINE_COLOR):
    return ft.Container(
        width=length,
        height=line_width,
        bgcolor=line_color,
        top=top,
        left=left
    )

def v_line(length, top = 0, left = 0, line_width = LINE_WITH, line_color = LINE_COLOR):
    return ft.Container(
        height=length,
        width=line_width,
        bgcolor=line_color,
        top=top,
        left=left
    )

class UIMidiNote:
    def __init__(self, line_width, x_unit_length, y_unit_length, note = TOTAL_KEYS, duration_in_beats: int = 1, start_beat: int = 0) -> None:
        self.acc_x = 0
        self.acc_y = 0
        self.midline_offset_x = line_width / 2
        self.midline_offset_y = line_width / 2

        self.note = note
        self.duration_in_beats = duration_in_beats
        self.start_beat = start_beat

        def on_pan_start(e: ft.DragStartEvent):
            self.acc_x = e.control.left
            self.acc_y = e.control.top

        def on_pan_update(e: ft.DragUpdateEvent):
            acc_x = self.acc_x
            acc_y = self.acc_y
            
            e.control.left = max(0, (math.floor(acc_x / x_unit_length)  * x_unit_length) + self.midline_offset_x)
            e.control.top = max(0, (math.floor(acc_y / y_unit_length) * y_unit_length) + self.midline_offset_y)

            acc_x += e.delta_x
            acc_y += e.delta_y

            self.acc_x = max(0, acc_x)
            self.acc_y = max(0, acc_y)
            e.control.update()

        self.container = ft.Container(
            width=x_unit_length * self.duration_in_beats,
            height=y_unit_length,
            bgcolor=ft.colors.GREEN,
            animate=ft.animation.Animation(0, ft.animation.AnimationCurve.LINEAR),
        )

        self.component = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            on_vertical_drag_start=on_pan_start,
            on_vertical_drag_update=on_pan_update,
            left=(x_unit_length * start_beat) + line_width / 2,
            top=(y_unit_length * (TOTAL_KEYS - note)) + line_width / 2,
            content=self.container
        )

    def update_beat(self, beats):
        self.component.width += 100
        self.component.update()

class UIGrid:
    def __init__(self, grid_num_rows, grid_num_col, x_unit_length, y_unit_length, container_size_x, container_size_y, line_width, line_color) -> None:
        
        self.container_size_x = container_size_x
        self.container_size_y = container_size_y
        

        self.grid_num_rows = grid_num_rows
        self.grid_num_col = grid_num_col
        self.x_unit_length = x_unit_length 
        self.y_unit_length = y_unit_length

        self.line_width = line_width
        self.line_color = line_color

        grid_lines = []

        # grid loop rows
        for i in range(grid_num_rows):
            grid_lines.append(h_line(x_unit_length * grid_num_col, top=y_unit_length * i, line_width=line_width, line_color=line_color))
        grid_lines.append(h_line(x_unit_length * grid_num_col, top=y_unit_length * grid_num_rows, line_width=line_width, line_color=line_color))
        
        # grid loop column
        for i in range(grid_num_col):
            grid_lines.append(v_line(y_unit_length * grid_num_rows, left=x_unit_length * i, line_width=line_width, line_color=line_color))
        grid_lines.append(v_line(y_unit_length * grid_num_rows, left=x_unit_length * grid_num_col, line_width=line_width, line_color=line_color))
        
        size_grid_x = (x_unit_length * grid_num_col)
        size_grid_y = (y_unit_length * grid_num_rows)

        self.component = ft.Container(
            content = ft.Stack(grid_lines),
            width=size_grid_x + 1,
            height=size_grid_y + 1, # +1 for bottom grid line
        )

class UIGridPage:
    def __init__(self, grid: UIGrid, notes: list[UIMidiNote]) -> None:
        self.acc_x = 0
        self.acc_y = 0 

        x_unit_length = grid.x_unit_length
        y_unit_length = grid.y_unit_length
        grid_num_col = grid.grid_num_col
        grid_num_rows = grid.grid_num_rows

        size_container_x = grid.container_size_x
        size_container_y = grid.container_size_y

        size_grid_x = (x_unit_length * grid_num_col)
        size_grid_y = (y_unit_length * grid_num_rows)

        x_nudge_space = abs(size_container_x - size_grid_x) 
        y_nudge_space = abs(size_container_y - size_grid_y) 
        def on_pan_update(e):
            acc_x = self.acc_x
            acc_y = self.acc_y
            e.control.left += e.delta_x
            e.control.top += e.delta_y

            e.control.left = min(0, e.control.left)
            e.control.top = min(0, e.control.top)

            x_wall = -1 * x_nudge_space 
            y_wall = -1 * y_nudge_space 

            # outer bound
            e.control.left = max(x_wall, e.control.left)
            e.control.top = max(y_wall, e.control.top)

            acc_x += e.delta_x
            acc_y += e.delta_y
            e.control.update()

        note_components = []
        for note in notes:
            note_components.append(note.component)

        self.component = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            on_vertical_drag_update=on_pan_update,
            left=0,
            top=0,
            content = ft.Stack(
                [
                    grid.component,
                ] + note_components
            )
        )

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 600
    page.window_width = 600
    page.title = "Piano Roll"
    # page.padding = ft.padding.all(0)

    # page.window_resizable = False


    line_width = 1
    line_color = ft.colors.BLACK
    grid_num_rows = TOTAL_KEYS
    grid_num_col = BEATS_PER_GRID
    x_unit_length = 50
    y_unit_length = 20

    container_size_x = (x_unit_length * grid_num_col) - 50 + 20
    container_size_y = (y_unit_length * grid_num_rows) - 50 + 20
    container_size_x = 400
    container_size_y = 400

    _grid = UIGrid(grid_num_rows, grid_num_col, x_unit_length, y_unit_length, container_size_x, container_size_y, line_width, line_color)


    _grid_container = ft.Container(
        width=_grid.container_size_x + 1,
        height=_grid.container_size_y + 1, # +1 for bottom grid line
    )

    _notes = [
        UIMidiNote(_grid.line_width, x_unit_length, y_unit_length, start_beat=0),
        # UIMidiNote(_grid.line_width, x_unit_length, y_unit_length,  start_beat=1).component
    ]

    _grid_page = UIGridPage(_grid, _notes)


    def increase_grid_size(e):
        # nonlocal x_unit_length
        # x_unit_length += 100
        # page.update()
        _notes[0].container.width +=  x_unit_length 
        _notes[0].container.update()
        # self.duration_in_beats = beats
        # self.component.width = self.x_unit_length * self.duration_in_beats
        # self.component.update()
        # pass


    def decrease_grid_size(e):
        print('-')
        pass

    page.add(
        ft.Column(
            [
                ft.Stack( 
                    [
                        _grid_container, 
                        _grid_page.component,
                        
                        
                    ],
                ),
                ft.Row([
                    ft.TextButton("+", on_click=increase_grid_size,),
                    ft.TextButton("-", on_click=decrease_grid_size,),
                ])
                
            ]
        )
        
    )

ft.app(target=main)