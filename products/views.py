from django.shortcuts import render
from .models import Product
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
@csrf_exempt
def get_products(request):
    if request.method == "GET":
        products = Product.objects.all()
        return JsonResponse({"products": list(products.values())})
    elif request.method == "POST":
        return create_product(request)
    else:
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)

@csrf_exempt
def create_product(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        Product.objects.create(
            name=data.get("name"),
            price=data.get("price"),
            )
        return JsonResponse({"success": "Product created successfully"} , status=201)
    else:
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)

@csrf_exempt
def remove_product(request, id):
    if request.method == "DELETE":
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return JsonResponse({"success": "Product deleted successfully"}, status=200)
        except:
            return JsonResponse({"error": "Product not found"}, status=404)
    else:
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)
    
@csrf_exempt
def get_product(request, id):
    if request.method == "GET":
        try:
            product = Product.objects.get(id=id)
            product_data = model_to_dict(product)
            return JsonResponse({"product": product_data}, status=200)
        except:
            return JsonResponse({"error": "Product not found"}, status=404)
    elif request.method == "DELETE":
        return remove_product(request, id)
    elif request.method == "PUT":
        return update_product(request, id)
    else:
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)
    

def update_product(request, id):
    try:
        product = Product.objects.get(id=id)
        data = json.loads(request.body.decode("utf-8"))
        product.name = data.get("name")
        product.price = data.get("price")
        product.save()
        return JsonResponse({"success": "Product updated successfully"}, status=200)
    except:
        return JsonResponse({"error": "Product not found"}, status=404)