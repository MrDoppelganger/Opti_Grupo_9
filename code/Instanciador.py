#----------------------------------Librerias------------------------------
import os
import random
import math


#----------------------------------Funciones------------------------------
'''
    ------------Funcion-----------------
    escribirMiniZinc: Funcion encargada de escribir los datos de la 
        instancia simulada dentro de un documento .dzn.
    ------------Parametros----------------
    str ruta_archivo: Ruta al documento .dzn
    int num_I: Numero de plantas.
    int num_J: Numero de centros de distribucion potenciales.
    int num_K: Numero de zonas de demanda.
    list S: Capacidades  maximas de las plantas.
    list H: Capacidades maximas de manejo de procuctos del centros.
    list R: Demandas de las zonas.
    int p_max: Limite de centros simultaneos.
    list F: Costos fijos de habilitación de los centros.
    list C: Matriz de los costos de las plantas hacia los centros.
    list D: Matriz de los costos desde el centro de distribución hacia la 
        las zonas de demanda.
    --------------Return------------------
    void: No retorna nada.
    ----------------------------------
'''
def escribirMiniZinc(ruta_archivo, num_I, num_J, num_K, S, H, R, p_max, F, C, D):
    with open(ruta_archivo, 'w') as documento:
        # Tamaños de los conjuntos
        documento.write("Tamaño de los conjuntos I, J y K")
        documento.write(f"num_I = {num_I};\n")
        documento.write(f"num_J = {num_J};\n")
        documento.write(f"num_K = {num_K};\n\n")
        # Parámetros normales
        documento.write("Parametros:")
        documento.write(f"S = {S};\n")
        documento.write(f"H = {H};\n")
        documento.write(f"R = {R};\n")
        documento.write(f"p_max = {p_max};\n")
        documento.write(f"F = {F};\n\n")
        # Parámetros Matriciales
        documento.write("C = [|\n")
        for fila in C:
            documento.write("  " + ", ".join(map(str, fila)) + " |\n")
        documento.write("|];\n\n")
        
        documento.write("D = [|\n")
        for fila in D:
            documento.write("  " + ", ".join(map(str, fila)) + " |\n")
        documento.write("|];\n")

'''
    ------------Funcion-----------------
    generarInstancia: Funcion encargada de crear aleatoriamente los datos 
    de una sola instancia, aseguramndo que esta cumple con ser un modelo
    factible, y luego escribir en el documento instanciado usando
    "escribirMiniZinc".
    ------------Parametros----------------
    str tipo: tipo de rango de generacion de instancias 'Chica', 'Mediana' 
        o 'Grande'.
    int num: Identificador de la instancia que va del 1 al 5.
    str carpeta_objetivo: Carpeta donde se guardara.
    --------------Return------------------
    void: No retorna nada.
    ----------------------------------
'''
def generarInstancia(tipo, num, carpeta_objetivo):
     #--------------------------Generacion de conjuntos---------------------------
    if tipo == 'Chica':     
        num_I = random.randint(3, 10)
        num_J = random.randint(6, 12)
        num_K = random.randint(8, 15)
    elif tipo == 'Mediana':
        num_I = random.randint(11, 20)
        num_J = random.randint(12, 24)
        num_K = random.randint(16, 30)
    else: 
        num_I = random.randint(21, 35)
        num_J = random.randint(25, 40)
        num_K = random.randint(31, 45)

   #---------------------------Generación de parametros----------------------------
    # Demandas y demanda total
    R = []
    for _ in range(num_K):
        R.append(random.randint(50, 200))    
    demanda_total = sum(R)
    # Capacidades de plantas
    S = []
    for _ in range(num_I):
        S.append(random.randint(100, 500))
        
    # Ajustamos la capacidad de las plantas sumandole 50 si es que no cubre totalmente la demanda.
    while sum(S) <= demanda_total:
        for i in range(num_I):
            S[i] = S[i] + 50

    # Capacidades de CDs
    H = []
    for _ in range(num_J):
        H.append(random.randint(150, 600))

    #Ajustamos la capacidad de Cds aumentando le 50 si es que son muy pequeños para ello flujo de demandas
    H_ordenado = sorted(H, reverse=True)
    while sum(H_ordenado[:p_max]) <= demanda_total:
        for i in range(num_J):
            H[i] = H[i] + 50
        H_ordenado = sorted(H, reverse=True)
    
    # Numero maximo de CDs simultaneos, para evita soluciones triviales debe ser menor al total de CD disponibles
    p_max = random.randint(max(2, num_J // 3), num_J - 1)

    # Costos de transporte (Matrices)
    C = []
    for _ in range(num_I):
        fila_C = []
        for j in range(num_J):
            fila_C.append(random.randint(10, 100))
        C.append(fila_C)

    D = []
    for _ in range(num_J):
        fila_D = []
        for k in range(num_K):
            fila_D.append(random.randint(10, 100))
        D.append(fila_D)

    #Costos fijos (Deben ser relevantes frente al transporte)
    F = []
    for _ in range(num_J):
        F.append(random.randint(2000, 8000))

    # ----------------------------------Guardado---------------------------------------
    nombre_archivo = f"instancia_{tipo.lower()}_{num}.dzn"
    ruta_completa = os.path.join(carpeta_objetivo, nombre_archivo)
    
    escribirMiniZinc(ruta_completa, num_I, num_J, num_K, S, H, R, p_max, F, C, D)

def main():
    #------------------Inicializacion---------------------------
    carpeta_objetivo_destino = "Instancias"
    
    # Definimos los tipos de instancias requeridos
    tipos_instancias = ['Chica', 'Mediana', 'Grande']

    #------------------Procesamiento---------------------------
    print("Generamos las intancias")
    
    total_generadas = 0
    for tipo in tipos_instancias:
        # Se solicitan 5 instancias por cada dimensionalidad
        for i in range(1, 6):
            generarInstancia(tipo, i, carpeta_objetivo_destino)
            total_generadas += 1
            
    print(f"Proceso finalizado. Se generaron {total_generadas} instancias en '{carpeta_objetivo_destino}'.")

#Pal makefile
if __name__ == "__main__":
    main()
