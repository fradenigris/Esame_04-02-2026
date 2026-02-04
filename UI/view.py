from UI.alert import AlertManager
import flet as ft

class View:
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Programmazione Avanzata - Secondo Appello - Artisti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK

        self._controller = None

        self._alert = AlertManager(page)

        self.txt_title = None
        self.dd_ruolo = None
        self.dd_iniziale = None
        self.input_L = None
        self.btn_crea_grafo = None
        self.btn_classifica = None
        self.btn_cerca_percorso = None
        self.list_risultato = None
        self.toggle_tema = None

    def set_controller(self, controller):
        self._controller = controller

    def popola_dropdown_ruolo(self, ruoli):
        self.dd_ruolo.options = [ft.dropdown.Option(text=r) for r in ruoli]
        self.dd_ruolo.update()

    def show_alert(self, message):
        self._alert.show_alert(message)

    def update(self):
        self._page.update()

    def load_interface(self):
        self.txt_title = ft.Text("Gestione Artisti", size=30, weight=ft.FontWeight.BOLD)

        self.dd_ruolo = ft.Dropdown(label="Seleziona ruolo artista", width=250, on_change=self._controller.on_ruolo_change)
        self._controller.popola_dd_ruolo()

        self.dd_iniziale = ft.Dropdown(label="Artista Iniziale", width=250, disabled=True, on_change=self._controller.on_artista_change)

        self.input_L = ft.TextField(label="Lunghezza cammino", width=200, value="3")

        self.btn_crea_grafo = ft.ElevatedButton("Crea Grafo", on_click=self._controller.handle_crea_grafo, disabled=True)
        self.btn_classifica = ft.ElevatedButton("Classifica", disabled=True, on_click=self._controller.handle_classifica)
        self.btn_cerca_percorso = ft.ElevatedButton("Cerca percorso", disabled=True, on_click=self._controller.handle_cerca_percorso)

        self.list_risultato = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        self.toggle_tema = ft.Switch(label="Tema scuro", value=True, on_change=self._cambia_tema)

        row1 = ft.Row([self.dd_ruolo, self.btn_crea_grafo, self.btn_classifica], alignment=ft.MainAxisAlignment.CENTER)
        row2 = ft.Row([self.dd_iniziale, self.btn_cerca_percorso], alignment=ft.MainAxisAlignment.CENTER)
        row3 = ft.Row([self.input_L], alignment=ft.MainAxisAlignment.CENTER)

        self._page.add(
            self.toggle_tema,
            self.txt_title,
            row1,
            row2,
            row3,
            self.list_risultato
        )

        self._page.scroll = "adaptive"
        self._page.update()

    def _cambia_tema(self, e):
        self._page.theme_mode = ft.ThemeMode.DARK if self.toggle_tema.value else ft.ThemeMode.LIGHT
        self.toggle_tema.label = "Tema scuro" if self.toggle_tema.value else "Tema chiaro"
        self.update()
