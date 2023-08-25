from flask import Flask, render_template, request, redirect, url_for, make_response, session
import requests
import os
import json
from markdown import markdown
if os.path.isfile("./secret.py"): import secret

app = Flask(__name__)
app.secret_key = os.environ.get('secret_key')
api_key = os.environ.get('api_key')
api_secret_key = os.environ.get('api_secret_key')
api_site = os.environ.get('api_site')
vk_key = os.environ.get('vk_key')
vk_site = "https://api.vk.com/method/"

def getCountry(user_id):
    req = requests.get(api_site+"c/"+user_id).json()
    if req["flag"].startswith("images"):
        req["flag"] = url_for('static', filename=req["flag"])
    req["desc"] = markdown(req["desc"])
    return req

def getCountryCID(cid):
    req = requests.get(api_site+"c/cid/"+cid).json()
    if req["flag"].startswith("images"):
        req["flag"] = url_for('static', filename=req["flag"])
    req["desc"] = markdown(req["desc"])
    return req

def getCountryPrewiew(user_id):
    req = requests.get(api_site+"c/pr/"+user_id).json()
    if req["flag"].startswith("images"):
        req["flag"] = url_for('static', filename=req["flag"])
    req["desc"] = markdown(req["desc"])
    return req

def getCountries():
    req = requests.get(api_site+"cs").json()["response"]
    for re in req:
        if re["flag"].startswith("images"):
            re["flag"] = url_for('static', filename=re["flag"])
        re["desc"] = markdown(re["desc"])
    return req

def getRuler(user_id):
    if user_id == "000000000":
        return {"id": "000000000", "photo": url_for('static', filename="images/profile/profile.png"), "name": "Неизвестно"} 
    elif user_id == "-11111111":
        return {"id": "-11111111", "photo": url_for('static', filename="images/profile/admin.png"), "name": "Админ Админский"}
    ruler = requests.get(vk_site+f"users.get?access_token={vk_key}&user_ids={user_id}&fields=photo_200&v=5.131").json()["response"][0]
    return {"id": ruler["id"], "photo": ruler["photo_200"], "name": ruler["first_name"]+" "+ruler["last_name"]}

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/markdown")
@app.route("/markdown/")
def markdown_docs():
    return render_template("/markdown.html")

@app.route("/countries")
@app.route("/countries/")
def countries():
    return render_template("/countries/index.html", countries=getCountries())

@app.route("/countries/<id>")
@app.route("/countries/<id>/")
def country(id):
    country = getCountryCID(id)
    return render_template("/countries/country.html", country=country, ruler=getRuler(country["id"]))

@app.route("/countries/prewiew")
@app.route("/countries/prewiew/")
def country_prewiew():
    r = request.args
    country = {"id": r.get("id"),
               "cid": r.get("cid"), 
               "flag": r.get("flag"), 
               "name": r.get("name"), 
               "group": r.get("group"), 
               "goverment_type": r.get("goverment_type"), 
               "goverment_form": r.get("goverment_form"), 
               "ideology": r.get("ideology"), 
               "political_type": r.get("political_type"), 
               "date": r.get("date"), 
               "desc": r.get("desc"), 
               "check":  r.get("check")}
    ruler = getRuler(r.get("id"))
    return render_template("/countries/country.html", country=country, ruler=ruler, prewiew=True)

@app.route("/countries/prewiew/<id>")
@app.route("/countries/prewiew/<id>/")
def country_prewiew_id(id):
    country = getCountryPrewiew(id)
    return render_template("/countries/country.html", country=country, ruler=getRuler(country["id"]), prewiew=True)

@app.route("/map")
@app.route("/map/")
def map():    
    return render_template("/map/index.html")

@app.route("/history")
@app.route("/history/")
def history():    
    return render_template("/history/index.html")

@app.route("/profile")
@app.route("/profile/")
def profile():
    return render_template("/profile/index.html", api_key=api_key, country=getCountry(session['user_id']))

@app.route("/profile/login")
@app.route("/profile/login/")
def profile_login():
    session['user_id'] = request.args.get("uid")
    session['name'] = request.args.get("first_name")+" "+request.args.get("last_name")
    session['photo'] = request.args.get("photo").replace("&amp;", "&")
    return redirect("/profile")

@app.route("/profile/logout")
@app.route("/profile/logout/")
def profile_logout():
    session.clear()
    session['user_id'] = "000000000"
    session['name'] = "Профиль"
    session['photo'] = url_for('static', filename='images/profile/profile.png')
    return redirect("/profile")

@app.route("/profile/admin")
@app.route("/profile/admin/")
def profile_admin():
    return render_template("/profile/admin.html")

@app.route("/profile/admin", methods=['POST'])
@app.route("/profile/admin/", methods=['POST'])
def profile_admin_auth():
    if requests.get(api_site+"code").text == request.form.get("code"):
        session['user_id'] = "-11111111"
        session['name'] = "Админ Админский"
        session['photo'] = url_for('static', filename='images/profile/admin.png')
    return redirect("/profile")

@app.route("/profile/country/register")
@app.route("/profile/country/register/")
def profile_register():
    return render_template("/profile/register.html")

@app.route("/profile/country/register", methods=['POST'])
@app.route("/profile/country/register/", methods=['POST'])
def profile_register_auth():
    requests.post(api_site+"c/register", params=request.form)
    return redirect("/profile")
    





@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def error(e):
    if not 'user_id' in session: return redirect("/profile/logout")

    error_number = str(e).split(":")[0]
    error_message = str(e).split(":")[1]
    if error_number.lower() == "403 forbidden":
        error_number = "403"
        error_message = "Вам запрещена эта страница."
    if error_number.lower() == "404 not found":
        error_number = "404"
        error_message = "Эта страница не найдена."
    if error_number.lower() == "410 gone":
        error_number = "410"
        error_message = "Эта страница была удалена."
    if error_number.lower() == "500 internal server error":
        error_number = "500"
        error_message = "Сервер обработал ваш запрос с ошибкой."

    return render_template("/error.html", error_number=error_number, error_message=error_message)

if __name__ == "__main__":
    app.run()
