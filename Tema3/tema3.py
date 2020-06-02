import math
'''
Tema 3 - Calcul Numeric
Mihai Elena Sorina si Cotfasa Octavian
Grupa 3A2
'''

class MatriceRara:
    def __init__(self, filePath):
        self.b = []
        self.matrix = [[]]
        theFile = open(filePath, "r") #citeste din fisier
        iternumber = theFile.read().split()
        self.n = int(iternumber[0]) #salveaza prima valoare din fisier = lungimea matricei
        i = 1

        for k in range(1, len(iternumber), 3):
            val = float(iternumber[k].replace(',', '')) #salveaza prima valoare din matrice
            i = int(iternumber[k + 1].replace(',', '')) #salveaza linia primei valori
            j = int(iternumber[k + 2].replace(',', '')) #salveaza coloana primei valori
            #print(val, ' ', i, ' ',j,'\n')

            while i >= len(self.matrix):
                self.matrix.append([])

            alreadyExist = False

            #verifica daca exista doua valori pe aceeasi coloana si linie si daca da,
            #le aduna ca sa obtina o singura valoare.
            for u in range(0, len(self.matrix[i])):

                if self.matrix[i][u][1] == j:
                    alreadyExist = True
                    self.matrix[i][u][0] += val

            if not alreadyExist:
                self.matrix[i].append([val, j])


        theFile.close()
        exceed = False

        #verifica daca sunt mai putin de 10 elemente nenule pe linie
        for i in range(0, len(self.matrix)):
            if len(self.matrix[i]) > 10:
                exceed = True
                #print(i,' ',len(self.matrix[i]),' ',self.matrix[i])

        if exceed==False:
            print('Matricea ' + filePath + ' nu are mai mult de 10 elemente nenule pe linie')
        elif exceed == True:
            print('Matricea ' + filePath + ' are mai mult de 10 elemente nenule pe linie')


    #realzeaza suma dintre cele doua matrice
    def add(self,second):
        newList = self.matrix.copy()
        len_second_matrix = len(second.matrix)
        for i in range(0,len_second_matrix):
            for j in range(0,len(second.matrix[i])):
                found = False
                #daca exista cate un element pe aceeasi pozitie in fiecare matrice, le aduna intr-o lista noua
                for k in range(0,len(newList[i])):
                    if second.matrix[i][j][1] == newList[i][k][1]:
                        found = True
                        newList[i][k][0] += second.matrix[i][j][0]
                #daca nu exista in ambele, dar exista intr-una din cele doua matrici, o adauga la lista noua
                if not found:
                    newList[i].append(second.matrix[i][j])

        #print(second.matrix)
        #print(self.matrix)
        #print(newList)

        return newList


    #realizeaza inmultirea matricelor
    def multiply(self, second):
        result = []
        nrOfRows = len(self.matrix)
        m1 = {}
        m2 = {}
        mf = {}

        for i in range(0, nrOfRows):
            m1[i] = {}
            m2[i] = {}
            mf[i] = {}

        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                m1[i][self.matrix[i][j][1]] = self.matrix[i][j][0]

        for i in range(0, len(second.matrix)):
            for j in range(0,len(second.matrix[i])):
                m2[i][second.matrix[i][j][1]] = second.matrix[i][j][0]

        #verifica daca exista valoarea in lista si daca nu inseamna ca este egala cu zero (nu sunt valori nule in schema de memorare economica)
        #apoi face inmultirea si suma pentru fiecare element din matricea finala
        for i in m1.keys():
            for k in m1[i].keys():
                for j in m2[k].keys():
                    if j not in mf[i]:
                        mf[i][j] = 0
                    if k not in m1[i]:
                        mf[i][k] = 0
                    if j not in m2[k]:
                        m2[k][j] = 0
                    mf[i][j] += m1[i][k] * m2[k][j]

        for i in mf.keys():
            result.append([])
            for j in mf[i].keys():
                result[i].append([mf[i][j], j])

        return result

 #compara doua matrici ca sa verfice daca operatiile s-au efectuat cum trebuie
    def compareWith(self,matrix):
        equal = True
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                a = float('%.8f' % (self.matrix[i][j][0]))
                b = float('%.8f' % (matrix[i][j][0]))
                #verifica conditiile ca sa fie egale
                if abs(a - b) >= math.e and self.matrix[i][j][1] == matrix[i][j][1]:
                    equal = False
        if equal:
            print('Matricele sunt egale')
        else:
            print('Matricele NU sunt egale')


A = MatriceRara('a.txt')
B = MatriceRara('b.txt')

C = MatriceRara('aplusb.txt')
D = MatriceRara('aorib.txt')
AoriB = A.multiply(B)
AplusB = A.add(B)

print('\n')

print("Pentru adunare: ")
C.compareWith(AplusB)


print("Pentru inmultire: ")
D.compareWith(AoriB)


print("\nO matrice cu mai putin de 10 elemente pe linie: ")
E = MatriceRara('testCuMaiPutinDe10NumerePeLinie.txt')