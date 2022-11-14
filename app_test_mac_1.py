# Import Module
from tkinter import *
from PIL import ImageTk, Image 
import os.path
import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import time
import csv
import numpy as np
import datetime
from scipy.signal import find_peaks, peak_widths
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

LARGE_FONT= ("Verdana",18, weight:="bold")
NORM_FONT= ("Verdana",16)
BOLD_FONT= ("Verdana",16, weight:="bold")
SMALL_FONT= ("Verdana",14)

CHOPTIONS = [
"CH1_PE",
"CH2_PE"
] 

DECOPTIONS = [
"1",
"8",
"64",
"1024",
"8192",
"65536",
"80000"
] 

global initialization
initialization=['192.168.0.15', 'F18', 'CH1_PE', '6.5', '2.5','23.4', '0', '0', '0', '630', '1.30', '65536','0.015','7000']

# Initialization function (Starts after Initialize button is pressed)
def init_measurement(IP1,P1,V1,h1,B1,CH):
    global initialization
    initialization[0]=str(IP1.get())
    initialization[1]=str(P1.get())
    initialization[2]=str(CH.get())
    initialization[3]=str(V1.get())
    initialization[4]=str(h1.get())
    initialization[5]=str(B1.get())
    #printing to terminal in GUI (text box T)
    T.insert(END,"Redpitaya IP adress: "+initialization[0]+ "\n")
    T.insert(END,"Measurement possition: "+initialization[1]+ "\n") 
    T.insert(END,"Measurement channel: "+initialization[2]+ "\n")
    T.insert(END,"Water volume:"+initialization[3]+"dl"+ "\n") 
    T.insert(END,"Detector height:"+initialization[4]+"m"+ "\n")   
    T.insert(END,"SiPM BIAS:"+initialization[5]+"V"+ "\n")
    T.insert(END,"-------------------------------------"+"\n")
    T.see(END)   
    #print("Redpitaya IP adress:"+initialization[0])
    #print("Measurement possition:"+initialization[1])
    #print("Measurement channel:"+initialization[2])
    #print("Water volume:"+initialization[3]+"dl")
    #print("Detector height:"+initialization[4]+"m")
    #print("SiPM BIAS:"+initialization[5]+"V")
  
    canvas.itemconfig(dot, fill='green')
    button4.config(state=DISABLED)
    IP.config(state=DISABLED)
    P.config(state=DISABLED)
    V.config(state=DISABLED)
    h.config(state=DISABLED)
    B.config(state=DISABLED)
    w.config(state=DISABLED)
    button5.config(state=NORMAL)
    #printinit()
    
def printinit():
    print(initialization)
# Measurement start function (Starts after Measure button is pressed)
def start_measurement(ND11,ND21,ND31,ID1,IR1,DEC1,TRL1,TRD1):
    global initialization
    initialization[6]=str(ND11.get())
    initialization[7]=str(ND21.get())
    initialization[8]=str(ND31.get())
    initialization[9]=str(ID1.get())
    initialization[10]=str(IR1.get())
    initialization[11]=str(DEC1.get())
    initialization[12]=str(TRL1.get())   
    initialization[13]=str(TRD1.get())  
    
    #printing to terminal in GUI (text box T)
    T.insert(END,"\n"+"Pulse ID:"+initialization[9]+"\n")
    T.insert(END,"Inserted reactivity:"+initialization[10]+" $"+"\n")
    T.insert(END,"ND06A:"+initialization[6]+"\n")
    T.insert(END,"ND10A:"+initialization[7]+"\n") 
    T.insert(END,"ND20A:"+initialization[8]+"\n")
    T.insert(END,"Decimation:"+initialization[11]+"\n")
    T.insert(END,"Trigger level:"+initialization[12]+" V"+"\n")
    T.insert(END,"Trigger delay:"+initialization[13]+" Samples"+"\n")
    T.insert(END,"-------------------------------------"+"\n")
    T.see(END) 
    
    #print("ND06A:"+initialization[6])
    #print("ND10A:"+initialization[7])
    #print("ND20A:"+initialization[8])
    #print("Pulse ID:"+initialization[9])
    #print("Inserted reactivity:"+initialization[10])
    #print("Decimation:"+initialization[11])
    #print("Trigger level:"+initialization[12]+"V")
    #print("Trigger delay:"+initialization[13]+"Samples")
  
    
    #button5.config(state=DISABLED)
    #ND1.config(state=DISABLED)
    #ND2.config(state=DISABLED)
    #ND3.config(state=DISABLED)
    #ID.config(state=DISABLED)
    #IR.config(state=DISABLED)
    #DEC.config(state=DISABLED)
    #TRL.config(state=DISABLED)
    #TRD.config(state=DISABLED)
    #printinit()  
    pulse_record()
    
    
# Pulse record function (starts after measure button is pressed)    
def pulse_record_test():
    global initialization  
    numberOfPulses = initialization[9] #pulse ID
    water_volume = initialization[3] #water volume
    position=initialization[1] #Channel position
    decimation=initialization[11] #Decimation
    trigger_level=initialization[12] #trigger level V
    trigger_delay=initialization[13] #trigger delay S
    pulse_ID=initialization[9] #pulse ID
    pulse_IR=initialization[10] #instrted reactivity
    measurement_channel=initialization[2] #redpitaya measurement channel
    
    #ND filter selection storage
    ND_filter="noND"
    if initialization[6]=="1":
        ND_filter = "ND06A"
    elif initialization[7]=="1":
        ND_filter = "ND10A"
    elif initialization[8]=="1":
        ND_filter = "ND20A"
    
    #print(ND_filter)
    
    #Pulses fired during measurements on that day
    datenow = datetime.datetime.now()
    date_string = datenow.strftime('%d_%m_%Y')
    fileNameP="recorded_pulses_"+date_string+".csv"
    fileP = open(fileNameP, "a")
    fileP.write(pulse_ID+","+pulse_IR+","+decimation+","+trigger_level+","+trigger_delay+","+ND_filter)
    fileP.close()
    
    #file creation
    fileName= "pulse_"+str(numberOfPulses)+".csv"  #name of the CSV file generated
    print("File created")
    file = open(fileName, "a")
    file.write('---------------------------------\n')
    file.write('Intention: Pulse testing\n')
    file.write('Sensor: Ketek Sipm PM3315\n')
    file.write('Amplifire: ThorLabs AMP220\n')
    file.write('ND Filter: ThorLabs ND06A\n')
    file.write('Water volume: '+water_volume+'dl\n')
    file.write('Data acquisition: Redpitaya STEMlab 125-14\n')
    file.write('Redpitaya decimation:'+decimation+'\n')
    file.write('Redpitaya trigger level:'+trigger_level+'\n')
    file.write('Redpitaya trigger delay:'+trigger_delay+'\n')
    file.write('Location: JSI TRIGA reactor ('+position+')\n')
    file.write('Pulse ID: '+pulse_ID+'\n')
    now = datetime.datetime.now()
    dt_string = now.strftime('%d/%m/%Y %H:%M:%S')
    file.write('Date and time:' + dt_string + '\n')
    file.write('---------------------------------\n')
    file.write('Time,Voltage\n')
    file.close()
    
    #Redpitaya measurement time line
    buffer_length=16384 #redpitaya buffer length
    sampling_rate=125000000 #redpitaya 125*10^6 S/s
    decimation_redpitaya=int(decimation)
    stop_time=(decimation_redpitaya/sampling_rate)*buffer_length
    #print(stop_time)

    t=np.linspace(start=0,stop=stop_time,num=16384)
    initialization[9]=str(int(numberOfPulses)+1)
    ID.delete(0,END)
    ID.insert(0,initialization[9])
    #redpitaya initialization
    rp_s = scpi.scpi(initialization[0])
    rp_s.tx_txt('ACQ:RST')


    #rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')
    #rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')
    rp_s.tx_txt('ACQ:DEC '+decimation)
    rp_s.tx_txt('ACQ:TRIG:LEV '+trigger_level) #trigger in Volts usual: 0.007
    rp_s.tx_txt('ACQ:TRIG '+measurement_channel)
    rp_s.tx_txt('ACQ:TRIG:DLY '+trigger_delay) #trigger delay

    print('Initialization')


    rp_s.tx_txt('ACQ:START')

    time.sleep(stop_time+0.5)  #flushing the buffer (waiting for new measurements)

    print('Ready')

    #while 1:
    #    rp_s.tx_txt('ACQ:TRIG:STAT?')
        #print('Waiting')
    #    if rp_s.rx_txt() == 'TD':
    #        print('TRIGGERED')
    #        break

    rp_s.tx_txt('ACQ:SOUR1:DATA?') #reading buffer
    buff_string = rp_s.rx_txt()
    buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
    buff = list(map(float, buff_string))  #measurements

    #save to file
    with open(fileName,"a") as f:
        writer=csv.writer(f)
        writer.writerows(zip(t,buff))

    #pulse analysis

    #peaks, _ =find_peaks(buff,height=0.11,width=100)
    #print(peaks)

    #peak
    signal=np.asarray(buff)
    maximum=max(buff)
    maximumind=buff.index(maximum)
    print("Signal peak: "+str(maximum)+" V")
    maximuminda=np.array([maximumind])
    #FWHM
    results_half = peak_widths(buff, maximuminda, rel_height=0.5)
    dt=stop_time/buffer_length
    fwhm=results_half[0]*dt
    print("FWHM: "+str(fwhm)+" s")
    
    #integral
    a=1000
    RE=np.trapz(signal[(maximumind-a):(maximumind+a)],dx=dt)
    print("Released energy: "+str(RE)+" a.u.")
    #measurement_on()
    fileP = open(fileNameP, "a")
    fileP.write(","+str(maximum)+","+str(fwhm)+","+str(RE)+"\n")
    fileP.close()
    
    #--------------------------------------------------------------------------------------------------------------------------------------
    ## New window with results
    #--------------------------------------------------------------------------------------------------------------------------------------
    window = Toplevel(root)
    window.title('Pulse number: '+numberOfPulses)
    window.minsize(500, 500)
    # the figure that will contain the plot
    fig = Figure(figsize = (6, 4),
                 dpi = 100)
  
    # adding the subplot
    plot1 = fig.add_subplot(111)
  
    # plotting the graph
    plot1.plot(t,signal,".")
    plot1.plot(t[maximumind], signal[maximumind], "x", color="C1")
    plot1.hlines(results_half[1],results_half[2]*dt,results_half[3]*dt, color="C1", linewidth=5)
    plot1.fill_between(t[(maximumind-a):(maximumind+a)],signal[(maximumind-a):(maximumind+a)], step="pre", alpha=0.4)
    plot1.legend(["Signal","Peak signal","FWHM","Integration area"], loc="upper right")
    plot1.set_ylabel("Voltage [V]")
    plot1.set_xlabel("Time [s]")
  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    #canvas.draw()
  
    # placing the widgets on the Tkinter window
    canvas.get_tk_widget().grid(row=0,column=0, padx = 10, pady = 10)
    label100 = Label(window, text="File name: "+fileName, font=NORM_FONT)
    label100.grid(row = 1, column = 0, pady = 2)
    label101 = Label(window, text="Signal peak: "+str(maximum)+" V", font=NORM_FONT)
    label101.grid(row = 2, column = 0, pady = 2)
    label102 = Label(window, text="FWHM: "+str(*results_half[0]*dt)+" s", font=NORM_FONT)
    label102.grid(row = 3, column = 0, pady = 2)
    label103 = Label(window, text="Energy released: "+str(RE)+" a.u.", font=NORM_FONT)
    label103.grid(row = 4, column = 0, pady = 2)
    
    
    
# Pulse record function (starts after measure button is pressed)    
def pulse_record():
    global initialization  
    numberOfPulses = initialization[9] #pulse ID
    water_volume = initialization[3] #water volume
    position=initialization[1] #Channel position
    decimation=initialization[11] #Decimation
    trigger_level=initialization[12] #trigger level V
    trigger_delay=initialization[13] #trigger delay S
    pulse_ID=initialization[9] #pulse ID
    pulse_IR=initialization[10] #instrted reactivity
    
    #ND filter selection storage
    ND_filter="noND"
    if initialization[6]=="1":
        ND_filter = "ND06A"
    elif initialization[7]=="1":
        ND_filter = "ND10A"
    elif initialization[8]=="1":
        ND_filter = "ND20A"
    
    #print(ND_filter)
    
    #Pulses fired during measurements on that day
    datenow = datetime.datetime.now()
    date_string = datenow.strftime('%d_%m_%Y')
    fileNameP="recorded_pulses_"+date_string+".csv"
    fileP = open(fileNameP, "a")
    fileP.write(pulse_ID+","+pulse_IR+","+decimation+","+trigger_level+","+trigger_delay+","+ND_filter+"\n")
    
    #file creation
    fileName= "pulse_"+str(numberOfPulses)+".csv"  #name of the CSV file generated
    print("File created")
    file = open(fileName, "a")
    file.write('---------------------------------\n')
    file.write('Intention: Pulse testing\n')
    file.write('Sensor: Ketek Sipm PM3315\n')
    file.write('Amplifire: ThorLabs AMP220\n')
    file.write('ND Filter: ThorLabs ND06A\n')
    file.write('Water volume: '+water_volume+'dl\n')
    file.write('Data acquisition: Redpitaya STEMlab 125-14\n')
    file.write('Redpitaya decimation:'+decimation+'\n')
    file.write('Redpitaya trigger level:'+trigger_level+'\n')
    file.write('Redpitaya trigger delay:'+trigger_delay+'\n')
    file.write('Location: JSI TRIGA reactor ('+position+')\n')
    file.write('Pulse ID: '+pulse_ID+'\n')
    now = datetime.datetime.now()
    dt_string = now.strftime('%d/%m/%Y %H:%M:%S')
    file.write('Date and time:' + dt_string + '\n')
    file.write('---------------------------------\n')
    file.write('Time,Voltage\n')
    file.close()
    
    #Redpitaya measurement time line
    buffer_length=16384 #redpitaya buffer length
    sampling_rate=125000000 #redpitaya 125*10^6 S/s
    decimation_redpitaya=int(decimation)
    stop_time=(decimation_redpitaya/sampling_rate)*buffer_length
    #print(stop_time)

    t=np.linspace(start=0,stop=stop_time,num=16384)
    initialization[9]=str(int(numberOfPulses)+1)
    ID.delete(0,END)
    ID.insert(0,initialization[9])
    #redpitaya initialization
    #measurement_on()
    
    #--------------------------------------------------------------------------------------------------------------------------------------
    ## New window with results
    #--------------------------------------------------------------------------------------------------------------------------------------
    window = Toplevel(root)
    window.title('Pulse number: '+numberOfPulses)
    window.geometry('600x'+str(root.winfo_height())+'+'+str(root.winfo_width()+10)+'+30')
    #window.minsize(500, 500)
    # the figure that will contain the plot
    fig = Figure(figsize = (6, 4),
                 dpi = 100)
  
    # list of squares
    y = [i**2 for i in range(101)]
  
    # adding the subplot
    plot1 = fig.add_subplot(111)
  
    # plotting the graph
    plot1.plot(y,y)
    plot1.set_ylabel("U [V]")
    plot1.set_xlabel("t [s]")
  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    #canvas.draw()
  
    # placing the widgets on the Tkinter window
    canvas.get_tk_widget().grid(row=0,column=0, padx = 10, pady = 10)
    label100 = Label(window, text="File name: "+fileName, font=NORM_FONT)
    label100.grid(row = 1, column = 0, pady = 2)
    label101 = Label(window, text="Signal peak: "+trigger_level+" V", font=NORM_FONT)
    label101.grid(row = 2, column = 0, pady = 2)
    label102 = Label(window, text="FWHM: "+trigger_level+" s", font=NORM_FONT)
    label102.grid(row = 3, column = 0, pady = 2)
    label103 = Label(window, text="Energy released: "+trigger_level+" a.u.", font=NORM_FONT)
    label103.grid(row = 4, column = 0, pady = 2)    
    
    
# create root window
def measurement_on():
    button5.config(state=NORMAL) #measurement button enabled
    canvas.itemconfig(dot, fill='red') #measurement light
    
root = Tk()

# root window title and dimension
root.title("Cherenkov pulse recorder")
# Set geometry(widthxheight)
#root.geometry('1150x800')
root.minsize(500, 500)

# adding menu bar in root window
# new item in menu bar labelled as 'New'
# adding more items in the menu bar
menu = Menu(root)
item = Menu(menu,tearoff=0)
item.add_command(label='New')
menu.add_separator()
item.add_command(label="Exit", command=quit)
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)


#filemenu.add_command(label="Settings", command= lambda: popupmsg("Not supported yet"))


# adding a label to the root window

img = ImageTk.PhotoImage(Image.open("logo.png"))
panel = Label(root, image = img)
panel.grid(row = 0, column = 2, columnspan = 2, rowspan = 15)
label = Label(root, text="Pulse recorder initialization", font=LARGE_FONT)
label.grid(row = 0, column = 0, pady = 2)



 #IP adress entry
label1 =Label(root, text="IP adress:", font=NORM_FONT)
label1.grid(row = 1, column = 0)
var1 = StringVar()
IP = Entry(root,textvariable=var1, font=NORM_FONT)
IP.grid(row = 1, column = 1)
IP.insert(0,initialization[0])
        #Measuremnt position
label2 =Label(root, text="Position:", font=NORM_FONT)
label2.grid(row = 2, column = 0)
var2 = StringVar()
P = Entry(root,textvariable=var2, font=NORM_FONT)
P.grid(row = 2, column = 1)
P.insert(0,initialization[1])
        #Water volume adress entry
label3 =Label(root, text="Water volume [dl]:", font=NORM_FONT)
label3.grid(row = 4, column = 0)
var3 = StringVar()
V = Entry(root,textvariable=var3, font=NORM_FONT)
V.grid(row = 4, column = 1)
V.insert(0,initialization[3])
        #Detector height
label4 = Label(root, text="Detector height [m]:", font=NORM_FONT)
label4.grid(row = 5, column = 0)
var4 = StringVar()
h = Entry(root,textvariable=var4, font=NORM_FONT)
h.grid(row = 5, column = 1)
h.insert(0,initialization[4])
        #SiPM BIAS voltage
label5 = Label(root, text="SiPM BIAS [V]:", font=NORM_FONT)
label5.grid(row = 6, column = 0)
var5 = StringVar()
B = Entry(root,textvariable=var5, font=NORM_FONT)
B.grid(row = 6, column = 1)
B.insert(0,initialization[5])

label = Label(root, text="Experiment properties", font=LARGE_FONT)
label.grid(row = 8, column = 0, pady = 2)

        #ND filter
label6 = Label(root, text="ND filter:", font=NORM_FONT)
label6.grid(row = 11, column = 0,rowspan = 3)
var6 = IntVar()
ND1 = Checkbutton(root, text='ND06A',variable=var6, onvalue=1, offvalue=0, font=NORM_FONT)
ND1.grid(row = 11, column = 1)
var7 = IntVar()
ND2 = Checkbutton(root, text='ND10A',variable=var7, onvalue=1, offvalue=0, font=NORM_FONT)
ND2.grid(row = 12, column = 1)
var8 = IntVar()
ND3 = Checkbutton(root, text='ND20A',variable=var8, onvalue=1, offvalue=0, font=NORM_FONT)
ND3.grid(row = 13, column = 1)
        
        #Pulse ID
label7 = Label(root, text="Pulse ID:", font=NORM_FONT)
label7.grid(row = 9, column = 0)
var9 = StringVar()
ID = Entry(root,textvariable=var9, font=NORM_FONT)
ID.grid(row = 9, column = 1)
ID.insert(0,initialization[9])
        
        #Inserted reactivity
label8 = Label(root, text="Inserted reactivity [$]:", font=NORM_FONT)
label8.grid(row = 10, column = 0)
var10 = StringVar()
IR = Entry(root,textvariable=var10, font=NORM_FONT)
IR.grid(row = 10, column = 1)
IR.insert(0,initialization[10])

        #Measuring channel

label9 = Label(root, text="Meassuring channel:", font=NORM_FONT)
label9.grid(row = 3, column = 0)
var11 = StringVar()
var11.set(CHOPTIONS[0])
w = OptionMenu(root, var11, *CHOPTIONS)
w.config(font=NORM_FONT)
w.grid(row = 3, column = 1)

        #Decimation

label10 = Label(root, text="Decimation:", font=NORM_FONT)
label10.grid(row = 15, column = 0)
var12 = StringVar()
var12.set(DECOPTIONS[5])
DEC = OptionMenu(root, var12, *DECOPTIONS)
DEC.config(font=NORM_FONT)
DEC.grid(row = 15, column = 1)

        #Trigger level 
label11 = Label(root, text="Trigger level [V]:", font=NORM_FONT)
label11.grid(row = 16, column = 0)
var13 = StringVar()
TRL = Entry(root,textvariable=var13, font=NORM_FONT)
TRL.grid(row = 16, column = 1)
TRL.insert(0,initialization[12])

        #Trigger delay
label12 = Label(root, text="Trigger delay [Samples]:", font=NORM_FONT)
label12.grid(row = 17, column = 0)
var14 = StringVar()
TRD = Entry(root,textvariable=var14, font=NORM_FONT)
TRD.grid(row = 17, column = 1)
TRD.insert(0,initialization[13])

label13 = Label(root, text="Ready to measure:", font=NORM_FONT)
label13.grid(row = 18, column = 0)
canvas = Canvas(root, 
           width=40, 
           height=40)
canvas.grid(row=18, column=1)

dot=canvas.create_oval(15,15,30,30, fill="red")

#Buttons
#-----------------------------------------------------------------  
#Initializatio      
button4 = Button(root, text="Initialize",
                    command=lambda: [init_measurement(var1,var2,var3,var4,var5,var11)], font=NORM_FONT)
button4.grid(row = 7, column = 0, columnspan=2, padx = 10, pady = 10)
#Measurement
button5 = Button(root, text="Measure",
                    command=lambda: [[start_measurement(var6,var7,var8,var9,var10,var12,var13,var14)]], state=DISABLED, font=NORM_FONT)
button5.grid(row = 19, column = 0, columnspan=2, padx = 10, pady = 10)

#print(initialization) 

# Terminal
#-----------------------------------------------------------------
label13 = Label(root, text="Terminal:", font=LARGE_FONT)
label13.grid(row = 12, column = 2)
T = Text(root, height = 10, width = 52, font=NORM_FONT)
T.grid(row = 13,column = 2,rowspan=8, padx = 10, pady = 10)

# Execute Tkinter
root.mainloop()
