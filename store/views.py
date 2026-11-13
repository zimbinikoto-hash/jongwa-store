from django.shortcuts import render
from .functions.reddit import get_reddit_posts
from io import BytesIO
from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.db import transaction
from decimal import Decimal

from .models import (
    Store,
    UserProfile,
    Product,
    Order,
    OrderItem,
    Invoice,
    Review
)

from .forms import StoreForm, ProductForm, ReviewForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm


def register(request):
    """Register a new vendor or buyer."""

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'store/register.html', {'form': form})


@login_required(login_url='login')
def home(request):
    """Display products available in the Jongwa Store marketplace."""

    products = Product.objects.select_related('store').all()

    return render(
        request,
        'store/home.html',
        {'products': products}
    )


@login_required(login_url='login')
def vendor_dashboard(request):
    """Display stores belonging to the logged-in vendor."""

    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'vendor':
        return redirect('home')

    stores = Store.objects.filter(owner=request.user)

    return render(
        request,
        'store/vendor_dashboard.html',
        {'stores': stores}
    )


@login_required(login_url='login')
def create_store(request):
    """Allow a vendor to create a store."""

    if not UserProfile.objects.filter(
        user=request.user,
        role='vendor'
    ).exists():
        return redirect('home')

    if request.method == 'POST':
        form = StoreForm(request.POST)

        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()

            return redirect('vendor_dashboard')

    else:
        form = StoreForm()

    return render(
        request,
        'store/create_store.html',
        {'form': form}
    )


@login_required(login_url='login')
def edit_store(request, store_id):
    """Allow a vendor to edit their own store."""

    store = get_object_or_404(
        Store,
        id=store_id,
        owner=request.user
    )

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)

        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')

    else:
        form = StoreForm(instance=store)

    return render(
        request,
        'store/edit_store.html',
        {'form': form, 'store': store}
    )


@login_required(login_url='login')
def delete_store(request, store_id):
    """Allow a vendor to delete their own store."""

    store = get_object_or_404(
        Store,
        id=store_id,
        owner=request.user
    )

    if request.method == 'POST':
        store.delete()
        return redirect('vendor_dashboard')

    return render(
        request,
        'store/delete_store.html',
        {'store': store}
    )


@login_required(login_url='login')
def add_product(request, store_id):
    """Allow a vendor to add a product to their own store."""
    if not UserProfile.objects.filter(
        user=request.user,
        role='vendor'
    ).exists():
        return redirect('home')

    store = get_object_or_404(
        Store,
        id=store_id,
        owner=request.user
    )

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()

            return redirect('vendor_dashboard')

    else:
        form = ProductForm()

    return render(
        request,
        'store/add_product.html',
        {'form': form, 'store': store}
    )


@login_required(login_url='login')
def edit_product(request, product_id):
    """Allow a vendor to edit a product in their own store."""

    product = get_object_or_404(
        Product,
        id=product_id,
        store__owner=request.user
    )

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'store/edit_product.html',
        {'form': form, 'product': product}
    )


@login_required(login_url='login')
def delete_product(request, product_id):
    """Allow a vendor to delete a product from their own store."""

    product = get_object_or_404(
        Product,
        id=product_id,
        store__owner=request.user
    )

    if request.method == 'POST':
        product.delete()
        return redirect('vendor_dashboard')

    return render(
        request,
        'store/delete_product.html',
        {'product': product}
    )


@login_required(login_url='login')
def product_detail(request, product_id):
    """Display product details and allow users to submit reviews."""

    product = get_object_or_404(Product, id=product_id)

    existing_review = Review.objects.filter(
        product=product,
        user=request.user
    ).first()

    form = ReviewForm(
        request.POST or None,
        instance=existing_review
    )

    if request.method == 'POST' and form.is_valid():

        is_verified = Order.objects.filter(
            buyer=request.user,
            status='completed',
            items__product=product
        ).exists()

        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.is_verified = is_verified
        review.save()

        form = ReviewForm(instance=review)

    reviews = product.reviews.all()

    return render(
        request,
        'store/product_detail.html',
        {
            'product': product,
            'form': form,
            'reviews': reviews,
        }
    )



@login_required(login_url='login')
def view_cart(request):
    """Display products currently in the buyer's shopping cart."""

    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(
        request,
        'store/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )


@login_required(login_url='login')
def add_to_cart(request, product_id):
    """Add a selected product to the buyer's shopping cart."""

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    cart[product_id] = cart.get(product_id, 0) + 1

    request.session['cart'] = cart

    return redirect('view_cart')


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    """Remove a product from the buyer's shopping cart."""

    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('view_cart')


@login_required(login_url='login')
def update_cart(request, product_id):
    """Update the quantity of a product in the shopping cart."""

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))

            if 1 <= quantity <= product.stock:
                cart = request.session.get('cart', {})
                cart[str(product_id)] = quantity
                request.session['cart'] = cart

        except ValueError:
            pass

    return redirect('view_cart')


@login_required(login_url='login')
def checkout(request):
    """Process checkout and create an order and invoice."""

    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    if not cart:
        return redirect('view_cart')

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = int(quantity)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        with transaction.atomic():

            # Check stock before creating the order.
            for item in cart_items:
                product = Product.objects.select_for_update().get(
                    id=item['product'].id
                )

                if item['quantity'] > product.stock:
                    return render(request, 'store/checkout.html', {
                        'cart_items': cart_items,
                        'total': total,
                        'error': f'Not enough stock for {product.name}.'
                    })

            order = Order.objects.create(
                buyer=request.user,
                total_amount=total,
                status='completed'
            )

            for item in cart_items:
                product = Product.objects.select_for_update().get(
                    id=item['product'].id
                )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )

                product.stock -= item['quantity']
                product.save(update_fields=['stock'])

            Invoice.objects.create(
                order=order,
                invoice_number=f'INV-{order.id:06d}'
            )
            invoice = order.invoice

        if request.user.email:
            print("BUYER EMAIL:", request.user.email)
            pdf_content = generate_invoice_pdf(order, invoice)

            email = EmailMessage(
                subject=f'Jongwa Store Invoice {invoice.invoice_number}',
                body=(
                    f'Hello {request.user.username},\n\n'
                    'Thank you for shopping with Jongwa Store. '
                    'Please find your invoice attached.\n\n'
                    'Thank you!'
                ),
                from_email=None,
                to=[request.user.email],
                
            )

            email.attach(
                f'invoice_{invoice.invoice_number}.pdf',
                pdf_content,
                'application/pdf'
            )
            print("EMAIL RECIPIENT:", email.to)
            email.send(fail_silently=False)
            print("EMAIL SENT:", email.send())

        request.session['cart'] = {}

        return redirect('order_success', order_id=order.id)

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required(login_url='login')
def order_success(request, order_id):
    """Display the completed order and its invoice."""

    # Retrieve the order belonging to the logged-in buyer.
    order = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user
    )

    # Calculate the subtotal for each product.
    for item in order.items.all():
        item.subtotal = item.price * item.quantity

    # Retrieve the invoice linked to the order.
    invoice = order.invoice

    # Display the order and invoice.
    return render(request, 'store/order_success.html', {
        'order': order,
        'invoice': invoice
    })


def generate_invoice_pdf(order, invoice):
    """Generate a PDF invoice and return it as bytes."""

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, 800, "JONGWA STORE")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 770, "CUSTOMER INVOICE")

    pdf.drawString(50, 730, f"Invoice Number: {invoice.invoice_number}")
    pdf.drawString(50, 710, f"Order Number: {order.id}")
    pdf.drawString(50, 690, f"Invoice Date: {invoice.issued_at}")

    pdf.drawString(50, 650, f"Customer: {order.buyer.username}")
    pdf.drawString(50, 630, f"Email: {order.buyer.email}")

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, 580, "Product")
    pdf.drawString(300, 580, "Quantity")
    pdf.drawString(380, 580, "Unit Price")
    pdf.drawString(480, 580, "Subtotal")

    pdf.setFont("Helvetica", 10)
    y = 555

    for item in order.items.all():
        subtotal = item.price * item.quantity

        pdf.drawString(50, y, item.product.name[:35])
        pdf.drawString(300, y, str(item.quantity))
        pdf.drawString(380, y, f"R{item.price:.2f}")
        pdf.drawString(480, y, f"R{subtotal:.2f}")

        y -= 25

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(380, y - 20, f"Grand Total: R{order.total_amount:.2f}")

    pdf.save()

    buffer.seek(0)
    return buffer.getvalue()


@login_required(login_url='login')
def download_invoice(request, order_id):
    """Generate and download a PDF invoice."""

    order = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user
    )

    invoice = order.invoice
    pdf_content = generate_invoice_pdf(order, invoice)

    response = HttpResponse(
        pdf_content,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    )

    return response


def reddit_feed(request):
    """Display posts from the ecommerce subreddit."""

    posts = get_reddit_posts()

    return render(
        request,
        'store/reddit_feed.html',
        {'posts': posts}
    )