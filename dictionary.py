import flet as ft

dictionary = {
    'the': [0, 2, 4, 7, 9, 12],
    'i': [0, -1, -3, -5, -8],
    'hi': [0, 0, 7, 7, 9, 9, 7]
}

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 400
    page.window_width = 400
    page.title = "Keyboard Dictionary"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def dict_entry(word: str, interval: list[int]):
        word = ft.Text(value=word, text_align=ft.TextAlign.CENTER, width=100)
        interval = ft.Container(
                    content=ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.PLAY_ARROW,
                                icon_color='black',
                                icon_size=20,
                                tooltip="Play interval",
                            ),
                            ft.IconButton(
                                icon=ft.icons.SHUFFLE,
                                icon_color='black',
                                icon_size=20,
                                tooltip="Random key",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.AMBER,
                    width=125,
                    height=60,
                    border_radius=10,
                )

        _dict_entry = ft.Row(
            [
                word,
                interval
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        return _dict_entry




    page.add(
        ft.Column(
            [
                dict_entry('yo', []),
                dict_entry('yup', []),

            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)