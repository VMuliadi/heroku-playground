from flask import Flask, request, jsonify, session

import auth
import random
import string

app = Flask(__name__)


@app.route("/")
def index_page():
  return jsonify({"success": True}), 204

@app.route("/login", methods=["POST"])
def authentication():
  if request.method == "POST":
    username = request.form.get("leecher_username")
    password = request.form.get("leecher_password")
    
    authentication = auth.Auth()
    token = authentication.login_auth(username, password)
    session["access_token"] = token["access_token"]
    if token["access_token"] != "":
      del token["access_token"]
      return jsonify({
        "success": True,
        "message": "Welcome " + token["username"]
      })

@app.route("/logout", methods=["POST"])
def logout():
  try:
    authentication = auth.Auth()
    if authentication.is_expired(session["access_token"]):
      return jsonify({"success": True, "message": "Your session has been expired"})
    session.pop("access_token", None)
    return jsonify({"success": True, "message": "User has been logged out"})

  except KeyError as exception: 
    print(exception)
    return jsonify({
      "success": False,
      "message": "User not login to the app yet"
    }), 400


@app.route("/fetch")
def fetch_data():
  try:
    authentication = auth.Auth()
    if not authentication.is_expired(session["access_token"]):
      import vgmdb
      vgm_fetcher = vgmdb.VGMDB()
      vgmdb_url = request.values["vgmdb_url"]
      vgmdb_filters = request.args.get("vgmdb_filters")
      tracklist = vgm_fetcher.get_tracklist(vgmdb_url, vgmdb_filters)
      return jsonify({
        "success": True,
        "tracklist": tracklist,
        "message": "Success to fetch data from VGMDB"
      })

  except KeyError as exception: 
    print(exception)
    return jsonify({
      "success": False,
      "message": "Login first"
    }), 400

  except Exception as exception:
    print(exception)
    return jsonify({
      "success": False,
      "message": "Contact our administrator!"
    }), 500

if __name__ == "__main__":
  app.run(debug=True)
  app.secret_key = "".join(random.choice(string.ascii_uppercase \
    + string.ascii_lowercase \
    + string.digits) for _ in range(256))
