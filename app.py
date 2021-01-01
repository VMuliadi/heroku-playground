from flask import Flask, request, jsonify, session
import auth
import os

app = Flask(__name__)
app.secret_key = os.urandom(128).hex()


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
    authentication = None
    if token["access_token"] != "":
      del token["access_token"]
      return jsonify({
        "success": True,
        "message": "Welcome " + token["username"]
      })

    return jsonify({
        "success": False,
        "message": "Failed to authenticate user"
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

  finally:
    authentication = None


@app.route("/fetch")
def fetch_data():
  try:
    if not authentication.is_expired(session["access_token"]):
      import vgmdb
      authentication = auth.Auth()
      vgm_fetcher = vgmdb.VGMDB()
      vgmdb_album_id = request.args.get("vgmdb_album_id")
      vgmdb_filters = request.args.get("vgmdb_filters")
      tracklist = vgm_fetcher.get_tracklist(vgmdb_album_id, vgmdb_filters)
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

  finally:
    authentication = None


if __name__ == "__main__":
  app.run(debug=True)
