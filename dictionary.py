import flet as ft
# from multiprocessing import Process
from midiaudio import play_motif
import random



dictionary = {
    'the': """C chrom< [0]-(1/4),[1]-(1/4),[2]-(1/4),[3]-(1/4),[4]-(1/4),[5]-(1/4),[6]-(1/4),[7]-(1/4),[8]-(1/4),[9]-(1/4),[10]-(1/4),[11]-(1/4), [12]-(3/4) :: 5>""",
    'i':  """A maj< [0]-(1/4),[1]-(1/4),[2]-(1/4),[3]-(1/4),[4]-(1/4),[5]-(1/4),[6]-(1/4) :: 5>""",
    'hi': """Bb m9< [0]-(1/4),[1]-(1/4),[2]-(1/4),[3]-(1/4),[4]-(1/4),[5]-(1/4),[6]-(1/4) :: 5>"""
}

# def run_as_process(func, args: tuple):
#     process = Process(target=func, args=args)
#     process.start()
#     return process 

# audio_process: Process = None

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 400
    page.window_width = 400
    page.title = "Keyboard Dictionary"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    bpm = 120

    def dict_entry(word: str, motif: str):
        word = ft.Text(value=word, text_align=ft.TextAlign.CENTER, width=100)

        def play(e):
            play_motif(motif, bpm)
            print(bpm)

        def play_random(e):
            play_motif(motif, bpm, transpose=random.randint(-12, 12))
            print(bpm)

        interval = ft.Container(
                    content=ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.PLAY_ARROW,
                                icon_color='black',
                                icon_size=20,
                                tooltip="Play interval",
                                on_click=play
                            ),
                            ft.IconButton(
                                icon=ft.icons.SHUFFLE,
                                icon_color='black',
                                icon_size=20,
                                tooltip="Random key",
                                on_click=play_random
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

    
    def on_change(e):
        nonlocal bpm
        if e.control.value == '': bpm = 0
        else: bpm = int(e.control.value)
        
    text_bpm = ft.TextField(value=f'{bpm}', text_align='center', width=100, on_change=on_change)

    bpm_edit = ft.Row(
            [
                ft.Text(value='bpm', text_align=ft.TextAlign.CENTER, width=100),
                text_bpm,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    page.add(
        ft.Column(
            [
                dict_entry('the', dictionary['the']),
                # dict_entry('yup', []),
                bpm_edit

            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)