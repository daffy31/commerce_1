from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist", views.createList, name="createlist",),
    path("catFilter", views.catFilter, name="catFilter"),
    #Sto str: vazoume to onoma tis metavlitis to opoio meta xrisimopoioume sto HtML arxeio    
    path("itemview/<int:id>", views.itemview, name="itemview"), 
    path("remWatchlist/<int:id>", views.remWatchlist, name="remWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.watchlsit, name="watchlist"),
    path("comments/<int:id>", views.comments, name="comments"),
    path("newBid/<int:id>", views.newBid, name="newBid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),

]
