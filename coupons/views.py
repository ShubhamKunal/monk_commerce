from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Coupon
import json
# Create your views here.

def create_coupon(request):
    data = json.loads(request.body.decode("utf-8"))
    coupon_type = data.get("type")
    print("Type of coupon: ", coupon_type)
    if coupon_type not in ["cart-wise", "product-wise", "bxgy"]:
        error = {
                "error": "Invalid coupon type"
            }
        return JsonResponse(error, status=400)
    else:
        Coupon.objects.create(
            type=data.get("type"),
            details=data.get("details"),
            )
        return JsonResponse({"success": "Coupon created successfully"} , status=201)
    
        
@csrf_exempt
def get_coupons(request):
    if request.method == "GET":
        coupons = Coupon.objects.all()
        return JsonResponse({"coupons": list(coupons.values())})
    elif request.method == "POST":
        return create_coupon(request)
    else:
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)

@csrf_exempt
def edit_coupon(request, id):
    try:
        coupon = get_object_or_404(Coupon, pk=id)
        if coupon is not None:
            if request.method == "PUT":
                try:
                    data = json.loads(request.body.decode("utf-8"))
                    coupon.type = data.get("type")
                    coupon.details = data.get("details")
                    coupon.save()
                    return JsonResponse({"success": "Coupon updated successfully"}, status=200)
                except:
                    return JsonResponse({"error": "Invalid data"}, status=400)
            elif request.method == "GET":
                coupon_data = model_to_dict(coupon)
                return JsonResponse({"coupon": coupon_data}, status=200)
            elif request.method == "DELETE":
                coupon.delete()
                return JsonResponse({"success": "Coupon deleted successfully"}, status=200)
            else:
                error = {
                    "error": "Method not allowed"
                }
                return JsonResponse(error, status=405)
        else:
            error = {
            "error": "coupon not found"
        }
            return JsonResponse(error, status=404)
    except:
        return JsonResponse({"error": "coupon not found"}, status=404)
    
    
    