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

    def incrimentaSaturacao(self):
        self.grauSaturacao += 1

    def decrementaSaturacao(self):
        self.grauSaturacao += 1

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

    def coresPossiveis(self,ordem):
        possibilidades = list(range(1,ordem+1))
        conjPossibilidades = set(possibilidades)
        jaExistente = set()
        for vizinho in self.vizinhos:
            if vizinho.getConteudo() == "N":
                continue
            jaExistente.add(int(vizinho.getConteudo()))
        conjPossibilidades = conjPossibilidades - jaExistente
        #print("conj",conjPossibilidades)
        #print("len",len(conjPossibilidades))
        #print("indice",self.indice)
        if (len(conjPossibilidades) == 0):
            return -1
        #print("retorno")
        return list(conjPossibilidades)

    def incrimentaSaturacaoVizinhos(self):
        for vizinho in self.vizinhos:
            vizinho.incrimentaSaturacao()

    def decrementaSaturacaoVizinhos(self):
        for vizinho in self.vizinhos:
            vizinho.decrementaSaturacao()



class grafo:
    def __init__(self,tabela,arquivoSaida):
        self.quantidadeVertices = len(tabela)
        self.ordem = int(math.sqrt(self.quantidadeVertices))
        self.dimensaoBloco = int(math.sqrt(self.ordem))
        self.vertices = self.constroiVertices(tabela)
        self.blocos = self.formaBloco()
        self.arquivoSaida = arquivoSaida
        self.mergeVizinhos()
        self.escreveArquivo()
        self.debug()
        if self.dsatur():
            self.escreveArquivo()
        else:
            print("Sem solução")
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

    def verticesNaoColoridos(self):
        verticesNaoColoridos = set()
        for vertice in self.vertices:
            if (self.vertices[vertice].getConteudo() == "N"):
                verticesNaoColoridos.add(vertice)
        return verticesNaoColoridos



    def dsatur(self):
        if self.todosColoridos():
            return True
        maiorSaturacao = self.maiorSaturacao()
        coresPossiveis = self.vertices[maiorSaturacao].coresPossiveis(self.ordem)
        if coresPossiveis == -1:
            return False
        if not coresPossiveis:
            return False
        for cor in coresPossiveis:
            self.vertices[maiorSaturacao].setConteudo(cor)
            self.vertices[maiorSaturacao].incrimentaSaturacaoVizinhos()
            if self.dsatur():
                return True
            else:
                self.vertices[maiorSaturacao].decrementaSaturacaoVizinhos()
                self.vertices[maiorSaturacao].setConteudo("N")
        return False


    def escreveArquivo(self):
        arquivoSaida = open(self.arquivoSaida, "w+")
        for vertices in self.vertices:                
            if(vertices % self.ordem == 0 and vertices != 0):
                print("\n",file=arquivoSaida)
            print(self.vertices[vertices].getConteudo()," ",end="",file=arquivoSaida)

    def debug(self):
        print("s")



    def getBlocos(self):
        print (self.blocos)

    def getVertices(self):
        for chave in self.vertices:
            self.vertices[chave].getVertice()





    


        





        


if __name__ == "__main__":
    nome_arquivo = ""
    if len(sys.argv) == 3:
        nome_arquivo = sys.argv[1]
        arquivo_saida = sys.argv[2]
    else:
        print("Número inválido de argumentos")
    arquivo = open(nome_arquivo,"r")
    tabela = ""
    for linha in arquivo:
        tabela = tabela + ((linha.replace("\n","").replace(".","N")))
    tabela = list(tabela)
    grafo(tabela,arquivo_saida)
    

            





