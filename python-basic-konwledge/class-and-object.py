class Bot():
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def move(self, speedx, speedy):
        self.posx += speedx
        self.posy += speedy

bot = Bot(3, 4)
bot.move(2, 2)
print(bot.posx, bot.posy)

# Homwword
class Car():
    def __init__(self, maxV, aV):
        self.maxV = maxV
        self.aV = aV
    def getTime(self, currentV):
        return (self.maxV - currentV) / self.aV

car = Car(120, 15)
time = car.getTime(40)
print(time)