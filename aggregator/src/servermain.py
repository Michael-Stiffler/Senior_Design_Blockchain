# Webserver to request, verify, and recieve data from the blockchain and/or local storage.
# Upon installing flask, can be run using "python3 servermain.py". 
# Test as needed, expected data input is as written.
# DON'T USE PYPLOT!

from flask import Flask, render_template, redirect, url_for, request
from flask import make_response
from matplotlib.figure import Figure
from io import BytesIO
import base64
from datetime import datetime
import datetime as dt
import validation as val
from numpy import NaN 
import PyDbConn

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('/index.html')

@app.route("/index")

@app.route('/datapull', methods=['GET', 'POST'])
def datepull():
    if request.method == 'POST':
        datafromjs = request.form['mydata']
      #  print(type(datafromjs))
        if(datafromjs == "NaN") :
            return "No date entered."

        epoch = int(datafromjs)
        data = PyDbConn.get24HFromEpoch(epoch)
        valed_data = val.validate_by_merkle(data)
        
        times =        []
        temperatures = []
        humidities =   []
        xvals =        []
        yvals =        []

        for i in valed_data :

            pulledtime = i[1]

            times.append(pulledtime.timestamp())

            temp = i[2]
            temperatures.append(temp)
            humidities.append(i[3])
            xvals.append(i[4])
            yvals.append(i[5])

 
    #    print(times)
    #    print(temperatures)
    #    print(humidities)
    #    print(xvals)
    #    print(yvals)
        

         
#        # Data exact form currently unknown.
#        # Best case = NxM array of entries where N OR M = 5. 
#        # 5 expected columns or rows are to be parsed to the following format:
#            #X AXIS - timestamps in EPOCH, will be later converted for prettiness.
#        times = [1649576267800, 1649576367212, 1649576378347, 1649576390624, 1649576397041, 1649576403630]
#
#            #Y AXIS GRAPH 1 - TEMPERATURE in centigrade, values between -40 and +125. expected range of DHT22 sensor.
#        temperatures = [60,61,63,61,61,62]
#
#            #Y AXIS GRAPH 1 - RELATIVE HUMIDITY in percent, values between 20 and 80. expected range of DHT22 sensor.
#        humidities = [32,35,35,36,37,36]
#        
#            # X AXIS GRAPH 2 - X value of joystick at timestamp, values between -511 and 512.  
#       xvals = [-511, 24, 500, 0, 300, -200]
#
#            # Y AXIS GRAPH 2 - Y value of joystick at timestamp, values between -511 and 512.  
#        yvals = [-511, 300, -500, 300, 0, 60]

        # Generate the figures WITHOUT USING PYPLOT!! pyplot WILL cause memory leaks, and will eventually overload the server. 
        
        # GRAPH 1 - Temperature and Humidity
        THfig = Figure()
        ax1 = THfig.subplots()
        ax1.set_title("Temperature and Humidity")
        ax2 = ax1.twinx()
        ax1.set_ylabel("Temperature (°C)",color="blue")
        ax2.set_ylabel("Relative Humidity (%)",color="red")
        ax1.plot(times, temperatures, color="blue")
        #ax1.plot(temperatures, color="blue")
        ax2.plot(times, humidities,color="red")
        #ax2.plot(humidities,color="red")

        # Save it to a temporary buffer.
        buf = BytesIO()
        THfig.savefig(buf, format="png")

        # Embed the result in the html output.
        THdata = base64.b64encode(buf.getbuffer()).decode("ascii")


        # GRAPH 2 - Joystick Motion (X/Y motion)
        JMfig = Figure()
        jm1 = JMfig.subplots()
        jm1.set_title("Joystick Motion")
        jm1.plot(xvals, yvals)
        jm1.set_xlim([-511,512])
        jm1.set_ylim([-511,512])
        JMbuf = BytesIO()
        JMfig.savefig(JMbuf, format="png")
        JMdata = base64.b64encode(JMbuf.getbuffer()).decode("ascii")

        return f"<img src='data:image/png;base64,{THdata}'/><img src='data:image/png;base64,{JMdata}'/>"

    return render_template('index.html', message='')

if __name__ == "__main__":
    app.run(debug = True)