import flet as ft

def main(page: ft.Page):
    page.title = "Grow"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def update_container(c: ft.Container):
        pass

    c = ft.Container(
        width=200,
        height=200,
        bgcolor=ft.colors.GREEN,
        animate=ft.animation.Animation(0, ft.animation.AnimationCurve.LINEAR),
    )

    def animate_container(e):
        # c.width = 100 if c.width == 200 else 200
        # c.height = 100 if c.height == 200 else 200
        # c.bgcolor = "blue" if c.bgcolor == "red" else "red"
        c.width += 100
        c.update()

    def minus_click(e):
        c.width += 30
        c.update()
        txt_number.value = str(int(txt_number.value) - 1)
        # page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # page.add(
    #     ft.Column(
    #         [
    #             c,
    #             ft.Row(
    #                 [
    #                     ft.IconButton(ft.icons.REMOVE, on_click=animate_container),
    #                     txt_number,
    #                     ft.IconButton(ft.icons.ADD, on_click=plus_click),
    #                 ],
    #                 alignment=ft.MainAxisAlignment.CENTER,
    #             ),
    #         ]
    #     )
        
    # )

    page.add(ft.Stack([
        ft.Container(
            width=500,
            height=500,
            bgcolor=ft.colors.WHITE
        ),
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    on_vertical_drag_update=plus_click,
                    left=9,
                    top=0,
                    content=c
                ),
                         ft.IconButton(ft.icons.REMOVE, on_click=animate_container)])
        
    )

ft.app(target=main)