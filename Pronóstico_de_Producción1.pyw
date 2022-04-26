from cmath import e
from turtle import clear
import numpy as np
import pandas as pd
import datetime as datetime
from datetime import timedelta
import time
import matplotlib.pyplot as plt
import csv
from distutils import command
from tkcalendar import Calendar 
import itertools
from cProfile import label
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import tkinter
from tkinter.tix import Tree
from tkcalendar import Calendar, DateEntry
from matplotlib.pyplot import title

#RESUMEN: pronóstico a partir de base de datos sql (continuidad, pozos nuevos, interferencia), excel (cierre pozos) y txt (pozos tipo), no incluye ajuste a demanda ni ventana carga de datos

#### VENTANA PRINCIPAL 'ROOT' #####
root = tkinter.Tk()
root.title("Data intro")
nb = ttk.Notebook(root)
root.geometry("620x550")
nb.pack(fill='both',expand='yes')
###########################################################################
#################### VENTANA 1 -POZOS CONTINUIDAD-#########################
###########################################################################

ventana1=ttk.Frame(nb)

miID1=StringVar()
miPozo1=StringVar()
miDna=StringVar()
mib=StringVar()
miFechainicio=StringVar()
miCaudalinicial=StringVar()

def conexionBaseDato1():
    miConexion=sqlite3.connect("BaseContinuidad")
    miCursor=miConexion.cursor()

    try:
        miCursor.execute('''
            CREATE TABLE continuidad (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Pozo VARCHAR(50) NOT NULL,
            Dna INT NOT NULL,
            b INT NOT NULL,
            Fecha_Inicio DATE NOT NULL,
            Caudal_Inicial INT NOT NULL)
            ''')
        messagebox.showinfo("CONEXION","Base de datos creada exitosamente")
    except:
        messagebox.showinfo("CONEXION","Conexión exitosa con la base de datos")

def eliminarBaseDato1():
    miConexion=sqlite3.connect("BaseContinuidad")
    miCursor=miConexion.cursor()
    if messagebox.askquestion(message="Los datos se perderán definitivamente, ¿Desea Continuar?",title="ADVERTENCIA"):
        miCursor.execute("DROP TABLE continuidad ")
    else:
        pass

def limpiarCampos1():
    miID1.set("")
    miPozo1.set("")
    mib.set("")
    miFechainicio.set("")
    miCaudalinicial.set("")
    miDna.set("")
def mensaje():
    acerca='''
    El cauda pronóstico es calculado con la siguiente función de Declinación Hiperbólica:
    q(t)=qi/((1+b*D*t)^(1/b))
    '''
    messagebox.showinfo(title="INFORMACIÓN", message=acerca)

 ########### Métodos ###############

def crear1():
    miConexion=sqlite3.connect("BaseContinuidad")
    miCursor=miConexion.cursor()
    try:
        datos= miPozo1.get(), miDna.get(),mib.get(),miFechainicio.get(),miCaudalinicial.get()
        miCursor.execute("INSERT INTO continuidad VALUES (NULL,?,?,?,?,?)",(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrió un error al crear el registro, verifique conexión con base de datos")
        pass
    limpiarCampos1()
    mostrar1()
    
def mostrar1():
    miConexion=sqlite3.connect("BaseContinuidad")
    miCursor=miConexion.cursor()
    resgistros=tree1.get_children()
    for elemento in resgistros:
        tree1.delete(elemento)
    try:
        miCursor.execute("SELECT*FROM continuidad")
        for row in miCursor:
            tree1.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5]))
    except:
        pass

#############TABLA1############
tree1=ttk.Treeview(ventana1,height=15,columns=('#0','#1','#2','#3','#4'))
tree1.place(x=0,y=170)
tree1.column('#0',width=50)
tree1.heading('#0',text="ID",anchor=CENTER)
tree1.heading('#1',text="Pozo",anchor=CENTER)
tree1.column('#1',width=130)
tree1.heading('#2',text="Dna",anchor=CENTER)
tree1.column('#2',width=80)
tree1.heading('#3',text="b",anchor=CENTER)
tree1.column('#3',width=80)
tree1.heading('#4',text="Fecha Inicio",anchor=CENTER)
tree1.column('#4',width=120)
tree1.heading('#5',text="Caudal Inicial",anchor=CENTER)
tree1.column('#5',width=140)

def seleccionarUsandoClick1(event):
    item=tree1.identify('item',event.x,event.y)
    miID1.set(tree1.item(item,"text"))
    miPozo1.set(tree1.item(item,"values")[0])
    miDna.set(tree1.item(item,"values")[1])
    mib.set(tree1.item(item,"values")[2])
    miFechainicio.set(tree1.item(item,"values")[3])
    miCaudalinicial.set(tree1.item(item,"values")[4])
tree1.bind("<Double-1>",seleccionarUsandoClick1)



def actualizar1():
    miConexion=sqlite3.connect("BaseContinuidad")
    miCursor=miConexion.cursor()
    try:
        datos=miPozo1.get(),miDna.get(),mib.get(),miFechainicio.get(),miCaudalinicial.get()
        miCursor.execute("UPDATE continuidad SET Pozo=?, Dna=?, b=?, Fecha_Inicio=?, Caudal_Inicial=? WHERE ID="+miID1.get(),(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrió un error al actualizar el registro")
        pass
    limpiarCampos1()
    mostrar1()

def borrar1():
    miConexion=sqlite3.connect("BaseContinuidad")
    miCursor=miConexion.cursor()
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?",title="ADVERTENCIA"):
            miCursor.execute("DELETE FROM continuidad WHERE ID="+miID1.get())
            miConexion.commit()
    except:
         messagebox.showwarning("ADVERTENCIA","Ocurrió un error al tratar de eliminar el registro")
         pass
    limpiarCampos1()
    mostrar1()

########## Creando etiquetas y cajas de texto #################
e11=Entry(ventana1,textvariable=miID1)

l21=Label(ventana1,text="Pozo",bg="#D6DADD")
l21.place(x=50,y=10)
e21=Entry(ventana1,textvariable=miPozo1, width=50)
e21.place(x=140,y=10)

l31=Label(ventana1,text="Dna",bg="#D6DADD")
l31.place(x=50,y=40)
e31=Entry(ventana1,textvariable=miDna)
e31.place(x=140,y=40)

l41=Label(ventana1,text="b",bg="#D6DADD")
l41.place(x=300,y=40)
e41=Entry(ventana1,textvariable=mib, width=10)
e41.place(x=320,y=40)

l51=Label(ventana1,text="Fecha Inicio",bg="#D6DADD")
l51.place(x=50,y=70)
e51=DateEntry(ventana1,textvariable=miFechainicio, width=30)
e51.place(x=140,y=70)

l61=Label(ventana1,text="Caudal Inicial",bg="#D6DADD")
l61.place(x=50,y=100)
e61=Entry(ventana1,textvariable=miCaudalinicial, width=50)
e61.place(x=140,y=100)


############ Creando botones ##########

b11=Button(ventana1, text="Crear Registro",bg="#ABEBC6", command=crear1)
b11.place(x=50,y=130)
b21=Button(ventana1, text="Modificar Registro", command=actualizar1)
b21.place(x=180,y=130)
b31=Button(ventana1, text="Mostrar Lista", command=mostrar1)
b31.place(x=320,y=130)
b41=Button(ventana1, text="Eliminar Registro", bg="#F1948A",command=borrar1)
b41.place(x=450,y=130)

#####################################################################################
############################  VENTANA 2 -POZOS NUEVOS- ##############################
#####################################################################################
ventana2=ttk.Frame(nb)
df1 = pd.read_csv(r'C:\Users\t01hkruteler\Desktop\Prono Producción Py\PozosTipo.txt', header=0)
df1=df1.astype(float,errors='raise')
df1=df1.round(1)
nombreColumnas=df1.columns.values
nombreColumnas=list(nombreColumnas)
nombreColumnas.insert(0,'*Seleccione Pozo Tipo*')
miID2=StringVar()
miPozo2=StringVar()
miFechaPEM=StringVar()
miPozoTipo=StringVar()
miPozoTipo.set(nombreColumnas[0])
miFactor=IntVar()
miFactor.set(1)
miComentario=StringVar()


def conexionBaseDato2():
    miConexion=sqlite3.connect("BasePozosNuevos")
    miCursor=miConexion.cursor()

    try:
        miCursor.execute('''
            CREATE TABLE pozos_nuevos (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Pozo2 VARCHAR(20) NOT NULL,
            FechaPEM DATE NOT NULL,
            PozoTipo INT NOT NULL,
            Factor INT NOT NULL,
            Comentario VARCHAR(20))
            ''')
        messagebox.showinfo("CONEXION","Base de datos creada exitosamente")
    except:
        messagebox.showinfo("CONEXION","Conexión exitosa con la base de datos")

def eliminarBaseDato2():
    miConexion=sqlite3.connect("BasePozosNuevos")
    miCursor=miConexion.cursor()
    if messagebox.askquestion(message="Los datos se perderán definitivamente, ¿Desea Continuar?",title="ADVERTENCIA"):
        miCursor.execute("DROP TABLE pozos_nuevos ")
    else:
        pass

def limpiarCampos2():
    miID2.set("")
    miPozo2.set("")
    miFechaPEM.set("")
    miPozoTipo.set("")
    miFactor.set(1)
    miComentario.set("")

def mensaje2():
    acerca='''
    Agregar info necesaria para pozos nuevos
    '''
    messagebox.showinfo(title="INFORMACIÓN", message=acerca)

 ########### Métodos #############

def crear2():
    miConexion=sqlite3.connect("BasePozosNuevos")
    miCursor=miConexion.cursor()

    comentario=miComentario.get()
    if comentario=='Agregue comentario' or comentario=='':
          comentario='Sin comentario'
    else:
        comentario=miComentario.get()


    try:
        datos= miPozo2.get(), miFechaPEM.get(),miPozoTipo.get(),miFactor.get(), comentario
        miCursor.execute("INSERT INTO pozos_nuevos VALUES (NULL,?,?,?,?,?)",(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrió un error al crear el registro, verifique conexión con base de datos")
        pass
    limpiarCampos2()
    mostrar2()
def mostrar2():
    miConexion=sqlite3.connect("BasePozosNuevos")
    miCursor=miConexion.cursor()
    registros=tree2.get_children()
    for elemento in registros:
        tree2.delete(elemento)
    try:
        miCursor.execute("SELECT*FROM pozos_nuevos")
        for row in miCursor:
            tree2.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5]))
    except:
        pass

#############TABLA2##############

tree2=ttk.Treeview(ventana2,height=15,columns=('#0','#1','#2','#3','#4'))
tree2.place(x=2,y=160)
tree2.column('#0',width=50)
tree2.heading('#0',text="ID",anchor=CENTER)
tree2.heading('#1',text="Pozo",anchor=CENTER)
tree2.column('#1',width=150)
tree2.heading('#2',text="Fecha de PEM",anchor=CENTER)
tree2.column('#2',width=140)
tree2.heading('#3',text="Pozo Tipo",anchor=CENTER)
tree2.column('#3',width=150)
tree2.heading('#4',text="Factor",anchor=CENTER)
tree2.column('#4',width=80)
tree2.heading('#5',text="Comentario",anchor=CENTER)
tree2.column('#5',width=320)


def seleccionarUsandoClick2(event):
    item=tree2.identify('item',event.x,event.y)
    miID2.set(tree2.item(item,"text"))
    miPozo2.set(tree2.item(item,"values")[0])
    miFechaPEM.set(tree2.item(item,"values")[1])
    miPozoTipo.set(tree2.item(item,"values")[2])
    miFactor.set(tree2.item(item,"values")[3])
    miComentario.set(tree2.item(item,"values")[4])
tree2.bind("<Double-1>",seleccionarUsandoClick2)

def actualizar2(): #error en el try linea miCursor
    miConexion=sqlite3.connect("BasePozosNuevos")
    miCursor=miConexion.cursor()
    try:
        datos=miPozo2.get(),miFechaPEM.get(),miPozoTipo.get(),miFactor.get(),miComentario.get()
        miCursor.execute("UPDATE pozos_nuevos SET Pozo2=?, FechaPEM=?, PozoTipo=?, Factor=?, Comentario=? WHERE ID="+miID2.get(),(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrió un error al actualizar el registro")
        pass
    limpiarCampos2()
    mostrar2()

def borrar2():
    miConexion=sqlite3.connect("BasePozosNuevos")
    miCursor=miConexion.cursor()
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?",title="ADVERTENCIA"):
            miCursor.execute("DELETE FROM pozos_nuevos WHERE ID="+miID2.get())
            miConexion.commit()
    except:
         messagebox.showwarning("ADVERTENCIA","Ocurrió un error al tratar de eliminar el registro")
         pass
    limpiarCampos2()
    mostrar2()

#############
############# --- Ventana Pozos Tipo
#############

def VerRegistroPT():
        df1.index.name='Dia'
        root=Tk()
        root.title("Pozos Tipo")
        root.geometry("700x440")

        table = Text(root)
        table.insert(INSERT, df1.to_string())
        table.pack()
        scrolly = tkinter.Scrollbar(root, command=table.yview, width=14)
        scrolly.place(in_=table, relx=1, relheight=1, bordermode="outside")
        
        table.config(bg="#5E91CD", border=3, fg="#FDFEFE", state="normal",
                     relief=tkinter.FLAT, yscrollcommand=scrolly.set, undo=True
                     )
        root.mainloop()

def CrearRegistroPT():
    NmbrPT=StringVar()
    root=Toplevel()
    root.title("Carga de Pozos Tipo")
    root.geometry("350x460")
    lpt=Label(root,text="Nombre Pozo Tipo")
    lpt.place(x=10,y=10)
    lmnj=Label(root,text="*Pegue la columna de valores \n sin el encabezado*")
    lmnj.place(x=10,y=420)
    lmnj.configure(font=("Arial", 8, "italic"))
    ept=Entry(root,textvariable=NmbrPT, width=30)
    ept.place(x=140,y=10)
    table = Text(root)
    table.place(x=10,y=40)
    table.configure(height=23,width=40)
    scrollv = tkinter.Scrollbar(root, command=table.yview, width=14)
    scrollv.place(in_=table, relx=1, relheight=1, bordermode="outside")
    table.config(bg="#5E91CD", border=3, fg="#FDFEFE", state="normal",
                     relief=tkinter.FLAT, yscrollcommand=scrollv.set, undo=True
                     )

    def tomarDato():
            mi_variable = table.get(1.0, 'end')
            df2=mi_variable.split('\n')
            df2=pd.DataFrame(df2)         
            df2.columns=[ept.get()]
            df3=df1.join(df2)
            df3.to_csv(r'C:\Users\t01hkruteler\Desktop\Prono Producción Py\PozosTipo.txt', index=False)
            bGuardar.configure(bg="#87F96D", text='Cargado', fg='#851F0B')
    bGuardar=Button(root, text="Cargar",fg='#25468B',width=10,command=tomarDato)
    bGuardar.place(x=260,y=420)
    root.mainloop()

def ventanaPozosTipo():
    ventanaPT=Toplevel()
    ventanaPT.title("Pozos Tipo")
    ventanaPT.geometry("250x100")
    bVer=Button(ventanaPT, text="Ver Registro Pozos Tipo  ",bg='#FDEBD0',command=VerRegistroPT)
    bVer.place(x=50,y=10)
    bCargar=Button(ventanaPT, text="Cargar Nuevo Pozo Tipo",bg='#F5CBA7',command=CrearRegistroPT)
    bCargar.place(x=50,y=40)
    ventanaPT.mainloop()
########## Creando etiquetas y cajas de texto #################

e12=Entry(ventana2,textvariable=miID2)

l22=Label(ventana2,text="Pozo",bg="#D6DADD")
l22.place(x=50,y=10)
e22=Entry(ventana2,textvariable=miPozo2, width=30)
e22.place(x=180,y=10)

l32=Label(ventana2,text="Fecha de PEM",bg="#D6DADD")
l32.place(x=50,y=40)
e32=DateEntry(ventana2,textvariable=miFechaPEM)
e32.place(x=180,y=40)

l42=Label(ventana2,text="Pozo Tipo",bg="#D6DADD")
l42.place(x=380,y=40)
e42=ttk.Combobox(ventana2,textvariable=miPozoTipo)
e42['values']=nombreColumnas
e42.place(x=450,y=40)

l52=Label(ventana2,text="Factor de conversión",bg="#D6DADD")
l52.place(x=50,y=70)
e52=Entry(ventana2,textvariable=miFactor, width=10)
e52.place(x=180,y=70)

e62=Entry(ventana2, textvariable=miComentario, width=35)
e62.place(x=375,y=70, height=30)
e62.insert(0, "Agregue comentario",)
e62.configure(font=("Arial", 8, "italic"))
############ Creando botones ##########

b12=Button(ventana2, text="Crear Registro",bg="#ABEBC6", command=crear2)
b12.place(x=50,y=120)
b22=Button(ventana2, text="Modificar Registro", command=actualizar2)
b22.place(x=180,y=120)
b32=Button(ventana2, text="Mostrar Lista", command=mostrar2)
b32.place(x=320,y=120)
b42=Button(ventana2, text="Eliminar Registro", bg="#F1948A",command=borrar2)
b42.place(x=450,y=120)

bPT=Button(ventana2, text="Ver/Cargar Pozo Tipo",bg='#FDEBD0',command=ventanaPozosTipo)
bPT.place(x=465,y=10)

#####################################################################################
############################ VENTANA3 -INTERFERENCIA-################################
#####################################################################################
ventana3=ttk.Frame(nb)

miPresión=IntVar()
miDistancia=IntVar()
miDiasPreviosCierre= IntVar()
miPozo3=StringVar()
miFechaInicio3=StringVar()
miFechaFin3=StringVar()
miPozoInterf=StringVar()
miFechaCierre3=StringVar()
miFechaApertura3=StringVar()
miID3=StringVar()

def conexionBaseDato3():
    miConexion=sqlite3.connect("BaseInterferencia")
    miCursor=miConexion.cursor()

    try:
        miCursor.execute('''
            CREATE TABLE interferencia (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Pozo VARCHAR(50) NOT NULL,
            FechaInicio DATE NOT NULL,
            FechaFin DATE NOT NULL,
            PozoInterferido VARCHAR(50) NOT NULL,
            Distancia INT NOT NULL,
            Presion INT NOT NULL,
            DiasPreviosCierre INT NOT NULL,
            FechaCierre DATE NOT NULL,
            FechaApertura DATE NOT NULL)
            ''')
        messagebox.showinfo("CONEXION","Base de datos creada exitosamente")
    except:
        messagebox.showinfo("CONEXION","Conexión exitosa con la base de datos")

def eliminarBaseDato3():
    miConexion=sqlite3.connect("BaseInterferencia")
    miCursor=miConexion.cursor()
    if messagebox.askquestion(message="Los datos se perderán definitivamente, ¿Desea Continuar?",title="ADVERTENCIA"):
        miCursor.execute("DROP TABLE interferencia ")
    else:
        pass
def salirAplicacion3():
    valor=messagebox.askquestion("Salir",'¿Está seguro que desea salir de la Aplicación?')
    if valor=="yes":
        ventana3.destroy()
def limpiarCampos3():
    miID3.set("")
    miPresión.set("")
    miDistancia.set("")
    miDiasPreviosCierre.set("")
    miPozo3.set("")
    miFechaInicio3.set("")
    miFechaFin3.set("")
    miPozoInterf.set("")
    miFechaCierre3.set("")
    miFechaApertura3.set("")
def mensaje3():
    ventanaExtra=Toplevel()
    ventanaExtra.title("info interferencia")
    ventanaExtra.geometry("450x250")
    img_gif = tkinter.PhotoImage(file = r'C:\Users\t01hkruteler\Documents\info y pruebas OBJET PEV\Pruebas\Interfaces y Bases\inter_gif.gif')
    label_img = Label(ventanaExtra, image = img_gif)
    label_img.place(x=50,y=60)
    texto=Label(ventanaExtra,text='El cálculo de días previos de cierre recomendados se basó en la siguiente tabla: ')
    texto.place(x=10,y=30)
    ventanaExtra.mainloop()

 ########### Métodos ###############

def crear3():
    miConexion=sqlite3.connect("BaseInterferencia")
    miCursor=miConexion.cursor()
    tabla = pd.DataFrame ({0:[30,30,30,15],100:[15,15,10,2], 200:[1,1,1,1],300:[1,1,1,1]})
    lista_p = list(tabla)
    lista_d = [0,200,300,400]
    tabla.index = lista_d
#busqueda de columna
    max_p = max(lista_p)
    if miPresión.get() > max_p:
        c = lista_p.index(max_p)
    else:
        for i in range(len(lista_p)):
            if miPresión.get() > lista_p[i] and miPresión.get() <= lista_p[i+1]:
                c=i
#busqueda de fila
    max_d = max(lista_d)
    if miDistancia.get() > max_d:
        f = lista_d.index(max_d)
    else:
        for x in range(len(lista_d)):
            if miDistancia.get() > lista_d[x] and miDistancia.get() <= lista_d[x+1]:
                f=x
    tiempo = tabla.loc[lista_d[f],lista_p[c]]
    miDiasPreviosCierre.set(tiempo)

    fecha1=datetime.datetime.strptime(miFechaInicio3.get(), "%m/%d/%y")
    fecha2=fecha1-timedelta(miDiasPreviosCierre.get())
    miFechaCierre3=datetime.datetime.strftime(fecha2, "%m/%d/%y")
    try:
        datos= miPozo3.get(),miFechaInicio3.get(),miFechaFin3.get(),miPozoInterf.get(),miDistancia.get(),miPresión.get(), miDiasPreviosCierre.get(),miFechaCierre3,miFechaFin3.get()
        miCursor.execute("INSERT INTO interferencia VALUES (NULL,?,?,?,?,?,?,?,?,?)",(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrió un error al crear el registro, verifique conexión con base de datos")
        pass
    limpiarCampos3()
    mostrar3()
    
def mostrar3():
    miConexion=sqlite3.connect("BaseInterferencia")
    miCursor=miConexion.cursor()
    registros=tree3.get_children()
    for elemento in registros:
        tree3.delete(elemento)
    try:
        miCursor.execute("SELECT*FROM interferencia")
        for row in miCursor:
            tree3.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
    except:
        pass

#############TABLA############

tree3=ttk.Treeview(ventana3, height=17, columns=('#0','#1','#2','#3','#4','#5','#6','#7','#8'))
tree3.place(x=0,y=140)
tree3.column('#0',width=50)
tree3.heading('#0',text="ID",anchor=CENTER)
tree3.heading('#1',text="Pozo",anchor=CENTER)
tree3.column('#1',width=100)
tree3.heading('#2',text="Fecha Inicio",anchor=CENTER)
tree3.column('#2',width=90)
tree3.heading('#3',text="Fecha Fin",anchor=CENTER)
tree3.column('#3',width=90)
tree3.heading('#4',text="Pozo Interferido",anchor=CENTER)
tree3.column('#4',width=100)
tree3.heading('#5',text="Distancia [m]",anchor=CENTER)
tree3.column('#5',width=60)
tree3.heading('#6',text="Presión [kg/cm2]",anchor=CENTER)
tree3.column('#6',width=80)
tree3.heading('#7',text="Días Previos de Cierre",anchor=CENTER)
tree3.column('#7',width=120)
tree3.heading('#8',text="Fecha de Cierre",anchor=CENTER)
tree3.column('#8',width=100)
tree3.heading('#9',text="Fecha de Apertura",anchor=CENTER)
tree3.column('#9',width=110)

def seleccionarUsandoClick3(event):
    item=tree3.identify('item',event.x,event.y)
    miID3.set(tree3.item(item,"text"))
    miPresión.set(tree3.item(item,"values")[5])
    miDistancia.set(tree3.item(item,"values")[4])
    miDiasPreviosCierre.set(tree3.item(item,"values")[6])
    miPozo3.set(tree3.item(item,"values")[0])
    miFechaInicio3.set(tree3.item(item,"values")[1])
    miFechaFin3.set(tree3.item(item,"values")[2])
    miPozoInterf.set(tree3.item(item,"values")[3])
    miFechaCierre3.set(tree3.item(item,"values")[7])
    miFechaApertura3.set(tree3.item(item,"values")[8])
tree3.bind("<Double-1>",seleccionarUsandoClick3)

def actualizar3():
    miConexion=sqlite3.connect("BaseInterferencia")
    miCursor=miConexion.cursor()
    tabla = pd.DataFrame ({0:[30,30,30,15],100:[15,15,10,2], 200:[1,1,1,1],300:[1,1,1,1]})
    lista_p = list(tabla)
    lista_d = [0,200,300,400]
    tabla.index = lista_d
#busqueda de columna
    max_p = max(lista_p)
    if miPresión.get() > max_p:
        c = lista_p.index(max_p)
    else:
        for i in range(len(lista_p)):
            if miPresión.get() > lista_p[i] and miPresión.get() <= lista_p[i+1]:
                c=i
#busqueda de fila
    max_d = max(lista_d)
    if miDistancia.get() > max_d:
        f = lista_d.index(max_d)
    else:
        for x in range(len(lista_d)):
            if miDistancia.get() > lista_d[x] and miDistancia.get() <= lista_d[x+1]:
                f=x
    tiempo = tabla.loc[lista_d[f],lista_p[c]]
    miDiasPreviosCierre.set(tiempo)
    fecha1=datetime.datetime.strptime(miFechaInicio3.get(), "%m/%d/%y")
    fecha2=fecha1-timedelta(miDiasPreviosCierre.get())
    miFechaCierre3=datetime.datetime.strftime(fecha2, "%m/%d/%y")
    try:
        datos=miPozo3.get(),miFechaInicio3.get(),miFechaFin3.get(),miPozoInterf.get(),miDistancia.get(),miPresión.get(), miDiasPreviosCierre.get(),miFechaCierre3,miFechaFin3.get()
        miCursor.execute("UPDATE interferencia SET Pozo=?, FechaInicio=?, FechasFin=?, PozoInterferido=?, Distancia=?, Presion=?, PozoInterferido=?, FechaCierre=?, FechaApertura=? WHERE ID="+miID3.get(),(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrió un error al actualizar el registro")
        pass
    limpiarCampos3()
    mostrar3()

def borrar3():
    miConexion=sqlite3.connect("BaseInterferencia")
    miCursor=miConexion.cursor()
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?",title="ADVERTENCIA"):
            miCursor.execute("DELETE FROM interferencia WHERE ID="+miID3.get())
            miConexion.commit()
    except:
         messagebox.showwarning("ADVERTENCIA","Ocurrió un error al tratar de eliminar el registro")
         pass
    limpiarCampos3()
    mostrar3()

############## Colocar elementos (widgets) en la vista ############
########## Creando etiquetas y cajas de texto #################
e13=Entry(ventana3,textvariable=miID3)

l23=Label(ventana3,text="Pozo",bg="#D6DADD")
l23.place(x=50,y=20)
e23=Entry(ventana3,textvariable=miPozo3, width=25)
e23.place(x=150,y=20)

l33=Label(ventana3,text="Fecha Inicio",bg="#D6DADD")
l33.place(x=320,y=20)
e33=DateEntry(ventana3,textvariable=miFechaInicio3, width=20)
e33.place(x=400,y=20)

l43=Label(ventana3,text="Fecha Fin",bg="#D6DADD")
l43.place(x=580,y=20)
e43=DateEntry(ventana3,textvariable=miFechaFin3, width=20)
e43.place(x=650,y=20)

l53=Label(ventana3,text="Pozo Interferido",bg="#D6DADD")
l53.place(x=50,y=60)
e53=Entry(ventana3,textvariable=miPozoInterf, width=25)
e53.place(x=150,y=60)

l73=Label(ventana3,text="Distancia [m]",bg="#D6DADD")
l73.place(x=320,y=60)
e73=Entry(ventana3,textvariable=miDistancia, width=15)
e73.place(x=400,y=60)


l83=Label(ventana3,text="Presión [kg/cm2]",bg="#D6DADD")
l83.place(x=540,y=60)
e83=Entry(ventana3,textvariable=miPresión, width=15)
e83.place(x=650,y=60)

lroot=Label(root,text="(Los cambios se guardarán de manera automática)",bg="#D6DADD")
lroot.place(x=340,y=520)
lroot.configure(font=("Arial", 8, "italic"))
############ Creando botones ##########

b13=Button(ventana3, text="Crear Registro",bg="#ABEBC6", command=crear3)
b13.place(x=50,y=100)
b23=Button(ventana3, text="Modificar Registro", command=actualizar3)
b23.place(x=250,y=100)
b33=Button(ventana3, text="Mostrar Lista", command=mostrar3)
b33.place(x=450,y=100)
b43=Button(ventana3, text="Eliminar Registro", bg="#F1948A",command=borrar3)
b43.place(x=650,y=100)

########################################
############## Creando menus ###########
########################################
def salirAplicacion():
    valor=messagebox.askquestion("Salir",'¿Está seguro que desea salir de la Aplicación?')
    if valor=="yes":
        root.destroy()

menubar=Menu(root)
menubasedat=Menu(menubar,tearoff=0)
submenu1=Menu(menubar,tearoff=0)
submenu2=Menu(menubar,tearoff=0)

menubasedat.add_cascade(label="Crear/Conectar Base de Datos", menu=submenu1)
menubasedat.add_cascade(label="Eliminar Base de Datos", menu=submenu2)
menubasedat.add_command(label="Salir", command=salirAplicacion) 
menubar.add_cascade(label="Inicio",menu=menubasedat)

submenu1.add_command(label="BD Continuidad", command=conexionBaseDato1)
submenu1.add_command(label="BD Pozos Nuevos", command=conexionBaseDato2)
submenu1.add_command(label="BD Interferencia", command=conexionBaseDato3)

submenu2.add_command(label="BD Continuidad", command=eliminarBaseDato1)
submenu2.add_command(label="BD Pozos Nuevos", command=eliminarBaseDato2)
submenu2.add_command(label="BD Interferencia", command=eliminarBaseDato3)

ayudamenu=Menu(menubar,tearoff=0)
ayudamenu.add_command(label="Continuidad", command=mensaje)
ayudamenu.add_command(label="Pozos nuevos", command=mensaje2)
ayudamenu.add_command(label="Interferencias",command=mensaje3)
menubar.add_cascade(label="Información acerca de...",menu=ayudamenu)

################################################
######### BARRA DE DESPLAZAMIENTO ##############
################################################
##### VENTANA 1 ######
scroll1 = tkinter.Scrollbar(ventana1, orient="vertical", command=tree1.yview, width=14)
scroll1.place(in_=tree1, relx=1, relheight=1, bordermode="outside")
tree1.configure(yscrollcommand = scroll1.set)
##### VENTANA 2 ######
scroll2 = tkinter.Scrollbar(ventana2, orient="vertical", command=tree2.yview, width=14)
scroll2.place(in_=tree2, relx=1, relheight=1, bordermode="outside")
tree2.configure(yscrollcommand = scroll2.set)
##### VENTANA 3 ######
scroll3 = tkinter.Scrollbar(ventana3, orient="vertical", command=tree3.yview, width=14)
scroll3.place(in_=tree3, relx=1, relheight=1, bordermode="outside")
tree3.configure(yscrollcommand = scroll3.set)

################################################
#############Estilo a Treeview y ventana####################
style=ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
            background="#A3C9E5",
            foreground="black",
            rowheight=19,
            fieldbackground="silver")
style.map('TNotebook.Tab',
         background=[('selected','#0B76C2')])
settings = {"TNotebook.Tab": {"configure": {"padding": [5, 1],
                                            "background": "#B2D5EF"
                                            }}}  
def on_tab(event):
    global tab_styles
    global style
    nb = event.widget
    tab = nb.tab(nb.select(), "text")
    st = tab_styles[tab]
    style.map('TNotebook.Tab', **st)
tab_styles = {}
nb.pressed_index = None
tab_styles["Continuidad"] ={"background": [("selected", "#568EB7")],
                             "foreground": [("selected", "#ffffff")]
                            }
nb.add(ventana1, text ='Continuidad')
nb.add(ventana2, text ='Pozos Nuevos')
nb.add(ventana3, text ='Interferencia')
nb.bind("<<NotebookTabChanged>>", on_tab)
root.config(menu=menubar)
root.mainloop()
#####################################################################
###############-----VENTANA INPUN FECHA PRONO------##################
#####################################################################
ventana =tkinter.Tk() 
ventana.geometry("500x350")   
ventana.configure(background = "white")
etiqueta=tkinter.Label(ventana,text= "Ingrese fecha pronóstico", bg="#A3E4D7",font="Helvetica 10")
etiqueta.pack(fill=tkinter.X,expand=True)
cal = Calendar(ventana,background="#57A5A6", disabledbackground="black", bordercolor="black", 
               headersbackground="#A3E2E3", normalbackground="white", foreground='black', 
               normalforeground='black', headersforeground='black') 
cal.pack(pady = 20,fill="both",expand=True) 

def fechaProno():
    fecha=cal.get_date()
    fecha= datetime.datetime.strptime(fecha, "%m/%d/%y")
    fecha=datetime.datetime.strftime(fecha,"%m-%d-%Y")
    fecha=datetime.datetime.strptime(fecha,"%m-%d-%Y")
    fecha_prono=fecha
    return (fecha_prono)

dias=IntVar()
dias.set(90)
l=Label(ventana,text="Ingrese cantidad de días pronóstico:", bg="white")
l.place(x=100,y=275)
entry=Entry(ventana,textvariable=dias, width=15)
entry.place(x=300,y=275)

def cantDiasProno():
    dias1=dias.get()
    return dias1

def cerrarVentana():
    ventana.destroy()

boton1=tkinter.Button(ventana, text = "OK", command = lambda:[fechaProno(), cantDiasProno(), cerrarVentana()], bg="#A3E2E3",width=10,height=1).pack(pady = 20)
ventana.mainloop()

diasProno=cantDiasProno()
inicio=fechaProno()
fin=fechaProno()+timedelta(days=diasProno-1)
lista_total_fechas1=[(inicio + timedelta(days=d)).strftime("%m-%d-%y") 
    for d in range((fin - inicio).days + 1)]

lista_total_fechas=pd.to_datetime(lista_total_fechas1)
lista_total_fechas=lista_total_fechas.to_pydatetime()
lista_total_fechas=pd.DataFrame(lista_total_fechas)
fechaListaProno=lista_total_fechas

################################################################################################
########################------ CIERRE POZOS PRESURIZADOS-------#################################
################################################################################################
##### ----->  Q = Qi*e^(-dnd*t) //  Declinación exponencial 

df_cierre_pozos= pd.read_excel(r'C:\Users\t01hkruteler\Documents\PEV Dic-Marzo\datos entrada\Data entrada.xlsx',sheet_name='Cierre de Pozos')
np_cierre_pozos = np.array(df_cierre_pozos)
delta_caudal=np_cierre_pozos[:,6]
dnd_diaria=np_cierre_pozos[:,7]
estado=np_cierre_pozos[:,1]
pozos1=np_cierre_pozos[:,0]
t = np.arange(0,diasProno,1) 
A= np.zeros([len(t),len(pozos1)])
for i in range(len(pozos1)):
    for j in range(len(t)):
        A[j,i]=delta_caudal[i]*(e**(-dnd_diaria[i]*t[j]))
cierre_de_pozos=pd.DataFrame(data=A,columns=pozos1)
cierre_de_pozos.insert(0,"fecha",fechaListaProno,True)
#cierre_de_pozos = cierre_de_pozos.iloc[0:diasProno,:]

################################################################################################
###########################--------POZOS CONTINUIDAD-------#####################################
################################################################################################
con1 = sqlite3.connect("BaseContinuidad")
decli_pozo_df=pd.read_sql("SELECT * FROM continuidad",con1)
decli_pozo_df['Pozo'] = decli_pozo_df['Pozo'].str.replace('[\n]', '')
decli_pozo_df.drop('ID', axis=1, inplace=True)
decli_pozo_np = np.array(decli_pozo_df)
fecha_inicio=decli_pozo_np[:,3]

for i in range(len(fecha_inicio)):
    fecha_inicio[i] = datetime.datetime.strptime(fecha_inicio[i],"%m/%d/%y")

delta_tiempo=fechaProno() - fecha_inicio 
delta_tiempo=pd.DataFrame(delta_tiempo)
delta_tiempo = delta_tiempo / np.timedelta64(1, 'D')
delta_tiempo=delta_tiempo.astype(int)
delta_tiempo=np.array(delta_tiempo[0])
pozos2 = decli_pozo_np[:,0] 
D = (decli_pozo_np[:,1])/360
b = decli_pozo_np[:,2]
qi = decli_pozo_np[:,4]
t = np.arange(0,diasProno,1)
delta_cierre=np_cierre_pozos[:,3] 
B = np.zeros([len(t),len(pozos2)])

####### ---->  Formula declinación hiperbólica:   q(t)=qi/((1+b*D*t)**1/b)
for i in range(len(pozos2)):
    for j in range(len(t)):
        for r in range(len(pozos1)):
             if (pozos1[r]==pozos2[i]):
                  B[j,i] = qi[i] / (1 + b[i] * D[i]*(t[j]+delta_tiempo[i]+delta_cierre[r])) ** 1/b[i]
             else:
                  B[j,i] = qi[i] / (1 + b[i] * D[i]*(t[j]+delta_tiempo[i])) ** 1/b[i] 

caudal_pronostico = pd.DataFrame(data=B, index=t, columns=pozos2)
caudal_pronostico.insert(0,"fecha",fechaListaProno,True)
fix, ax = plt.subplots()
pozos=pozos2[1:]
for g in pozos:
    ax.plot(t, caudal_pronostico[g])
    ax.set_xlabel("Tiempo (días)")
    ax.set_ylabel("Caudal")
    ax.set_title("Continuidad de pozos")
#plt.show()
################################################################################################
###################--POZOS CONTINUIDAD + CIERRE POZOS PRESURIZADOS--############################
################################################################################################

pozos1=list(cierre_de_pozos)
pozos2=list(caudal_pronostico)
for k in range(len(pozos1)):
    for j in range(len(pozos2)):
        for i in range(len(caudal_pronostico)):
            if (pozos1[k]!='fecha'==pozos2[j]!='fecha'):
                caudal_pronostico.loc[i,j]=caudal_pronostico.loc[i,j]+cierre_de_pozos.loc[i,r]


continuidad_y_cierre_pozos=pd.DataFrame(caudal_pronostico)

################################################################################################
############################--------- POZOS NUEVOS---------#####################################
################################################################################################

con2 = sqlite3.connect("BasePozosNuevos")
datos_pozos_nuevos_df=pd.read_sql("SELECT * FROM pozos_nuevos",con2)
datos_pozos_nuevos_df['Pozo'] = datos_pozos_nuevos_df['Pozo'].str.replace('[\n]', '')
datos_pozos_nuevos_df.drop('ID', axis=1, inplace=True)
datos_pozos_nuevos_np=np.array(datos_pozos_nuevos_df)
A=np.zeros([len(fechaListaProno), len(datos_pozos_nuevos_np[:,0])])
pozos2=datos_pozos_nuevos_np[:,0]

for i in range(len(datos_pozos_nuevos_np[:,1])):
     datos_pozos_nuevos_np[i,1] = datetime.datetime.strptime(datos_pozos_nuevos_np[i,1],"%m/%d/%y")
lista_total_fechas2=lista_total_fechas1
for i in range(len(lista_total_fechas2)):
     lista_total_fechas2[i] = datetime.datetime.strptime(lista_total_fechas2[i],"%m-%d-%y")

pt_df = df1
pt_np=np.array(pt_df)
pozos_tipo=list(pt_df)  

PN=pd.DataFrame()
PN.index=lista_total_fechas2

#tomamos los pozos PT del imput
for i in range(len(pozos2)):
#verificamos que esten dentro del listado
    if datos_pozos_nuevos_np[i,2] in pozos_tipo:
#comenzamos a llenar el frame
        for m in PN.index:
            if m >= datos_pozos_nuevos_np[i,1]:
                PN.loc[m,i]=(pt_df.loc[(m-datos_pozos_nuevos_np[i,1]).days,datos_pozos_nuevos_np[i,2]])*datos_pozos_nuevos_np[i,3] 
PN=PN.fillna(0)
pozos_nuevos=np.array(PN)
pozos_nuevos=pd.DataFrame(data=pozos_nuevos,columns=datos_pozos_nuevos_np[:,0])
pozos_nuevos=pozos_nuevos.astype(float,errors='raise') #el frame anterior estaba en formato Object y no generaba la suma de pozos nuevos, se lo paso a float

################################################################################################
########################------ CIERRE POZOS INTERFERENCIA-------################################
################################################################################################
inicio1 = inicio.strftime("%m-%d-%y")
df_final1=continuidad_y_cierre_pozos
df_final1_copy=df_final1.copy()
np_final1_copy=np.array(df_final1_copy)
con3 = sqlite3.connect("BaseInterferencia")
df_interferencia=pd.read_sql("SELECT * FROM interferencia",con3)
df_interferencia.drop('ID', axis=1, inplace=True)
df_interferencia['Pozo'] = df_interferencia['Pozo'].str.replace('[\n]', '')
df_interferencia['PozoInterferido'] = df_interferencia['PozoInterferido'].str.replace('[\n]', '')
np_final1=np.array(df_final1)
np_interferencia=np.array(df_interferencia)
pozos_final1=decli_pozo_np[:,0] 
pozos_interf=np_interferencia[:,3]
fechas_cierre_interf=np_interferencia[:,7]
fechas_apertura_interf=np_interferencia[:,8]
for i in range(len(fechas_cierre_interf)):
    fechas_cierre_interf[i] = datetime.datetime.strptime(fechas_cierre_interf[i],"%m/%d/%y")

fechas_apertura_interf=np_interferencia[:,8]
for i in range(len(fechas_apertura_interf)):
    fechas_apertura_interf[i] = datetime.datetime.strptime(fechas_apertura_interf[i],"%m/%d/%y")
dias_cerrado=[]
for i in range(len(fechas_cierre_interf)):
    if fechas_cierre_interf[i]<fechaProno():
        dias_cerrado=fechas_apertura_interf-fechaProno()   
    else:
        dias_cerrado[i]=fechas_apertura_interf[i]-fechas_cierre_interf[i]
dias_cerrado=pd.DataFrame(dias_cerrado)
dias_cerrado = dias_cerrado / np.timedelta64(1, 'D')
dias_cerrado=dias_cerrado.astype(int)
dias_cerrado=np.array(dias_cerrado)
for i in range(len(dias_cerrado)): #cuando la fecha de apertura es anterior a la fecha prono ingresada entonces no se concidera el cierre
    if dias_cerrado[i]<0:
        dias_cerrado[i]=0
for r in range(len(pozos_interf)):
    for j in range(len(pozos_final1)):
        for i in range(len(lista_total_fechas1)):
            if pozos_interf[r]==pozos_final1[j]:
                if fechas_cierre_interf[r]<=lista_total_fechas1[i]<=fechas_apertura_interf[r]:
                     np_final1[i,j+1]=0 
                else:
                    if lista_total_fechas1[i]>=fechas_apertura_interf[r]:
                        c=i-dias_cerrado[r]
                        np_final1[i,j+1]=np_final1_copy[c,j+1]

###############################################################################################################
############### COLUMNAS SUMAS: TOTAL, TOTAL CONT+PRESURIZADOS+INTERF, TOTAL POZOS NUEVOS######################
############################################## MERGE ##########################################################
cont_presur_interf=pd.DataFrame(np_final1)

encabezado=list(continuidad_y_cierre_pozos.columns)
cont_presur_interf=pd.DataFrame(np_final1,columns=encabezado)
cont_presur_interf=cont_presur_interf.drop(columns=['fecha'], axis=1)
cont_presur_interf=cont_presur_interf.astype(float, errors='raise')
sum_pozos_nuevos = pozos_nuevos.sum(axis=1)
sum_continuidad_presurizados_e_interf = cont_presur_interf.sum(axis=1)
sum_total=sum_continuidad_presurizados_e_interf+sum_pozos_nuevos

cont_presur_interf.insert(0,"fecha",fechaListaProno,True)
pozos_nuevos.insert(0,"fecha",fechaListaProno,True)


final=pd.merge(cont_presur_interf,pozos_nuevos,on="fecha")
final.insert(1,"Total",sum_total,True)
final.insert(2,"Total cont,presurizados e interferencias",sum_continuidad_presurizados_e_interf,True)
final.insert(3,"Total pozos nuevos",sum_pozos_nuevos,True)
final=final.round(1)
#####--------------Agregado de columna Demanda-----------------

#por ahora agrego una columna de demanda de prueba con valores contantes que cruza la curva de produccion total

# a=13000
# demanda=list([a]*diasProno)
# final.insert(1,"Demanda",demanda,True)
final.to_excel('Prono Producción.xlsx')

#final2.to_csv('final2.txt')