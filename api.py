from flask import request, make_response, jsonify, render_template, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import logging, requests, datetime

from sweater import app, db, manager
from sweater.models import Contacts, Mailings, Messages, User

logger = logging.getLogger("api")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/logs.log", mode="a")
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# gui -------------------------
@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
@login_required
def main():
    return render_template('main.html')

@app.route("/contacts", methods=["GET"])
@login_required
def contacts_gui():
    if request.method == "GET":
        r = requests.get(f"{request.host_url}api/contact")
        contacts = r.json()["contacts"]
        return render_template("contacts.html", contacts=contacts)

@app.route("/contact/delete/<int:id>")
@login_required
def contact_delete(id):
    requests.delete(f"{request.host_url}api/contact", json={"id": id})
    return redirect("/contacts")

@app.route("/contact/update/<int:id>", methods=["GET", "POST"])
@login_required
def contact_put(id):
    if request.method == "POST":
        number = request.form.get("number")
        operator_code = request.form.get("operator_code")
        tag = request.form.get("tag")
        time_zone = request.form.get("time_zone")

        requests.put(f"{request.host_url}api/contact", json={"change": id, "number": number, "operator_code": operator_code, "tag": tag, "time_zone": time_zone})
        return redirect("/contacts")

    elif request.method == "GET":
        contact = Contacts.query.get(id)
        return render_template("contact_put.html", contact=contact)


@app.route("/contact/add", methods=["POST", "GET"])
@login_required
def contact_add():
    if request.method == "POST":
        number = request.form.get("number")
        operator_code = request.form.get("operator_code")
        tag = request.form.get("tag")
        time_zone = request.form.get("time_zone")

        requests.post(f"{request.host_url}api/contact", json={"number":number, "operator_code":operator_code, "tag":tag, "time_zone":time_zone})
        return redirect("/contacts")

    return render_template("contact_post.html")


@app.route("/mailings", methods=["GET"])
@login_required
def mailing_gui():
    r = requests.get(f"{request.host_url}api/mailing")
    mailings = r.json()["mailings"]
    return render_template("mailings.html", mailings=mailings)

@app.route("/mailing/add", methods=["POST", "GET"])
@login_required
def mailing_add():
    if request.method == "POST":
        start_time = request.form.get("start_time")
        message = request.form.get("message")
        filters = request.form.get("filters")
        end_time = request.form.get("end_time")

        requests.post(f"{request.host_url}api/mailing", json={"start_time":start_time, "message":message, "filters":filters, "end_time":end_time})
        return redirect("/mailings")

    return render_template("mailing_post.html")

@app.route("/mailing/update/<int:id>", methods=["GET", "POST"])
@login_required
def mailing_put(id):
    if request.method == "POST":
        start_time = request.form.get("start_time")
        message = request.form.get("message")
        filters = request.form.get("filters")
        end_time = request.form.get("end_time")

        requests.put(f"{request.host_url}api/mailing", json={"change": id, "start_time": start_time, "message": message, "filters": filters, "end_time": end_time})
        return redirect("/mailings")

    elif request.method == "GET":
        mailing = Mailings.query.get(id)
        return render_template("mailing_put.html", mailing=mailing)

@app.route("/mailing/delete/<int:id>")
@login_required
def mailing_delete(id):
    requests.delete(f"{request.host_url}api/mailing", json={"id": id})
    return redirect("/mailings")


@app.route("/messages", methods=["GET"])
@login_required
def messages_gui():
    r = requests.get(f"{request.host_url}api/messages", json={"query": "all"})
    messages = r.json()["messages"]
    return render_template("messages.html", messages=messages)

@app.route("/message/add", methods=["POST", "GET"])
@login_required
def message_add():
    if request.method == "POST":
        datetime_now = str(datetime.datetime.now())
        status = request.form.get("status")
        mailing_id = request.form.get("mailing_id")
        contact_id = request.form.get("contact_id")

        requests.post(f"{request.host_url}api/messages", json={"datetime":datetime_now, "status":status, "mailing_id":mailing_id, "contact_id":contact_id})
        return redirect("/messages")

    return render_template("message_post.html")

@app.route("/message/update/<int:id>", methods=["GET", "POST"])
@login_required
def message_put(id):
    if request.method == "POST":
        datetime_now = str(datetime.datetime.now())
        status = request.form.get("status")
        mailing_id = request.form.get("mailing_id")
        contact_id = request.form.get("contact_id")

        requests.put(f"{request.host_url}api/messages", json={"change": id, "datetime": datetime_now, "status": status, "mailing_id": mailing_id, "contact_id": contact_id})
        return redirect("/messages")

    elif request.method == "GET":
        message = Messages.query.get(id)
        return render_template("message_put.html", message=message)

@app.route("/message/delete/<int:id>")
@login_required
def message_delete(id):
    requests.delete(f"{request.host_url}api/messages", json={"id": id})
    return redirect("/messages")

@app.route("/mailing_general", methods=["GET", "POST"])
@login_required
def mailing_search():
    if request.method == "POST":
        id = request.form.get("id")
        r = requests.get(f"{request.host_url}api/mailing/{id}")

        if r.status_code == 200:
            json = r.json()
            msg_count = json["message_general"]["message_count"]
            messages = json["message_general"]["messages"]
            mailing = json["mailing_general"]

            return render_template("mailing_detailing.html", mailing=mailing, msg_count=msg_count, messages=messages)

    return render_template("mailing_detailing.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        flash('Please fill login and password fields')
    else:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect("/")
        else:
            flash('Login or password is not correct')
        
    return render_template('login_page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash("Passwords are not equal!")
        elif User.query.filter_by(login=login).first():
            flash('Account with this login already exists')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))
    
    return render_template('register_page.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page'))
    
    return response

# api -------------------------
@app.route("/api/contact", methods = ["POST", "PUT", "DELETE", "GET"])
def contact():
    if request.method == "POST":
        try:
            r = request.get_json()
            if Contacts.query.filter_by(number=r["number"]).first() != None:
                raise Exception("Запись с таким номером уже существует...")
            for k in r:
                if r[k].strip() == '' and k != "tag" and k != "time_zone":
                    raise Exception("Заполните все поля...")

            contact = Contacts(number=r["number"], operator_code=r["operator_code"], tag=r["tag"], time_zone=r["time_zone"])
            db.session.add(contact)
            db.session.commit()

            logger.info(f"{request.method} {request.base_url} {contact.id}-contacts 200\n{r}")
            return jsonify(id=contact.id)
        except Exception as err:
            logger.warning(f"{request.method} {request.base_url} contacts 400\n{r}\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)

    elif request.method == "PUT":
        try:
            r = request.get_json()
            for key in r:
                if key == 'change': continue
                Contacts.query.filter_by(id=r["change"]).update({key:r[key]})

            db.session.commit()

            contact = Contacts.query.filter_by(id=r["change"]).first()
            ans = {"id": contact.id, "number": contact.number, "operator_code": contact.operator_code, "tag": contact.tag, "time_zone": contact.time_zone}

            logger.info(f"{request.method} {request.base_url} {contact.id}-contacts 200\n{r}")
            return jsonify(contact=ans)
        except Exception as err:
            logger.warning(f"{request.method} {request.base_url} contacts 400\n{r}\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)

    elif request.method == "DELETE":
        try:
            r = request.get_json()
            if Contacts.query.filter_by(id=r["id"]).first() == None:
                raise Exception("Записи с таким id не существует...")

            Contacts.query.filter_by(id=r["id"]).delete()
            db.session.commit()

            logger.info(f"{request.method} {request.base_url} {r['id']}-contacts 200\n{r}")
            return make_response(jsonify(code="ok"), 200)
        except Exception as err:
            logger.warning(f"{request.method} {request.base_url} contacts 400\n{r}\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)
    
    elif request.method == "GET":
        try:
            contacts = Contacts.query.all()

            ans = []
            for contact in contacts:
                ans.append({"id":contact.id, "number": contact.number, "operator_code": contact.operator_code, "tag": contact.tag, "time_zone": contact.time_zone})

            return make_response(jsonify(contacts=ans), 200)
        except Exception as err:
            return make_response(jsonify(error=str(err)), 400)

@app.route("/api/mailing", methods = ["POST", "PUT", "DELETE", "GET"])
def mailing():
    if request.method == "POST":
        r = request.get_json()
        try:
            if Mailings.query.filter_by(start_time=r["start_time"], message=r["message"], filters=r["filters"], end_time=r["end_time"]).first() != None:
                raise Exception("Такая запись уже существует...")
            for k in r:
                if r[k].strip() == '':
                    raise Exception("Заполните все поля...")

            mailing = Mailings(start_time=r["start_time"], message=r["message"], filters=r["filters"], end_time=r["end_time"])
            db.session.add(mailing)
            db.session.commit()

            logger.info(f"{request.method} {request.base_url} {mailing.id}-mailing 200\n{r}")
            return jsonify(id=mailing.id)
        except Exception as err:
            logger.warning(f"{request.method} {request.base_url} mailing 400\n{r}\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)

    elif request.method == "PUT":
        r = request.get_json()
        try:
            for key in r:
                if key == 'change': continue
                Mailings.query.filter_by(id=r["change"]).update({key:r[key]})

            db.session.commit()

            mailing = Mailings.query.filter_by(id=r["change"]).first()
            ans = {"id": mailing.id, "start_time": mailing.start_time, "message": mailing.message, "filters": mailing.filters, "end_time": mailing.end_time}

            logger.info(f"{request.method} {request.base_url} {mailing.id}-mailing 200\n{r}")
            return jsonify(mailing=ans)
        except Exception as err:
            logger.warning(f"{request.method} {request.base_url} mailing 400\n{r}\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)

    elif request.method == "DELETE":
        r = request.get_json()
        try:
            if Mailings.query.filter_by(id=r["id"]).first() == None:
                raise Exception("Записи с таким id не существует...")

            Mailings.query.filter_by(id=r["id"]).delete()
            db.session.commit()

            logger.info(f"{request.method} {request.base_url} {r['id']}-mailing 200\n{r}")
            return make_response(jsonify(code="ok"),200)
        except Exception as err:
            logger.warning(f"{request.method} {request.base_url} mailing 400\n{r}\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)
    
    elif request.method == "GET":
        try:
            mailings = Mailings.query.all()

            ans = []
            for mailing in mailings:
                ans.append({"id":mailing.id, "start_time": mailing.start_time, "message": mailing.message, "filters": mailing.filters, "end_time": mailing.end_time})

            return make_response(jsonify(mailings=ans), 200)
        except Exception as err:
            return make_response(jsonify(error=str(err)), 400)

@app.route("/api/mailing/<int:id>", methods=["GET"])
def mailing_general(id):
    if request.method == "GET":
        try:
            mailing = Mailings.query.get(id)
            messages = Messages.query.filter_by(mailing_id=id).all()

            msg_json = {"message_count": len(messages), "messages":{"Успешно": [], "Ожидается": [], "Не отправлено": []}}        
            mailing_json = {"id": mailing.id, "start_time": mailing.start_time, "message": mailing.message, "filters": mailing.filters, "end_time": mailing.end_time}

            for message in messages:
                if message.status == "Успешно":
                    msg_json["messages"]["Успешно"].append({"id": message.id, "datetime": message.datetime, "status": message.status, "mailing_id": message.mailing_id, "contact_id": message.contact_id})
                elif message.status == "Не отправлено":
                    msg_json["messages"]["Не отправлено"].append({"id": message.id, "datetime": message.datetime, "status": message.status, "mailing_id": message.mailing_id, "contact_id": message.contact_id})
                else:
                    msg_json["messages"]["Ожидается"].append({"id": message.id, "datetime": message.datetime, "status": message.status, "mailing_id": message.mailing_id, "contact_id": message.contact_id})

            logger.info(f"{request.method} {request.base_url} 200")
            return jsonify(message_general=msg_json, mailing_general=mailing_json)
        except Exception as err:
            logger.info(f"{request.method} {request.base_url} 400\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)

@app.route("/api/messages", methods = ["POST", "PUT", "DELETE", "GET"])
def messages():
    r = request.get_json()
    if request.method == "POST":
        try:
            messages = Messages(datetime=r["datetime"], status=r["status"], mailing_id=r["mailing_id"], contact_id=r["contact_id"])
            db.session.add(messages)
            db.session.commit()

            logger.info(f"{request.method} {request.base_url} {messages.id}-messages 200\n{r}")
            return jsonify(id=messages.id)
        except Exception as err:
            logger.warning(f"{request.method} {request.base_url} messages 400\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)

    if request.method == "PUT":
        try:
            for key in r:
                if key == 'change': continue
                Messages.query.filter_by(id=r["change"]).update({key:r[key]})
            db.session.commit()

            message = Messages.query.filter_by(id=r["change"]).first()
            ans = {"id": message.id, "datetime": message.datetime, "status": message.status, "mailing_id": message.mailing_id, "contact_id": message.contact_id}

            logger.info(f"{request.method} {request.base_url} {message.id}-messages 200\n{r}")
            return jsonify(message=ans)
        except Exception as err:
            logger.warning(f"{request.method} {request.base_url} messages 400\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)

    if request.method == "DELETE":
        try:
            if Messages.query.filter_by(id=r["id"]).first() == None:
                raise Exception("Записи с таким id не существует...")

            Messages.query.filter_by(id=r["id"]).delete()
            db.session.commit()

            logger.info(f"{request.method} {request.base_url} {r['id']}-messages 200\n{r}")
            return make_response(jsonify(code="ok"), 200)
        except Exception as err:
            logger.warning(f"{request.method} {request.base_url} messages 400\n{r}\n{str(err)}")
            return make_response(jsonify(error=str(err)), 400)
    
    if request.method == "GET":
        if r["query"] == "all":
            try:
                messages = Messages.query.all()

                ans = []
                for message in messages:
                    ans.append({"id": message.id, "datetime": message.datetime, "status": message.status, "mailing_id": message.mailing_id, "contact_id": message.contact_id})

                return make_response(jsonify(messages=ans), 200)
            except Exception as err:
                return make_response(jsonify(error=str(err)), 400)
        else:
            try:
                message = Messages.query.filter_by(mailing_id=r["query"][0], contact_id=r["query"][1]).first()

                return make_response(jsonify(id=message.id, datetime=message.datetime, status=message.status, mailing_id=message.mailing_id, contact_id=message.contact_id), 200)
            except Exception as err:
                return make_response(jsonify(error=str(err)), 400)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, host="0.0.0.0")