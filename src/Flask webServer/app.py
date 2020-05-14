from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    Response,
    url_for
)
from portfolio import JSON, resultsPos, resultsNeg, overall
from robot import Robot
from camera import Camera

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = [User(id=1, username='Padraig', password='password'), User(id=2, username='Jane', password='password'),
         User(id=3, username='Joe', password='password')]

app = Flask(__name__)
app.secret_key = 'thisisasecret'
# robot = Robot()


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/GUI')
def GUI():
    return render_template('GUI.html')


@app.route('/')
def homepage():
    print("Re-directed user to login page")
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home'))

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/home')
def home():
    if not g.user:
        return redirect(url_for('login'))

    return render_template("home.html")


@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


@app.route("/portfolio")
def portfolio():
    data = JSON()
    return render_template('prediction.html', page_title='Portfolio', ML=data, lenPos=len(resultsPos),
                           lenNeg=len(resultsNeg), Neg=resultsNeg, Pos=resultsPos, overall=overall)


@app.route('/companion/<move>')
def companion(move):
    if move == 'forward':
        robot.forward()
    elif move == 'backward':
        robot.backward()
    elif move == 'left':
        robot.left()
    elif move == 'right':
        robot.right()
    elif move == 'stop':
        robot.stop()

    return '', 204


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True, threaded=True)
