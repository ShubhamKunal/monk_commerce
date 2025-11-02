
# Tech Stack used:

Backend: Django

Database: SQLite

Testing: Thunder Client

---------------------------------------------------------------------------------------------------------

# Endpoint I created & implemented:
## 1. For Products

    1.1     GET /products/ - to get all products
   
    1.2     POST /products/ - to add a product
    
    1.3     GET /products/<product_id>/ - to get a specific product  
    
    1.4     DELETE /products/<product_id>/ - to delete a specific product  
    
    1.5     PUT /products/<product_id>/ - to edit a specific product

## 2. For Coupons

    2.1     GET /coupons/ - to get all coupons
    
    2.2     POST /coupons/ - to add a coupon
    
    2.3     GET /coupons/<coupon_id>/ - to get a specific coupon
    
    2.4     DELETE /coupons/<coupon_id>/ - to delete a specific coupon
    
    2.5     PUT /coupons/<coupon_id>/ - to edit a specific coupon

## 3. For Cart

    3.1     GET /cart/ - to get all carts
   
    3.2     POST /cart/create/ - to create an empty cart
    
    3.3     GET /cart/<cart_id>/ - to get a specific cart
    
    3.4     DELETE /cart/<cart_id>/ - to delete a specific cart
    
    3.5     POST /cart/update/ - to add a product into a cart (or increases quantity by 1 if already exists)
    
    3.6     DELETE /cart/update/ - to remove a product from a cart (Deletes if quantity is 1, decreases quantity by 1 if quantity more than 1)

### 4. POST applicable-coupons/ - gets all the applicable coupons in the given cart

### 5. POST apply-coupon/<coupon_id>/ - applies the given coupon in the given cart

---------------------------------------------------------------------------------------------------------
# Limitations/Constraints I can think of/Non-implemented:

1. Max discount cap per cart or per product or per user (for eg. 10% discount upto 200)
2. Coupon expiry
3. Minimum number of products in cart requirement for a coupon (to encourage more shopping)
4. Geographic constraints (for eg. you want to allow this coupon for only Indian customers or American customers)
5. Currently coupons can be applied on top of each other. There can be scenario where we don't want to allow that.
6. Per user limit (for eg. you wish to allow one user only 2 coupons or 2 coupons per day)
7. Slightly modified BxGy ( what if we want Buy x, and get discount on y). Many such variations of BxGy.
8. Premium user privileges (more discount cap, more coupons, better limit etc.)
9. Updated cart after application of coupon is generated in real-time and not stored. (Needs caching in real-world application) 


---------------------------------------------------------------------------------------------------------
# Assumptions:

1. Coupons can be applied on top of each other (stack-able)
2. JSONs of products, coupons will be correctly formatted and will have appropriate data of appropriate type
3. Authentication/Authorization/Payment/Refund/Tax/Shipping system - out of scope for this
4. The discount in coupon details is assumed to be percentage discount and not the discount amount. Likewise for product discount.
5. Coupons are applied before adding the tax.
6. Data-validation is minimal. (eg coupon details, prices, products details are not validated)
7. Cart total is calculated at requested time. (Needs caching in real-world application)
8. Product quantities are assumed to be available in stock
9. Coupons can only be added or deleted. Cannot be deactivated (In real-world app - deactivation capability is desirable)
10. I have annotated each python view with csrf_exempt. Needs to be removed for production.

---------------------------------------------------------------------------------------------------------
# Suggestions for improvement:
1. Address the limitations mentioned above
2. Choose database like MongoDB since it allows flexible schema design.
3. Add start and end date for coupons and string field for description to be shown on website
4. More types of coupons: category-product-based (eg. footwear) or brand-product-based (eg. Adidas)
5. Amount-based coupons. Currently I am assuming cart and product based coupons offer percentage based discounts.
6. Validation of all coupons by administrator before getting added. A layer of security.
7. Automatic coupon application on checkout
8. Even more sophisticated error handling (Currently it exists but can be improved)
9. Premium user privileges - extra coupons not available for ordinary user.

---------------------------------------------------------------------------------------------------------
# How to run this django project:
1. Make sure you have latest python + pip installed properly and running
2. Create virtual environment (_python3 -m venv venv_)
3. Activate it using command (_source venv/bin/activate_)
4. Using pip install the dependencies. requirements.txt is given in the project (_pip install -r requirements.txt_)
5. Apply database migrations (_python manage.py migrate_)
6. Run the development server (_python manage.py runserver_)

---------------------------------------------------------------------------------------------------------



