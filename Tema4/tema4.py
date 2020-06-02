import math

class MatriceRara:

    def __init__(self, filePath1, filePath2):
        self.b = []
        self.matrix = [[]]
        self.valid = True
        theFile1 = open(filePath1, "r")
        theFile2 = open(filePath2, "r")
        iternumb1 = theFile1.read().split()
        iternumb2 = theFile2.read().split()
        self.n = int(iternumb1[0])
        i = 1

        for k in range(1, len(iternumb2), 3):
            val = float(iternumb2[k].replace(',', ''))  # salveaza prima valoare din matrice
            i = int(iternumb2[k + 1].replace(',', ''))  # salveaza linia primei valori
            #j = int(iternumb2[k + 2].replace(',', ''))  # salveaza coloana primei valori
            print(val,' ', i)
            # print(val, ' ', i, ' ',j,'\n')

            while i >= len(self.matrix):
                self.matrix.append([])

            alreadyExist = False
            if i not in self.matrix.keys():
                self.matrix[i] = {}
            if j in self.matrix[i].keys():
                self.matrix[i][j][0] += val
            else:
                self.matrix[i][j] = [val, j]
        theFile1.close()
        theFile2.close()
        for i in range(0, max(self.matrix.keys())):
            if i not in self.matrix.keys() or i not in self.matrix[i].keys():
                print('Matricea are elemente nule pe diagonala')
                self.valid = False
                break

    def print(self):
        print(self.matrix)

    def gaussSeidel(self):
        if self.valid is False:
            return
        xc = {}
        k = 0
        for i in range(0, self.n):
            xc[i] = 0
        k = k + 1
        e = 0.000000001
        countIteration = 0
        while True:
            norm = 0
            for i in self.matrix.keys():
                sum = 0
                for j in range(0, i):
                    if j in self.matrix[i].keys():
                        sum += self.matrix[i][j][0] * xc[j]
                        countIteration = countIteration + 1
                for j in range(i + 1, self.n):
                    if j in self.matrix[i].keys():
                        sum += self.matrix[i][j][0] * xc[j]
                        countIteration = countIteration + 1
                old = xc[i]
                xc[i] = (self.b[i] - sum) / self.matrix[i][i][0]
                norm = norm + (xc[i] - old) ** 2
            norm = math.sqrt(norm)
            k = k + 1
            if norm <= e and k < 10000:
                print(xc)
                print('Numarul de iteratii este ', countIteration)
                break
        self.calculateNorma(xc)

    def calculateNorma(self, xgs):
        result = {}
        for i in self.matrix.keys():
            value = 0
            for j in self.matrix[i].keys():
                value += self.matrix[i][j][0] * xgs[j]
            result[i] = value - self.b[i]
        norm = 0
        for i in result.keys():
            norm = norm + result[i]**2
        print(math.sqrt(norm))


A = MatriceRara('b_3.txt','a_3.txt')
A.gaussSeidel()