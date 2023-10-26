from flask import Flask
from flask import request
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from tools import valid_response
from tools import invalid_response
from models import models
import os
import json

app = Flask(__name__, static_folder="static")
engine = create_engine(os.getenv("DATABASE_PATH"))


@app.route("/")
def index():
    return render_template("index.html")


# Additional features


@app.route("/api/v1/domain/get_all")
def domain_get_all():
    with session(autoflush=False, bind=engine) as session_db:
        domains = session_db.query(models.DomainRecords).all()
        return valid_response(
            {
                "domains": [
                    {
                        "id": i.id,
                        "name": i.name,
                    }
                    for i in domains
                ]
            }
        )


@app.route("/api/v1/domain/get_ip", methods=["POST"])
def domain_get_ip():
    if request.method == "POST":
        data = json.loads(request.data)
        if data.get("domain_name", False):
            domain = data["domain_name"]
            with Session(autoflush=False, bind=engine) as session_db:
                domain_obj = (
                    session_db.query(models.DomainRecords)
                    .filter(models.DomainRecords.name == domain)
                    .first()
                )
                return valid_response(
                    {
                        "id": domain_obj.id,
                        "ipv4": [
                            {"id": ipv4.id, "ip_string": ipv4.ip_string}
                            for ipv4 in domain_obj.ipv4
                        ],
                        "ipv6": [
                            {"id": ipv6.id, "ip_string": ipv6.ip_string}
                            for ipv6 in domain_obj.ipv6
                        ],
                    }
                )
        else:
            return invalid_response(message='argument "domain_name" not found')


@app.route("/api/v1/domain/get_id", methods=["POST"])
def get_domain_id():
    if request.method == "POST":
        data = json.loads(request.data)
        if data.get("domain_name", False):
            domain = data["domain_name"]
            with Session(autoflush=False, bind=engine) as session_db:
                domain_obj = (
                    session_db.query(models.DomainRecords)
                    .filter(models.DomainRecords.name == domain)
                    .first()
                )
                return valid_response({"id": domain_obj.id, "name": domain_obj.name})
        else:
            return invalid_response(message='argument "domain_name" not found')


# CRUD


@app.route("/api/v1/domain/create", methods=["POST"])
def domain_create():
    if request.method == "POST":
        data = json.loads(request.data)

        domain_name = data.get("domain_name", False)
        ipv4 = data.get("ipv4", False)
        ipv6 = data.get("ipv6", False)

        if not domain_name:
            return invalid_response(message='argument "domain_name" not found')

        with Session(autoflush=False, bind=engine) as session_db:
            domain_obj = models.DomainRecords(name=domain_name)

            ipv4_obj = [models.IpV4Records(ip_string=i) for i in ipv4] if ipv4 else []
            ipv6_obj = [models.IpV6Records(ip_string=i) for i in ipv6] if ipv6 else []

            domain_obj.ipv4 = ipv4_obj
            domain_obj.ipv6 = ipv6_obj

            session_db.add(domain_obj)
            session_db.commit()

            return valid_response({"id": domain_obj.id, "domain_name": domain_obj.name})


@app.route("/api/v1/domain/update", methods=["POST"])
def domain_update():
    if request.method == "POST":
        pass


@app.route("/api/v1/domain/delete", methods=["POST"])
def domain_delete():
    if request.method == "POST":
        pass


@app.route("/api/v1/domain/read", methods=["POST"])
def domain_get():
    if request.method == "POST":
        pass


if __name__ == "__main__":
    app.run(port=8000, debug=True)
