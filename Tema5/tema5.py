import numpy as np
from random import randint

import scipy
import scipy.linalg as la
import math

e = 0.000000001


class MatriceRara:

    def __init__(self, filePath):

        self.randMatrix = {}
        self.clasicMatrix = []
        theFile = open(filePath, "r")
        # citirea matricii din fisier
        iternumb = theFile.read().split()
        self.n = int(iternumb[0])
        if "," in iternumb[1]:
            self.matrix = {}
            self.rara = True
            for k in range(1, len(iternumb), 3):
                i = int(iternumb[k + 1].replace(',', ''))
                j = int(iternumb[k + 2].replace(',', ''))
                val = float(iternumb[k].replace(',', ''))
                if i not in self.matrix.keys():
                    self.matrix[i] = {}
                if j in self.matrix[i].keys():
                    self.matrix[i][j][0] += val
                else:
                    self.matrix[i][j] = [val, j]
            theFile.close()
            # verificarea simetriei matricei rare
            symetric = True
            for i in self.matrix.keys():
                for j in self.matrix.keys():
                    if j in self.matrix.keys() and i in self.matrix[j].keys():
                        if self.matrix[i][j][0] != self.matrix[j][i][0]:
                            symetric = False
            if not symetric:
                print('Matricea din fisier este simetrica')
            else:
                print('Matricea din fisier nu este simetrica')
        else:

            self.rara = False
            self.m = int(iternumb[1])
            self.matrix = np.zeros((self.n, self.m))
            for k in range(2, len(iternumb), 3):
                i = int(iternumb[k + 1].replace(',', ''))
                j = int(iternumb[k + 2].replace(',', ''))
                val = float(iternumb[k].replace(',', ''))
                self.matrix[i][j] = val

            theFile.close()

    def print(self):
        print(self.n)

    def generateRandomMatrix(self):
        # generarea aleatoare a unei matrice patratice, rare, cu elemente nenule pozitive
        if self.n > 500:
            self.randMatrix = {}
            for i in range(0, self.n):
                if i not in self.randMatrix.keys():
                    self.randMatrix[i] = {}
                for j in range(i, self.n):
                    generatenumber = randint(0, 2)
                    if (generatenumber == 1):
                        randNum = randint(0, 10)
                        if randNum != 0:
                            self.randMatrix[i][j] = [randNum, j]
                            if j not in self.randMatrix.keys():
                                self.randMatrix[j] = {}
                            self.randMatrix[j][i] = [randNum, i]
            print("Matrice random generata")

    def transformFileMatrix(self):
        self.clasicMatrix = []
        for i in range(0, self.n):
            self.clasicMatrix.append([])
            for j in range(0, self.n):
                if i not in self.matrix.keys() or j not in self.matrix[i].keys():
                    self.clasicMatrix[i].append(0)
                else:
                    self.clasicMatrix[i].append(self.matrix[i][j][0])
        return self.clasicMatrix

    def transformRandomMatrix(self):
        if self.randMatrix != {}:
            self.newRandomMatrix = []
            for i in range(0, self.n):
                self.newRandomMatrix.append([])
                for j in range(0, self.n):
                    if i not in self.randMatrix.keys() or j not in self.randMatrix[i].keys():
                        self.newRandomMatrix[i].append(0)
                    else:
                        self.newRandomMatrix[i].append(self.randMatrix[i][j][0])
            return self.newRandomMatrix

    def calculatePowerMatrix(self):
        # implementarea algortimului metodei puterii
        v1 = [1]
        for i in range(1, self.n):
            v1.append(0)
        w = np.dot(self.clasicMatrix, v1)
        # print(w)
        sigma1 = np.dot(w, v1)
        k = 0

        while True:
            temp = 1 / np.linalg.norm(w)
            v2 = [temp * x for x in w]
            w = np.dot(self.clasicMatrix, v2)
            sigma2 = np.dot(w, v2)
            k = k + 1
            r = np.subtract(w, np.dot(sigma1, v1))
            if np.linalg.norm(r) > self.n * e and k < 1000000:
                sigma1 = sigma2
                v1 = v2
            else:
                v1 = v2
                sigma1 = sigma2
                break
        print("Valoarea proprie asociata matricei din fisier este: ", sigma1)
        print("Un vector propriu asociat: ", v1)
        # print(k)

    def calculatePowerRandomMatrix(self):
        # implementarea algortimului metodei puterii
        if self.randMatrix != {}:
            v1 = [1]
            for i in range(1, self.n):
                v1.append(0)
            w = np.dot(self.newRandomMatrix, v1)
            # print(w)
            sigma1 = np.dot(w, v1)
            k = 0

            while True:
                temp = 1 / np.linalg.norm(w)
                v2 = [temp * x for x in w]
                w = np.dot(self.newRandomMatrix, v2)
                sigma2 = np.dot(w, v2)
                k = k + 1
                r = np.subtract(w, np.dot(sigma1, v1))
                if np.linalg.norm(r) > self.n * e and k < 1000000:
                    sigma1 = sigma2
                    v1 = v2
                else:
                    v1 = v2
                    sigma1 = sigma2
                    break
            print("Valoarea proprie asociata matricei random este: ", sigma1)
            print("Un vector propriu asociat: ", v1)
            # print(k)

    def SVD(self):
        u, s, v = np.linalg.svd(self.matrix)
        print("USV", "\nU: ", u, "\nS: ", s, "\nV:", v)
        rank = np.linalg.matrix_rank(self.matrix)
        print("Rank: ", rank)
        CondNum = np.linalg.cond(self.matrix)
        print("Condition Number of Matrix: ", CondNum)
        PseudoInverseMoorePenrose = np.linalg.pinv(self.matrix)
        print("Moore-Penrose Pseudo-inverse: ", PseudoInverseMoorePenrose)
        b = [6, -4, 27, 5]
        x, residuals, rank, s = scipy.linalg.lstsq(self.matrix, b)
        print(self.matrix)
        print("Vectorul x: ", x)
        nrm = np.linalg.norm(b - self.matrix.dot(x))
        print("Norma: ", nrm)
        At = np.transpose(self.matrix)
        AtA = np.dot(At, self.matrix)
        AtA = np.linalg.inv(AtA)
        Aj, residuals, rank, s = np.linalg.lstsq(AtA, At, rcond=-1)
        print("Aj = ", Aj)

        finalnrm = np.linalg.norm(PseudoInverseMoorePenrose - Aj)
        print("Final norm: ", finalnrm)


A = MatriceRara('a_2020.txt')
if A.rara:
    A.generateRandomMatrix()
    A.transformFileMatrix()
    A.transformRandomMatrix()
    A.calculatePowerRandomMatrix()
    A.calculatePowerMatrix()
else:
    A.SVD()
