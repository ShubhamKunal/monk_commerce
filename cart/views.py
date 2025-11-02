from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from .models import Cart
from products.models import Product
import json


#UTIL FUNCTIONS
def serialize_product(product):
    return {
        "id": product.id,
        "name": product.name,
        "price": float(product.price),
        "quantity": product.quantity
    }
def serialize_cart(cart):
    cart_dict = model_to_dict(cart)
    cart_dict["products"] = [serialize_product(p) for p in cart.products.all()]
    cart_dict["total_price"] = get_total_price(cart)
    return cart_dict

def get_all_carts(request):
    carts = Cart.objects.all()
    carts_json = [serialize_cart(c) for c in carts]
    return JsonResponse(carts_json, safe=False)

def get_total_price(cart):
    total_price = 0
    for p in cart.products.all():
        total_price += p.price * p.quantity
    return float(total_price)

# Create your views here.
@csrf_exempt
def get_carts(request):
    if request.method == "GET":
        return get_all_carts(request)
    else:
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)
    
@csrf_exempt
def get_cart(request,id):
    if request.method == "GET":
        try:
            cart = Cart.objects.get(id=id)
            return JsonResponse({"cart": serialize_cart(cart)}, status=200)
        except:
            return JsonResponse({"error": "Cart with id: " + str(id) + " not found"}, status=404)
    elif request.method == "DELETE":
        return remove_cart(request, id)
    else:
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)


@csrf_exempt
def create_cart(request):
    if request.method == "POST":
        Cart.objects.create()
        return JsonResponse({"success": "Cart created with id: " + str(Cart.objects.latest("id").id) + " successfully"} , status=201)
    else:
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)

def remove_cart(request, id):
        try:
            cart = Cart.objects.get(id=id)
            cart.delete()
            return JsonResponse({"success": "Cart deleted successfully"}, status=200)
        except:
            return JsonResponse({"error": "Cart not found"}, status=404)
    

@csrf_exempt
def add_product_in_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            cart_id = data.get("cart_id")
            product_id = data.get("product_id")
            cart = Cart.objects.get(id=cart_id)
            product = Product.objects.get(id=product_id)
            for p in cart.products.all():
                if p.id == product_id:
                    p.quantity += 1
                    p.save()
                    return JsonResponse({"success": "Product quantity updated in cart successfully"}, status=201)
            product.quantity = 1  
            cart.products.add(product)
            return JsonResponse({"success": "Product added to cart successfully"}, status=201)
        except:
            return JsonResponse({"error": "Product/Cart not found"}, status=404)
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body.decode("utf-8"))
            cart_id = data.get("cart_id")
            product_id = data.get("product_id")
            cart = Cart.objects.get(id=cart_id)
            product = Product.objects.get(id=product_id)
            if product.quantity > 1:
                product.quantity -= 1
                product.save()
                return JsonResponse({"success": "Product quantity updated in cart successfully"}, status=200)
            cart.products.remove(product)
            return JsonResponse({"success": "Product removed from cart successfully"}, status=200)
        except:
            return JsonResponse({"error": "Product/Cart not found"}, status=404)
    else:
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)

