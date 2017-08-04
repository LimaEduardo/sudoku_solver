import sys
import math

class vertice:
    def __init__(self,indice,conteudo):
        self.indice = indice
        self.conteudo = conteudo
        self.vizinhos = []
        self.grauSaturacao = 0
        self.grau = 0

    def calculaSaturacao(self):
        for vizinho in self.vizinhos:
            if vizinho.getConteudo() != "N":
                self.grauSaturacao += 1

    def getConteudo(self):
        return self.conteudo

    def setConteudo(self,conteudo):
        self.conteudo = conteudo

    def getGraus(self):
        print("Grau:",self.grau)
        print("Grau saturação:",self.grauSaturacao)

    def getSaturacao(self):
        return self.grauSaturacao

    def getIndice(self):
        return self.indice

    def getVertice(self):
        print (self.indice,self.conteudo)

    def getVizinhos(self):
        for vizinho in self.vizinhos:
            print(vizinho.conteudo)
        return self.vizinhos

    def setVizinhos(self,vertice):
        self.vizinhos.append(vertice)
        self.grau += 1

    def menorCorPossivel(self,ordem):
        possibilidades = list(range(1,ordem+1))
        conjPossibilidades = set(possibilidades)
        print (conjPossibilidades)
        jaExistente = set()
        for vizinho in self.vizinhos:
            if vizinho.getConteudo() == "N":
                continue
            jaExistente.add(int(vizinho.getConteudo()))
        print("conjPoss",conjPossibilidades)
        print("jaExis",jaExistente)
        conjPossibilidades = conjPossibilidades - jaExistente
        print (self.getIndice())
        print ("conjpossFin",conjPossibilidades)
        return min(conjPossibilidades)



class grafo:
    def __init__(self,tabela):
        self.quantidadeVertices = len(tabela)
        self.ordem = int(math.sqrt(self.quantidadeVertices))
        self.dimensaoBloco = int(math.sqrt(self.ordem))
        self.vertices = self.constroiVertices(tabela)
        self.blocos = self.formaBloco()
        self.mergeVizinhos()
        self.dsatur()
        self.debug()
        #self.getBlocos()
        #self.getVertices()

    def constroiVertices(self,tabela):
        vertices = {}
        for i in range(self.quantidadeVertices):
            vertices[i] = vertice(i,tabela[i])
        return vertices
    
    def formaBloco(self):
        lista_blocos = []
        for primeiroBlocoVertical in range (0,self.quantidadeVertices,self.dimensaoBloco*self.ordem):
            for primeiroBlocoHorizontal in range(primeiroBlocoVertical, primeiroBlocoVertical+self.ordem, self.dimensaoBloco):
                bloco = set()
                for vertical in range(primeiroBlocoHorizontal,primeiroBlocoHorizontal + self.ordem*self.dimensaoBloco-1,self.ordem):
                    for horizontal in range(vertical,vertical+self.dimensaoBloco):
                        bloco.add(horizontal)
                lista_blocos.append(bloco)
        return lista_blocos

    def vizinhosDaLinha(self,indice):
        mod = indice % self.ordem
        dif = self.ordem - mod
        lim = indice + dif

        vizinhos = set()
        for i in range(indice-mod,lim):
            vizinhos.add(i)
        return vizinhos

    def vizinhosDaColuna(self,indice):
        vizinhos = set()
        for subindo in range(indice,0,-self.ordem):
            vizinhos.add(subindo)
        for descendo in range(indice,self.quantidadeVertices,self.ordem):
            vizinhos.add(descendo)
        return vizinhos

    def vizinhosBloco(self,indice):
        for bloco in self.blocos:
            if indice in bloco:
                return bloco

    def mergeVizinhos(self):
        for vertice in self.vertices:
            vinLin = self.vizinhosDaLinha(vertice)
            vinCol = self.vizinhosDaColuna(vertice)
            vinBloco = self.vizinhosBloco(vertice)
            vizinhos = vinLin | vinCol | vinBloco
            self.atribuiVizinhos(vertice,vizinhos)

    def atribuiVizinhos(self,vertice,vizinhos):
        for vizinho in vizinhos:
            if (vertice != vizinho):
                self.vertices[vertice].setVizinhos(self.vertices[vizinho])
        self.vertices[vertice].calculaSaturacao()

    def maiorSaturacao(self):
        maiorSaturacao = 0
        indiceMaior = 0
        for vertice in self.vertices:
            if self.vertices[vertice].getSaturacao() > maiorSaturacao and self.vertices[vertice].getConteudo() == "N":
                maiorSaturacao = self.vertices[vertice].getSaturacao()
                indiceMaior = vertice
        return indiceMaior  

    def todosColoridos(self):
        for vertice in self.vertices:
            if self.vertices[vertice].getConteudo() == "N":
                return False
        return True



    def dsatur(self):
        todosColoridos = False
        while not todosColoridos:
            maiorSaturacao = self.maiorSaturacao()
            self.vertices[maiorSaturacao].setConteudo(self.vertices[maiorSaturacao].menorCorPossivel(self.ordem))
            todosColoridos = self.todosColoridos()



    def debug(self):
        
        

        for chave in self.vertices:
            print("---")
            print("conteudo:",self.vertices[chave].getConteudo())
            print("---")

    def getBlocos(self):
        print (self.blocos)

    def getVertices(self):
        for chave in self.vertices:
            self.vertices[chave].getVertice()





    


        





        


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
    

            





