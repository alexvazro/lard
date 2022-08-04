from flask import Flask, render_template, request

from threading import Thread


application = Flask('')
app = application



@app.route('/')
def home():

    return "I'm alive"

  

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/restart')
def restart():
  import main
  app.run(host='0.0.0.0',port=8080)
  return "done"


@app.route('/next', methods = ["POST"])
def next():
    command_name = request.form.get("new_command")
    new_info = request.form.get("new_info")
    return render_template("next.html", command_name = command_name, new_info = new_info)




def run():
  import main
  app.run(host='0.0.0.0',port=8080)



def keep_alive():  

    t = Thread(target=run)

    t.start()
