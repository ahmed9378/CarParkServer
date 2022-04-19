from flask import Flask, render_template, request, redirect, abort

# my libraries
import master


# setup
app = Flask(__name__, template_folder="../templates")
mst = master.Master()

# variables
glist = []
ful = ''
avslots = 0
data = ''

# check requests
@app.before_request
def before_request_func():
    redirect('/')
    req_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    mst.addRequestRecord(str(req_ip))
    if(mst.checkRequestLimits(str(req_ip))):
        abort(429)


# routes > 4 route
@app.route('/')
def index():
    return updateData()

@app.route('/parkcar', methods=['POST'])
def parkcar():
    global data
    inputTxt = request.form['CarNumber']
    if inputTxt != '':
        try:
            data = mst.parkACar(inputTxt)
        except Exception as e:
            print("error parking car", e)
            pass
    return redirect('/')

@app.route('/unparkcar', methods=['POST'])
def unparkcar():
    global data
    inputTxt = request.form['SlotNumber']
    if inputTxt != '' and inputTxt.isnumeric():
        try:
            data = mst.unParkACar(slot_number=int(inputTxt))
        except Exception as e:
            print("error unparking car", e)
            pass
    else:
        data = "Please enter correct data format"
    return redirect('/')

@app.route("/parkinfo", methods=['POST', 'GET'])
def parkinfo():
    global data
    inputTxt = request.form['SNumber']
    if inputTxt != '' and inputTxt.isnumeric():
        try:
            data = mst.getParkInfo(slot_id=int(inputTxt))
        except Exception as e:
            print("error finding slot info", e)
            pass
    else:
        data = "Please enter correct data format"
    return redirect('/')

# update view data
def updateData():
    global data,glist,ful,avslots
    try:
        ful = '#FF0000' if mst.isGarageFull() else '#7CFC00'
        glist = mst.getParkStrList()
        avslots = mst.countFreeSlots()
    except:
        print("Error Updating Data")
        pass
    return render_template('index.html', park_info=str(data), garageInfo=glist, fuleGrageColor=ful, avilableSlots=avslots)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
