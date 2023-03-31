# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 22:32:12 2023

@author: Stats
"""
import numpy as np
import pandas as pd
import os


a = np.array([1,2,3])
np.mean(a)
np.sum(a)
[1,2,3]+[1,2,3]

# numpy actua de forma vectorizado
2*a 
2*[1,2,3]
a+a


estaturas = pd.Series([180, 170, 160])

df = {'esttura': [180, 170, 160] , 'peso': [76, 67, 56]}
df = pd.DataFrame.from_dict(df)

df.shape
df.columns
df.index

df3 = df
df3.esttura[0] = 185


df2 = df.copy()
df2.esttura[0] = 195
df2
df




os.chdir(r'F:\Laboral 2023\central')
os.listdir()


# Leer indicando la clase de la columna

# datos = pd.read_csv('Lucy.csv')


datos = pd.read_csv('Lucy.csv', dtype={
    'ID': str,
    'Ubication': str,
    'Level': str,
    'Zone': str,
    'Income': float,
    'Employees': int,
    'Taxes': float,
    'SPAM': str
})

# Seleccionar una base de datos reducidos
df = datos[['ID', 'Level', 'Income']]

sel = ['ID', 'Level', 'Income']
df = datos[sel]

datos.iloc[:, [1, 3]] 

datos.loc[:, ['Ubication', 'Zone']] 



# Como renombrar variables
df = datos[['ID', 'Level', 'Income']]


df = df.rename(columns={'Level': 'tamano', 'Income': 'ingreso'})


# Ordenar por tamaño e ingreso

df = df.sort_values(by=['tamano', 'ingreso'], ascending=[True, False])


# Si quisieramos filtrar por las empresas pequeñas con la base de datos reducida y con variables renombradas a español

df2 = datos[['ID', 'Level', 'Income']] \
       .rename(columns={'Level': 'tamano', 'Income': 'ingreso'}) \
       .sort_values(by='ingreso', ascending=False) \
       .query('tamano == "Small"') \
       .drop(columns=['tamano'])
       
# Otra alternativa es utilizar utilizar el método loc

df2 = (datos[['ID', 'Level', 'Income']] \
       .rename(columns={'Level': 'tamano', 'Income': 'ingreso'}) \
       .sort_values(by='ingreso', ascending=False) \
       .loc[df['tamano'] == 'Small'] \
       .drop(columns=['tamano']))   

  
    
# Calcular los datos agregados por tamaño de la empresa    
def cv(x):
    return(np.std(x) / np.mean(x) * 100)    
 
cv(np.array([170, 190, 180, 182]))    
cv(pd.Series(np.array([170, 190, 180, 182])))    

df = {'esttura': [180, 170, 160] , 'peso': [76, 67, 56]}
df = pd.DataFrame.from_dict(df)
cv(df['esttura'])

   
consulta = datos.groupby(datos['Level']).agg(prom_ingreso=('Income', np.mean),
desv_ingreso = ('Income', np.std), cv_ingreso = ('Income', cv))
consulta = consulta.reset_index()

consulta = datos.groupby(datos['Level']).agg(prom_ingreso=('Income', np.mean),
desv_ingreso = ('Income', np.std), cv_ingreso = ('Income', cv))
consulta.reset_index(inplace = True)


# No funciona
#consultaB = datos.agg(prom_ingreso=('Income', np.mean),
#desv_ingreso = ('Income', np.std), cv_ingreso = ('Income', cv))


# Parentesis

# Create a Series of integers
s = pd.Series([1, 2, 3, 4, 5])

# Define a function that squares its input
def cuadrados(x):
    return x**2

# Apply the function to each element of the Series
s_cuadrados = s.apply(cuadrados)

# Print the squared Series
print(s_cuadrados)

# También se pueden usar expresiones lambda:

    
# Create a Series of strings
s = pd.Series(['apple', 'banana', 'cherry'])

# Apply the lambda function to each element of the Series
s_length = s.apply(lambda x: len(x))

# Print the length Series
print(s_length)


# Con un dataframe

# Create a DataFrame of numbers
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})

# Define a function that sums its input
def sum_row(row):
    return sum(row)

# Apply the function to each row of the DataFrame
df_summed_rows = df.apply(sum_row, axis=1) # 1 por fila, 0 por columna

# Print the summed row DataFrame
print(df_summed_rows)



    
# Alternativamente puede agregarse así:

consulta2 = datos.groupby('Level').apply(lambda x: pd.Series({
    'prom_ingreso': np.mean(x['Income']),
    'desv_ingreso': np.std(x['Income']),
    'cv_ingreso': np.std(x['Income']) / np.mean(x['Income']) * 100
}))    
    
# Sin agregar:
    
consulta_noAgregar = pd.DataFrame(pd.Series({
    'prom_ingreso': np.mean(datos['Income']),
    'desv_ingreso': np.std(datos['Income']),
    'cv_ingreso': np.std(datos['Income']) / np.mean(datos['Income']) * 100
})).T

# La T es la transposición


# Crear nuevas variables, ingreso por empleado y ver la empresa con más productividad:
datos['ingresoXempleado'] = datos['Income'] / datos['Employees']
datos = datos.sort_values('ingresoXempleado', ascending = False)




# Otra manera de agregar
datos['temp'] = 'Global'
consulta2 = datos.groupby(datos['temp']).agg(prom_ingreso=('Income', np.mean),
desv_ingreso = ('Income', np.std), cv_ingreso = ('Income', cv))

consulta2.reset_index(inplace = True)
consulta2 = consulta2.rename(columns={'temp': 'Level'})

consulta = datos.groupby(datos['Level']).agg(prom_ingreso=('Income', np.mean),
desv_ingreso = ('Income', np.std), cv_ingreso = ('Income', cv))
consulta.reset_index(inplace = True)
# Pegado por debajo
consulta3 = pd.concat([consulta, consulta2], axis=0)


# Pivotear variables

# Sacar el ingreso por zona y tamaño y pivotearlo, en filas colocar las zonas y en las columnas el tamaño:
consulta4 = datos.groupby(['Zone', 'Level']).agg(prom_ingreso=('Income', np.mean)) 

    
consulta5 = consulta4.pivot_table(values='prom_ingreso', index=['Zone'], columns='Level')
consulta5.reset_index(inplace = True)

consulta5.to_excel('filename.xlsx', index=False)

# Revisemos como se puede revertir
#pd.DataFrame.to_dict(consulta5)

df_long = pd.melt(consulta5, id_vars=['Zone'], var_name='Size', value_name='Value')

df_long = df_long.rename(columns={'Value': 'Income'})


consulta5 = consulta5.rename(columns={'Big': 'Level_Big', 
                                      'Medium': 'Level_Medium',
                                      'Small': 'Level_Small'})




#df1 = pd.read_clipboard()
#pd.DataFrame.to_dict(df1)
df1 = {'ID': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5},
 'Ingreso': {0: 4, 1: 3, 2: 5, 3: 7, 4: 2}}
df1 =  pd.DataFrame.from_dict(df1)

#df2 = pd.read_clipboard()
#pd.DataFrame.to_dict(df2)
df2 = {'Id': {0: 1, 1: 2, 2: 4, 3: 5},
 'Edad': {0: 24, 1: 23, 2: 27, 3: 32},
 'Sexo': {0: 'M', 1: 'F', 2: 'M', 3: 'F'},
 'Email': {0: 'fddf@gmail.com',
  1: 'trtrt@yahoo.es',
  2: np.nan,
  3: 'trrt1234@hotmail.com'}}
df2 =  pd.DataFrame.from_dict(df2)



merged_df = df1.merge(df2, left_on='ID', right_on='Id', how='left')

# Creación de deciles
datos['Decil_Income'] = pd.qcut(datos['Income'], 10, labels=False)
datos.groupby('Decil_Income')['Taxes'].mean()
