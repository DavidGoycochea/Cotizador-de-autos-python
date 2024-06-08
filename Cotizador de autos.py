from tkinter import *
import mysql.connector
from tkinter import ttk

class conexion:
    def __init__(self):
        self.conex = mysql.connector.connect(
            host = 'localhost',
            port = '3306',
            user = 'root',
            password = '',
            db = 'vehiculos_marca_maserati'
            )
        self.cur = self.conex.cursor()

    #Operaciones
    def preciobase(self,model):
        global precibase
        precibase = 0
        consulta = "SELECT precio FROM modelos WHERE numero_orden = '" + str(model) + "';"
        self.cur.execute(consulta)
        cont = self.cur.fetchone()
        precibase = cont[0]
        txt1.delete(0,'end')
        txt1.insert(0,"S/."+str(precibase))
        return precibase
        
    def accesorios(self,lista):
        global suma
        suma = 0
        for i in lista:
            consulta = "SELECT precio FROM accesorios WHERE id = '" + str(i) + "';"
            self.cur.execute(consulta)
            cont = self.cur.fetchone()
            suma = suma + cont[0]
        txt2.delete(0,'end')
        txt2.insert(0,"S/."+str(suma))

    def preciototal(self, precibase):
        global precito        
        precito = suma + precibase
        txt3.delete(0,'end')
        txt3.insert(0,"S/."+str(precito))
        return precito

    def cuotainicial(self,pc,forap):
        global cuotainicial
        global cuoini
        if forap == 1:
            cuotainicial = 0
        else:
            cuoini = 0
            consulta = "SELECT porcentaje FROM porcentaje_inicial WHERE id = '" + str(pc) + "';"
            self.cur.execute(consulta)
            cont = self.cur.fetchone()
            cuoini = cont[0]
            cuotainicial = precito * (cuoini/100)
            ko = round(cuotainicial,2)
            txt4.delete(0,'end')    
            txt4.insert(0,"S/. "+str(ko))
            return cuotainicial

    def saldo(self):
        global saldooo
        saldooo = precito - cuotainicial
        saldi = round(saldooo,2)
        txt5.delete(0,'end')
        txt5.insert(0,"S/. "+str(saldi))        
        return saldooo

    def pagomensual(self):
        tas = float(spxbox.get())/100
        plaz = float(spxbox2.get())
        pagmen = (saldooo * tas)/(1-(1+tas)**(-plaz))
        pagmen2 = round(pagmen,2)
        txt8.delete(0,'end')
        txt8.insert(0, "S/. "+str(pagmen2))

con = conexion()
ventana = Tk()
ventana.title("Tarea Final - Menú")
ventana.geometry("800x600")
ventana.config(bg='#0cb7f2')

titu = Label(ventana, text= "COTIZACIÓN DE VEHÍCULOS MARCA MASERATI", fg="yellow", font="Helvetica 25 bold",bg="#0cb7f2")
titu.place(x=10,y=10)

#Solitarios
lbl0 = Label(ventana,text="Modelo: ")
lbl0.place(x=130,y=60)
lbl0.config(bg="#0cb7f2",font="Helvetica 10 bold")
combx1 = ttk.Combobox(ventana)
combx1["values"]=("Quattroporte","GranSport","Coupe","GranSport Spyder","Heritage","MC12","R&D")
combx1.current(0)
combx1.place(x=190,y=60)
def modelo():
    mod = combx1.get()
    if mod == "Quattroporte":
        model = 1
    elif mod == "GranSport":
        model = 2
    elif mod == "Coupe":
        model = 3
    elif mod == "GranSport Spyder":
        model = 4
    elif mod == "Heritage":
        model = 5
    elif mod == "MC12":
        model = 6
    elif mod == "R&D":
        model = 7
    else:
        pass
    return model

def junta():
    model = modelo()
    pc = porcen()
    forap = forpa()
    precibase = con.preciobase(model)
    lista = escoger2()
    con.accesorios(lista)
    con.preciototal(precibase)
    con.cuotainicial(pc,forap)
    con.saldo()
    con.pagomensual()

listbx = Listbox(ventana, width=12,height=4)
listbx.place(x=670,y=60)
listbx.insert(0,'5%')
listbx.insert(1,'10%')
listbx.insert(2,'15%')
listbx.insert(3,'20%')
listbx.insert(4,'25%')
listbx.insert(5,'30%')

def porcen():
    por = listbx.get(ACTIVE)
    if por == "5%":
        pc = 1
    elif por == "10%":
        pc = 2
    elif por == "15%":
        pc = 3
    elif por == "20%":
        pc = 4
    elif por == "25%":
        pc = 5
    elif por == "30%":
        pc = 6
    else:
        pass
    return pc

#Forma de Pago
frame3 = LabelFrame(ventana,text="Forma de pago" ,width=130,height=90,bg="#0cb7f2")
frame3.place(x=480,y=60)
seleccion = IntVar()
def forpa():
    forap = 0
    if seleccion.get()==1:
        forap = 1
    if seleccion.get()==2:
        forap = 2
    return forap
        
rb1 = Radiobutton(frame3, text="Contado", variable=seleccion, value=1, command=forpa, bg="#0cb7f2")
rb1.place(x=10,y=10)

rb2 = Radiobutton(frame3, text="Credito", variable=seleccion, value=2,command=forpa, bg="#0cb7f2")
rb2.place(x=10,y=40)

#Accesorios
frame2 = LabelFrame(ventana,text="Accesorios" ,width=520,height=170,bg="#0cb7f2",font="bold")
frame2.place(x=140,y=150)
intchk1 = IntVar()
intchk2 = IntVar()
intchk3 = IntVar()
intchk4 = IntVar()
intchk5 = IntVar()
intchk6 = IntVar()
chk1 = Checkbutton(frame2, text="Lunas Polarizadas", variable=intchk1, bg="#0cb7f2")
chk1.place(x=60,y=10)
chk2 = Checkbutton(frame2, text="Radio CD", variable=intchk2, bg="#0cb7f2")
chk2.place(x=60,y=60)
chk3 = Checkbutton(frame2, text="Llantas Radiales", variable=intchk3, bg="#0cb7f2")
chk3.place(x=60,y=110)
chk4 = Checkbutton(frame2, text="Aros de Magnesio", variable=intchk4, bg="#0cb7f2")
chk4.place(x=300,y=10)
chk5 = Checkbutton(frame2, text="Alarma Integral", variable=intchk5, bg="#0cb7f2")
chk5.place(x=300,y=60)
chk6 = Checkbutton(frame2, text="Asientos de Cuero", variable=intchk6, bg="#0cb7f2")
chk6.place(x=300,y=110)
def escoger2():
    lista=[]
    if (intchk1.get()==1):
        lista.append(1)
    if (intchk2.get()==1):
        lista.append(2)
    if (intchk3.get()==1):
        lista.append(3)
    if (intchk4.get()==1):
        lista.append(4)
    if (intchk5.get()==1):
        lista.append(5)
    if (intchk6.get()==1):
        lista.append(6)
    return lista

#Cotización
frame1 = LabelFrame(ventana,text="Cotización", font="bold" ,width=650,height=250,bg="#0cb7f2")
frame1.place(x=60,y=320)

lbl1 = Label(frame1, text= "Precio base:", fg="white", font="Helvetica 10 bold",bg="#0cb7f2")
lbl1.place(x=30,y=10)
lbl2 = Label(frame1, text= "Accesorios:", fg="white", font="Helvetica 10 bold",bg="#0cb7f2")
lbl2.place(x=30,y=60)
lbl3 = Label(frame1, text= "Precio Total:", fg="white", font="Helvetica 10 bold",bg="#0cb7f2")
lbl3.place(x=30,y=110)
lbl4 = Label(frame1, text= "Cuota Inicial:", fg="white", font="Helvetica 10 bold",bg="#0cb7f2")
lbl4.place(x=30,y=160)
lbl5 = Label(frame1, text= "Saldo:", fg="white", font="Helvetica 10 bold",bg="#0cb7f2")
lbl5.place(x=320,y=10)
lbl6 = Label(frame1, text= "Tasa Mensual:", fg="white", font="Helvetica 10 bold",bg="#0cb7f2")
lbl6.place(x=320,y=60)
lbl7 = Label(frame1, text= "Plazo Meses:", fg="white", font="Helvetica 10 bold",bg="#0cb7f2")
lbl7.place(x=320,y=110)
lbl8 = Label(frame1, text= "Pago Mensual:", fg="white", font="Helvetica 10 bold",bg="#0cb7f2")
lbl8.place(x=320,y=160)

spxbox = Spinbox(frame1,from_=1.5,to=4.5,increment=0.1,state='readonly',width=11)
spxbox.place(x=420,y=60)
spxbox2 = Spinbox(frame1,from_=12,to=120,increment=6,state='readonly',width=11)
spxbox2.place(x=420,y=110)

txt1 = Entry(frame1)
txt1.place(x=130,y=10,width=150,height=30)
txt2 = Entry(frame1)
txt2.place(x=130,y=60,width=150,height=30)
txt3 = Entry(frame1)
txt3.place(x=130,y=110,width=150,height=30)
txt4 = Entry(frame1)
txt4.place(x=130,y=160,width=150,height=30)
txt5 = Entry(frame1)
txt5.place(x=420,y=10,width=150,height=30)
txt8 = Entry(frame1)
txt8.config(bg="yellow")
txt8.place(x=420,y=160,width=150,height=30)

botoneco = Button(frame1, text="Calcular", command=junta,bg="black",fg="white",font="Helvetica 10 bold")
botoneco.place(x=550,y=195)

ventana.mainloop()