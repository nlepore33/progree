DESIGN

My website mirrors C$50 Finance, so I won't explain the entire Flask portion, or many of the things that come along with Finance.
I will touch on files one at a time...

scripts.js
    Used specifically to search for classes in the drop-down menu style of Mashup. I copied a lot of code from Mashup, and with the
    guidance of my TF, made the same style work for adding classes by either number or name.
    search() checks the database for typeahead suggestions.
    configure() configures the typeahead using jQuery, and also has a function that is called when something is selected in typeahead,
    and it leads into /addclass in application.py.

styles.css
    copied from both Mashup and Finance.

templates
    addclass.html
        Based on Mashup's input box, it displays classes that match the search so far.
    apology.html
        Taken from Finance.
    changepass.html
        Takes 3 input text fields for new password.
    classlist.html
        Based on Finance's history.html, it displays a table of all classes a user is in.
    classsearch.html
        Takes an input field, displays a table for all matches to the input field
    index.html
        Orients the entire index, shows multiple progress bars, shows Gen Eds completed and not finished, shows averages for each field.
    layout.html
        Taken from Finance.
    login.html
        Taken from Finance.
    register.html
        Taken from Finance.
    removeclass.html
        Based on sell.html, it displays all of the courses taken in a drop-down menu, select one and hit submit.

application.py
    Took much of the setup from Finance, added Python classes to beginning to make organization of information better.
    index()
        Progress to Graduation
            Takes the number of classes and divides by 32. Not a completely accurate way to get progress to graduation, but if students
            fulfill their concentration, it's accurate. Changes color based on how close you are to graduation (from red to green).
        Gen Eds
            Looks through the notes section of each class with the right user ID in classfolio, checks to see which Gen Eds it fulfills,
            adds them to a list and adds the ones that still need to be completed to another list. Also calculates percentage to being done
            with Gen Eds, I use the old Gen Ed system so I divide Gen Ed classes by 9.
        Departments
            Selects the short names for the departments that each class falls into, makes a list of the departments and uses the class Departments
            to correspond a percentage with each department. Colors each department on a rotation basis. Calculates where a student studies most and
            displays it, if a student studies equally in more than one place, the HTML doesn't display it.
        Rating, Difficulty, Workload
            I put these three together because they do the same thing with different aspects of the database.
            Each will find the number of 1s-5s for each category throughout the years of ratings, and create stackable progress bars for each,
            color coding them with 1s as red and 5s as green.
        Averages
            Gets a list of all the average scores for each category (Rating, Difficulty, Workload) from the table Qcourses, calculates the average
            of the list of averages, and sends them to HTML.
    addclass()
        Similar to buy() in Finance, recognizes the course selected, checks if it is already added, then adds the class to classfolio.
        It is triggered by scripts.js when typeahead is selected, and it passes the full name of the course.
    removeclass()
        Similar to sell() in Finance, it displays the options for deletion, then deletes the chosen class from classfolio.
    classsearch()
        Combines aspects from addclass() and classlist() to take text, look through a joined SQL table, and return all results possible,
        making sure not to duplicate.
    search()
        Taken from Mashup but joins courses with Qcourses to get more options, used for JavaScript.
    classlist()
        Similar to history() in Finance, searches for all classes that a user is taking in classfolio, uses a list of NumTitle objects to make
        sure there are no duplicates, then loads them to the HTML.
    login()
        Taken from Finance.
    logout()
        Taken from Finance.
    register()
        Taken from Finance.
    changepass()
        Checks if the fields are empty, checks that the old password is correct, checks if the two new passwords are the same, updates database.
    errorhandler()
        Taken from Finance.

courses50.db
    Given to me by heads, I use the same database for users and classfolio (similar to users and portfolio in Finance).

helpers.py
    Used for the apology and the login, take from Finance.

requirements.txt
    Displays requirements for Flask, taken from Finance.