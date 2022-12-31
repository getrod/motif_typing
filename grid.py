import flet as ft
import math
import numpy

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 400
    page.window_width = 400
    page.title = "Grid"
    page.padding = ft.padding.all(0)

    

    line_width = 5
    line_color = ft.colors.AMBER
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
    

    grid_container = ft.Container()



    interval = 50
    acc_x = 0
    acc_y = 0
    def on_pan_update(e: ft.DragUpdateEvent):
        nonlocal acc_x
        nonlocal acc_y

        e.control.left = max(0, math.floor(acc_x / x_unit_length)  * x_unit_length)
        e.control.top = max(0, math.floor(acc_y / y_unit_length) * y_unit_length)

        # if abs(acc_x) >= interval:
        #     # e.control.left = max(0,  e.control.left + numpy.sign(acc_x) * interval)
        #     e.control.left = max(0,  e.control.left + e.delta_x)
        #     acc_x = 0
        # if abs(acc_y) >= interval:
        #     e.control.top = max(0,  e.control.top + e.delta_y)
        #     acc_y = 0
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
        left=0,
        top=0,
        content=ft.Container(
            width=x_unit_length,
            height=y_unit_length,
            bgcolor=ft.colors.CYAN,
        ),
    )


    page.add(
        ft.Stack(
            [
                grid_container,
                gd,
                # h_line(50),
                # v_line(50),
                
            ] + grid_lines, 
            expand=True
        )
    )

ft.app(target=main)