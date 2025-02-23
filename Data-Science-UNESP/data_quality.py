import pandas as pd 
import re

def dict_sum(table):
    count=0
    for i in table.keys():
        count+=table[i]
    return count

def report(metric, aux_dict, total):
    if(metric == 'duplicated'):
        duplicated_data=dict_sum(aux_dict)
        percentage=float(duplicated_data/total)
        print('--------------DUPLICATED')
        print('\tTOTAL DATA: '+str(total))
        print('\tDUPLICATED DATA: '+str(duplicated_data))
        print('\tPERCENTAGE: '+str(percentage*100)+'%')

    if(metric == 'uniquiness'):
        unique_data=dict_sum(aux_dict)
        percentage=float(unique_data/total)
        print('--------------UNIQUINESS')
        print('\tTOTAL DATA: '+str(total))
        print('\tUNIQUE DATA: '+str(unique_data))
        print('\tPERCENTAGE: '+str(percentage*100)+'%')
    
    if metric == 'missing':
        mis=aux_dict[0]
        percentage=float(mis/total)
        print('--------------MISSING')
        print('\tTOTAL DATA: '+str(total))
        print('\tMISSING DATA: '+str(mis))
        print('\tPERCENTAGE: '+str(percentage*100)+'%')

    if metric == 'validity':
        invalid=dict_sum(aux_dict)
        percentage=float(invalid/total)
        print('--------------VALIDITY')
        print('\tTOTAL DATA: '+str(total))
        print('\tINVALID DATA: '+str(invalid))
        print('\tPERCENTAGE: '+str(percentage*100)+'%')

def column_types(col_list):
    aux=col_list.value_counts()
    aux_dict={}
    for reg in aux.keys():
        aux_dict[reg]=aux[reg]
    print(aux_dict)
    
def duplicated(col_list):
    aux=col_list.value_counts()
    aux_dict={}
    for reg in aux.keys():
        if(aux[reg]==1):
            break
        if(reg=='*' or reg==''):
            continue
        aux_dict[reg]=aux[reg]
    report('duplicated', aux_dict, len(col_list))

def uniquiness(col_list):
    aux=col_list.value_counts()
    aux_dict={}
    for reg in aux.keys():
        if(aux[reg]>1):
            continue
        aux_dict[reg]=aux[reg]
    report('uniquiness', aux_dict, len(col_list))

def missing(col_list): #quantidade de registros nao vazios
    mis=0
    aux_dict={}
    for reg in col_list:
        if reg == '*' or reg == '':
	        mis+=1
    aux_dict[0]=mis
    report('missing',aux_dict,len(col_list))

def validity(col_list, data_type):
    aux=col_list.value_counts() #dict atributo:qnt_vezes_planilha
    aux_dict={}
    aux_dict[0]=0 #dicionario para mandar para func report(), poderia ser apenas uma variavel count por exemplo
    if data_type == 'link':
        link = re.compile("https://www.[a-z0-9]+.[A-Za-z0-9/.]+")
        for i in aux.keys():
            if not link.match(i):
                aux_dict[0]+=aux[i]
            else:
                print(i)

    elif data_type == 'endereço':
        #re
        aux=0
 
    elif data_type == 'nome':
        nome = re.compile("[a-z-'ãáõéêâíôó().ç 0-9&\n\t]+")
        for i in aux.keys():
            if not nome.match(i.lower()):
                aux_dict[0]+=aux[i]
                print(i.lower())
                print(c)
            else:
                continue
    
    elif data_type == 'rating':
        for i in aux.keys():
            try:
                if float(i) < 0.0 or float(i) > 5.0:
                    aux_dict[0]+=aux[i]
            except: #Nan cases
                if  not (i == '*' or i == ''):
                    aux_dict[0]+=aux[i]

    elif data_type == 'fone':
        #re
        aux=0

    elif data_type == 'ifood':
        for i in aux.keys():
            if not(i == 'Ativo' or i == '*'):
                    aux_dict[0]+=aux[i]

    elif data_type == 'cep':
        #re
        aux=0
    
    elif data_type == 'porte':
        portes=['MICRO EMPRESA', 'INDIVIDUAL', 'EMPRESA DE PEQUENO PORTE', 'DEMAIS', '*', 'GRANDE']
        for i in aux.keys():
            if i not in portes:
                    aux_dict[0]+=aux[i]

    elif data_type == 'cnae':
        #re
        aux=0

    elif data_type == 'cnpj':
        #re
        aux=0

    else:
        print('\nERROR: Data type invalid!')
        return

    report('validity', aux_dict, len(col_list))