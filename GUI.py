import flet as ft
import time, os, json, get_data
from selenium import webdriver

def main(page: ft.Page):
    page.window_width = 850
    page.window_height = 600
    page.window_resizable = False
    page.window_maximizable = False
    page.update()
    
    ports = []
    
    #Funcion para agregar o quitar puertos de la lista ports
    def checkbox_changed(e,port):
        if port in ports:
            ports.remove(port)
        else:
            ports.append(port) 
        ports.sort()


    #Texto de esperando media pantalla
    t = ft.Text(value="ESPERANDO...",size=15,weight=ft.FontWeight.BOLD)
    
    pb = ft.ProgressBar(width=500,height=10)
    pb.value = 0

    #Fila de esperando
    rowTxt = ft.Row(width=850,alignment=ft.MainAxisAlignment.CENTER,height=all,controls=[
        ft.Column([ t, pb])
    ])
    #Columna de esperando
    colTxt = ft.Column(spacing=0,alignment=ft.MainAxisAlignment.CENTER,controls=[
        rowTxt
    ])

    #Funcion de datos principal
    def start_data(e,ports):
        emptyJson = {}
        if(not os.path.exists(f'./outputs')):
            os.mkdir('./outputs')
        for portJ in ports:
            with open(f'./outputs/data_{portJ}.json', 'w') as f: 
                json.dump(emptyJson, f)
        if(len(ports)>=1):
            driver = webdriver.Chrome(get_data.options)
            for port in ports:
                progreso = 0
                ruts = get_data.conseguirJson(f"./{port}.json")
                items = ruts
                l = len(items)

                # Initial call to print 0% progress
                #show = get_data.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
                #t.value = f'{port} {show}'
                #t.update()
                t.value = f'{port} Progreso {((100*progreso)/l)}% | 0/{l} | Último cliente revisado: '
                t.update()
                pb.value = 0
                pb.update()
                for item in ruts:
                    get_data.main(port,item,driver)
                    # Update Progress Bar
                    #show = get_data.printProgressBar(progreso + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
                    progreso+=1
                    t.value = f'{port} Progreso {((100*progreso)/l)}% | {progreso}/{l} | Último cliente revisado: {list(item.keys())[0]}'
                    t.update()
                    pb.value = ((100*progreso)/l)/100
                    pb.update()
                    #t.value = f'{port} {show}'
                    #t.update()

    #Titulo puertos arriba de las checkbox
    lbl = ft.Text(value="PUERTOS",size=20,weight=ft.FontWeight.BOLD)

    #Crear los checkbox       
    check = ft.Checkbox(label="50701", on_change=lambda e:checkbox_changed(e,50701))
    check2 = ft.Checkbox(label="51001", on_change=lambda e:checkbox_changed(e,51001))
    check3 = ft.Checkbox(label="51301", on_change=lambda e:checkbox_changed(e,51301))
    check4 = ft.Checkbox(label="51501", on_change=lambda e:checkbox_changed(e,51501))
    check5 = ft.Checkbox(label="55001", on_change=lambda e:checkbox_changed(e,55001))

    #Fila del texto PUERTOS
    row1 = ft.Row(width=850,alignment=ft.MainAxisAlignment.CENTER,height=all,controls=[
        lbl    
    ])
    #Fila de las checkbox
    row2 = ft.Row(width=850,alignment=ft.MainAxisAlignment.SPACE_EVENLY,height=all,controls=[
        check,
        check2,
        check3,
        check4,
        check5
    ])
    
    #Columna de PUERTOS y las checkbox
    col1 = ft.Column(spacing=0,alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[
        row1,
        row2
    ])

    #Declarar el contenedor superior
    superior = ft.Container(col1,width=850,height=100, margin=ft.margin.only(top=40,bottom=40))

    #Crear boton inferior
    btn = ft.ElevatedButton(width=100,height=50,text="COMENZAR",on_click=lambda e:start_data(e,ports))
    #Crear contenedor inferior
    inferior = ft.Container(btn,width=850,height=100)

    col = ft.Column(width=850,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,controls=[
        superior,
        colTxt,
        inferior
    ])

    contenedor = ft.Container(col,width=850,height=500,padding=0)
    
    page.add(contenedor)

ft.app(target=main)