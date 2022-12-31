import flet as ft
import math

LINE_WITH = 1
LINE_COLOR = ft.colors.BLACK

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
    def __init__(self, line_width, x_unit_length, y_unit_length, duration = None, start_x = None, start_y = None) -> None:
        self.acc_x = 0
        self.acc_y = 0
        self.midline_offset_x = line_width / 2
        self.midline_offset_y = line_width / 2


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

        self.component = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            on_vertical_drag_update=on_pan_update,
            left=line_width / 2,
            top=line_width / 2,
            content=ft.Container(
                width=x_unit_length * 3,
                height=y_unit_length,
                bgcolor=ft.colors.GREEN,
            ),
        )

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

        self.component = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            on_vertical_drag_update=on_pan_update,
            left=0,
            top=0,
            content = ft.Stack(
                [
                    grid.component,
                ] + notes
            )
        )

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 400
    page.window_width = 400
    page.title = "Grid w. Note"
    # page.padding = ft.padding.all(0)

    # page.scroll = ft.ScrollMode.AUTO
    # page.window_resizable = False

    

    
    # grid_lines = []

    

    # # grid loop rows
    # for i in range(grid_num_rows):
    #     grid_lines.append(h_line(x_unit_length * grid_num_col, top=y_unit_length * i))
    # grid_lines.append(h_line(x_unit_length * grid_num_col, top=y_unit_length * grid_num_rows))
    
    # # grid loop column
    # for i in range(grid_num_col):
    #     grid_lines.append(v_line(y_unit_length * grid_num_rows, left=x_unit_length * i))
    # grid_lines.append(v_line(y_unit_length * grid_num_rows, left=x_unit_length * grid_num_col))
    




    # acc_x = 0
    # acc_y = 0 

    # size_container_x = (x_unit_length * grid_num_col) - 50 + 20
    # size_container_y = (y_unit_length * grid_num_rows) - 50 + 20

    # size_grid_x = (x_unit_length * grid_num_col)
    # size_grid_y = (y_unit_length * grid_num_rows)

    # x_nudge_space = abs(size_container_x - size_grid_x) 
    # y_nudge_space = abs(size_container_y - size_grid_y) 
    # def on_pan_update(e):
    #     nonlocal acc_x
    #     nonlocal acc_y
    #     e.control.left += e.delta_x
    #     e.control.top += e.delta_y

    #     e.control.left = min(0, e.control.left)
    #     e.control.top = min(0, e.control.top)

    #     x_wall = -1 * x_nudge_space 
    #     y_wall = -1 * y_nudge_space 

    #     # outer bound
    #     e.control.left = max(x_wall, e.control.left)
    #     e.control.top = max(y_wall, e.control.top)

    #     acc_x += e.delta_x
    #     acc_y += e.delta_y
    #     e.control.update()

    # grid = ft.Container(
    #     content = ft.Stack(grid_lines),
    #     width=size_grid_x + 1,
    #     height=size_grid_y + 1, # +1 for bottom grid line
    # )

    line_width = 1
    line_color = ft.colors.BLACK
    grid_num_rows = 30
    grid_num_col = 10
    x_unit_length = 50
    y_unit_length = 20

    container_size_x = (x_unit_length * grid_num_col) - 50 + 20
    container_size_y = (y_unit_length * grid_num_rows) - 50 + 20
    container_size_x = 400
    container_size_y = 400
    _grid = UIGrid(grid_num_rows, grid_num_col, x_unit_length, y_unit_length, container_size_x, container_size_y, line_width, line_color)

    # grid_container = ft.Container(
    #     width=size_container_x + 1,
    #     height=size_container_y + 1, # +1 for bottom grid line
    # )

    _grid_container = ft.Container(
        width=_grid.container_size_x + 1,
        height=_grid.container_size_y + 1, # +1 for bottom grid line
    )

    # grid_page = ft.GestureDetector(
    #     mouse_cursor=ft.MouseCursor.MOVE,
    #     on_vertical_drag_update=on_pan_update,
    #     left=0,
    #     top=0,
    #     content = ft.Stack(
    #         [
    #             _grid.component,
    #             UIMidiNote(line_width, x_unit_length, y_unit_length).component
    #         ]
    #     )
    # )

    _notes = [
        UIMidiNote(_grid.line_width, x_unit_length, y_unit_length).component,
        UIMidiNote(_grid.line_width, x_unit_length, y_unit_length).component
    ]

    _grid_page = UIGridPage(_grid, _notes)
    


    page.add(
        ft.Stack( 
            [
                _grid_container, 
                _grid_page.component
                
            ],
            # expand=True
        )
    )

ft.app(target=main)