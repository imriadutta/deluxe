from django.db import models


class Room(models.Model):
    room_no = models.IntegerField()
    title = models.CharField(max_length=20)
    image = models.ImageField()
    passcode = models.CharField(max_length=15)
    date = models.DateField(auto_now_add=True)
    price = models.IntegerField()
    features = models.CharField(max_length=500)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.room_no) + ': ' + self.title


class Guest(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.firstname + ' ' + self.lastname


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bill = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return 'Room no.' + str(self.room.room_no)


class Service(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    electricity = models.IntegerField()
    gas = models.IntegerField()
    internet = models.IntegerField()

    def __str__(self):
        return 'Room no.' + str(self.reservation.room.room_no)


class Payment(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    method = models.CharField(max_length=25)

    def __str__(self):
        return str(self.id)


class LoginStat(models.Model):
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date)
