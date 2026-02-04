import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self._current_role = None
        self._current_artista = None

    def popola_dd_ruolo(self):

        self._view.dd_ruolo.options.clear()

        ruoli = self._model.get_ruoli()

        if ruoli:
            for r in ruoli:
                self._view.dd_ruolo.options.append(ft.dropdown.Option(str(r)))
        else:
            self._view.show_alert("Errore nel caricamento dei ruoli.")

        self._view.update()

    def on_ruolo_change(self, e):

        selected_option = e.control.value
        if not selected_option:
            self._current_role = None
            self._view.show_alert("Errore nella selezione del ruolo.")
            return

        self._view.btn_crea_grafo.disabled = False

        self._current_role = selected_option

        self._view.update()

    def handle_crea_grafo(self, e):

        self._view.list_risultato.controls.clear()

        self._view.btn_classifica.disabled = False
        self._view.dd_iniziale.disabled = False
        self._view.btn_cerca_percorso.disabled = False

        self._model.build_graph(self._current_role)

        num_nodes, num_archi = self._model.get_num_nodes_num_edges()

        self._view.list_risultato.controls.append(ft.Text(f'Nodi: {num_nodes} | Archi: {num_archi}'))

        self.popola_dd_iniziale()

        self._view.update()

    def handle_classifica(self, e):

        self._view.list_risultato.controls.clear()

        diz = self._model.classifica()

        self._view.list_risultato.controls.append(ft.Text('Artisti in ordine decrescente di influenza:'))

        for item in diz.keys():
            self._view.list_risultato.controls.append(ft.Text(f'{item.name} -> delta = {diz[item]:.2f}'))

        self._view.update()

    def popola_dd_iniziale(self):

        self._view.dd_iniziale.options.clear()

        nodes = self._model.get_nodes()

        if nodes:
            for n in nodes:
                self._view.dd_iniziale.options.append(ft.dropdown.Option(text=n.name, data=n))
        else:
            self._view.show_alert("Errore nel caricamento dei ruoli.")

        self._view.update()


    def on_artista_change(self, e):

        self._view.list_risultato.controls.clear()

        selected_option = e.control.value
        if not selected_option:
            self._current_artista = None
            self._view.show_alert("Errore nella selezione dell'artista.")
            return

        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break

        self._current_artista = found

        self._view.update()


    def handle_cerca_percorso(self, e):

        self._view.list_risultato.controls.clear()

        num_nodes, num_archi = self._model.get_num_nodes_num_edges()

        try:
            lunghezza = int(self._view.input_L.value)
        except ValueError:
            self._view.show_alert('Inserire un intero!')
            return

        if lunghezza < 3 or lunghezza > num_nodes:
            self._view.show_alert("L'intero deve essere nell'intervallo [3, num_nodes]")
            return

        self._view.list_risultato.controls.clear()

        path, score = self._model.percorso(self._current_artista, lunghezza)

        if not path or not score:
            self._view.show_alert('Ricorsione errata!')
            return

        self._view.list_risultato.controls.append(ft.Text('Percorso ottimo:'))

        for item in path:
            self._view.list_risultato.controls.append(ft.Text(f'{item.name}'))

        self._view.list_risultato.controls.append(ft.Text(f'Peso totale: {score}'))

        self._view.update()