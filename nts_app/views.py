from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Sum
from django.template.context_processors import request

from .models import Product, Order, OrderItem, Category, Cart, CartItem, Wishlist


# ---------------- HOME ----------------
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            messages.error(request, "All fields required!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')


# 🔹 LOGIN
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard')
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff or user.is_superuser:
                return redirect('dashboard')
            return redirect('home')

        messages.error(request, "Invalid credentials")
        return redirect('login')

    return render(request, 'login.html')
# 🔹 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')

#------user Dashboard----------#
# @login_required(login_url='/login')
@login_required
def ec_dashboard(request):
    if request.user.is_superuser:
        return redirect("ec_dashboard")

    if request.user.is_staff:
        return redirect("staff_dashboard")

    recent_orders = Order.objects.filter(user=request.user)

    return render(request, 'ec_dashboard.html', {
        'recent_orders': recent_orders
    })

# ---------------- PROFILE ----------------
@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'orders': orders
    })

# ---------------- ABOUT ----------------
def about(request):
    return render(request, 'about.html')


# ---------------- CONTACT ----------------
def contact(request):
    if request.method == "POST":
        messages.success(request, "Thank you for contacting N TECH STORE!")
    return render(request, 'contact.html')


# ---------------- PASSWORD RESET ----------------
@login_required
def password_reset(request):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('password_reset')

        try:
            user = User.objects.get(username=username)
            user.set_password(password1)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'password_reset.html')

#--------------ORDER_SUCCESS--------------#
@login_required
def order_success(request):
    return render(request, 'order_success.html')


#----------------product-by-category------------------#
# ✅ ALL PRODUCTS
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'product_list.html', context)


# ✅ CATEGORY WISE PRODUCTS
def product_by_category(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    context = {
        'category': category,
        'products': products,
        'categories': categories
    }
    return render(request, 'product_list.html', context)

def products(request):

    products = Product.objects.all()

    return render(request, "products.html", {"products": products})
@login_required
def product_detail(request, id):

    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        user = request.user
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart')
    context = {
        'product': product,
        'related_products': related_products
    }

    return render(request, 'product_detail.html', context)


def product_by_category(request, id):

    category = Category.objects.get(id=id)

    products = Product.objects.filter(category=category)

    context = {
        'products': products,
        'category': category
    }

    return render(request, 'product_list.html', context)
@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total_price = 0

    for item in cart_items:
        total_price += item.total

    return render(request,'cart.html',{
        'cart_items':cart_items,
        'total_price':total_price
    })


@login_required
def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        products=product
    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    return redirect("cart")

def remove_from_cart(request, id):
    item = get_object_or_404(Cart, id=id)
    item.delete()
    return redirect('cart')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()

    return redirect('wishlist')

@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {
        'items': items
    })

# import razorpay
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('/cart/')

    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    amount_in_paise = int(total_amount * 100)

    client = razorpay.Client(auth=(
        'rzp_test_ytoQRUzHn3jtXL',
        'Sc3eDMyJEuNfGzcf5r5eWiLz'
    ))

    razorpay_order = client.order.create({
        'amount': amount_in_paise,
        'currency': 'INR',
        'payment_capture': 1
    })

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        payment_method = request.POST.get('payment_method')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')

        if payment_method == 'cod':
            Checkout.objects.create(
                user=request.user,
                fullname=fullname,
                email=email,
                phone=phone,
                address=address,
                city=city,
                total_amount=total_amount,
                payment_status="Pending",
                payment_method="Cash on Delivery"
            )

            Orderlist.objects.create(
                user=request.user,
                fullname=fullname,
                address=address,
                phone=phone,
                total_amount=total_amount
            )

            cart_items.delete()
            return redirect('/order_success/')

        elif payment_method == 'razorpay':
            Checkout.objects.create(
                user=request.user,
                fullname=fullname,
                email=email,
                phone=phone,
                address=address,
                city=city,
                total_amount=total_amount,
                payment_status="Paid",
                payment_method="Razorpay",
                razorpay_order_id=razorpay_order['id'],
                razorpay_payment_id=razorpay_payment_id
            )

            Orderlist.objects.create(
                user=request.user,
                fullname=fullname,
                address=address,
                phone=phone,
                total_amount=total_amount
            )

            cart_items.delete()
            return redirect('/order_success/')

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'amount_in_paise': amount_in_paise,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': 'rzp_test_ytoQRUzHn3jtXL',
        'currency': 'INR',
    }

    return render(request, 'checkout.html', context)
# @login_required(login_url='/login')
def upi_payment(request):
    return render(request, 'upi_payment.html')

@login_required
def order_page(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'order.html', {'orders': orders})
