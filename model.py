# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 16:53:05 2020

@author: Robab
"""
import matplotlib
matplotlib.use('TkAgg') 

import random
import operator
import matplotlib.pyplot
import matplotlib.animation
import agentframework
import csv
import tkinter
import requests
import bs4



#run the model when GUI menu acted
def run():
    num_of_agents = 10
    num_of_iterations = 100
    neighbourhood = 10
    
    #get data from web address
    r = requests.get(
        'http://www.geog.leeds.ac.uk/courses/computing/'
        'practicals/python/agent-framework/part9/data.html'
        )
    content = r.text
    soup = bs4.BeautifulSoup(content, 'html.parser')
    td_ys = soup.find_all(attrs={"class" : "y"})
    td_xs = soup.find_all(attrs={"class" : "x"})
    print(td_ys)
    print(td_xs)
    
    #get environment data from csv file
    f = open('in.txt', newline='')
    reader = csv.reader(f)
    environment = []
    for row in reader:
        rowlist = []
        for value in row:
            rowlist.append(float(value)) #float - matplotlib conversion error 
        environment.append(rowlist)       
    f.close()

    
    agents = [] #create empty 'agents' list
    
    #create agents from web data and add to 'agents' list
    for i in range(num_of_agents):
        y = int(td_ys[i].text)
        x = int(td_xs[i].text)
        agents.append(agentframework.Agent(environment, agents, y, x))
        
    carry_on = True
    
    # Move the agents (uses functions in agentframework.py)
    for j in range(num_of_iterations):
        for i in range(num_of_agents):
            agents[i].move()
            agents[i].eat()
            agents[i].share_with_neighbours(neighbourhood)    
    
    #update agents locations
    def update(frame_number):
        
        fig.clear()  
        global carry_on
    
        for i in range(num_of_agents):
                if random.random() < 0.5:
                    agents[i].y  = (agents[i].y + 1) % 99 
                else:
                    agents[i].y  = (agents[i].y - 1) % 99
                
                if random.random() < 0.5:
                    agents[i].x  = (agents[i].x + 1) % 99 
                else:
                    agents[i].x  = (agents[i].x - 1) % 99 
                    
        #update matplotlib scatter with new locations
        for i in range(num_of_agents):
            matplotlib.pyplot.scatter(agents[i].y, agents[i].x)
            matplotlib.pyplot.imshow(environment)

    
    fig = matplotlib.pyplot.figure(figsize=(7, 7))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_autoscale_on(False)
    
    matplotlib.pyplot.xlim(0, 99)
    matplotlib.pyplot.ylim(0, 99)
    for i in random.sample(range(num_of_agents),num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
    
    def gen_function(b = [0]):
        a = 0
        global carry_on 
        while (a < num_of_iterations):
            yield a			
            a = a + 1

    animation = matplotlib.animation.FuncAnimation(
        fig, update, frames=gen_function, repeat=False
        )
    canvas.show()
    
#setup GUI
fig1 = matplotlib.pyplot.figure(figsize=(7, 7))
root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig1, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run) 

tkinter.mainloop() 



