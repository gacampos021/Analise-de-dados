import string

def remove(name):
    aux=name.split('.')
    if(len(aux) == 2):
        name=aux[0]
    else:
        aux=str(aux[1:])
        print('ERROR: file has more than one extention: '+aux)
    return(name)