
from django.http import JsonResponse
from django.forms.models import model_to_dict
from cart.models import Cart
from django.views.decorators.csrf import csrf_exempt
from products.models import Product
from coupons.models import Coupon
from cart.views import serialize_cart
import json


def serialize_coupons(coupons):
    serialized_coupons = []
    for coupon in coupons:
        serialized_coupons.append(model_to_dict(coupon))
    return serialized_coupons

@csrf_exempt
def applicable_coupons(request):
    if request.method != "POST":
        error = {
            "error": "Method not allowed"
        }
        return JsonResponse(error, status=405)
    else:
        try:
            
            data = json.loads(request.body.decode("utf-8"))
            all_coupons = Coupon.objects.all()
            cart_id = data.get("cart_id")
            cart = Cart.objects.get(id=cart_id)
            products = cart.products.all();
            cart_total = 0
            applicable_coupons_objects = []
            #check for product specific coupon
            for product in products:
                cart_total = cart_total + product.price
                for coupon in all_coupons:
                    if coupon.type == "product-wise":
                        if product.id == coupon.details["product_id"]:
                            applicable_coupons_objects.append(coupon)
                            continue
                        
            #check for cart-wise coupon
            for coupon in all_coupons:
                if coupon.type == "cart-wise":
                    if cart_total >= coupon.details["threshold"]:
                        applicable_coupons_objects.append(coupon)
                        continue
            
        
            #check for bxgy
            for product in products:
                for coupon in all_coupons:
                    if coupon.type == "bxgy":
                        for buy_product in coupon.details["buy_products"]:
                            if product.id == buy_product['product_id']:
                                if product.quantity >= buy_product['quantity']:
                                    if (buy_product['quantity'] * coupon.details['repition_limit']>= product.quantity):
                                        applicable_coupons_objects.append(coupon)
                                        continue
            
            if applicable_coupons_objects == []:
                return JsonResponse({"applicable_coupons": []}, status=200)
            else:
                return JsonResponse({"applicable_coupons": serialize_coupons(applicable_coupons_objects)}, status=200)
        except:
            return JsonResponse({"error": "some error occurred"}, status=404)

def applicable_coupon_by_cart_id(cart_id):
            all_coupons = Coupon.objects.all()
            cart = Cart.objects.get(id=cart_id)
            products = cart.products.all();
            cart_total = 0
            applicable_coupons_objects = []
            #check for product specific coupon
            for product in products:
                cart_total = cart_total + product.price
                for coupon in all_coupons:
                    if coupon.type == "product-wise":
                        if product.id == coupon.details["product_id"]:
                            applicable_coupons_objects.append(coupon)
                            continue
                        
            #check for cart-wise coupon
            for coupon in all_coupons:
                if coupon.type == "cart-wise":
                    if cart_total >= coupon.details["threshold"]:
                        applicable_coupons_objects.append(coupon)
                        continue
            
        
            #check for bxgy
            for product in products:
                for coupon in all_coupons:
                    if coupon.type == "bxgy":
                        for buy_product in coupon.details["buy_products"]:
                            if product.id == buy_product['product_id']:
                                if product.quantity >= buy_product['quantity']:
                                    if (buy_product['quantity'] * coupon.details['repition_limit']>= product.quantity):
                                        applicable_coupons_objects.append(coupon)
                                        continue
            
            return applicable_coupons_objects


@csrf_exempt
def apply_coupon(request,id):
    try:
        coupon_to_apply = Coupon.objects.get(pk=id)
        data = json.loads(request.body.decode("utf-8"))
        cart_id = data.get("cart_id")
        cart = Cart.objects.get(id=cart_id)
        # check if coupon is applicable or not
        coupons_applicable = applicable_coupon_by_cart_id(cart_id)
        if coupon_to_apply not in coupons_applicable:
            error = {
                "error": "Coupon is not applicable"
            }
            return JsonResponse(error, status=400)
        else:
            
            # if coupon is cart-wise
            if coupon_to_apply.type == "cart-wise":
                
                cart_total = 0
                for product in cart.products.all():
                    cart_total = cart_total + (product.price * product.quantity)
                
                discount = coupon_to_apply.details["discount"]
                print("cart total: ", cart_total)
                new_cart_total = float(cart_total - (cart_total * discount / 100))
                
                return JsonResponse({"success": "Coupon applied successfully", "updated_cart_total": new_cart_total, "updated_cart": serialize_cart(cart)}, status=200)
        
            # if coupon is product-wise
            if coupon_to_apply.type == "product-wise":
                product_id = coupon_to_apply.details["product_id"]
                product = Product.objects.get(id=product_id)
                product.price = product.price - (product.price * coupon_to_apply.details["discount"] / 100)
                product.save()
                return JsonResponse({"success": "Coupon applied successfully", "updated_cart": serialize_cart(cart)}, status=200)
        
            # if coupon is bxgy
            if coupon_to_apply.type == "bxgy":
                buy_products = coupon_to_apply.details["buy_products"]
                for buy_product in buy_products:
                    for product in cart.products.all():
                        if product.id == buy_product["product_id"]:
                            get_products_json = coupon_to_apply.details["get_products"]
                            get_products_objects = []
                            try:
                                for get_product in get_products_json:
                                    for i in range(get_product["quantity"]):
                                        get_products_objects.append(Product.objects.get(id=get_product["product_id"]))
                            except:
                                return JsonResponse({"error": "Get product not found"}, status=404)
                            
                            for get_product in get_products_objects:
                                cart.products.add(get_product)
                            return JsonResponse({"success": "Coupon applied successfully", "updated_cart": serialize_cart(cart)}, status=200)
        
        return JsonResponse({"success": "Coupon applied successfully", "updated_cart": ""}, status=200)
    except:
        return JsonResponse({"error": "Oh oh! Something went wrong!"}, status=404)
    