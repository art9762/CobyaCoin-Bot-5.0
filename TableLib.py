arr = [["1", "2", "3"], ["1", "5", "6"]]
def getMas(name): #возвращает двумерный массив таблицы
    a = []
    tab = []
    with open(name, 'r+') as f:
        a = f.readlines()
        for i in a:
            i = i[:-1]
            tab.append(i.split("$"))
    return tab

def wrTo(mass, name): #вписывает двумерный массив в файл
    s = ''
    m = []
    for i in mass:
        for j in i:
            s += str(j)+"$"
        m.append(s[:-1]+"\n")
        s = ''

    with open(name, 'w') as f:
        f.writelines(m)

def addMass(s, name):
    tb = getMas(name)
    tb.append(s) 
    wrTo(tb, name)

def find_string(table, search_string):
    i = 0
    for i in range(len(table)):
        if table[i][0] == search_string:
            return i
        
def getCols(name):
    matrix = getMas(name)
    transposed_matrix = []
    for i in range(len(matrix[1])):
        transposed_row = []
        for j in range(len(matrix)):
            transposed_row.append(matrix[j][i])
        transposed_matrix.append(transposed_row)
    return transposed_matrix

def find_in(name, target, column_index):
    array_2d = getMas(name)
    for index, row in enumerate(array_2d):
        if column_index < len(row):
            if row[column_index] == target:
                return index 
                
    return None  

