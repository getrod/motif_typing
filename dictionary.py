import flet as ft
from midiaudio import play_motif
import random
import json
from moteaf import motif_2_midi, motif_parse


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 400
    page.window_width = 400
    page.title = "Keyboard Dictionary"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    bpm = 120

    # get words
    json_f = open('dictionary.json')
    dictionary = json.loads(json_f.read())
    json_f.close()

    def dict_entry(word: str, motif: str, bpm: int = bpm):
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

    # create dictionary entries
    entries = []
    for entry in dictionary[1:]:
        entries.append(dict_entry(entry[0], entry[1], int(entry[2])))

    page.add(
        ft.Column(
            entries + [
                # dict_entry(dictionary[0], dictionary[1]),
                # dict_entry('yup', []),
                bpm_edit
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)