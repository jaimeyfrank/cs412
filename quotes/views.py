from django.shortcuts import render
import random

"""global variables: lists of quotes and images"""

quotes = ["An actor should never be larger than the film he's in.",
          "It's the actors who are prepared to make fools of themselves who are usually the ones who come to mean something to the audience.",
          "The only thing that I'm obsessed with is sleeping and, actually, it is more than an obsession, it is a pleasure. I love sleeping so much that I could do it 12 hours a day if I didn't have to turn on the alarm clock... and still, sometimes..."
]

images = ["https://pyxis.nymag.com/v1/imgs/737/d3a/2c6a79c13a667c80b8a672a26c975c6e6b-christian-bale.rsquare.w330.jpg",
          "https://variety.com/wp-content/uploads/2022/07/MCDDAKN_EC004.jpg?w=1000&h=667&crop=1&resize=910%2C607",
          "https://www.bosshunting.com.au/cdn-cgi/imagedelivery/izM8XxyLg9MD6py1ribxJw/www.bosshunting.com.au/2022/05/Christian-Bale-American-Psycho-Tom-Cruise-David-Letterman.jpg/w=770,h=433"]


"""view definitions"""

def quote(request):
    """
    View for displaying a random quote and image.
    """
   
    random_index = random.randint(0, len(quotes) - 1)
    random_quote = quotes[random_index]
    random_index = random.randint(0, len(quotes) - 1)
    random_image = images[random_index]

    context = {"quote": random_quote, "image": random_image}

    return render(request, 'quotes/quote.html', context)

def show_all(request):
    """
    View for displaying all quotes and images.
    """
    context = {"quotes": quotes, "images": images}

    return render(request, "quotes/show_all.html", context)

def about(request):
    """
    View for displaying information about Christian Bale.
    """
    return render(request, "quotes/about.html")