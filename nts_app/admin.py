from django.contrib import admin
from .models import Category, Product, Cart, Order, OrderItem


# admin.site.register(Profile)
# ------------------------
# CATEGORY
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','is_active')


# -------------------------
# PRODUCT
# -------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'description', 'image','storage','brand')
    search_fields = ('name',)
    list_filter = ('category',)


# -------------------------
# CART
# -------------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total')

    def total_price(self, obj):
        return obj.product.price * obj.quantity

# -------------------------
# ORDER ITEM INLINE
# -------------------------
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#
#
# # -------------------------
# # ORDER
# # -------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_editable = ['status']
    list_filter = ('status', 'created_at')
    search_fields = ['fullname', 'email', 'phone']
    # inlines = [OrderItemInline]
#
#
# # -------------------------
# # ORDER ITEM (OPTIONAL)
# # -------------------------
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']

admin.site.register(OrderItem, OrderItemAdmin)

#-------------------------
# WISHLIST
#-------------------------
#
# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ('user', 'product', 'created_at')
#     list_filter = ('created_at',)
#     search_fields = ('user__username', 'product__name')
#     ordering = ('-created_at',)