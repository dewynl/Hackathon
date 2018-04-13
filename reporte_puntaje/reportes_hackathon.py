import pdfkit

if __name__ == '__main__':
    for i in range(22):
        pdfkit.from_url('http://localhost:8000/detalle-puntos-reporte/' + str(i+1), 'reporte-equipo' + str(i+1) + '.pdf', )
    print('listo')