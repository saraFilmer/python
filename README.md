# Word Game Application

This project is a web-based word game application built using Flask. It allows users to register, log in, play a word-based game, and track their game history.

---

## Features

- **User Management**: Registration, login, and logout functionality.
- **Game Management**: Start a game, update game results, and view game history.
- **Word Management**: Randomly selects words from a file (`words.txt`) for gameplay.
- **Game History**: Tracks games played, words used, wins, and losses.

---

## Server-Side Implementation

The server-side is implemented using Flask and includes the following:

1. **User Management**:
   - Users can register with a username and password.
   - Login functionality authenticates users and starts a session.
   - Logout functionality clears the session.

2. **Game Logic**:
   - A game starts by selecting a random word from `words.txt`.
   - Tracks the number of games played, words used, and game outcomes (win/loss).
   - Updates game results and maintains a detailed history for each user.

3. **Session Management**:
   - Sessions are used to track user login state and enforce a session timeout of 120 seconds.

4. **Error Handling**:
   - Handles cases like expired sessions, missing words, and invalid user actions.

---

## Client-Side Interaction

The client interacts with the server through RESTful API endpoints:

1. **Registration** (`/register`):
   - Sends a POST request with `username` and `password` to register a new user.

2. **Login** (`/login`):
   - Sends a POST request with `username` and `password` to log in.

3. **Start Game** (`/start_game/<word_choice>`):
   - Sends a GET request to start a game with a randomly selected word.

4. **Update Game** (`/update_game`):
   - Sends a POST request with the game result (`word` and `won` status).

5. **View History** (`/history`):
   - Sends a GET request to retrieve the user's game history.

---

## Notes

- The `words.txt` file must exist in the project directory and contain a list of words for the game.
- The application is designed to run locally with `debug=True` for development purposes.

                                                                                                          -------עברית-------
  # אפליקציית משחק מילים

פרויקט זה הוא אפליקציית ווב מבוססת Flask לניהול משחק מילים. האפליקציה מאפשרת למשתמשים להירשם, להתחבר, לשחק במשחק מילים ולעקוב אחר היסטוריית המשחקים שלהם.

---

## תכונות עיקריות

- **ניהול משתמשים**: רישום, התחברות והתנתקות.
- **ניהול משחקים**: התחלת משחק, עדכון תוצאות משחק וצפייה בהיסטוריית המשחקים.
- **ניהול מילים**: בחירת מילים אקראיות מתוך קובץ (`words.txt`) למשחק.
- **היסטוריית משחקים**: מעקב אחר משחקים ששוחקו, מילים שנבחרו, ניצחונות והפסדים.

---

## מימוש צד שרת

צד השרת ממומש באמצעות Flask וכולל את הפונקציות הבאות:

1. **ניהול משתמשים**:
   - רישום משתמשים חדשים עם שם משתמש וסיסמה.
   - התחברות משתמשים קיימים ואימות פרטי ההתחברות.
   - התנתקות משתמשים וניקוי הסשן.

2. **לוגיקת משחק**:
   - התחלת משחק על ידי בחירת מילה אקראית מתוך קובץ `words.txt`.
   - מעקב אחר מספר המשחקים, המילים שנבחרו ותוצאות המשחקים (ניצחון/הפסד).
   - עדכון תוצאות המשחק ושמירת היסטוריית המשחקים של המשתמש.

3. **ניהול סשן**:
   - שימוש בסשנים לניהול מצב ההתחברות של המשתמש.
   - הגבלת זמן סשן ל-120 שניות.

4. **טיפול בשגיאות**:
   - טיפול במקרים כמו סשן שפג תוקפו, חוסר במילים, או פעולות משתמש לא חוקיות.

---

## מימוש צד לקוח

צד הלקוח מתקשר עם צד השרת באמצעות נקודות קצה של RESTful API:

1. **רישום** (`/register`):
   - שליחת בקשת POST עם שם משתמש וסיסמה לרישום משתמש חדש.

2. **התחברות** (`/login`):
   - שליחת בקשת POST עם שם משתמש וסיסמה להתחברות.

3. **התחלת משחק** (`/start_game/<word_choice>`):
   - שליחת בקשת GET להתחלת משחק עם מילה שנבחרה אקראית.

4. **עדכון משחק** (`/update_game`):
   - שליחת בקשת POST עם תוצאת המשחק (המילה שנבחרה ומצב ניצחון/הפסד).

5. **צפייה בהיסטוריה** (`/history`):
   - שליחת בקשת GET לקבלת היסטוריית המשחקים של המשתמש.

---

## הערות

- קובץ `words.txt` חייב להיות קיים בתיקיית הפרויקט ולכלול רשימת מילים למשחק.
- האפליקציה מיועדת להרצה מקומית עם `debug=True` לצורכי פיתוח.
