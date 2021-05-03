from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Product
from store.models.category import Category
from django.views import View


# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity==1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        # if request.session['category']:
        #        print(request.session['category']+'ok')
        cat = request.GET.get('category')
        categoryID=None
        if request.session['category']:
            categoryID = int(request.session['category'])
        elif cat==None:
            request.session['category']=None

        #
        # print(categoryID)
        if not categoryID:
          return redirect('homepage')
        else:
          return redirect('http://127.0.0.1:8000/?category='+str(categoryID))
#
#
#
    def get(self , request):
            cart = request.session.get('cart')
            if not cart:
                request.session['cart'] = {}
            products = None
            categories = Category.get_all_categories()
            categoryID = request.GET.get('category')
            if categoryID:
                request.session['category'] = categoryID
            elif not categoryID:
                request.session['category'] = None
            # print(request.session['category'])
            name = None
            if categoryID:
                for cat in categories:
                    if cat.id == int(categoryID):
                        name= cat.name

            if categoryID:
                products = Product.get_all_products_by_categoryid(categoryID)
            else:
                products = Product.get_all_products();

            data = {}
            data['products'] = products
            data['categories'] = categories
            data['name'] = name

            # print(name)
            return render(request, 'index.html', data)
#         # print()
#         return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


