xmin, ymin, xmax, ymax = 0, 0, 50, 50

def calcular_codigo(x, y):
    codigo = 0
    if x < xmin:
        codigo |= 1  
    elif x > xmax:
        codigo |= 2  
    if y < ymin:
        codigo |= 4  
    elif y > ymax:
        codigo |= 8  
    return codigo

def clipping(x1, y1, x2, y2):
    codigo1 = calcular_codigo(x1, y1)
    codigo2 = calcular_codigo(x2, y2)
    while True:
        if codigo1 == 0 and codigo2 == 0:
            return "contida", (x1, y1), (x2, y2)
        elif codigo1 & codigo2 != 0:
            return "não contida", None, None
        else:
            codigo_out = codigo1 if codigo1 != 0 else codigo2
            if codigo_out & 1:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin
            elif codigo_out & 2:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif codigo_out & 4:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif codigo_out & 8:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            
            if codigo_out == codigo1:
                x1, y1 = x, y
                codigo1 = calcular_codigo(x1, y1)
            else:
                x2, y2 = x, y
                codigo2 = calcular_codigo(x2, y2)

casos = {
    "AB": ((15, 10), (30, 20)),  
    "CD": ((20, 55), (40, 60)),  
    "EF": ((15, 45), (60, -10))  
}

resultados = {linha: clipping(*pontos[0], *pontos[1]) for linha, pontos in casos.items()}

print(resultados)
