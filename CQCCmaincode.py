from ast import operator
import numpy as np
import matplotlib as mpl
from qiskit import *
from qiskit.quantum_info import Pauli
from qiskit.opflow import X, Y, Z, I, OperatorBase, PauliOp, PauliTrotterEvolution, CircuitSampler, MatrixEvolution, Suzuki, ListOp
from qiskit.quantum_info.operators import Operator, Pauli
from qiskit.visualization.array import array_to_latex
#from HamiltonianManipulationFunctions import Format_Hamiltonian , Order_Hamiltonian_PauliStrings


from audioop import reverse
from typing import List


def Format_Hamiltonian(filepath = str):
    '''
    Takes a txt file of a hamiltonian and converts it into a a list of lists with 
    each inner list containing the pauli string and its associated magnitude
    
    Make sure that .txt file representing the hamiltonian contains one pauli string per line 
    additionally add an r infront of the file path if it contains escape characters
    '''
    file = open(filepath)
    
    Hamiltonian_List = list()
    for x in file:
        
        line = x.split()
        
        if len(line) > 0:
            if line[0] == "-":
                Hamiltonian_List.append([float(line[0] + line[1]), line[-1]])
            else:
                Hamiltonian_List.append([float(line[1]),  line[-1]])

           
    file.close()
    
    return(Hamiltonian_List)



def Order_Hamiltonian_PauliStrings(HList = list(), specifier = str):
    '''
    Orders the hamiltonian list according to the specifier
    the specifier can have the following values: "magnitude", "lexicographic"
    lexicographic sorting will sort each term by its pauli string contents with 
    the identity that X < Y < Z < I
    '''
    newH = list()
    magP = list()
    pauliList = list()
    if specifier == "magnitude":
        HList.sort(reverse = True)
        
    elif specifier == "lexicographic":
        def lexsort(Pstring):
            psum = 0
            for i in Pstring:
                if i == "X":
                    psum += 1
                elif i == "Y":
                    psum += 2
                elif i == "Z":
                    psum += 3
                elif i == "I":
                    psum += 4
            return psum
        HList.sort(reverse = False, key = lambda x: lexsort(x[1]))
    
    return HList
#the initialized lists representing the hamiltonians. We can 
LexH = Order_Hamiltonian_PauliStrings(Format_Hamiltonian(r"C:\Users\DLG\Desktop\HamiltonianCopy.txt"), "lexicographic")
MagH = Order_Hamiltonian_PauliStrings(Format_Hamiltonian(r"C:\Users\DLG\Desktop\HamiltonianCopy.txt"), "magnitude")
H = Format_Hamiltonian(r"C:\Users\DLG\Desktop\HamiltonianCopy.txt")

#converts all the strings in the hamiltonian lists to Pauli Objects
def To_Pauli(harray):
    for i in harray:
        i[1] =  Pauli(i[1])
    return harray

#returns a numpy array where a_{i,j} gives whether P_i and P_j commute and has values 1 or 0
def Get_Commutation_Matrix(harray= list()):
    A = list()
    for i in harray:
        B = list()
        for j in harray: 
            if i[1].commutes(j[1]):
                B.append(0)
            else:
                B.append(1)
        A.append(B)
    return np.asarray(A)

#converts the hamiltonian as a list to string that can be interpreted as an operator in qiskit
def ConvertToPop(harray):
    string = "("
    P = PauliOp(Pauli('IIIIIIIIII'), 0)
    for x in harray:
        P += PauliOp(Pauli(x[1]), x[0])
        '''if x[0] < 0:
            string += str(x[0]) + " * "
        else:
            string += "+" + str(x[0]) + " * "
        a = x[1]
        b = '('
        for i in range(len(a)-1):
            b+= a[i] + "^"

        b+= a[-1] + ")"
        
        string += b +"\n"
    string += ")"'''
    return P
# returns A circuit representing the time evolution operator of 
def toQcircuit(po = PauliOp):
    Evolved_op = po.exp_i()
    trot_op = PauliTrotterEvolution().convert(Evolved_op)
    TrotCircuit = trot_op.to_circuit()
    A = TrotCircuit.decompose().decompose()

    return A





Converted_Unsorted_H = ConvertToPop(To_Pauli(H))
Converted_LexSort_H = ConvertToPop(To_Pauli(LexH))
Converted_MagSort_H = ConvertToPop(To_Pauli(MagH))

MagSortCircuit = toQcircuit(Converted_MagSort_H)
LexSortCircuit = toQcircuit(Converted_LexSort_H)
UnsortedCircuit = toQcircuit(Converted_Unsorted_H)

print(LexSortCircuit.count_ops())
print(UnsortedCircuit.count_ops())
print(LexSortCircuit.depth())
print(LexSortCircuit.depth())

LexSortCircuit.qasm("LexSortqasm")








        






