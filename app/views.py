from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CutomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

# def home(request):
#  return render(request, 'app/home.html')


# Home view
class HomeView(View):
    def get(self, request):
        topwears = Product.objects.filter(category="TW")
        bottomwears = Product.objects.filter(category="BW")
        mobiles = Product.objects.filter(category="M")
        return render(
            request,
            "app/home.html",
            {"topwears": topwears, "bottomwears": bottomwears, "mobiles": mobiles},
        )


# def product_detail(request):
#  return render(request, 'app/productdetail.html')


# product detail view
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", {"product": product})


def add_to_cart(request):
    return render(request, "app/addtocart.html")


def buy_now(request):
    return render(request, "app/buynow.html")


def profile(request):
    return render(request, "app/profile.html")


def address(request):
    return render(request, "app/address.html")


def orders(request):
    return render(request, "app/orders.html")


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category="M")
    elif data == "Samsung" or data == "Apple":
        mobiles = Product.objects.filter(category="M").filter(brand=data)
    elif data == "below":
        mobiles = Product.objects.filter(category="M").filter(discounted_price__lt=2000)
    elif data == "above":
        mobiles = Product.objects.filter(category="M").filter(discounted_price__gt=2000)

    return render(request, "app/mobile.html", {"mobiles": mobiles})


def login(request):
    return render(request, "app/login.html")


# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CutomerRegistrationForm()
        return render(request, "app/customerregistration.html", {"form": form})

    def post(self, request):
        form = CutomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "You have been registered successfully...")
            form.save()
        return render(request, "app/customerregistration.html", {"form": form})


def checkout(request):
    return render(request, "app/checkout.html")


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(
            request, "app/profile.html", {"form": form, "active": "btn-primary"}
        )

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            reg = Customer(
                user=usr,
                name=name,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode,
            )
            reg.save()
            messages.success(
                request, "Congratulation Profile has been updated successfully"
            )
        return render(
            request, "app/profile.html", {"form": form, "active": "btn-primary"}
        )
