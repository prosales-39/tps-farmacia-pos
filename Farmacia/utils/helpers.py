def formatear_precio(valor):
    try:
        return f"${valor:,.0f}".replace(",", ".")
    except:
        return "$0"