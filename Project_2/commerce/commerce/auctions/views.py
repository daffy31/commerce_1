from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, categoryList,itemList, itemComments, Bid


def index(request):
    activeItems = itemList.objects.filter(itemIsActive = True)
    allCategories = categoryList.objects.all()
    return render(request, "auctions/index.html",{
        "activeItems":activeItems,
        "categories":allCategories,

    })

#San deutero argument vazoume to onoma tis metavlitis pou paei sto urls
def itemview(request, id):
    
    #id is byDefault the primary key in Django (i can change it if i want)
    itemDetails = itemList.objects.get(id = id)
    showComments = itemComments.objects.filter(itemDetails = itemDetails)
    userWon = itemDetails.itemPrice.bidUser
    # inWatchlist = request.user in itemDetails.itemWatchlist.all()
    if request.user == itemDetails.itemOwner:
        isOwner = True
    else:
        isOwner = False
    if request.user in itemDetails.itemWatchlist.all():
       inWatchlist = True
    else:
       inWatchlist = False
    return render(request, "auctions/itemview.html", {

        "inWatchlist":inWatchlist,
        "itemDetails":itemDetails,
        "newComment":showComments,
        "isOwner": isOwner,
        "userWon": userWon,
    })

def closeAuction(request, id):
    itemDetails = itemList.objects.get(id = id)
    itemDetails.itemIsActive = False
    itemDetails.save()
    activeItems = itemList.objects.filter(itemIsActive = True)
    allCategories = categoryList.objects.all()
    userWon = itemDetails.itemPrice.bidUser
    return render(request, "auctions/index.html",{
        "activeItems":activeItems,
        "categories":allCategories,
    })
    

def addWatchlist(request, id):
    itemDetails = itemList.objects.get(id = id)
    loggedUser = request.user
    itemDetails.itemWatchlist.add(loggedUser)
    return HttpResponseRedirect(reverse("itemview", args=(id, )))

def remWatchlist(request, id):
    itemDetails = itemList.objects.get(pk = id)
    loggedUser = request.user
    itemDetails.itemWatchlist.remove(loggedUser)
    return HttpResponseRedirect(reverse("itemview", args=(id, ))) 
  
def watchlsit(request):
    loggedUser = request.user
    # To itemInWatchlist einai to *related name* apo ta models
    itemsInWatchlist = loggedUser.itemInWatchlist.all()
    return render(request, "auctions/watchlist.html", {
       "itemsInWatchlist":itemsInWatchlist,

    })

def comments(request, id):
    loggedUser = request.user
    itemDetails = itemList.objects.get(id = id)
    userComment = request.POST['message']

    newComment = itemComments(

        #Aristera ta vars tou DB dexia ta vars tou function
        authorComment = loggedUser,        
        dbComment = userComment,
        itemDetails = itemDetails,

    )

    newComment.save()

    return HttpResponseRedirect(reverse("itemview", args=(id, ))) 

def newBid(request, id):
    userBid = request.POST["bidPrice"]
    itemDetails = itemList.objects.get(id=id)
    if float(userBid) > itemDetails.itemPrice.bidPrice:
        updatePrice = Bid(bidUser = request.user, bidPrice = float(userBid))
        updatePrice.save()
        itemDetails.itemPrice = updatePrice
        itemDetails.save()
        showComments = itemComments.objects.filter(itemDetails = itemDetails)
        if request.user == itemDetails.itemOwner:
            isOwner = True
        else:
            isOwner = False
        return render(request, "auctions/itemview.html",{
            "bidMessage":"Successful Bid!",
            "itemDetails":itemDetails,
            "successBid":True,
            "newComment":showComments,
            "isOwner":isOwner,
                        
    })
    else:
        return render(request, "auctions/itemview.html",{
            "bidMessage":"Unsuccessful Bid!",
            "itemDetails":itemDetails,
            "successBid":False
            
    })

def catFilter(request):
    userChoice = request.POST["categoryFilter"]
    if (request.method == "POST"):
        
        catChoice = categoryList.objects.get(itemCategory = userChoice)
        activeItems = itemList.objects.filter(itemIsActive = True, itemCategory = catChoice)
        allCategories = categoryList.objects.all()
        return render(request, "auctions/index.html",{
            "activeItems":activeItems,
            "categories":allCategories,

    })


def createList(request):
    # We use get to send values to our page
    if request.method == "GET":
        allCategories = categoryList.objects.all()
        return render(request, "auctions/createlist.html", {
        "categories":allCategories,
    })

    # We set the name of html item to a variable
    elif request.method == "POST":
        title = request.POST["title"]
        price = request.POST["price"]
        imageUrl = request.POST["imageUrl"]
        description = request.POST["description"]
        category = request.POST["categoryFilter"]   #This goes to html name attr

        #Get Data to create instance cause it is a foreign key
        owner = request.user
        categoryInstance =  categoryList.objects.get(itemCategory = category)
        bid = Bid(bidPrice=float(price), bidUser = owner)
        bid.save()

        # Create new object from models
        # We set the previous variable to our model variable
        newItem= itemList(
            itemTitle = title,
            itemPrice = bid,
            itemDecr = description,
            itemImage = imageUrl,
            itemCategory = categoryInstance,
            itemOwner = owner,

        )
        # We save the new object to our database
        newItem.save()

        return HttpResponseRedirect(reverse(index))
        
    
    



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
