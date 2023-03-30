import json

def total_carrito(request):
    total = 0
    if "carrito_compras" in request.COOKIES:
        cart = json.loads(request.COOKIES["carrito_compras"])
        for key, value in cart.items():
            total += float(value["acumulado"])

    return {"total_carrito":total}
