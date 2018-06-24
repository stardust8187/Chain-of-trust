from flask import Flask, render_template, request
import os
import subprocess
import requests as req
import json


app = Flask(__name__)


def readMoney():
    c = None
    e = None
    d = None
    with open("money","r") as mon:
        c,e,d = map(int,mon.read().split(' '))
    return (c,e,d) 

def writeMoney(c,e,d):
    with open("money",'w') as mon:
        mon.write(c.__str__()+" "+e.__str__()+" "+d.__str__())
    return 

def tx(money):
    c,e,d = readMoney()
    writeMoney(c,e-money,d+money)

@app.route('/')
def home():
    c,e,d = readMoney()
    return render_template('home.html',client=c,escrow=e,developer=d)


@app.route('/client')
def homeClient():    
   r = req.get('http://localhost:3000/api/Submitcode')
   l = []
   for I in r.json():
      print I["timestamp"]
      l1 = []
      l1.append(I['modulenum'])
      l1.append(I['time'])
      l1.append(I['date'].__str__()+"-"+I['month'].__str__()+"-"+I['year'].__str__())
      if (I['result'] == 0):
         l1.append("Test has failed")
      else:
         l1.append("Test has passed")
      l.append(l1)  
   return render_template('home1.html',item=l)



@app.route('/upload')
def upload_file():
   return render_template('upload.html')
    
@app.route('/up', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      m = request.form['mod']
      f = request.files['file']
      f.save(f.filename)
      ar = ["python",str(f.filename)]
      p = subprocess.Popen(args=ar,stdout=subprocess.PIPE)
      output = str(p.communicate()[0].decode("UTF-8"))
      o = None
      headers = {'Content-type': 'application/json'}
       
      data = '''
    {
    "$class": "org.example.basic.Submitcode",
    "modulenum": "MOD",
    "time": 5,
    "date": DATE,
    "month": MONTH,
    "year": YEAR,
    "result": RES,
    "transactionId": "",
    "timestamp": "2018-06-24T02:07:49.905Z"
    }
      '''
      url= "http://127.0.0.1:3000/api/Submitcode/"
      if (m == '1'):
          data = data.replace("MOD","1")
          data = data.replace("DATE","1")
          data = data.replace("MONTH","11")
          data = data.replace("YEAR","2018")
          money = 10
          with open('output','r') as op:
              o = op.read()
          string = "<center><b><h1>Module has been completed on time</h1></b></center>"
      elif (m=='2'):
          data = data.replace("MOD","2")
          data = data.replace("DATE","31")
          data = data.replace("MONTH","12")
          data = data.replace("YEAR","2019")
          money = 5
          with open('output','r') as op:
              o = op.read()
          string = "<center><h1> Module has been completed after the deadline </h1></center>"
      elif (m=='3'):
          data = data.replace("MOD","3")
          data = data.replace("DATE","15")
          data = data.replace("MONTH","11")
          data = data.replace("YEAR","2018")
          money =0
          with open ("outputfalse",'r') as op:
              o = op.read()
          string = "<center><h1>Module has failed the test cases</h1></center>"
      if (output == o):
          data = data.replace('RES',str(1))
      else:
          data = data.replace('RES',str(0))
      print data,url
      r = req.post(url, data=data, headers=headers)
      tx(money)
      print vars(r)
      return string






@app.route('/clientTransfer',methods=['POST'])
def client():
    j = request.args.get('money')
    c , e, d= readMoney()
    c -= int(j)
    e += int(j)
    writeMoney(c,e,d)
    print c,e,d
    return "success"

@app.route('/transfer',methods=['GET','POST'])
def transferFunds(): 
    j = request.args.get('money')
    c , e, d = readMoney()
    e -= int(j)
    d += int(j)
    writeMoney(c,e,d)
    return "success"


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)

