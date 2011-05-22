#game adventures in geometric forms words
# general rules: form can be placed to another for, but no to itself
# shifting can be done
# win point is
# create levels
from __future__ import division
from Gui import *
import Tkinter as Tk
import random
import math
global msx, msy
msx = -1
msy = -1

def is_in_walls_area(i,j):
    if i in range(1, field.nx-1) and j in range(1,field.ny-1):
        return True
    else:
      return False
    
def is_free_point_around(i,j):
    #full shiting
    #around = ( (i-1,j), (i+1,j), (i,j-1), (i, j+1), (i-1,j-1),  (i-1,j+1),(i+1,j+1),(i+1,j-1) )
    
    #only ortogonal shiftign
    around = ( (i-1,j), (i+1,j), (i,j-1), (i, j+1) )
    
    #nado shtobi sdvigalist v raznie napravlenia
    t = []
    #print i,j
    for item in around:
        x = random.randint(0,len(around)*10)
        t.append((x, item))
        
    t.sort()
    #print around
    #print t
    #raw_input()
    
    
    for x,(i,j) in t:
        if is_in_walls_area(i,j) and (i,j) not in walls_ind and object.i != i and object.j!=j:
            return True, i,j
        else:
            return False, 0 ,0

def shifting(event=None):
    #print 'here'
    # usoverh: kvadrat moget naezdat na krug i naoborot)
    for (i,j) in walls_ind:
        #print i,j
        #raw_input()
        flag, i_new, j_new = is_free_point_around(i,j)
        if flag:
            print 'shifting!'
            delta_i ,delta_j = i_new - i, j_new - j
            dx = delta_i * lensize
            dy = delta_j * lensize
            walls[(i,j)].i = walls[(i,j)].i + delta_i
            walls[(i,j)].j = walls[(i,j)].j + delta_j
            walls[(i,j)].obj.move(dx,-dy) # as in gui y point down
            # here we can update other parameters of walls: xllc, yllc
            del walls_ind[(i,j)]
            walls_ind[(i_new,j_new)] = walls[(i,j)].id
            walls[(i_new,j_new)] = walls[(i,j)]
            del walls[(i,j)]
        else:
            continue

def bindall():
    print "bind"
    #print object
    #print object.id
    if object.id == 1:
        print 'circle'
        g.bind('<Alt-a>',object.invl)
        g.bind('<Alt-d>',object.invr)
        g.bind('<Alt-w>',object.invu)
        g.bind('<Alt-s>',object.invd)
    elif object.id == 2:
        g.bind('<q>',object.perevul)
        g.bind('<e>',object.perevur)
        g.bind('<z>',object.perevdl)
        g.bind('<c>',object.perevdr)

        
    g.bind('<w>',object.mu)
    g.bind('<s>',object.md)
    g.bind('<a>',object.ml)
    g.bind('<d>',object.mr)
    g.bind('<W>',object.mu)
    g.bind('<S>',object.md)
    g.bind('<A>',object.ml)
    g.bind('<D>',object.mr)
    g.bind('<g>',object.change)
    g.bind('<h>',shifting)
    g.bind('<H>',shifting)
    g.bind('<Escape>',quit)
    
    
def unbindall():
    print "unbind"
    print object
    print object.id
    if object.id == 1:
        g.unbind('<Alt-a>')
        g.unbind('<Alt-d>')
        g.unbind('<Alt-w>')
        g.unbind('<Alt-s>')
    elif object.id == 2:
        g.unbind('<q>')
        g.unbind('<e>')
        g.unbind('<z>')
        g.unbind('<c>')

        
    g.unbind('<w>')
    g.unbind('<s>')
    g.unbind('<a>')
    g.unbind('<d>')
    g.unbind('<W>')
    g.unbind('<S>')
    g.unbind('<A>')
    g.unbind('<D>')
    g.unbind('<g>')
    g.unbind('<h>')
    g.unbind('<H>')
    g.unbind('<Escape>')   
    

    
class XY_template:
    """ represent basic form in 2D"""
    
    def __init__(self, width, height, lw):
        self.width = width
        self.height = height
        self.linewidth = lw
    
#xy = XY_template(5,4,2)
#print xy.width, xy.height


class SimpleForms(XY_template):
    """ represent plaing forms in 2D: square, /, \, circle, triangle 
    Circle, / and \  can be packed in square, 
    triangle can be packed in \, / and circle and square
    """
    
    def __init__(self, size, padx, pady, lw):
        XY_template.__init__(self, size, size, lw)
        self.size = size
        self.padx = padx
        self.pady = pady
        self.i = 0
        self.j = 0
        
    
    def move(self, event):
        pass
        
    def mu(self,  event):
        print "UP"
        self.move(event,0,1)
       
    def md(self, event):
        self.move(event,0,-1)
        
    def mr(self, event):
        
        self.move(event,1,0)    

    def ml(self, event):
        self.move(event,-1,0)    

    
# f = SimpleForms(10, 5,5,2)
# print f
# print f.size, f.width, f.padx, f.pady

lensize = 30
linewidth = 1

class GeoCircle(SimpleForms):
    """represents a playin circle
    as circle packed into square its padx = lensize - savedwidth - linewidth(square) - savedwidth = ls-3lw
    circle can be packed only 1 time
    
    pady -same cause of symmetry
    
    """
    
    def __init__(self, color='black'):
        SimpleForms.__init__(self, lensize, lensize-3*linewidth, lensize-3*linewidth, linewidth)
        self.cent_x = int(lensize/2)
        self.cent_y = int(lensize/2)
        self.rad = int((lensize-3*linewidth)/2)
        self.canvas = field.canvas
        self.color = color
        self.id = 1
        self.insquare = False
        
    def draw(self, i,j):
        # place circle in i j square of field
        
        flag, x,y = field.ij2xy(i,j,'c')#field is global var
        if flag:
        # if True - place new position, if not - do nothing
            self.i = i
            self.j=  j
            self.cent_x, self.cent_y = x,y
            self.obj = self.canvas.circle([self.cent_x, self.cent_y], self.rad, 'white',outline=self.color)

        else:
            pass
    
    
    def move(self,event,delta_i,delta_j):
        #print delta_i, delta_j, self.i, self.j, field.test_ij(self.i + delta_i,self.j + delta_j)
        global msx, msy, xscrollbar, yscrollbar
        if (self.i + delta_i,self.j + delta_j) in walls_ind:
            id = walls_ind[(self.i + delta_i,self.j + delta_j)] 
            if id == self.id:
                return
            if id == 2: #square
                if self.insquare:
                    #print self.insquare
                    return
                else:
                    self.insquare = True
            else:
                self.insquare = False
        else:
            self.insquare = False
            
        if field.test_ij(self.i + delta_i,self.j + delta_j):
            dx = delta_i * lensize
            dy = delta_j * lensize
            self.i = self.i + delta_i
            self.j = self.j + delta_j
            self.obj.move(dx,-dy) # as in gui y point down
            [[xlu, ylu], [xrd, yrd]] = self.obj.coords()
              #autoscroll
            if msx == -1 and msy == -1:
                sdx = xscrollbar.get()
                # print sdx, xscrollbar, type(xscrollbar)
                msx = 1- (sdx[1]-sdx[0])
               
                sdy = yscrollbar.get()
                sdy = sdy[1]-sdy[0]
                msy =1-sdy
                
            print "MSX",msx, msy

            new_xview = msx*(self.i * lensize) / ( field.nx*lensize)
            field.canvas.xview_moveto(new_xview)
            new_yview =  msy*((field.ny-self.j) * lensize) / ( field.ny*lensize)
            #print new_xview, new_yview, (field.canvas_xsize-field.window_xsize)/field.canvas_xsize
            field.canvas.yview_moveto(new_yview)
            # print self.cent_x, self.cent_y
            
            
            # print xlu, ylu, xrd, yrd
            self.cent_x = xlu + (xrd-xlu)/2.
            self.cent_y = ylu + (yrd-ylu)/2.
            # print self.cent_x, self.cent_y
            global win
            if win.i == self.i and win.j == self.j:
                print "You Win", self.id, win.id, walls_ind[(win.i,win.j)]
            else:
                pass
                #shifting()
    def invl(self, event):
        
        if (self.i -1,self.j) not in walls or \
           (self.i ,self.j-1) not in walls or \
           (self.i ,self.j+1) not in walls: \
            return
        
        if  self.insquare == False and \
           (walls_ind[(self.i -1,self.j)] == 2 or\
            walls_ind[(self.i ,self.j-1)] ==2 or \
            walls_ind[(self.i ,self.j+1)] ==2):
            return
        
        self.move(event,-2,0)
        
        
    def invr(self, event):
        if (self.i +1,self.j) not in walls or \
           (self.i ,self.j-1) not in walls or \
           (self.i ,self.j+1) not in walls: \
            return
        
        if  self.insquare == False and \
           (walls_ind[(self.i +1,self.j)] == 2 or\
            walls_ind[(self.i ,self.j-1)] ==2 or \
            walls_ind[(self.i ,self.j+1)] ==2):
            return
        
        self.move(event,2,0)
    
    def invu(self, event):
        print "invu", self.insquare
        if (self.i ,self.j-1) not in walls or \
           (self.i -1,self.j) not in walls or \
           (self.i +1,self.j) not in walls: \
            return
        
        if  self.insquare == False and \
           (walls_ind[(self.i,self.j-1)] == 2 or\
            walls_ind[(self.i -1 ,self.j)] ==2 or \
            walls_ind[(self.i +1,self.j)] ==2):
            return
        
        self.move(event,0,2)
        
    def invd(self, event):
        if (self.i ,self.j-1) not in walls or \
           (self.i -1,self.j) not in walls or \
           (self.i +1,self.j) not in walls: \
            return
        
        if  self.insquare == False and \
           (walls_ind[(self.i ,self.j-1)] == 2 or\
            walls_ind[(self.i -1,self.j)] ==2 or \
            walls_ind[(self.i +1,self.j)] ==2):
            return
        
        self.move(event,0,-2)
        
  
    
    def change(self, event):
        global object
        global walls
        if  (self.i ,self.j) in walls:
            #unbindall()
            walls_ind[(self.i ,self.j)] = self.id
            walls[(self.i ,self.j)] , object = object, walls[(self.i ,self.j)] 
            walls[(self.i ,self.j)].obj.lower()
            object.obj.lift()
            object.obj.config(outline='blue')
            walls[(self.i ,self.j)].obj.config(outline='black')
            object.oncircle = True
            bindall()

        else:
            return

    
class GeoSquare(SimpleForms):
    """represents a playin square
    
    """
    
    def __init__(self, color='black'):

        SimpleForms.__init__(self, lensize, lensize-3*linewidth, lensize-3*linewidth, linewidth)
        self.len = int(lensize-4*linewidth)
        self.xllc = 2 #lower left corner
        self.yllc = 2   
        self.color = color
        self.canvas = field.canvas
        self.id=2
        self.oncircle = False
        
        
        
    def draw(self, i,j):
        # place square in i j square of field
        
        flag, x,y = field.ij2xy(i,j,'s')#field is global var
        if flag:
        # if True - place new position, if not - do nothing
            self.i = i
            self.j = j
            self.xllc, self.yllc = x,y
            self.obj = self.canvas.rectangle([[self.xllc,self.yllc], [self.xllc+self.len, self.yllc+self.len]],   'white',outline=self.color)

        else:
            pass
    
    
    def move(self,event,delta_i,delta_j):
        global field, xscrollbar, yscrollbar, msx,msy
        #print delta_i, delta_j, self.i, self.j, field.test_ij(self.i + delta_i,self.j + delta_j)
        print "enter move"
        if (self.i + delta_i,self.j + delta_j) in walls_ind:
            print "1"
            id = walls_ind[(self.i + delta_i,self.j + delta_j)] 
            if id == self.id:
                return
            if id == 1: #circle
                if self.oncircle:
                    #print self.insquare
                    return
                else:
                    self.oncircle = True
            else:
                self.oncircle = False
        else:
            self.oncircle = False
        
        print "2"
       
        if field.test_ij(self.i + delta_i,self.j + delta_j):
            dx = delta_i * lensize
            dy = delta_j * lensize
            self.i = self.i + delta_i
            self.j = self.j + delta_j
            self.obj.move(dx,-dy) # as in gui y point down
            [[xlu, ylu], [xrd, yrd]] = self.obj.coords()
            # print xlu, ylu, xrd, yrd
            self.xulc = xlu 
            self.uulc = yrd
            
            #autoscroll
            if msx == -1 and msy == -1:
                sdx = xscrollbar.get()
                # print sdx, xscrollbar, type(xscrollbar)
                msx = 1- (sdx[1]-sdx[0])
               
                sdy = yscrollbar.get()
                sdy = sdy[1]-sdy[0]
                msy =1-sdy
                
            print "MSX",msx, msy

            new_xview = msx*(self.i * lensize) / ( field.nx*lensize)
            field.canvas.xview_moveto(new_xview)
            new_yview =  msy*((field.ny-self.j) * lensize) / ( field.ny*lensize)
            #print new_xview, new_yview, (field.canvas_xsize-field.window_xsize)/field.canvas_xsize
            field.canvas.yview_moveto(new_yview)
            # print self.cent_x, self.cent_y
        
            global win
            if win.i == self.i and win.j == self.j:
                print "You Win"
            else:
                pass
                #shifting()

        # xnew = math.fabs(delta_i) / 10
        # ynew = math.fabs(delta_j) / 10 
        # xscrollbar.set(xnew,xnew + sdx)
        # yscrollbar.set(ynew, ynew + sdy)

        
    def perevul(self, event):
        
        if (self.i -1,self.j) not in walls or \
           (self.i ,self.j+1) not in walls :
           
            return
        
        if  self.oncircle == False and \
           (walls_ind[(self.i -1,self.j)] == 1 or\
            walls_ind[(self.i ,self.j+1)] ==1) :
            
            return
        
        self.move(event,-1,1)
        
        
    def perevdl(self, event):
        if (self.i ,self.j-1) not in walls or \
           (self.i -1,self.j) not in walls :
           
            return
        
        if  self.oncircle == False and \
           (walls_ind[(self.i,self.j-1)] == 1 or\
            walls_ind[(self.i-1 ,self.j)] ==1 ) :
            
            return
        
        self.move(event,-1,-1)
    
    def perevur(self, event):
        if (self.i ,self.j+1) not in walls or \
           (self.i +1,self.j) not in walls  :
           
            return
        
        if  self.oncircle == False and \
           (walls_ind[(self.i,self.j+1)] == 1 or\
            walls_ind[(self.i +1 ,self.j)] ==1 ) :
            
            return
        
        self.move(event,1,1)
        
    def perevdr(self, event):
        if (self.i ,self.j-1) not in walls or \
           (self.i +1,self.j) not in walls :
           
            return
        
        if  self.oncircle == False and \
           (walls_ind[(self.i ,self.j-1)] == 1 or\
            walls_ind[(self.i +1,self.j)] == 1) :
            
            return
        
        self.move(event,1,-1)
        
    def change(self, event):
        global object
        global walls
        if  (self.i ,self.j) in walls:
            walls_ind[(self.i ,self.j)] = self.id
            walls[(self.i ,self.j)] , object = object, walls[(self.i ,self.j)] 
            walls[(self.i ,self.j)].obj.lower()
            object.obj.lift()
            object.obj.config(outline='blue')
            walls[(self.i ,self.j)].obj.config(outline='black')
            # unbindall()
            object.onsqare = True
            bindall()# pochemu nenado unbindit..bindi dla drugogo ijecta ne rabotaut i ne pishiet error
           
        else:
            return
  
def CreateGeoByType(type, color=None):
    if type == 1:
        return GeoCircle(color)
    elif type ==2:
        return GeoSquare(color)
  
class Field():
    """ a game map """
    def __init__(self, num_x, num_y, pad):
        self.nx = num_x
        self.ny = num_y
        self.width = self.nx * lensize 
        self.height = self.ny * lensize 
        self.pad = pad
        # coords of lower left corner
        self.x_llc = -num_x * lensize/2.
        self.y_llc = -num_y * lensize/2.
        self.act_geo = None
        
        
    def draw(self):
        self.canvas_xsize = self.width + 2*self.pad
        self.canvas_ysize = self.height  + 2*self.pad
        print self.canvas_xsize, self.canvas_ysize
        self.canvas=g.ca(width= self.canvas_xsize,height= self.canvas_ysize, bd=0,
                xscrollcommand=xscrollbar.set,
                yscrollcommand=yscrollbar.set, scrollregion=(0, 0, self.canvas_xsize , self.canvas_ysize ))
        self.canvas.config(bg='white')
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        for i in range(0,self.ny+1):
            x1 = -self.canvas.width/2+self.pad
            y1 = self.canvas.height/2-self.pad - i* lensize 
            x2 = -x1
            y2 = y1
            self.canvas.line([[x1,y1],[x2,y2]],width=linewidth)
        for i in range(0,self.nx+1):
            x1 = -self.canvas.width/2+self.pad + i * lensize
            y1 = self.canvas.height/2-self.pad 
            x2 = x1
            y2 = -y1
            self.canvas.line([[x1,y1],[x2,y2]],width=linewidth)
        
    def xy2ij(self,x,y):
        # x,y in decartian, i,j - from lowest left corner
        
        x = x - self.x_llc
        y = y - slef.x_llc
        if x<0 or y<0:
            print "xy2ij, out of field"
            x = 0
            y=0
        i = int(x) / self.nx 
        j = int(y) / self.ny 
        return i,j
 
    def ij2xy(self,i,j, case):
        if case == 'c':
            # return central point in square
            if self.test_ij(i,j):
                x = i*lensize + lensize/2. + self.x_llc
                y = j*lensize + lensize/2. + self.y_llc
                return True,x,y
            else:
                return False, 0, 0
        elif case=='s':
            # return lower left coord +1,+1 in square
            if self.test_ij(i,j):
                x = i*lensize + 2 + self.x_llc
                y = j*lensize + 2 + self.y_llc
                return True,x,y
            else:
                return False, 0, 0
        elif case=='0':
            # return verhniy leviy ugol
            if self.test_ij(i,j):
                x = i*lensize +  self.x_llc
                y = j*lensize +  self.y_llc
                return True,x,y
            else:
                return False, 0, 0
       
    def test_ij(self,i,j):
        if i < 0 or j < 0 or i >= self.nx or j >= self.ny:
            return False
        else:
            return True
        
        

    
g=Gui()
g.title('Adventures in Geometric Forms')
def center_window(w=800, h=600):
 # get screen width and height
 ws = g.winfo_screenwidth()
 hs = g.winfo_screenheight()
 # calculate position x, y
 x = (ws/2) - (w/2) 
 y = (hs/2) - (h/2)
 #print ws, hs, x,y
 #return x,y
 #root.geometry('%dx%d+%d+%d' % (w, h, x, y))
 g.geometry("%dx%d%+d%+d" % (w, h, x, y))



center_window()


frame = g.frame
    
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)    

xscrollbar = Tk.Scrollbar(frame, orient='horizontal')
xscrollbar.grid(row=1, column=0, sticky=E+W)

yscrollbar = Tk.Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)



field = Field(25,25,lensize*2.0)
field.window_xsize = 800
field.window_ysize = 600
field.draw()

xscrollbar.config(command=field.canvas.xview)
yscrollbar.config(command=field.canvas.yview)

field.canvas.xview_moveto(0.0)
field.canvas.yview_moveto(1.0)


num_geos = []


# create walls
walls_ind=dict()
walls=dict()
num_obj_class = 2
for i in range(1, field.nx-1):
    for j in range(1, field.nx-1):
        chance = random.randint(0,2)
        if chance !=0:
            walls_ind[(i,j)] = chance
            
# place walls
for key in walls_ind:
    if walls_ind[key] == 1:
        walls[key] = GeoCircle()
    elif walls_ind[key] == 2:
        walls[key] = GeoSquare()
        
# draw walls
for key in walls:
    walls[key].draw(*key)

# creating walker and bindings
# if create him before walls, walls be located on another canvas over it.
# must be same canvas for field and objects...
#c = GeoCircle('red')
#c.draw(0,0)
s = GeoSquare('blue')
s.draw(0,0)
object = s
bindall() 
is_win = False
for i in range(field.nx/2, field.nx-1):
    for j in range(field.nx/2, field.nx-1):
        if not is_win and (i,j) not in walls_ind:
            is_win = True
            win = GeoCircle('red')
            win.draw(i,j)
            walls_ind[(i,j)]  = win.id
            print "Win point created"
            break
if not is_win:
    print "No win point"


#scrollbar = Tk.Scrollbar(field.canvas)
#scrollbar.pack(side=RIGHT, fill=Y)
#a=Tk.Scrollbar(field.canvas)
g.mainloop()




