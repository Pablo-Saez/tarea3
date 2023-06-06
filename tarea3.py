

import os
from pathlib import Path
from os import path


#Creacion del arbol para el fyle system
class TreeNode:
    def __init__(self):
        self.nombre_carpeta= 'a'
        self.ruta = ''
        
        self.children = []
        self.parent = None
        

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level
    def getRuta (self):
        return self.ruta
   
    def setRuta(self,ruta):
        self.ruta = ruta    
    def getNombreCarpeta(self):
        return self.nombre_carpeta
   
    def setNombreCarpeta(self,nombre_carpeta):
        self.nombre_carpeta = nombre_carpeta 
    
    def verHijos(self):
        
        if self.children:
            print(".: "+ self.getNombreCarpeta())
            for hijos in self.children:
                print(hijos.getNombreCarpeta())
                
            for hijos in self.children:
                hijos.verHijos()
        else:
            nombre = self.getNombreCarpeta()
            aux = nombre.split('.')
            if(len(aux)!=2):
                print('./'+nombre+": \n")

        


    
    

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.ruta)
        if self.children:
            for child in self.children:
                child.print_tree()
    
    def mostrarDatos(self):
        print("ruta:  " + self.ruta )
        print("nombre:" + self.nombre_carpeta)
        
    def lsRecursivo(self,ruta):
        
        if(self.getRuta()==ruta):
            self.verHijos()    
        
        elif self.children:
            for hijo in self.children:
                if(hijo.getRuta()==ruta):
                    hijo.verHijos()
                    break
                else:
                    hijo.lsRecursivo(ruta)
                
        
                    

        
    def existeRuta(self,child):
        
        if self.children:
            for hijo in self.children:      
                if(hijo.getRuta()==child.getRuta()):
                    #print("entroo")
                    return True
                else:
                    a=hijo.existeRuta(child)
                    if(a):
                        return True

    def existeHijo(self,child,nombre):
        
        if self.children:
            for hijo in self.children:      
                if(hijo.getRuta()==child.getRuta()):
                    # print("entro 1")
                    # print(hijo.getNombreCarpeta())
                    # print(nombre)
                    if(hijo.getNombreCarpeta()==nombre):
                        #print("entro 2")
                        return True
                else:
                    a=hijo.existeHijo(child,nombre)
                    if(a):
                        return True

        return False 

    def CambiarNombre(self,child,nombre,nueva_ruta):
        #print("xd")
        if self.children:
            for hijo in self.children:
                # print(hijo.getRuta())
                # print(child.getRuta())      
                if(hijo.getRuta()==child.getRuta()):
                    hijo.setNombreCarpeta(nombre)
                    print("nombre cambiado")
                    hijo.setRuta(nueva_ruta)
                    return True
                        
                else:
                    a=hijo.CambiarNombre(child,nombre,nueva_ruta)
                    if(a):
                        return True

        return False    


    def recorrer_arbol(self):
        print(self.mostrarDatos())
        if self.children:
            for hijo in self.children:
                hijo.mostrarDatos()
                hijo.recorrer_arbol()

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def add_child2(self,child):
        ruta = child.getRuta()
        ruta_split = ruta.split('/')
        lenght = len(ruta_split)

        ruta_padre = self.getRuta()
        ruta_split_padre = ruta_padre.split('/')
        lenght_padre = len(ruta_split_padre)
        flag = True
        for i in range (0,lenght_padre):
            if(ruta_split[i]==ruta_split_padre[i]):
                continue
            else:
                flag= False
                break
        if(lenght-lenght_padre==1 and flag):
            child.parent= self
            self.children.append(child)

            print("nodo agregado")
           
        else:
            if self.children:
                for hijos in self.children:
                    hijos.add_child2(child)



if __name__ == '__main__':
    ruta_base = os.getcwd()
    root = TreeNode()
    root.setRuta(ruta_base)
    flag = True
    
    while(flag):
        
        opcion_orignial = input(ruta_base+"$ ")
        opcion=opcion_orignial.split(' ')
        parametros= len(opcion)
        if(parametros == 1):
            if(opcion[0]=='ls'):
                #aux = os.listdir('/home/pablosky/Escritorio/sistemas_operativos/tarea3')
                #print(path.abspath('tarea3.py'))
                directorios= os.listdir(ruta_base) 
                print(directorios)
            elif(opcion[0]=='exit'):
                flag=False
                
                
            elif(opcion[0]=='ver'):
                root.print_tree()
        else:
            if(opcion[0]=='ls' and opcion[1]=='-R'):
            
                root.lsRecursivo(ruta_base)
                
            elif(opcion[0]=='mkdir'):
                path_aux = path.join(ruta_base,opcion[1])
                nodo = TreeNode()
                nodo.setRuta(path_aux)
                nodo.setNombreCarpeta(opcion[1])
                root.add_child2(nodo)
                #print(path_aux)
                os.mkdir(path_aux)

            elif(opcion[0]=='cd' and opcion[1]!='..'): ##cd algo
                path_aux= path.join(ruta_base,opcion[1])
                nodo_prueba = TreeNode()
                nodo_prueba.setRuta(path_aux)
                #print("ruta desde el main: " +path_aux)
                valor = root.existeRuta(nodo_prueba)
                #print(valor)
                if(valor):
                    #nodo_prueba.setRuta(path_aux)
                    ruta_base=path.join(ruta_base,opcion[1])
                    #print("la nueva ruta es " + ruta_base)
                else:
                    print("bash: cd : "+ opcion[1]+": No existe el archivo o directorio")

            elif(opcion[0]=='cd' and opcion[1]=='..'):
                aux= ruta_base.split('/')
                size = len(aux)
                size2 = len(aux[size-1])
                ruta_base = ruta_base[0:len(ruta_base)-size2-1]
            
            elif(opcion[0]== 'rm'):
                aux = opcion[1].split('.')
                if(len(aux)!=2):
                    print("rm: no se puede borrar '"+opcion[1]+"': Es un directorio")
                else:
                    path_aux= path.join(ruta_base,opcion[1])
                    nodo_prueba = TreeNode()
                    nodo_prueba.setRuta(path_aux)
                    valor = root.existeRuta(nodo_prueba)
                    if(valor):
                        os.remove(path_aux)
                    else:
                        print("rm: fallo al borrar '"+opcion[1]+"': No existe el archivo o directorio")
            elif(opcion[0]=='rmdir'):
                path_aux= path.join(ruta_base,opcion[1])
                nodo_prueba = TreeNode()
                nodo_prueba.setRuta(path_aux)
                valor = root.existeRuta(nodo_prueba)
                if(valor):
                    os.rmdir(path_aux)
                else:
                    print("rmdir: fallo al borrar '"+opcion[1]+"': No existe el archivo o directorio")
            
            elif(opcion[0]=='ls' and opcion[1]=='-i'):
                with os.scandir(ruta_base) as itr:
                    for entry in itr :
                        if not entry.name.startswith('.') :
                            print(entry.name, " :", entry.inode())

            elif(opcion[0]=='mv'):
                #caso en que quiera renombrarlo
                #primero hay que ver si existe el arvhio
                path_aux = path.join(ruta_base,opcion[1])
                nueva_ruta = path.join(ruta_base,opcion[2])
                
                nodo_prueba = TreeNode()
                nodo_prueba.setRuta(path_aux)
                valor = root.existeHijo(nodo_prueba,opcion[1])
                if(valor):
                    root.CambiarNombre(nodo_prueba,opcion[2],nueva_ruta)





            

                
                

                
                
                
                

            

            elif(opcion[0]=='touch'):
                path_aux = path.join(ruta_base,opcion[1])
                nodo = TreeNode()
                nodo.setNombreCarpeta(opcion[1])
                nodo.setRuta(path_aux)
                root.add_child2(nodo)
                Path(path_aux).touch()
            



            
            


       