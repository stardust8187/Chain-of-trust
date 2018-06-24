from flask import Flask, render_template, request
import thread
import subprocess
import requests as req
import json
app = Flask(__name__)


@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/up', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
      ar = ["python",str(f.filename)]
      p = subprocess.Popen(args=ar,stdout=subprocess.PIPE)
      output = str(p.communicate()[0].decode("UTF-8"))
      o = None
      headers = {'Content-type': 'application/json'}
       
      with open("output",'r') as out:
          o = out.read() 
      data = '''
	{
    "$class": "org.example.basic.Submitcode",
    "modulenum": "1234",
    "time": 0,
    "date": 0,
    "month": 0,
    "year": 0,
    "result": RES,
    "transactionId": "",
    "timestamp": "2018-06-24T02:07:49.905Z"
  	}
      '''
      if (output == o):
          data = data.replace('RES',str(1))
          string = "success"
      else:
          data = data.replace('RES',str(0))
          string =  "Error"
      print data
      r = req.post("http://127.0.0.1:3000/api/Submitcode/", data=data, headers=headers)
      print vars(r)
      return string
		
if __name__ == '__main__':
   app.run(debug=True,host="0.0.0.0",port=6000)
