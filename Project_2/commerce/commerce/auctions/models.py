from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class categoryList(models.Model):
    itemCategory = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.itemCategory
    
class Bid(models.Model):
    bidPrice = models.FloatField()
    bidUser = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBidded")

    def __float__(self):
        return self.bidPrice

class itemList(models.Model):
    itemTitle = models.CharField(max_length=32)
    itemPrice = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")
    itemDecr = models.CharField(max_length=1000)
    itemImage = models.CharField(max_length=2000)
    itemIsActive = models.BooleanField(default=True)
    itemOwner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    itemCategory = models.ForeignKey(categoryList, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    itemWatchlist = models.ManyToManyField(User,blank=True, null=True, related_name="itemInWatchlist")

    def __str__(self) -> str:
        return self.itemTitle
    
class itemComments(models.Model):
    authorComment = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    dbComment = models.CharField(max_length=250)
    itemDetails = models.ForeignKey(itemList, on_delete=models.CASCADE, blank=True, null=True, related_name="details")

    def __str__(self):
        return self.dbComment

