from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import (
    EditProfileForm,
    EditClassesForm,
    NewHomeworkForm,
    EditHomeworkForm,
    NewTestForm,
    EditTestForm,
    CustomizationForm,
)
from app.models import User, Homework, Test
import os
from datetime import datetime, timezone, timedelta

TZ_NAME = os.environ.get("TZ_NAME") or "Eastern Daylight Time"
TZ_OFFSET = os.environ.get("TZ_OFFSET") or -4


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    now = datetime.now(tz=timezone(timedelta(hours=TZ_OFFSET), TZ_NAME))

    start = 0
    end = -1
    schedule_day = ""
    bell_schedule = ""
    with open(os.path.join(os.getcwd(), "data/stuy_schedule.csv")) as f:
        lines = f.read().split("\n")
        for line in lines:
            if line.split(",")[0] == now.strftime("%-m/%-d/%-y"):
                start = int(line.split(",")[2])
                end = int(line.split(",")[3])
                schedule_day = line.split(",")[1].lower()
                bell_schedule = line.split(",")[4]

    times = []
    if bell_schedule == "R":
        with open(os.path.join(os.getcwd(), "data/stuy_times_regular.csv")) as f:
            times = f.read().split("\n")
    elif bell_schedule == "H":
        with open(os.path.join(os.getcwd(), "data/stuy_times_homeroom.csv")) as f:
            times = f.read().split("\n")
    elif bell_schedule == "C":
        with open(os.path.join(os.getcwd(), "data/stuy_times_conference.csv")) as f:
            times = f.read().split("\n")
    elif bell_schedule == "S":
        with open(os.path.join(os.getcwd(), "data/stuy_times_special.csv")) as f:
            times = f.read().split("\n")

    schedule = []
    for i in range(start, end + 1):
        schedule_item = {
            "period": i,
            "times": times[i - 1].split(",")[1] + " - " + times[i - 1].split(",")[2],
            "subject": current_user["period_" + str(i) + schedule_day[0]],
            "link": current_user["period_" + str(i) + schedule_day[0] + "_zoom"],
        }
        schedule.append(schedule_item)

    if end == -1:
        day = "No school today!"
    elif schedule_day == "n":
        day = "No live instruction today!"
    else:
        day = "Day " + schedule_day.upper() + " (" + str(start) + "-" + str(end) + ")"

    homeworks = Homework.query.filter(
        Homework.user_id == current_user.id, Homework.done == False
    ).order_by(Homework.due_date, Homework.name)

    tests = Test.query.filter(
        Test.user_id == current_user.id, Test.done == False
    ).order_by(Test.due_date)

    date = now.strftime("%A, %B %-d, %Y")

    light = current_user.theme == "Light"
    popup = current_user.popup
    current_user.popup = False
    db.session.commit()

    return render_template(
        "index.html",
        title="Home",
        date=date,
        day=day,
        homeworks=homeworks,
        tests=tests,
        schedule=schedule,
        light=light,
        popup=popup,
    )


@bp.route("/profile")
@login_required
def profile():
    periods = {}
    for i in range(1, 11):
        periods["Period " + str(i) + " (A)"] = "period_" + str(i) + "a"
        periods["Period " + str(i) + " Zoom (A)"] = "period_" + str(i) + "a_zoom"
        periods["Period " + str(i) + " (B)"] = "period_" + str(i) + "b"
        periods["Period " + str(i) + " Zoom (B)"] = "period_" + str(i) + "b_zoom"

    return render_template("profile.html", title="Profile", periods=periods)


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@bp.route("/edit_classes", methods=["GET", "POST"])
@login_required
def edit_classes():
    form = EditClassesForm()
    periods = []
    for i in range(1, 11):
        periods.append("period_" + str(i) + "a")
        periods.append("period_" + str(i) + "a_zoom")
        periods.append("period_" + str(i) + "b")
        periods.append("period_" + str(i) + "b_zoom")

    if form.validate_on_submit():
        for field in periods:
            current_user[field] = form[field].data
            # If B Day info is None, replace with A Day info
            if form[field].data is None or form[field].data == "":
                if field.endswith("b"):
                    if (
                        form[field[:-1] + "a"].data is not None
                        or form[field[:-1] + "a"].data != ""
                    ):
                        current_user[field] = form[field[:-1] + "a"].data
                if field.endswith("b_zoom"):
                    if (
                        form[field[:-6] + "a_zoom"].data is not None
                        or form[field[:-6] + "a_zoom"].data != ""
                    ):
                        current_user[field] = form[field[:-6] + "a_zoom"].data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.profile"))
    elif request.method == "GET":
        for field in periods:
            if current_user[field] is not None:
                form[field].data = current_user[field]
    return render_template(
        "edit_classes.html", title="Edit Classes", periods=periods, form=form
    )


@bp.route("/new_homework", methods=["GET", "POST"])
@login_required
def new_homework():
    periods = []
    for i in range(1, 11):
        periods.append("period_" + str(i) + "a")
        periods.append("period_" + str(i) + "b")

    subjects = []
    for field in periods:
        if current_user[field] not in subjects and current_user[field] != "Free Period":
            subjects.append(current_user[field])
    form = NewHomeworkForm()

    # Workaround for no due date
    if form.due_date.data == "":
        form.due_date.data = None

    if form.validate_on_submit():
        homework = Homework(
            subject=form.subject.data,
            name=form.name.data,
            due_date=form.due_date.data,
            submit=form.submit_method.data,
            link=form.link.data,
            user_id=current_user.id,
        )
        db.session.add(homework)
        db.session.commit()
        flash("Homework assignment added!")
        return redirect(url_for("main.index"))
    return render_template(
        "new_homework.html", title="New Homework", form=form, subjects=subjects
    )


@bp.route("/edit_homework", methods=["GET", "POST"])
@login_required
def edit_homework():
    homework = Homework.query.filter(
        Homework.id == request.args.get("id"), Homework.done == False
    ).first()
    if homework.user_id != current_user.id:
        return render_template("errors/500.html"), 500

    form = EditHomeworkForm()
    if form.validate_on_submit():
        homework.subject = form.subject.data
        homework.name = form.name.data
        homework.due_date = form.due_date.data
        homework.submit = form.submit_method.data
        homework.link = form.link.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.index"))
    else:
        periods = []
        for i in range(1, 11):
            periods.append("period_" + str(i) + "a")
            periods.append("period_" + str(i) + "b")

        subjects = []
        for field in periods:
            if (
                current_user[field] not in subjects
                and current_user[field] != "Free Period"
            ):
                subjects.append(current_user[field])

        subject = homework.subject
        form.name.data = homework.name
        form.due_date.data = homework.due_date.strftime("%Y-%m-%d")
        form.submit_method.data = homework.submit
        form.link.data = homework.link
    return render_template(
        "edit_homework.html",
        title="Edit Homework",
        form=form,
        subjects=subjects,
        subject=subject,
    )


@bp.route("/complete_homework")
@login_required
def complete_homework():
    homework = Homework.query.filter(Homework.id == request.args.get("id")).first()
    if homework.user_id != current_user.id:
        return render_template("errors/500.html"), 500

    homework.done = True
    db.session.commit()
    flash("Assignment Done!")
    return redirect(url_for("main.index"))


@bp.route("/new_test", methods=["GET", "POST"])
@login_required
def new_test():
    periods = []
    for i in range(1, 11):
        periods.append("period_" + str(i) + "a")
        periods.append("period_" + str(i) + "b")

    subjects = []
    for field in periods:
        if current_user[field] not in subjects and current_user[field] != "Free Period":
            subjects.append(current_user[field])
    form = NewTestForm()

    # Workaround for no due date
    if form.due_date.data == "":
        form.due_date.data = None

    if form.validate_on_submit():
        test = Test(
            subject=form.subject.data,
            name=form.name.data,
            due_date=form.due_date.data,
            user_id=current_user.id,
        )
        db.session.add(test)
        db.session.commit()
        flash("Test added!")
        return redirect(url_for("main.index"))
    return render_template(
        "new_test.html", title="New Test", form=form, subjects=subjects
    )


@bp.route("/edit_test", methods=["GET", "POST"])
@login_required
def edit_test():
    test = Test.query.filter(
        Test.id == request.args.get("id"), Test.done == False
    ).first()
    if test.user_id != current_user.id:
        return render_template("errors/500.html"), 500

    form = EditTestForm()
    if form.validate_on_submit():
        test.subject = form.subject.data
        test.name = form.name.data
        test.due_date = form.due_date.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.index"))
    else:
        periods = []
        for i in range(1, 11):
            periods.append("period_" + str(i) + "a")
            periods.append("period_" + str(i) + "b")

        subjects = []
        for field in periods:
            if (
                current_user[field] not in subjects
                and current_user[field] != "Free Period"
            ):
                subjects.append(current_user[field])

        subject = test.subject
        form.name.data = test.name
        form.due_date.data = test.due_date.strftime("%Y-%m-%d")
    return render_template(
        "edit_test.html",
        title="Edit Test",
        form=form,
        subjects=subjects,
        subject=subject,
    )


@bp.route("/complete_test")
@login_required
def complete_test():
    test = Test.query.filter(Test.id == request.args.get("id")).first()
    if test.user_id != current_user.id:
        return render_template("errors/500.html"), 500

    test.done = True
    db.session.commit()
    flash("Test Done!")
    return redirect(url_for("main.index"))


@bp.route("/schedule/<username>")
def schedule(username):
    periods = []
    for i in range(1, 11):
        periods.append("period_" + str(i) + "a")
        periods.append("period_" + str(i) + "b")

    user = User.query.filter(User.username == username).first_or_404()
    subjects = []
    for field in periods:
        subjects.append(user[field])

    return render_template(
        "schedule.html",
        title=username + "'s Schedule",
        username=username,
        subjects=subjects,
    )


@bp.route("/schedule_widget")
@login_required
def schedule_widget():
    now = datetime.now(tz=timezone(timedelta(hours=TZ_OFFSET), TZ_NAME))

    start = 0
    end = -1
    schedule_day = ""
    bell_schedule = ""
    with open(os.path.join(os.getcwd(), "data/stuy_schedule.csv")) as f:
        lines = f.read().split("\n")
        for line in lines:
            if line.split(",")[0] == now.strftime("%-m/%-d/%-y"):
                start = int(line.split(",")[2])
                end = int(line.split(",")[3])
                schedule_day = line.split(",")[1].lower()
                bell_schedule = line.split(",")[4]

    times = []
    if bell_schedule == "R":
        with open(os.path.join(os.getcwd(), "data/stuy_times_regular.csv")) as f:
            times = f.read().split("\n")
    elif bell_schedule == "H":
        with open(os.path.join(os.getcwd(), "data/stuy_times_homeroom.csv")) as f:
            times = f.read().split("\n")
    elif bell_schedule == "C":
        with open(os.path.join(os.getcwd(), "data/stuy_times_conference.csv")) as f:
            times = f.read().split("\n")
    elif bell_schedule == "S":
        with open(os.path.join(os.getcwd(), "data/stuy_times_special.csv")) as f:
            times = f.read().split("\n")

    schedule = []
    for i in range(start, end + 1):
        schedule_item = {
            "period": i,
            "times": times[i - 1].split(",")[1] + " - " + times[i - 1].split(",")[2],
            "subject": current_user["period_" + str(i) + schedule_day[0]],
            "link": current_user["period_" + str(i) + schedule_day[0] + "_zoom"],
        }
        schedule.append(schedule_item)

    if end == -1:
        day = "No school today!"
    elif schedule_day == "n":
        day = "No live instruction today!"
    else:
        day = "Day " + schedule_day.upper() + " (" + str(start) + "-" + str(end) + ")"

    light = current_user.theme == "Light"

    return render_template(
        "schedule_widget.html",
        title="Schedule Widget",
        day=day,
        schedule=schedule,
        light=light,
    )


@bp.route("/resources")
def resources():
    return render_template("resources.html", title="Student Resources")


@bp.route("/users_count")
def users_count():
    users = len(User.query.all())
    return render_template("users_count.html", users=users)


@bp.route("/customization", methods=["GET", "POST"])
@login_required
def customization():
    form = CustomizationForm()
    if form.validate_on_submit():
        current_user.theme = form.theme.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.profile"))
    elif request.method == "GET":
        form.theme.data = current_user.theme
    return render_template("customization.html", title="Customization", form=form)
