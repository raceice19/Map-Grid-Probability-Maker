# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 19:10:52 2023

@author: Kairas
"""
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import os.path
import re

class MapDivider:
    def __init__(self, master):
        self.master = master
        #Image
        self.render = ImageTk.PhotoImage(Image.open("map.png"))
        self.h = self.render.height()
        self.w = self.render.width()
        master.geometry(str(self.h+150)+"x"+str(self.w+75))
        #Frame setup
        self.buttons_frame = tk.Frame(master, bg="cyan")
        self.image_frame = tk.Frame(master, height=self.h, width=self.w,)
        self.color_frame = tk.Frame(master, bg="green")
        self.image_frame.grid(row=0, column=0, padx=5, pady=5)
        self.buttons_frame.grid(row=0, column=1, padx=5, pady=5)
        self.color_frame.grid(row=1, column=0, padx=5, pady=5)
        #Canvas
        self.canvas = tk.Canvas(self.image_frame, height=self.h, width=self.w)
        self.canvas.pack()
        self.canvas.create_image(0,0, anchor=tk.NW, image=self.render)
        self.canvas.bind("<Button-3>", self.erase)
        self.canvas.bind("<B3-Motion>", self.erase)
        #Code Variables
        self.boxsize = [0,0, 10,10]
        self.box_click = False
        self.edit_area_ison = False
        self.erase_ison = False
        self.box_list = {}
        self.x_scale = int(self.w/(self.boxsize[2]-self.boxsize[0]))
        self.y_scale = int(self.h/(self.boxsize[3]-self.boxsize[1]))
        self.colorsDict = {"#FF0000":10,"#FF8800":9,"#FFFF00":8,"#88FF00":7,"#00FF00":6,"#00FF88":5,"#00FFFF":4,"#0000FF":3,"#8800FF":2,"#FF00FF":1}
        self.colors = ["#FF0000","#FF8800","#FFFF00","#88FF00","#00FF00","#00FF88","#00FFFF","#0000FF","#8800FF","#FF00FF"]
        self.color = "#FF00FF"
        #UI Elements
        #Buttons
        self.box_resize = tk.Button(self.buttons_frame, text="Box Size", command = self.get_box_size)
        self.box_resize.grid(row=1, column = 0, padx=5, pady=5)
        self.render_lines = tk.Button(self.buttons_frame, text="Create Lines", command = self.render_lines_func)
        self.render_lines.grid(row=2, column = 0, padx=5, pady=5)
        self.edit_area_button = tk.Button(self.buttons_frame, text="Edit Areas", command = self.edit_area)
        self.edit_area_button.grid(row=3, column = 0, padx=5, pady=5)
        self.create_array = tk.Button(self.buttons_frame, text="Output Array", command = self.output_array)
        self.create_array.grid(row=4, column = 0, padx=5, pady=5)
        self.input_array_button = tk.Button(self.buttons_frame, text="Input Array", command = self.input_array)
        self.input_array_button.grid(row=5, column = 0, padx=5, pady=5)
        self.clear_colors = tk.Button(self.buttons_frame, text="Clear Area", command = self.reset_area)
        self.clear_colors.grid(row=6, column = 0, padx=5, pady=5)
        self.clear_lines = tk.Button(self.buttons_frame, text="Clear Lines", command = self.reset_lines)
        self.clear_lines.grid(row=7, column = 0, padx=5, pady=5)
        self.x_scale_label = tk.Label(master, textvariable=self.x_scale)
        self.x_scale_label.grid(row=0, column = 2, padx=5, pady=5)
        self.y_scale_label = tk.Label(master, textvariable=self.y_scale)
        self.y_scale_label.grid(row=0, column = 2, padx=5, pady=5)
        #Colors
        self.color_buttons = []
        num = 1
        for color in self.colors:
            button = tk.Button(self.color_frame, bg=color, width=4, height=2, command=lambda c=color: self.pick_color(c))
            button.grid(row=2, column = num, padx=5, pady=5)
            num = num+1
            self.color_buttons.append(button)

    def get_box_size(self):
        self.box_resize.config(relief=tk.SUNKEN)
        self.edit_area_button.config(relief=tk.RAISED)
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.box_clicker)
    
    def box_clicker(self, event):
        if(self.box_click):
            self.boxsize[2] = event.x
            self.boxsize[3] = event.y
            self.box_click = False
            self.canvas.unbind("<Button-1>")
            self.x_scale = int( self.w/(self.boxsize[2]-self.boxsize[0]) )
            self.y_scale = int( self.h/(self.boxsize[3]-self.boxsize[1]) )
            self.box_resize.config(relief=tk.RAISED)
        else:
            self.boxsize[0] = event.x
            self.boxsize[1] = event.y
            self.box_click = True
        print(self.boxsize)
        
    def render_lines_func(self):
        self.canvas.delete("lines")
        box_size = (self.boxsize[2]-self.boxsize[0], self.boxsize[3]-self.boxsize[1])
        for i in range(int(self.w/box_size[0])+1):
            self.canvas.create_line(box_size[0]*i,0, box_size[0]*i,self.h, fill="black", width=1, tags="lines")
        for i in range(int(self.h/box_size[1])+1):
            self.canvas.create_line(0, box_size[1]*i, self.w, box_size[1]*i, fill="black", width=1, tags="lines")
    
    def edit_area(self):
        if(self.edit_area_ison):
            self.edit_area_button.config(relief=tk.RAISED)
            self.edit_area_ison = False
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.draw()
        else:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.box_resize.config(relief=tk.RAISED)
            self.edit_area_button.config(relief=tk.GROOVE)
            self.edit_area_ison = True
            self.canvas.bind("<Button-1>", self.edit_area_func)
            self.canvas.bind("<B1-Motion>", self.edit_area_func)
        
    def edit_area_func(self, event):
        box_size = (self.boxsize[2]-self.boxsize[0], self.boxsize[3]-self.boxsize[1])
        x = event.x // (box_size[0])
        y = event.y // (box_size[1])
        self.box_list.update({(x, y): self.color})
        self.draw_one(x, y, self.color)
     
    def draw_one(self, x, y, color):
        box_size = (self.boxsize[2]-self.boxsize[0], self.boxsize[3]-self.boxsize[1])
        self.canvas.create_rectangle(x*box_size[0], y*box_size[1], 
                                     x*box_size[0]+box_size[0], y*box_size[1]+box_size[1], fill = color, stipple='gray50', tags="boxes")
    def draw(self):
        self.canvas.delete("boxes")
        box_size = (self.boxsize[2]-self.boxsize[0], self.boxsize[3]-self.boxsize[1])
        for coords, color in self.box_list.items():
            self.canvas.create_rectangle(coords[0]*box_size[0], coords[1]*box_size[1], 
                                         coords[0]*box_size[0]+box_size[0], coords[1]*box_size[1]+box_size[1], fill = color, stipple='gray50', tags="boxes")

            
    def output_array(self):
        arr = np.zeros((self.y_scale+1, self.x_scale+1), dtype=np.int8 )
        for coords, color in self.box_list.items():
            arr[coords[1], coords[0]] = self.colorsDict.get(color);
        f = open("output.txt", "w")
        np.set_printoptions(linewidth=500)
        f.write(str(self.boxsize[2]-self.boxsize[0])+','+str(self.boxsize[3]-self.boxsize[1])+'\n')
        f.write(np.array2string(arr, threshold=np.inf).replace('10', 'a').replace(' ',''))
        f.close()
    
    def input_array(self):
        path = './output.txt'
        self.box_list = {}
        inverseColorsDict = dict((v, k) for k, v in self.colorsDict.items())
        if(os.path.isfile(path)):
            f = open(path, "r")
            boxsize_string = f.readline()
            boxsize_array = np.array(eval(boxsize_string))
            self.boxsize = [0,0]+boxsize_array.tolist()
            print(self.boxsize)
            
            file = f.read()
            result = re.sub("([0-9a-z])",lambda x:x.group(0)+',',file)
            result = re.sub("]\n","],\n",result)
            array = np.array(eval(result.replace('a', '10')))
            for i in range(len(array)):
                for j in range(len(array[i])):
                    num = array[i][j]
                    if num > 0:
                        self.box_list.update({(j, i): inverseColorsDict.get(num)})
            self.draw()
            f.close()
        else:
            print("File doesn't exist")
            
        return
    def pick_color(self, color):
        self.color=color
        
    def erase(self, event):
        box_size = (self.boxsize[2]-self.boxsize[0], self.boxsize[3]-self.boxsize[1])
        x = event.x // (box_size[0])
        y = event.y // (box_size[1])
        if (x,y) in self.box_list: self.box_list.pop((x, y))
        self.draw()
        return
    
    def reset_lines(self):
        self.canvas.delete("lines")
        
        
    def reset_area(self):
        self.box_list = {}
        self.canvas.delete("boxes")
        
root = tk.Tk()
mapDiv = MapDivider(root)
root.mainloop()
