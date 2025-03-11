from flask import Flask, request, jsonify, session
from functools import wraps  # מייבא את המודול לעיטוף פונקציות
import time
import random

app = Flask(__name__)  # יוצר מופע של Flask
app.secret_key = "SariFilmer7373"  # מגדיר מפתח סודי עבור הסשן


class User:  # מגדיר מחלקת משתמש
    def __init__(self, username, user_id, password):  # בנאי
        self.username = username  # שומר את שם המשתמש
        self.user_id = user_id  # שומר את מזהה המשתמש
        self.password = password  # שומר את הסיסמה
        self.games_played = 0  # סופר את מספר המשחקים ששוחקו
        self.words_played = set()  # שומר את המילים ששוחקו
        self.wins = 0  # סופר את הניצחונות
        self.losses = 0  # סופר את ההפסדים
        self.history = []  # שומר את ההיסטוריה


users = {}  # שומר את כל המשתמשים
next_user_id = 1  # משתנה לשמירת מזהה המשתמש הבא


def login_required(f):  # דקורטור לבדוק אם המשתמש מחובר
    @wraps(f)
    # *args=ניתן להעביר מספר בלתי מוגבל של ארגומנטים לפונקציה כטאפל
    # **kwargs=, ניתן להעביר לפונקציה מספר בלתי מוגבל של ארגומנטים במבנה של מילון
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return jsonify("❌נדרש להתחבר למשחק לאחר ההרשמה"), 401
        if time.time() - session["login_time"] > 120:
            session.pop("username", None)  # מסיר את שם המשתמש מהסשן
            session.pop("login_time", None)  # מסיר את זמן ההתחברות
            return jsonify({"error": "פג תוקף ההפעלה ⌛"}), 401
        return f(*args, **kwargs)  # פונקציה המקורית

    return decorated_function  # הפונקציה המעוטפת


@app.route("/register", methods=["POST"])  # להרשמה
def register():
    global next_user_id  # היא מאפשרת לפונקצית register לשנות את ערך next_user_id
    data = request.json  # מקבל את הנתונים מהבקשה
    username = data["username"]  # שומר את שם המשתמש
    password = data["password"]  # שומר את הסיסמה

    if username in users:
        return jsonify("❌המשתמש כבר קיים!!!!!!!!"), 400

    users[username] = User(username, next_user_id, password)  # יוצר משתמש חדש
    next_user_id += 1  # מעדכן את המשתמש הבא
    return jsonify("\033[93mהמשתמש נרשם בהצלחה👍\033[0m"), 201


@app.route("/login", methods=["POST"])  # להתחברות
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    user = users.get(username)  # מחפש את המשתמש במילון
    if user and user.password == password:  # אם המשתמש קיים והסיסמה נכונה
        session["username"] = username  # שומר את שם המשתמש בסשן
        session["login_time"] = time.time()  # שומר את זמן ההתחברות
        yellow_message = f"\033[93mשלום ל{username}! הינך יכול/ה להתחיל לשחק ולהנות במשחקינו בהנאה!\033[0m"
        return (
            jsonify({"message": yellow_message}),
            200,
        )
    return jsonify({"error": "❌אינך רשום למערכת, יש להרשם!!"}), 401


@app.route("/logout", methods=["POST"])  # להתנתקות
@login_required  # דורש שהמשתמש יהיה מחובר
def logout():
    session.pop("username", None)  # מסיר את שם המשתמש מהסשן
    session.pop("login_time", None)  # מסיר את זמן ההתחברות
    return jsonify("☎️התנתק בהצלחה!!!!!! "), 200


@app.route("/start_game/<int:word_choice>", methods=["GET"])  # להתחלת משחק
@login_required
def start_game(word_choice):
    if time.time() - session["login_time"] > 120:
        return jsonify({"error": "פג תוקף ההפעלה ⌛"}), 401
    user = users[session["username"]]  # מקבל את המשתמש מהסשן
    words = get_all_words()  # מקבל את כל המילים
    if not words:
        return jsonify("❌אין מילים זמינות 📃"), 500
    word_choice = word_choice % len(words)  # מחשב את האינדקס בצורה מעגלית
    word = words[word_choice]  # בוחר מילה

    user.words_played.add(word)  # מוסיף את המילה ששוחקה
    user.games_played += 1  # מעדכן את מספר המשחקים
    user.history.append(  # מוסיף את ההיסטוריה של המשחק
        {
            "date": time.strftime("%Y-%m-%d"),
            "time": time.strftime("%H:%M:%S"),
            "word": word,
            "won": False,
        }
    )
    print(f'User {session["username"]} התחיל משחק עם מילה: {word}.')
    return jsonify({"word": word}), 200


@app.route("/update_game", methods=["POST"])  # עדכון משחק
@login_required
def update_game():
    data = request.json  # מקבל את הנתונים מהבקשה
    won = data["won"]  # שומר אם המשחק ניצח
    user = users[session["username"]]  # מקבל את המשתמש מהסשן
    current_time = time.time()  # שומר את הזמן הנוכחי

    for entry in user.history:  # עובר על ההיסטוריה של המשתמש
        if entry["word"] == data.get("word", "") and not entry.get(
            "won", False
        ):  # אם המילה תואמת והמשחק לא עודכן
            entry["won"] = won  # מעדכן אם ניצח
            if won:
                user.wins += 1
            else:
                user.losses += 1
            break

    if current_time - session["login_time"] > 120:
        return jsonify({"error": "פג תוקף ההפעלה ⌛"}), 401

    print(f'User {session["username"]} {"ניצח" if won else "הפסיד"} את המשחק.')
    return (
        jsonify({"message": "👍המשחק עודכן בהצלחה!!!!!!!!!!!"}),
        200,
    )


@app.route("/history", methods=["GET"])  # לקבלת היסטוריה
@login_required
def history():
    user = users.get(session.get("username"))  # מקבל את המשתמש מהסשן

    if user is None:
        return jsonify("❌נדרש להתחבר למשחק לאחר ההרשמה!!!!"), 401
    if not user.history:
        return jsonify("❌אין היסטוריה זמינה למשתמש!!!!!!!"), 200

    print(f'היסטוריה של המשתמש {session["username"]}: {user.history}')
    return (
        jsonify(
            {
                "games_played": user.games_played,
                "words_played": list(user.words_played),
                "wins": user.wins,
                "losses": user.losses,
                "history": user.history,
            }
        ),
        200,
    )


def get_all_words():  # פונקציה לקבלת כל המילים
    try:
        with open("words.txt", "r", encoding="utf-8") as file:
            words = file.read().splitlines()
            random.shuffle(words)  # מערבב את המילים
        return words if words else []
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"שגיאה בקריאת קובץ המילים: {e}")
        return []


if __name__ == "__main__":
    app.run(debug=True)
