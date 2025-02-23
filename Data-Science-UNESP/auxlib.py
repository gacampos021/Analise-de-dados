import string

def remove(name):
    aux=name.split('.')
    if(len(aux) == 2):
        name=aux[0]
    else:
        aux=str(aux[1:])
        print('ERROR: file has more than one extention: '+aux)
    return(name)

def printl(df):
    for i in range(len(df)):
        print(df[i], end = "\t")
        if(i+1%4 == 0):
            print('\n')
    print('\n')

def select_col(df):
    flag='Z'
    income_col=list(df.columns)
    return_col=[]
    while(len(income_col) != 0):
        print('\n\n\nAvailable columns: ')
        print(income_col)
        print('Selected columns: ')
        print(return_col)
        flag=input(str('>   (X to continue)'))
        if(flag in income_col):
            income_col.remove(flag)
            return_col.append(flag)
        elif(flag in 'X'):
            break
        else:
            print("Column doesn't exist!")
    return return_col