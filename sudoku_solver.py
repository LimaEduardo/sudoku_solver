import sys
import math

class vertice:
    def __init__(self,indice,conteudo):
        self.indice = indice
        self.conteudo = conteudo
        self.vizinhos = []
        self.grauSaturacao = 0
        self.grau = 0

    def getConteudo(self):
        return self.conteudo

    def getIndice(self):
        return self.indice

    def getVertice(self):
        print (self.indice,self.conteudo)

    def getVizinhos(self):
        return self.vizinhos

    def setVizinhos(self,vertice):
        self.vizinhos.append(vertice)


class grafo:
    def __init__(self,tabela):
        self.vertices = {}
        self.quantidadeVertices = len(tabela)
        self.ordem = int(math.sqrt(self.quantidadeVertices))
        self.dimensaoBloco = int(math.sqrt(self.ordem))
        for i in range(self.quantidadeVertices):
            self.vertices[i] = vertice(i,tabela[i])

        #for chave in self.vertices:
         #   self.vertices[chave].getVertice()

        for linha in range(0,self.quantidadeVertices,self.ordem):
            limiteLinha = linha + (self.ordem)
            for i in range(linha,limiteLinha):
                #Acha todos os vizinhos horizontalmente
                for j in range(i+1,limiteLinha):
                    self.vertices[i].setVizinhos(self.vertices[j])
                    self.vertices[j].setVizinhos(self.vertices[i])
                #Acha todos os vizinhos verticalmente
                for k in range(i+self.ordem, self.quantidadeVertices, self.ordem):
                    self.vertices[i].setVizinhos(self.vertices[k])
                    self.vertices[k].setVizinhos(self.vertices[i])
                #Acha os vizinhos do bloco
        for i in range (0,self.quantidadeVertices,self.dimensaoBloco*self.ordem):
            for j in range(i, i+self.ordem, self.dimensaoBloco):
                inicioBloco = j+self.ordem+1
                for k in range(inicioBloco, inicioBloco + (self.ordem * (self.dimensaoBloco -2)) + 1,self.ordem):
                    for l in range(k, k + self.dimensaoBloco-1):
                        print (l)
                print("---")
            
            #lista = self.vertices[0].getVizinhos()
             #   for vizinho in lista:
              #  print(vizinho.getIndice())
    
                    


        





        


if __name__ == "__main__":
    nome_arquivo = ""
    if len(sys.argv) == 2:
        nome_arquivo = sys.argv[1]
    else:
        print("Número inválido de argumentos")
    arquivo = open(nome_arquivo,"r")
    tabela = ""
    for linha in arquivo:
        tabela = tabela + ((linha.replace("\n","").replace(".","N")))
    tabela = list(tabela)
    grafo(tabela)
    

            





