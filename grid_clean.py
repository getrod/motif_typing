import flet as ft
import math

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 400
    page.window_width = 400
    page.title = "Grid Cleaner"
    # page.padding = ft.padding.all(0)

    # page.scroll = ft.ScrollMode.AUTO
    # page.window_resizable = False

    

    line_width = 1
    line_color = ft.colors.BLACK
    def h_line(length, top = 0, left = 0, line_width = line_width, line_color = line_color):
        return ft.Container(
            width=length,
            height=line_width,
            bgcolor=line_color,
            top=top,
            left=left
        )

    def v_line(length, top = 0, left = 0, line_width = line_width, line_color = line_color):
        return ft.Container(
            height=length,
            width=line_width,
            bgcolor=line_color,
            top=top,
            left=left
        )

    

    grid_num_rows = 10
    grid_num_col = 10
    grid_lines = [
        # h_line(50, top=0),
        # h_line(50, top=interval * 1),
        # h_line(50, top=interval * 2),

        # v_line(50, left=0),
        # v_line(50, left=interval * 1),
        # v_line(50, left=interval * 2),
    ]

    x_unit_length = 50
    y_unit_length = 20

    # grid loop rows
    for i in range(grid_num_rows):
        grid_lines.append(h_line(x_unit_length * grid_num_col, top=y_unit_length * i))
    grid_lines.append(h_line(x_unit_length * grid_num_col, top=y_unit_length * grid_num_rows))
    
    # grid loop column
    for i in range(grid_num_col):
        grid_lines.append(v_line(y_unit_length * grid_num_rows, left=x_unit_length * i))
    grid_lines.append(v_line(y_unit_length * grid_num_rows, left=x_unit_length * grid_num_col))
    

    offset_x = line_width / 2
    offset_y = line_width / 2
    acc_x = 0
    acc_y = 0
    def on_pan_update(e: ft.DragUpdateEvent):
        nonlocal acc_x
        nonlocal acc_y
        
        e.control.left = max(0, (math.floor(acc_x / x_unit_length)  * x_unit_length) + offset_x)
        e.control.top = max(0, (math.floor(acc_y / y_unit_length) * y_unit_length) + offset_y)

        acc_x += e.delta_x
        acc_y += e.delta_y

        acc_x = max(0, acc_x)
        acc_y = max(0, acc_y)
        print(f'x: {e.control.left}, y: {e.control.top}')
        print(f'acc_x: {acc_x}, acc_y: {acc_y}')
        e.control.update()

    gd = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        on_vertical_drag_update=on_pan_update,
        left=offset_x,
        top=offset_y,
        content=ft.Container(
            width=x_unit_length * 2,
            height=y_unit_length,
            bgcolor=ft.colors.CYAN,
        ),
    )

    grid_container_width = (x_unit_length * grid_num_col) + 1
    grid_container_height = (y_unit_length * grid_num_rows) + 1

    widget_lines = ft.Container(
        content = ft.Stack(grid_lines),
        width=(x_unit_length * grid_num_col) + 1,
        height=(y_unit_length * grid_num_rows) + 1, # +1 for bottom grid line
    )

    def on_scroll_update(e: ft.ScrollEvent):
        e.control.top = e.control.top+ e.scroll_delta_y
        e.control.update()
        pass

    acc_2_x = 0
    acc_2_y = 0 

    size_container_x = (x_unit_length * grid_num_col) - 50 + 20
    size_container_y = (y_unit_length * grid_num_rows) - 50 + 20

    size_grid_x = (x_unit_length * grid_num_col)
    size_grid_y = (y_unit_length * grid_num_rows)

    x_nudge_space = abs(size_container_x - size_grid_x) 
    y_nudge_space = abs(size_container_y - size_grid_y) 
    def on_pan_2(e):
        nonlocal acc_2_x
        nonlocal acc_2_y
        e.control.left += e.delta_x
        e.control.top += e.delta_y

        e.control.left = min(0, e.control.left)
        e.control.top = min(0, e.control.top)

        
        
        x_wall = -1 * x_nudge_space 
        y_wall = -1 * y_nudge_space 
        print(f'x_wall: {x_wall}')
        # outer bound
        e.control.left = max(x_wall, e.control.left)
        e.control.top = max(y_wall, e.control.top)
        print(e.control.left)
        acc_2_x += e.delta_x
        acc_2_y += e.delta_y
        e.control.update()
        pass

    gd_grid = ft.GestureDetector(
        on_scroll=on_scroll_update,
        # mouse_cursor=ft.MouseCursor.MOVE,
        # on_vertical_drag_update=on_pan_2,
        left=0,
        top=0,
        content = ft.Stack(grid_lines)
    )

    grid_container = ft.Container(
        width=size_container_x + 1,
        height=size_container_y + 1, # +1 for bottom grid line
    )

    grid_page = ft.GestureDetector(
        # on_scroll=on_scroll_update,
        mouse_cursor=ft.MouseCursor.MOVE,
        on_vertical_drag_update=on_pan_2,
        left=0,
        top=0,
        content = ft.Stack(
            [
                gd_grid,
                gd
            ]
        )
    )
    


    page.add(
        ft.Stack( 
            [
                grid_container, 
                # gd_grid,
                # # widget_lines,
                # gd,

                grid_page
                
            ],
            # expand=True
        )
    )

ft.app(target=main)