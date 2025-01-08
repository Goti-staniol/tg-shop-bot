from db.methods import  get_user_products, get_products_list

products = get_products_list()

for product in products:
    print(product.product_id)
    
    
n = (20 + 5 - 1) // 5
print(n)

