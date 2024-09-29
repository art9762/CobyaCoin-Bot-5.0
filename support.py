import TableLib as db
liders_kl = []
liders_cb = []
liders_act = []
liders_cas = []


def cols(matrix):
    transposed_matrix = []
    for i in range(len(matrix[1])):
        transposed_row = []
        for j in range(len(matrix)):
            transposed_row.append(matrix[j][i])
        transposed_matrix.append(transposed_row)
    return transposed_matrix  
        
def update():
    matrix = db.getMas('users.txt')
    sorted_matrix_kl = sorted(matrix, key=lambda x: int(x[1]), reverse=True)
    sorted_matrix_cb = sorted(matrix, key=lambda x: int(x[2]), reverse=True)
    sorted_matrix_at = sorted(matrix, key=lambda x: int(x[4]), reverse=True)
    sorted_matrix_cs = sorted(matrix, key=lambda x: int(x[5]), reverse=True)

    global liders_kl
    global liders_cb
    global liders_act
    global liders_cas

    liders_kl = cols(sorted_matrix_kl)[0]
    liders_cb = cols(sorted_matrix_cb)[0]
    liders_act = cols(sorted_matrix_at)[0]
    liders_cas = cols(sorted_matrix_cs)[0]

