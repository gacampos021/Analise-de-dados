import pandas as pd
import string
import quality as q 
import noiser as n
from hunspell import Hunspell
from auxlib import printl, select_col
import re

print('''
    \t\t----------------------------------
    \t\t-------------WELCOME!-------------
    \t\t----------------------------------
    ''')

# File reading
####################################################################
file_path = str(input('Insert file path/name: '))
aux = file_path.split('.')
df=pd.DataFrame()

if(str(aux[len(aux)-1]) == 'xlsx'):
    try:
        df=pd.read_excel(file_path)
        print('Excel file reading completed successfully!\n')
    except:
        print('ERROR: file does not exist!')
elif(str(aux[len(aux)-1]) == 'csv'):
    try:
        df=pd.read_csv(file_path)
        print('CSV file reading completed successfully!\n')
    except:
        print('ERROR: file does not exist!')
else:
    print('ERROR: Extension not supported: '+str(aux[len(aux)-1]))
####################################################################

#  OBS: PARAR ALGORITMO CASO DE ERRO NA LEITURA DOA RQUIVVO

# Primary key consistency
####################################################################
printl(df.columns)
key_col = str(input('Select primary key column: '))
while(key_col not in df.columns):
    printl(df.columns)
    key_col = str(input('Select valid option: '))
prim_miss, prim_dupli = q.cons_key(df,key_col)
####################################################################

# Format and datatype
####################################################################
wrong_type, type_list = q.cons_type(df)
syntax = q.acc_syn(df, type_list)
semantic = q.acc_sem(df, type_list)
####################################################################

print('\n')

# Completeness
####################################################################
completeness_row = q.comp_row(df)
completeness_col=q.com_col(df)
completeness_fake=0
fake=input(str('Has this base fake completeness problems?[Y/N]'))
if(fake.upper() in 'Y'):
    completeness_fake=q.fake_comp(df)
####################################################################

print('\n')

# TYPO
####################################################################
print('Select the text columns (only words, not links, note date, ...)')
typo_col = select_col(df)
typo_df = q.cons_typo(df, typo_col)
####################################################################

# DUPLICATE
####################################################################
dupli = q.duplicated(df)
####################################################################



# Final Report
####################################################################
report=pd.DataFrame(index = ['syntax', 'semantic'], columns = df.columns)
row_qua=['VERY POOR', 'POOR\t', 'NEED SUPPORT', 'OK\t', 'PERFECT!']

print('-------------------------------------------------------------')

print('Total rows: '+str(len(df)))

# primary key
print('\n\tPRIMARY KEY')
print('Missing: '+str(prim_miss))
print('Duplicated: '+str(prim_dupli))

print('\n')

# format
print('\n\tFORMAT')
if(wrong_type == 0):
    print('No wrong columns type!')
else:
    print(str(wrong_type)+' wrong columns in the dataframe!\n')
    print('COLUMN\t\t\tDETECTED\t\tINCONSISTENT')
    for i in df.columns:
        if(str(type_list[i]) not in str(df.dtypes[i])):
            print(str(i)+'\t\t'+str(type_list[i])+'\t\t'+str(df.dtypes[i]))

print('\n')

for i in syntax.columns:
    report[i]['syntax'] = syntax[i]['total'] - syntax[i]['correct']
    report[i]['semantic'] = semantic[i]['total'] - semantic[i]['correct']

print('\n\t\tACCURACY REPORT (number of invalid rows)\n')
print(report)

print('\n')

# completeness
print('\n\tCOMPLETENESS REPORT\n')
print('\n\t   ROW INCOMPLETENESS\n')
for i in range(5):
    print('\t'+str(row_qua[i])+'\t'+str(completeness_row[i]))
print('\n\t   COLUMN INCOMPLETENESS\n')
print(completeness_col)

if(fake.upper() in 'Y'):
    print('\n\t   COLUMN FAKE COMPLETENESS\n')
    print(completeness_fake.loc['wrong'])

# typo
print('\n\tTYPO MISTAKE\n')
print(typo_df)

# dupli
print('\n\tDUPLICATED ROWS:  '+str(dupli))

print('-------------------------------------------------------------')
####################################################################