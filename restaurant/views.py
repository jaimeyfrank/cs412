from django.shortcuts import render, redirect
import random, time

specials = ["Four cheese pizza",
            "Margherita pizza",
            "Fig and prosciutto pizza",
            "Caramelized onion and goat cheese pizza",]

def main(request):
    """
    View for displaying the main page.
    """
    return render(request, "restaurant/main.html")

def order(request):
    """
    View for displaying the order page.
    """
    if request.method == "POST":
        # Process form data
        items = []
        total_price = 0
        if 'spaghetti' in request.POST:
            items.append("Spaghetti and Meatballs")
            total_price += 15
        if 'fettucine' in request.POST:
            fettucine_option = request.POST.get('fettucine_option', 'plain')
            if fettucine_option == 'plain':
                items.append("Fettucine Alfredo - Plain")
                total_price += 15
            elif fettucine_option == 'chicken':
                items.append("Fettucine Alfredo - Chicken")
                total_price += 18
            elif fettucine_option == 'shrimp':
                items.append("Fettucine Alfredo - Shrimp")
                total_price += 20
        if 'lasagna' in request.POST:
            items.append("Lasagna")
            total_price += 20
        if 'vealparm' in request.POST:
            items.append("Veal Parmesean")
            total_price += 20
        if 'bread' in request.POST:
            items.append("Garlic Bread")
            total_price += 10
        if 'special' in request.POST:
            items.append(request.POST['special'])
            total_price += 25

        instructions = request.POST.get('instructions', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')

        # Store data in session
        request.session['items'] = items
        request.session['total_price'] = total_price
        request.session['instructions'] = instructions
        request.session['name'] = name
        request.session['phone'] = phone
        request.session['email'] = email

        return redirect('confirmation')

    random_special = random.choice(specials)
    context = {"special": random_special}

    return render(request, "restaurant/order.html", context)

def confirmation(request):
    """
    View for displaying the confirmation page.
    """
    curr_time = time.time()
    cook_time = random.randint(30, 61)
    finish_time = curr_time + cook_time * 60

    curr_time = time.ctime(curr_time)
    finish_time = time.ctime(finish_time)

    context = {
        "time": curr_time,
        "readytime": finish_time,
        "items": request.session.get('items', []),
        "total_price": request.session.get('total_price', 0),
        "instructions": request.session.get('instructions', ''),
        "name": request.session.get('name', ''),
        "phone": request.session.get('phone', ''),
        "email": request.session.get('email', '')
    }

    return render(request, "restaurant/confirmation.html", context)