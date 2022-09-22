from time import sleep
import board
import random
import asyncio
from rainbowio import colorwheel
import neopixel

NUM_PIXELS = 37
PIXEL_PIN = board.A3


class Lights:   

    def __init__(self):        
        self.cmap = [0] * NUM_PIXELS        
        self.pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, auto_write=False)
        self.pixels.brightness = 0.01
        self.stop_flag = False
        self.methods = self.getMethods()
        self.colormaps = self.getColorMaps()
        self.currentColorMap = random.choice(list(self.colormaps.keys()))
        self.currentMethod = random.choice(list(self.methods.keys()))

    async def run(self):
        self.SetColorMap()        
        await self.methods[self.currentMethod]()

    # Colormap methods
    def getRed(self, color):
        return (color >> 16)

    def getGreen(self, color):
        return ((color & 0x00ff00) >> 8)

    def getBlue(self, color):
        return (color & 0x0000ff)
        
    def getColor(self, r, g, b):
        color = r << 16
        color += g << 8
        color += b
        return color

    def SingleColor(self, color):
        for i in range(NUM_PIXELS):
            self.cmap[i] = color
        
    def LinearFade(self, colorStops):
        num = len(colorStops)-1
        steps = NUM_PIXELS // (2 * num)
        extra = NUM_PIXELS % (2 * num)
        
        idx = 0
        cursteps = 0
        for i in range(num):
            cursteps = steps
            if i == 0:
                cursteps -= 1
                extra += 1
            if extra and i:
                cursteps += 1
                extra -= 1
            c1 = [self.getRed(colorStops[i]), self.getGreen(colorStops[i]), self.getBlue(colorStops[i])]
            c2 = [self.getRed(colorStops[i+1]), self.getGreen(colorStops[i+1]), self.getBlue(colorStops[i+1])]
            d = [(c2[0] - c1[0])//cursteps, (c2[1] - c1[1])//cursteps, (c2[2] - c1[2])//cursteps]
            
            for j in range(cursteps):
                r = c1[0] + d[0] * j
                g = c1[1] + d[1] * j
                b = c1[2] + d[2] * j
                self.cmap[idx + j] = self.getColor(r,g,b) 
            
            idx += cursteps
        
        self.cmap[idx] = self.cmap[idx - 1]
        idx += 1
        for i in range(NUM_PIXELS//2 -1):
            self.cmap[idx + i] = self.cmap[idx - i - 1]
        
        self.cmap[ NUM_PIXELS  -1] = self.cmap[0]

    def SetColorMap(self):
        for k, v in self.colormaps.items():
            if k == self.currentColorMap:
                if isinstance(v, int):
                    self.SingleColor(v)
                else:
                    self.LinearFade(v)

    # Set methods
    async def Wipe(self):        
        for i in range(NUM_PIXELS):
            self.pixels[i] = self.cmap[i]
            await asyncio.sleep(0.1)
            self.pixels.show()

        for i in range(NUM_PIXELS):
            self.pixels[i] = 0
            await asyncio.sleep(0.1)
            self.pixels.show()
    
    async def Pulse(self):
        for j in range(5, 255, 5):
            for k in range(NUM_PIXELS):
                r = int (j/256.0 * self.getRed(self.cmap[k])) & 0xff
                g = int (j/256.0 * self.getGreen(self.cmap[k])) & 0xff
                b = int (j/256.0 * self.getBlue(self.cmap[k])) & 0xff
                c = self.getColor(r,g,b)
                self.pixels[k] = c
            
            await asyncio.sleep(0.01)
            self.pixels.show()
        
        for j in range(255, 5, -5):
            for k in range(NUM_PIXELS):
                r = int (j/256.0 * self.getRed(self.cmap[k])) & 0xff
                g = int (j/256.0 * self.getGreen(self.cmap[k])) & 0xff
                b = int (j/256.0 * self.getBlue(self.cmap[k])) & 0xff
                c = self.getColor(r,g,b)
                self.pixels[k] = c
            
            await asyncio.sleep(0.01)
            self.pixels.show()

    async def Chase(self):
        for j in range(3):
            self.pixels.fill((0, 0, 0))
            for k in range(j, NUM_PIXELS, 3):
                self.pixels[k] = self.cmap[k]
            
            await asyncio.sleep(0.5)
            self.pixels.show()
    
    async def Wheel(self):
        if isinstance(self.colormaps[self.currentColorMap],int):
            mult = 256/NUM_PIXELS
            for i in range(NUM_PIXELS):
                k = i * mult
                r = int (k/256.0 * self.getRed(self.cmap[i])) & 0xff
                g = int (k/256.0 * self.getGreen(self.cmap[i])) & 0xff
                b = int (k/256.0 * self.getBlue(self.cmap[i])) & 0xff
                self.cmap[i] = self.getColor(r,g,b)

        for j in range(NUM_PIXELS):
            for k in range(NUM_PIXELS):
                idx = (j+k) % NUM_PIXELS
                self.pixels[idx] = self.cmap[k]
            await asyncio.sleep(0.1)
            self.pixels.show()

    async def Sparkle(self):    
        for j in range(NUM_PIXELS):
            k = random.randint(0,256)
            r = int (k/256.0 * self.getRed(self.cmap[j])) & 0xff
            g = int (k/256.0 * self.getGreen(self.cmap[j])) & 0xff
            b = int (k/256.0 * self.getBlue(self.cmap[j])) & 0xff
            self.pixels[j] = self.getColor(r,g,b)
        await asyncio.sleep(0.1)
        self.pixels.show()

    async def Random(self):
        for j in range(NUM_PIXELS):
            m = random.randint(0,100) % 2
            n = random.randint(0,NUM_PIXELS-1)
            if m:
                self.pixels[j] = self.cmap[n]
            else:
                self.pixels[j] = 0
        await asyncio.sleep(0.2)
        self.pixels.show()

    def getMethods(self):
        methods =  {
        "random" : self.Random,
        "sparkle" : self.Sparkle,
        "wheel" : self.Wheel,
        "chase" : self.Chase,
        "pulse": self.Pulse,
        "wipe": self.Wipe
        }
        return methods

    def getColorMaps(self):
        colormaps = {   
            'red'    : 0xff0000, 
            'orange' : 0xff5000, 
            'yellow' : 0xffff00,
            'green'  : 0x00ff00,
            'blue'   : 0x0000ff,
            'purple' : 0x7f00ff,
            'pink'   : 0xff1493,
            'white'  : 0xffffff,
            'rainbow': [0x8000ff, 0x00b4ec, 0x80ffb4, 0xffb462, 0xff0000],
            'hot'    : [0x0b0000, 0xb20000, 0xff5a00, 0xffff04, 0xffffff],
            'cool'   : [0x00ffff, 0x40bfff, 0x8080ff, 0xbf40ff, 0xff00ff],
            'jet'    : [0x000080, 0x0080ff, 0x7bff7b, 0xff9700, 0x800000],
            'bone'   : [0x000000, 0x38384e, 0x707b8f, 0xa8c7c7, 0xffffff],
        }
        return colormaps



