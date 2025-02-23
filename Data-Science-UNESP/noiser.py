import pandas as pd 
import numpy as np
import random as rand
import string

kb_table={'a':['q','w','s','z'], 
            'b':['v','n','g','h'],
            'c':['x','d','f','v'],
            'd':['x','s','r','t','g'],
            'e':['w','s','d','f','r'],
            'f':['d','c','v','g','t','r'],
            'g':['v','f','t','y','h','b'],
            'h':['g','b','n','j','u','y'],
            'i':['u','j','k','o'],
            'j':['h','n','m','k','i','u'],
            'k':['i','j','m','l','o'],
            'l':['p','o','k'],
            'm':['k','j','n'],
            'n':['b','h','j','m'],
            'o':['p','l','k','i'],
            'p':['o','l'],
            'q':['w','s','a'],
            'r':['e','d','f','g','t'],
            's':['w','a','z','x','d','e'],
            't':['r','f','g','h','y'],
            'u':['y','k','h','j','i'],
            'v':['c','f','g','b'],
            'w':['q','a','s','d','e'],
            'x':['z','s','d','c'],
            'y':['t','g','h','j','u'],
            'z':['a','s','x']
}

# FUNCTIONS
#########################################
#
# DUPLICATE ROWS BY PERCENTAGE
def duplicate_rows(df, fraction):
    samp = df.sample(frac=fraction, axis=0) # by index
    df=pd.concat([df,samp], axis=0)
    return df
#
# TRANSFORM INTO NAN BY COLUMNS PERCENTAGE
def insert_nan(df, fraction, cols):
    for i in cols:
        samp = df.sample(frac=fraction, axis=0) # by index
        df=pd.concat([df,samp], axis=0)
        df=df.drop_duplicates(keep=False)
        samp[i]=np.NAN
        df=pd.concat([df,samp], axis=0)
    return(df)
#
# SIMULATE TYPO ERRORS
def typo(word, lvl=1):
#try:
    word=list(word)
  
    k=0
    while k < lvl:
        err_type=rand.randint(0,4) # tipo do erro (0:keyboard, 1:pop_letter, 2:dupli, 3:swap, 4:sec_word)
        letter_swap = rand.choice(range(len(word))) #char position
        old_char=word[letter_swap].lower()  #

        #keyboard missclick
        if(err_type == 0 and old_char in kb_table.keys()):  # 1- type 2- char must be in kb_tables dict
            #print('missclick')
            if(word[letter_swap] == old_char): #lower case            
                new_char=kb_table[old_char][rand.choice(range(len(kb_table[old_char])))]    #get char from table (def function?)
                word[letter_swap]=new_char  #swap old to newone
                k+=1
                #print('lower')

            elif(word[letter_swap] == old_char.upper()): #upper case
                new_char=kb_table[old_char][rand.choice(range(len(kb_table[old_char])))]    #get char from table (def function?)
                word[letter_swap]=new_char.upper()  #swap old to newone
                k+=1
                #print('upper')

        #pop off char
        elif(err_type == 1):    
            ind=letter_swap
            #print('pop char')
            while ind < len(word):
                word[ind-1]=word[ind]
                ind+=1
            word[ind-1]=''  #exclude last char
            k+=1

        #duplicate char
        elif(err_type == 2 and letter_swap < len(word)-1 and letter_swap in kb_table.keys()): #1- type 2- char must not be the last
            #print('double click')
            ind=letter_swap
            buf=word[ind:]  #buffer for the chars that will be swapped
            aux=0
            ind+=1  #the selected char will be duplicate, so itself must stay on the str

            while aux < len(buf)-1: #len-1 because ind runs out of index, so .append() after while statement
                word[ind]=buf[aux]  #       ||
                ind+=1              #       ||
                aux+=1              #       \/
            word.append(buf[aux])   # HERE !!!!
            k+=1
        
        #swap char position
        elif(err_type == 3 and letter_swap > 0 and word[letter_swap] in kb_table.keys() and word[letter_swap-1] in kb_table.keys()  and word[letter_swap] != word[letter_swap-1]): #1- tpye 2-char must not be 1st 3 and 4 both swapped chars must be a lower letter
            #print('swap position')
            aux=word[letter_swap]
            word[letter_swap]=word[letter_swap-1]
            word[letter_swap-1]=aux
            k+=1

        #insert second char
        elif(err_type == 4 and old_char in kb_table.keys()):
            #print('second char click')
            ind=letter_swap
            buf=word[ind:]  #buffer for the chars that will be swapped
            new_char=kb_table[old_char][rand.choice(range(len(kb_table[old_char])))] 
            word=word[:ind]
            word.append(new_char)
            word=word+buf                
            k+=1
    word="".join(word)  #list->str 
        #aux[i]=word
        #word=" ".join(aux)
    return(word)
    # except:
    #     print('ERROR')

def df_typo(df, fraction, cols, lvl=1):
    for i in cols:
        samp = df.sample(frac=fraction, axis=0) # by index
        df=pd.concat([df,samp], axis=0)
        df=df.drop_duplicates(keep=False)

        for j in range(len(samp)):
            word=samp[i].iloc[j]
            word = typo(word, lvl=lvl)
            df=pd.concat([df,samp], axis=0)

    return df
#
# TIPE ERROR num -> str
def to_str(df, fraction, cols):
    for i in cols:
        samp = df.sample(frac=fraction, axis=0) # by index
        df=pd.concat([df,samp], axis=0)
        df=df.drop_duplicates(keep=False)
        samp[i]=samp[i].astype('str').str.replace('.', ',').astype('str')
        df=pd.concat([df,samp],axis=0)
    return df
#

# 
## EXAMPLES
#########################################

## INSERT NAN
#print(df.isnull().sum())
#col=['Outra Plataforma de Delivery', 'Link da Plataforma ', 'Avaliação Google', 'Avaliação Ifood']
#df=insert_nan(df,0.2,col)
#print(df.isnull().sum())
#
## TYPOS SIMULATING
#print(df['Segmento '].value_counts())
#df=typo(df, 0.02, ['Segmento '], 1)
#print(df['Segmento '].value_counts().tail(30))
#
## CONVERT NUMERICAL VALUES TO OBJECT VALUES (num -> str)
#
#       convert to numerical to test function
#df['Número de Seguidores']=pd.to_numeric(df['Número de Seguidores'], errors='coerce').convert_dtypes() 
#print(df.dtypes)
#
#df=to_str(df, 0.2, ['Número de Seguidores'])
#print(df.dtypes)
#
#
## DUPLICATE ROWS BY %
#print(df.duplicated().sum())
#df=duplicate_rows(df,0.2)
#print(df.duplicated().sum())
#
## SAVE IN FILE
##################################################
#df.to_excel('test.xlsx')