__author__ = 'daniel'
from math import sqrt


class Rmsd():
    def __init__(self):
        self.index_list = []

    def cal_rmsd(self, vectores, txtval, listadosd):
        self.index_list_list = []
        #scn_list_list = vectores
        scn_list_list = []
        for elem in vectores:
            scn_list_list.append(elem)
        list_of_list = listadosd
        valrmsd = txtval
        while len(scn_list_list) > 0:
            lista_a = scn_list_list[0]
            rng_lista = len(lista_a)
            self.index_list.append(list_of_list[0][0])
            cont = 0
            del scn_list_list[0]
            del list_of_list[0]
            while cont < len(scn_list_list):
                lista_b = scn_list_list[cont]
                sumatoria = 0.0
                for el in range(0, rng_lista):
                    sumatoria += (float(lista_a[el]) - float(lista_b[el])) ** 2.0
                rmsd = sqrt(sumatoria / rng_lista)
                if rmsd <= float(valrmsd):
                    # linea con hardcode
                    self.index_list.append(list_of_list[cont][0])
                    del scn_list_list[cont]
                    del list_of_list[cont]
                    cont -= 1
                cont += 1
            self.index_list_list.append(self.index_list[:])
            self.index_list = []
        #self.fbe_min = min(self.fbe_listL)
        #self.fbe_max = max(self.fbe_listL)
        return self.index_list_list
