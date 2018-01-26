"""
Modul pro kresleni grafu pomoci knihovny tkinter
Blind Pew 2017 <blind.pew96@gmail.com>
GNU GPL v3

Test:

>>> import pygraf
>>> from tkinter import Tk, Canvas
>>> root = Tk()
>>> can = Canvas(root, width=200, height=200)
>>> can.pack()
>>> graf = pygraf.DigitalGraf(can,0,0,200,200,'red',200,'test',st = True)
>>> graf.run()

Vytvoreni grafu:

graf = pygraf.AnalogGraf(can, #platno kde se bude kreslit
                            0, #souradnice X
                            0, #souradnice Y
                            500, #velikost grafu X
                            500, #velikost grafu Y
                            'red', #barva cary
                            200, #rychlost prekreslovani v ms
                            'test', #jmenovka grafu
                            smooth = False) #zakaze vyhlazeni grafu
graf.run()
graf.buff(20) #vykresli zadanou hodnotu

"""

class Cons:
    """Konstanty"""
    
    OFFSET_TITLE = 40 #zacatek grafu
    OFFSET_FRAME = 2 #ramecek
    OFFSET_TEXTX = 25 #posun textu x
    OFFSET_TEXTY = 10 #posun textu y
    MIN_TIME_PRN = 100 #minimalni mereny cas vysoke urovne
    
    COLOR_GRID = "green"
    COLOR_TEXT = "white"
    COLOR_BACK = "black"
    
class Utils:
    """Pomocne funkce"""
        
    def frange(start, stop, step):
        """range pro cisla typu float"""
        i = start
        while i < stop:
            yield round(i,2)
            i += step

    def map(x, in_min, in_max, out_min, out_max):
        """arduino map() funkce"""
        try:
            return ((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min) 
        except:
            return 0
            
    def dash_x(sizex, delay, res):
        """rozestup casove osy"""
        return ((sizex//delay)*res)
    
    def random_data(od, do):
        """nahodne data pro testovani"""
        from random import randint
        
        if(od==0 and do==1):
            return bool(randint(0,1))
        else:
            return randint(od,do)
    
    def byte2bool(b):
        """prevede byte na bool"""
        return [bool(b & (1<<n)) for n in range(4)]

class Graf:
    """Spolecna trida pro kresleni grafu"""
    
    cislo = 0
    
    def __init__(self, can, x, y, sizex, sizey, col, delay, title, smooth=False, st=False):
        Graf.cislo = Graf.cislo + 1
        self.c = str(Graf.cislo) #pocitadlo instanci
        self.canvas = can #platno
        self.x = x #souradnice grafu
        self.y = y
        self.sizex = sizex #velikost grafu
        self.sizey = sizey
        self.color = col #barva grafu
        self.delay = delay #rychlost prekreslovani
        self.data = [] #namerena data
        self.b = 0 #buffer dat
        self.coords = [] #souradnice pro kresleni
        self.title = title #popisek grafu
        self.smooth = smooth #vyhlazeni
        self.st = st #self test
        self.ramecek()
                
    def ramecek(self):
        """vykresli ramecek okolo grafu"""
        self.canvas.create_rectangle(self.x,
            self.y,
            self.x+self.sizex,
            self.y+self.sizey,
            outline=Cons.COLOR_TEXT,
            fill=Cons.COLOR_BACK)
        self.canvas.create_text(self.x,
                self.y+Cons.OFFSET_TEXTY,
                text=self.title,
                fill=Cons.COLOR_TEXT,
                font='Helvica 16',
                anchor='w')
    
    def buff(self, data):
        """zasobnik pro prijata data"""
        self.b = data
        
    def plot(self):
        """vykresli graf"""
        self.canvas.delete('cara'+self.c)
        self.canvas.create_line(self.coords,
            width=1,
            smooth=self.smooth,
            tags='cara'+self.c,
            fill=self.color)
            
    def run(self):
        """casovac vykreslovani grafu"""
        self.pocitej()
        self.plot()
        self.canvas.after(self.delay, self.run)
                
class AnalogGraf(Graf):
    """Analogovy graf"""
    def __init__(self, can, x, y, sizex, sizey, col, delay, title, smooth=False, st = False):
        super().__init__(can, x, y, sizex, sizey, col, delay, title, smooth, st)
        self.res = 10
        self.mini = 0
        self.maxi = 0
        self.dilku = 5
        self.mrizka_ver()
        
        """seznam pro merena data"""
        for i in range(int((sizex-Cons.OFFSET_TITLE)/self.res)):
            self.data.append(0)
        
    def mrizka_ver(self):
        """vykresli mrizku - vertikalni"""
        x = Utils.dash_x(self.sizex,self.delay, self.res)
        for i in range(self.x+Cons.OFFSET_TITLE,self.x+self.sizex,x):
            self.canvas.create_line(i,
                self.y,
                i,self.y+self.sizey,
                fill=Cons.COLOR_GRID,
                tags='vgrid'+self.c,
                dash=5)
    
    def mrizka_horz(self):
        """horizontalni"""
        self.canvas.delete('hgrid'+self.c)
        for i in Utils.frange(self.mini,self.maxi,(self.maxi-self.mini)/self.dilku):
            y = Utils.map(i,self.mini,self.maxi,self.y+self.sizey-Cons.OFFSET_FRAME, self.y)
            self.canvas.create_line(self.x,
                y,
                self.x+self.sizex,
                y,
                fill=Cons.COLOR_GRID,
                tags='hgrid'+self.c,
                dash=5)
            self.canvas.create_text(self.x+Cons.OFFSET_TEXTX,
                y-Cons.OFFSET_TEXTY,
                text=i,
                fill=Cons.COLOR_TEXT,
                tags='hgrid'+self.c)

                    
    def pocitej(self):
        """Odstrani prvni hodnotu grafu, prida na posledni misto novou
        hodnotu"""
        del self.data[0]
        if(self.st):
            self.data.append(Utils.random_data(0, 20))
        else:
            self.data.append(self.b)
                
        """Ulozi krajni hodnoty grafu"""
        if(min(self.data) < self.mini):
            self.mini = min(self.data)
            self.mrizka_horz()
        if(max(self.data) > self.maxi):
            self.maxi = max(self.data)
            self.mrizka_horz()
                
        """Prepocita data grafu na souradnice"""
        del self.coords[:]
        for i in range(len(self.data)):
            self.coords.append(self.x+(i*self.res)+Cons.OFFSET_TITLE) #osa x
            self.coords.append(Utils.map(self.data[i],
                self.mini,
                self.maxi,
                self.y+self.sizey-Cons.OFFSET_FRAME,
                self.y)) #osa y

class DigitalGraf(Graf):
    """Digitalni graf"""
    def __init__(self, can, x, y, sizex, sizey, col, delay, title, smooth=False, st = False):
        super().__init__(can, x, y, sizex, sizey, col, delay, title, smooth, st)
        self.ms = 0 #delka trvani posledni vysoke urovne
        self.res = 5
        self.on = self.y+(self.sizey/2)
        self.off= self.y+self.sizey - Cons.OFFSET_TEXTY
        self.mrizka_horz()
        
        """seznam pro merena data"""
        for i in range(int((sizex-Cons.OFFSET_TITLE)/self.res)):
            self.data.append(False)
    
    def stav(self, s):
        if(s):
            return self.on
        else:
            return self.off
    
    def mrizka_horz(self):
        """popis vysoka nizka"""
        self.canvas.delete('hgrid'+self.c)
        self.canvas.create_text(self.x+Cons.OFFSET_TEXTX,
                self.on,
                text='High',
                fill=Cons.COLOR_TEXT,
                tags='hgrid'+self.c)
        self.canvas.create_text(self.x+Cons.OFFSET_TEXTX,
                self.off,
                text='Low',
                fill=Cons.COLOR_TEXT,
                tags='hgrid'+self.c)
                        
    def pocitej(self):
        """odstrani prvni hodnotu grafu, prida na posledni misto novou
        hodnotu"""
        del self.data[0]
        if(self.st):
            self.data.append(Utils.random_data(0,1))
        else:
            self.data.append(self.b)

        self.delka()
                
        """prepocita data grafu na souradnice"""
        del self.coords[:]
        x = 0
        for b in self.data:
            self.coords.append(self.x+(x*self.res)+Cons.OFFSET_TITLE)
            self.coords.append(self.stav(b))
            x = x+1
            self.coords.append(self.x+(x*self.res)+Cons.OFFSET_TITLE)
            self.coords.append(self.stav(b))
    
    def delka(self):
        """pocita delku trvani posledni vysoke urovne"""
        if(not self.data[-2] and self.data[-1]):
            #zacinam merit
            self.ms = 0
        if(self.data[-2] and self.data[-1]):
            #mereneni pokracuje
            self.ms += self.delay
        if(self.data[-2] and not self.data[-1]):
            #konec mereni
            if(self.ms > Cons.MIN_TIME_PRN):
                print("{0} - {1}ms".format(self.title, self.ms))

def main():
    
    from tkinter import Tk, Canvas
    okno = Tk()
    okno.title('PyGraf test')
    okno.resizable(False, False)

    platno = Canvas(okno,width=1020,height=520, background='black')
    platno.pack()

    graf = DigitalGraf(platno, 10, 10, 1000, 100, 'blue', 50, 'Digital', st = True)
    graf2 = AnalogGraf(platno, 10, 115, 1000, 400, 'red', 500, 'Analog', st = True, smooth = True)
    graf.run()
    graf2.run()

    okno.mainloop()

if __name__ == "__main__":
    main()
