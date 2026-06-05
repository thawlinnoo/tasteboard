from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__) #creates the app with flask
app.config["SECRET_KEY"] = "dev-secret-key"

Bootstrap5(app) #connect the Bootstrap styling

@app.route("/") #homepage
def home():
    return render_template("index.html") #shows HTML page

if __name__ == "__main__":
    app.run(debug=True)