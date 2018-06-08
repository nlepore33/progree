from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from pytz import timezone

from helpers import apology, login_required

import random

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///courses50.db")


class Departments:
    def __init__(self, name, amt, color):
        self.n = name
        self.a = amt
        self.c = color

class QCourses:
    def __init__(self, classid):
        self.id = classid
        self.scores = []
        self.scoresd = []
        self.scoresw = []

    def addScore(self, score):
        self.scores.append(score)

    def addScored(self, score):
        self.scoresd.append(score)

    def addScorew(self, score):
        self.scoresw.append(score)

class NumTitle:
    def __init__(self, n, t):
        self.num = n
        self.title = t

@app.route("/")
@login_required
def index():

    classes = db.execute("SELECT * FROM classfolio WHERE userid=:id", id=session["user_id"])


    # Progress to Graduation

    numofclass = len(classes)

    percenttodegree = (numofclass / 32) * 100
    percenttodegree = "%.1f" % percenttodegree

    gradcolor = ""

    # Determines color of bar
    if float(percenttodegree) > 80:
        gradcolor = "bg-success"
    elif float(percenttodegree) > 60:
        gradcolor = "bg-info"
    elif float(percenttodegree) > 40:
        gradcolor = ""
    elif float(percenttodegree) > 20:
        gradcolor = "bg-warning"
    else:
        gradcolor = "bg-danger"

    #Gen Eds

    finishedgeneds = []
    unfinishedgeneds = []

    del finishedgeneds [:]
    del unfinishedgeneds [:]

    # Looks for courses that match classes in classfolio, makes completed and to be completed list
    for course in classes:
        classid = int(course["classid"])

        note = db.execute("SELECT notes FROM courses WHERE id=:id AND notes LIKE '%General Education%'", id=classid)

        note = str(note)

        if 'Aesthetic and Interpretive Understanding' in note and 'Aesthetic and Interpretive Understanding' not in finishedgeneds:
            finishedgeneds.append("Aesthetic and Interpretive Understanding")

        if 'Culture and Belief' in note and 'Culture and Belief' not in finishedgeneds:
            finishedgeneds.append("Culture and Belief")

        if 'Empirical and Mathematical Reasoning' in note and 'Empirical and Mathematical Reasoning' not in finishedgeneds:
            finishedgeneds.append("Empirical and Mathematical Reasoning")

        if 'Ethical Reasoning' in note and 'Ethical Reasoning' not in finishedgeneds:
            finishedgeneds.append("Ethical Reasoning")

        if 'Science of Living Systems' in note and 'Science of Living Systems' not in finishedgeneds:
            finishedgeneds.append("Science of Living Systems")

        if 'Science of the Physical Universe' in note and 'Science of the Physical Universe' not in finishedgeneds:
            finishedgeneds.append("Science of the Physical Universe")

        if 'Societies of the World' in note and 'Societies of the World' not in finishedgeneds:
            finishedgeneds.append("Societies of the World")

        if 'United States in the World' in note and 'United States in the World' not in finishedgeneds:
            finishedgeneds.append("United States in the World")

        if 'Study of the Past' in note and 'Study of the Past' not in finishedgeneds:
            finishedgeneds.append("Study of the Past")

    if 'Aesthetic and Interpretive Understanding' not in finishedgeneds:
        unfinishedgeneds.append('Aesthetic and Interpretive Understanding')

    if 'Culture and Belief' not in finishedgeneds:
        unfinishedgeneds.append('Culture and Belief')

    if 'Empirical and Mathematical Reasoning' not in finishedgeneds:
        unfinishedgeneds.append('Empirical and Mathematical Reasoning')

    if 'Ethical Reasoning' not in finishedgeneds:
        unfinishedgeneds.append('Ethical Reasoning')

    if 'Science of Living Systems' not in finishedgeneds:
        unfinishedgeneds.append('Science of Living Systems')

    if 'Science of the Physical Universe' not in finishedgeneds:
        unfinishedgeneds.append('Science of the Physical Universe')

    if 'Societies of the World' not in finishedgeneds:
        unfinishedgeneds.append('Societies of the World')

    if 'United States in the World' not in finishedgeneds:
        unfinishedgeneds.append('United States in the World')

    if 'Study of the Past' not in finishedgeneds:
        unfinishedgeneds.append('Study of the Past')

    # Calculates percent to completion of Gen Eds
    genedpercent = (len(finishedgeneds) / 9) * 100
    genedpercent = "%.1f" % genedpercent


    #Department

    departments = db.execute("SELECT short_name FROM classfolio JOIN courses ON classfolio.classid=courses.id JOIN departments ON courses.department_id=departments.id WHERE classfolio.userid=:userid", userid=session["user_id"])

    departs = []

    for each in departments:
        eachs = str(each)
        eachs = eachs[16:-2]
        departs.append(eachs)

    used = []
    departobj = []
    ran = 0

    # uses a class to make a list of departments, cycles through colors for each
    for each in departs:
        if each not in used:
            used.append(each)
            num = (departs.count(each) / len(departs)) * 100
            num = "%.1f" % num
            if ran == 0:
                clr = "bg-success"
            elif ran == 1:
                clr = "bg-info"
            elif ran == 2:
                clr = ""
            elif ran == 3:
                clr = "bg-warning"
            elif ran == 4:
                clr = "bg-danger"
            ran += 1
            if ran == 5:
                ran = 0
            obj = Departments(each, num, clr)
            departobj.append(obj)

    max = 0

    mostdepart = ""

    # decides where a person studies most
    for each in departobj:
        if float(each.a) > max:
            max = float(each.a)
            mostdepart = "You Study Most in the " + each.n + " Department"

    count = 0

    for each in departobj:
        if max == float(each.a):
            count += 1

    if count > 1:
        mostdepart = ""


    #Rating

    onepers = []
    twopers = []
    threepers = []
    fourpers = []
    fivepers = []

    for course in classes:

        ones = 0
        twos = 0
        threes = 0
        fours = 0
        fives = 0

        classid = int(course["classid"])
        scores = db.execute("SELECT * FROM QCourseOverall WHERE course_id=:classid", classid=classid)

        lenscores = len(scores)

        # counts up each total of each rating (1-5)
        for row in range(lenscores):
            ones += int(scores[row]["1s"])
            twos += int(scores[row]["2s"])
            threes += int(scores[row]["3s"])
            fours += int(scores[row]["4s"])
            fives += int(scores[row]["5s"])

        totalrates = ones + twos + threes + fours + fives

        # finds percentage for each
        if totalrates > 0:
            onepers.append((ones / totalrates) * 100)
            twopers.append((twos / totalrates) * 100)
            threepers.append((threes / totalrates) * 100)
            fourpers.append((fours / totalrates) * 100)
            fivepers.append((fives / totalrates) * 100)

    # finds average percentage
    if len(onepers) > 0:
        onespercent = sum(onepers) / len(onepers)
        twospercent = sum(twopers) / len(twopers)
        threespercent = sum(threepers) / len(threepers)
        fourspercent = sum(fourpers) / len(fourpers)
        fivespercent = sum(fivepers) / len(fivepers)
    else:
        onespercent = 0
        twospercent = 0
        threespercent = 0
        fourspercent = 0
        fivespercent = 0

    del onepers[:]
    del twopers[:]
    del threepers[:]
    del fourpers[:]
    del fivepers[:]


    # Difficulty

    for course in classes:

        ones = 0
        twos = 0
        threes = 0
        fours = 0
        fives = 0

        classid = int(course["classid"])
        scores = db.execute("SELECT * FROM QDifficulty WHERE course_id=:classid", classid=classid)

        lenscores = len(scores)

        # counts up each total of each rating (1-5)
        for row in range(lenscores):
            ones += int(scores[row]["1s"])
            twos += int(scores[row]["2s"])
            threes += int(scores[row]["3s"])
            fours += int(scores[row]["4s"])
            fives += int(scores[row]["5s"])

        totalrates = ones + twos + threes + fours + fives

        # finds percentage for each
        if totalrates > 0:
            onepers.append((ones / totalrates) * 100)
            twopers.append((twos / totalrates) * 100)
            threepers.append((threes / totalrates) * 100)
            fourpers.append((fours / totalrates) * 100)
            fivepers.append((fives / totalrates) * 100)

    # finds average percentage
    if len(onepers) > 0:
        onespercentd = sum(onepers) / len(onepers)
        twospercentd = sum(twopers) / len(twopers)
        threespercentd = sum(threepers) / len(threepers)
        fourspercentd = sum(fourpers) / len(fourpers)
        fivespercentd = sum(fivepers) / len(fivepers)
    else:
        onespercentd = 0
        twospercentd = 0
        threespercentd = 0
        fourspercentd = 0
        fivespercentd = 0

    del onepers[:]
    del twopers[:]
    del threepers[:]
    del fourpers[:]
    del fivepers[:]


    #Workload

    for course in classes:

        ones = 0
        twos = 0
        threes = 0
        fours = 0
        fives = 0

        classid = int(course["classid"])
        scores = db.execute("SELECT * FROM QWorkload WHERE course_id=:classid", classid=classid)

        lenscores = len(scores)

        # counts up each total of each rating (1-5)
        for row in range(lenscores):
            ones += int(scores[row]["1s"])
            twos += int(scores[row]["2s"])
            threes += int(scores[row]["3s"])
            fours += int(scores[row]["4s"])
            fives += int(scores[row]["5s"])

        totalrates = ones + twos + threes + fours + fives

        # finds percentage for each
        if totalrates > 0:
            onepers.append((ones / totalrates) * 100)
            twopers.append((twos / totalrates) * 100)
            threepers.append((threes / totalrates) * 100)
            fourpers.append((fours / totalrates) * 100)
            fivepers.append((fives / totalrates) * 100)

    # finds average percentage
    if len(onepers) > 0:
        onespercentw = sum(onepers) / len(onepers)
        twospercentw = sum(twopers) / len(twopers)
        threespercentw = sum(threepers) / len(threepers)
        fourspercentw = sum(fourpers) / len(fourpers)
        fivespercentw = sum(fivepers) / len(fivepers)
    else:
        onespercentw = 0
        twospercentw = 0
        threespercentw = 0
        fourspercentw = 0
        fivespercentw = 0

    del onepers[:]
    del twopers[:]
    del threepers[:]
    del fourpers[:]
    del fivepers[:]

    # Averages

    qcourses = db.execute("SELECT * FROM Qcourses JOIN classfolio ON Qcourses.course_id=classfolio.classid WHERE classfolio.userid=:userid", userid=session["user_id"])

    qobjlist = []

    # makes list of objects
    for each in qcourses:
        clsid = each["course_id"]
        if not any(x.id == clsid for x in qobjlist):
            obj = QCourses(clsid)
            qobjlist.append(obj)

    # adds to list of different scores for Rating, Difficulty, Workload
    for each in qobjlist:
        for cls in qcourses:
            if each.id == cls["course_id"]:
                if cls["CourseOverall"] is not None:
                    each.addScore(cls["CourseOverall"])
                if cls["Difficulty"] is not None:
                    each.addScored(cls["Difficulty"])
                if cls["Workload"] is not None:
                    each.addScorew(cls["Workload"])

    avglist = []
    avglistd = []
    avglistw = []

    # finds average of each, adding to a list
    for each in qobjlist:
        if len(each.scores) > 0:
            avg = sum(each.scores) / len(each.scores)
            avglist.append(avg)

        if len(each.scoresd) > 0:
            avg = sum(each.scoresd) / len(each.scoresd)
            avglistd.append(avg)

        if len(each.scoresw) > 0:
            avg = sum(each.scoresw) / len(each.scoresw)
            avglistw.append(avg)

    # finds average of list of averages
    if len(avglist) > 0:
        ratingavg = sum(avglist) / len(avglist)
        ratingavg = "%.2f" % ratingavg

        ratingavgd = sum(avglistd) / len(avglistd)
        ratingavgd = "%.2f" % ratingavgd

        ratingavgw = sum(avglistw) / len(avglistw)
        ratingavgw = "%.2f" % ratingavgw
    else:
        ratingavg = 0
        ratingavgd = 0
        ratingavgw = 0

    del onepers[:]
    del twopers[:]
    del threepers[:]
    del fourpers[:]
    del fivepers[:]

    return render_template("index.html", pertodegree=percenttodegree, genedpercent=genedpercent, gradcolor=gradcolor, finishedgeneds=finishedgeneds, unfinishedgeneds=unfinishedgeneds,
        onespercent=onespercent, twospercent=twospercent, threespercent=threespercent, fourspercent=fourspercent, fivespercent=fivespercent, onespercentd=onespercentd,
        twospercentd=twospercentd, threespercentd=threespercentd, fourspercentd=fourspercentd, fivespercentd=fivespercentd, onespercentw=onespercentw,
        twospercentw=twospercentw, threespercentw=threespercentw, fourspercentw=fourspercentw, fivespercentw=fivespercentw, departobj=departobj, mostdepart=mostdepart,
        ratingavg=ratingavg, ratingavgd=ratingavgd, ratingavgw=ratingavgw)

@app.route("/addclass", methods=["GET", "POST"])
@login_required
def addclass():

    if request.method == "POST":

        look = request.form.get("q")

        course = db.execute("SELECT * FROM courses WHERE title=:look", look=look)

        title = course[0]["title"]

        classid = int(course[0]["id"])

        check = db.execute("SELECT * FROM classfolio WHERE classid=:id AND userid=:userid", id=classid, userid=session["user_id"])

        # makes sure no repeats
        if not (len(check) > 0):
            db.execute("INSERT INTO classfolio (userid, classid, title) VALUES (:userid, :classid, :title)", userid=session["user_id"], classid=classid, title=title)

        return redirect("/")
    else:
        return render_template("addclass.html")


@app.route("/removeclass", methods=["GET", "POST"])
@login_required
def removeclass():

    if request.method == "POST":

        course = request.form.get("title")

        db.execute("DELETE FROM classfolio WHERE userid=:id AND title=:title", id=session["user_id"], title=course)

        return redirect("/")
    else:
        classes = db.execute("SELECT title FROM classfolio WHERE userid=:id", id=session["user_id"])

        return render_template("removeclass.html", classes=classes)


@app.route("/classsearch", methods=["GET", "POST"])
@login_required
def classsearch():

    if request.method == "POST":

        query = "%" + request.form.get("classsearch") + "%"

        classlist = db.execute("SELECT * FROM courses JOIN Qcourses ON courses.id=Qcourses.course_id WHERE courses.title LIKE :q OR Qcourses.number LIKE :q", q=query)

        numtitlelist = []

        del numtitlelist [:]

        # makes sure no repeats
        for each in classlist:
            if not any(x.title == each["title"] for x in numtitlelist):
                cls = NumTitle(each["number"], each["title"])
                numtitlelist.append(cls)

        listlen = len(numtitlelist)

        return render_template("classsearch.html", numtitlelist=numtitlelist, listlen=listlen)
    else:
        numtitlelist = []
        listlen = 0

        return render_template("classsearch.html", numtitlelist=numtitlelist, listlen=listlen)


@app.route("/search")
def search():
    """Search for places that match query"""

    query = "%" + request.args.get("q") + "%"

    cls = db.execute("SELECT * FROM courses JOIN Qcourses ON courses.id=Qcourses.course_id WHERE courses.title LIKE :q OR Qcourses.number LIKE :q", q=query)

    if len(cls) > 10:
        return jsonify(cls[0], cls[1], cls[2], cls[3], cls[4], cls[5], cls[6], cls[7], cls[8], cls[9])
    else:
        return jsonify(cls)



@app.route("/classlist")
@login_required
def classlist():

    classlist = db.execute("SELECT * FROM classfolio JOIN Qcourses ON classfolio.classid=Qcourses.course_id WHERE classfolio.userid=:id", id=session["user_id"])

    numtitlelist = []

    del numtitlelist [:]

    # makes sure no repeats
    for each in classlist:
        if not any(x.title == each["title"] for x in numtitlelist):
            cls = NumTitle(each["number"], each["title"])
            numtitlelist.append(cls)

    listlen = len(numtitlelist)

    return render_template("classlist.html", numtitlelist=numtitlelist, listlen=listlen)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match")

        users = db.execute("SELECT * FROM users")

        for each in users:
            if each["username"] == request.form.get("username"):
                return apology("username taken")

        ins = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"),
                         hash=generate_password_hash(request.form.get("password")))

        if not ins:
            return apology("username taken")

        # Remember which user has logged in
        session["user_id"] = ins

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():

    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE id=:id", id=session["user_id"])

        # makes sure page is done correctly
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("oldpass")):
            return apology("old password doesn't match")

        if not request.form.get("changepass1"):
            return apology("must provide new password")

        elif not request.form.get("changepass2"):
            return apology("must provide confirmation")

        elif not request.form.get("oldpass"):
            return apology("must provide old password")

        elif request.form.get("changepass1") != request.form.get("changepass2"):
            return apology("passwords must match")


        newpass = generate_password_hash(request.form.get("changepass1"))

        db.execute("UPDATE users SET hash=:newpass WHERE id=:id",
                   newpass=newpass, id=session["user_id"])

        return redirect("/")

    else:
        return render_template("changepass.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
