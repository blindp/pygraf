# pyGraf

Modul pro kreslení realtime grafů, analogových i digitálních.
Používá tkinter modul.

* self test:$ python3 -m pygraf

![Alt tag](./pygraf_test.png?raw=true "pygraf.py")

* použití:

```python

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

```
