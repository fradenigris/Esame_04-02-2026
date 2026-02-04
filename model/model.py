import networkx as nx
from database.dao import DAO
import copy

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self._nodes = None

        self._best_path = None
        self._best_score = None
        self._lunghezza_target = None

    @staticmethod
    def get_ruoli():
        return DAO.get_ruoli()

    def build_graph(self, role: str):

        self.G.clear()

        self._nodes = DAO.get_artisti(role)
        self.G.add_nodes_from(self._nodes)

        diz = {}

        for a in self._nodes:
            indice = DAO.get_indice_per_specific_artist(a.artist_id)
            diz[a] = indice

        for a1 in self._nodes:
            for a2 in self._nodes:
                if a1.artist_id != a2.artist_id:
                    if diz[a1] > 0 and diz[a2] > 0:
                        if diz[a1] > diz[a2]:
                            self.G.add_edge(a2, a1, weight = abs(diz[a1] - diz[a2]))
                        elif diz[a1] < diz[a2]:
                            self.G.add_edge(a1, a2, weight = abs(diz[a1] - diz[a2]))

    def get_num_nodes_num_edges(self):
        num_nodes = len(self._nodes)
        num_edges = len(self.G.edges())

        return num_nodes, num_edges


    def classifica(self):

        diz = {}
        for a in self._nodes:
            archi_entranti = self.G.in_edges(a, data=True)
            entranti = 0
            for u, v, dati in archi_entranti:
                entranti += dati['weight']

            archi_uscenti = self.G.out_edges(a, data=True)
            uscenti = 0
            for u, v, dati in archi_uscenti:
                uscenti += dati['weight']

            diz[a] = uscenti - entranti

            nuovo_diz = dict(sorted(diz.items(), key=lambda x: x[1], reverse=True))

            return nuovo_diz

    def percorso(self, artista_iniz, lunghezza):

        self._best_path = []
        self._best_score = 0
        self._lunghezza_target = lunghezza

        parziale = [artista_iniz]

        self._ricorsione(parziale)

        return self._best_path, self._best_score

    def _ricorsione(self, parziale):

        last_node = parziale[-1]

        if len(parziale) == self._lunghezza_target:
            score_attuale = self.get_score(parziale)

            if score_attuale > self._best_score:
                self._best_score = score_attuale
                self._best_path = copy.deepcopy(parziale)

            return

        successors = list(self.G.successors(last_node))

        ammissibili = []
        for n in successors:
            if n not in parziale:
                ammissibili.append(n)

        for n in ammissibili:
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()

    def get_score(self, parziale):

        score = 0
        for i in range(0, len(parziale)-1):
            u = parziale[i]
            v = parziale[i+1]
            weight = self.G[u][v]['weight']
            score += weight

        return score

    def get_nodes(self):
        return self._nodes