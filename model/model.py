import copy

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self._nodes = []
        self._edges = []
        self.G = nx.Graph()
        self._idMap = {}

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()

        all_rifugi = DAO.get_rifugi()

        for r in all_rifugi:
            self._idMap[r.id] = r

        archi = DAO.read_connessioni(year)

        for arco in archi:
            id1 = arco['id_rifugio1']
            id2 = arco['id_rifugio2']
            distanza=float(arco['distanza'])
            difficolta=arco['difficolta']
            difficolta_mom=0
            if difficolta=='facile':
                difficolta_mom=1
            elif difficolta=='media':
                difficolta_mom=1.5
            elif difficolta=='difficile':
                difficolta_mom=2

            if id1 in self._idMap and id2 in self._idMap:
                nodo_obj_1 = self._idMap[id1]
                nodo_obj_2 = self._idMap[id2]
                peso=difficolta_mom*distanza

                self.G.add_edge(nodo_obj_1, nodo_obj_2, weight=peso)

        self._nodes = list(self.G.nodes())
        self._edges= list(self.G.edges())
        return self.G

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        if len(self.G.edges) == 0:
            return 0, 0

        pesi = [d['weight'] for u, v, d in self.G.edges(data=True)]

        return min(pesi), max(pesi)

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori = 0
        maggiori = 0

        for u, v, d in self.G.edges(data=True):
            peso = d['weight']
            if peso < soglia:
                minori += 1
            elif peso > soglia:
                maggiori += 1

        return minori, maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def get_cammino_minimo_dijkstra(self, soglia):


        archi_validi = [(u, v) for u, v, d in self.G.edges(data=True) if d['weight'] > soglia]
        G_filtrato = self.G.edge_subgraph(archi_validi)

        best_percorso = []
        min_total_peso = 1000000


        for partenza, (distanze, cammini) in nx.all_pairs_dijkstra(G_filtrato, weight='weight'):

            # partenza è il nodo di partenza
            # distanze è un dizionario {nodo_destinazione: peso_totale}
            # cammini è un dizionario {nodo_destinazione: [lista_nodi_percorso]}

            for target, dist in distanze.items():

                percorso = cammini[target]


                if len(percorso) >= 3:

                    if dist < min_total_peso:
                        min_total_peso = dist
                        best_percorso = percorso

        return best_percorso

    def get_cammino_minimo_ricorsivo(self, soglia):
        self.best_percorso = []
        self.min_total_peso = 1000000

        for nodo in self.G.nodes():
            self.ricorsione([nodo], 0, soglia)

        return self.best_percorso


    def ricorsione(self, parziale, peso_corrente, soglia):

        if peso_corrente >= self.min_total_peso:
            return

        if len(parziale) >= 3:
            self.min_total_peso = peso_corrente
            self.best_percorso = parziale.copy()
            return


        ultimo = parziale[-1]


        for vicino in self.G.neighbors(ultimo):
            if vicino not in parziale:
                peso = self.G[ultimo][vicino]['weight']


                if peso > soglia:
                    parziale.append(vicino)
                    self.ricorsione(parziale, peso_corrente + peso, soglia)
                    parziale.pop()


    def trova_cammino_libero(self,soglia):
        a=self.get_cammino_minimo_dijkstra(soglia)
        b=self.get_cammino_minimo_ricorsivo(soglia)

        return b