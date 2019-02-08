from flask import Flask,request,render_template

from flask import Flask, flash, request, redirect, url_for

from werkzeug.utils import secure_filename

import os

import csv

from zeep import Client, exceptions

from zeep.wsse.username import UsernameToken

 

 

 

def readcsv(filename):

    r=[]

    with open(filename, newline='') as myFile:

        reader = csv.reader(myFile, delimiter=";")

        for row in reader:

         r.append(row)

    return r

 

def charinstring(str,ch):

    r=0

    for char in str:

        if char==ch:

         r = 1

    return r

 

 

 

def savedocfromfstore (key):

    head = {"ip": "127.0.0.1", "login": "some_nice_user", "mac": "22:42:46:28:c1:57"}

    client = Client("http://cc-haproxy.rgs.ru:28080/filestore?wsdl",

                    wsse=UsernameToken('loginwebservice', 'passwordwebservice', use_digest=True))

    keyvalue = {"key": key}

    result = client.service.readFile(head, keyvalue)

    doc = (result["document"])

    cont = doc["content"]

    typedoc = doc["mimeType"]

    type = ""

    i = 0

    for char in typedoc:

        i = i + 1

        if char == "/":

            n = i

    doctype = typedoc[n:i]

    path=os.getcwd()+"""/ExportFstore/"""

    res=charinstring(key,'/')

    if res == 1:

       src = key

       key = src.split('/')[5]

    print (key)

    filename =path+key+"."+doctype

    out_file = open(filename, "wb")

    out_file.write(cont)

    out_file.close()

    return ("777")

 

 

UPLOAD_FOLDER = os.getcwd()+"/"

    #'C:/Distr/'

ALLOWED_EXTENSIONS = set(['csv'])

 

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

 

def allowed_file(filename):

    return '.' in filename and \

           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 

 

@app.route("/")

def hello():

   return render_template("index.html")

 

 

 

 

@app.route('/', methods=['GET', 'POST'])

def upload_file():

    if request.method == 'POST':

        # check if the post request has the file part

        if 'file' not in request.files:

            flash('No file part')

            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also

        # submit an empty part without filename

        if file.filename == '':

            flash('No selected file')

            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            csvdata = readcsv(UPLOAD_FOLDER+filename)

            for x in csvdata:

             try:

                savedocfromfstore(x[0])

                print("SUCESS: " + x[0])

 

 

             except:

                print("ERROR: " + x[0])

 

 

    return render_template('index.html')

 

 

 

if __name__ == "__main__":

    app.run(host='10.221.1.39', port = 8080)
