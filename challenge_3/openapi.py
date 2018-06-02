from apispec import APISpec
from flask import json

#Create spec
spec = APISpec(
    title='Book-A-Meal API',
    version='1.0.0',
    info=dict(
        description='A meal booking API'
        ),
    plugins=[
        'apispec.ext.flask'
        ],
    )

from bookameal import UserSchema, Meal, Menu, Order

spec.definition('User', schema=UserSchema)
spec.definition('Meal', schema=Meal)
spec.definition('Menu', schema=Menu)
spec.definition('Order', schema=Order)





from bookameal import app, home, register, login, account_get_meals, account_get_specific_meal,\
     account_create_meal, account_update_meal, account_delete_meal, get_menu, setup_menu, \
     get_all_orders, remove_order


with app.test_request_context():
    spec.add_path(view=home)
    spec.add_path(view=register)
    spec.add_path(view=login)
    spec.add_path(view=account_get_meals)
    spec.add_path(view=account_get_specific_meal)
    spec.add_path(view=account_create_meal)
    spec.add_path(view=account_update_meal)
    spec.add_path(view=account_delete_meal)
    spec.add_path(view=get_menu)
    spec.add_path(view=setup_menu)
    spec.add_path(view=get_all_orders)
    spec.add_path(view=remove_order)
    
    


with open('swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)
    
