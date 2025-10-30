def esEntero(cadena):
    try: 
        int(cadena)
        return True
    except ValueError:
        return False

def esDecimal(cadena):
    try: 
        float(cadena)
        return True
    except ValueError:
        return False