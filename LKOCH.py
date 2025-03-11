import requests
import re  # בשביל הבדיקת תקינות

# בשביל הצבעים
from colorama import init, Fore, Back, Style

# כתובת השרת
BASE_URL = "http://127.0.0.1:5000"  # הגדרת כתובת השרת
session = requests.Session()  # יצירת סשן חדש


init()


# רישום משתמש חדש
def register(username, password):
    if not username or not password:
        print(Fore.RED + "⚠️אזהרה: יש למלא את שם המשתמש והסיסמה." + Style.RESET_ALL)
        return  # יציאה מהפונקציה
    response = session.post(  # מכיל את התגובה מהשרת לאחר שליחת הבקשה
        f"{BASE_URL}/register",
        json={"username": username, "password": password},  # העברת נתוני המשתמש
    )
    print(response.json())  # הדפסת התגובה מהשרת


# התחברות משתמש קיים
def login(username, password):
    if not username or not password:
        print(Fore.RED + "⚠️אזהרה: יש למלא את שם המשתמש והסיסמה." + Style.RESET_ALL)
        return
    response = session.post(  # שליחת בקשת POST לשרת
        f"{BASE_URL}/login",
        json={"username": username, "password": password},
    )
    if response.status_code == 200:  # בדיקה אם ההתחברות הצליחה
        print(response.json()["message"])
    else:
        print(response.json()["error"])


# התנתקות משתמש
def logout():
    response = session.post(f"{BASE_URL}/logout")  # שליחת בקשת POST לשרת להתנתקות
    if response.status_code == 200:
        print("חבל! התנתקת בהצלחה✅.")
    else:
        print(Fore.RED + "⚠️אזהרה: לא ניתן להתנתק!!!!!!" + Style.RESET_ALL)


# התחלת משחק חדש
def start_game(word_choice):
    response = session.get(
        f"{BASE_URL}/start_game/{word_choice}"
    )  # שליחת בקשת GET לשרת להתחלת משחק
    if response.status_code == 200:  # התחיל בהצלחה
        return response.json().get("word")  # החזרת המילה מהשרת
    else:
        print(
            response.json().get("error", "⚠️אזהרה: נדרש להרשם ולהתחבר לפני התחלת המשחק")
        )
        return None


# הצג היסטוריית משחקים
def show_history():
    response = session.get(
        f"{BASE_URL}/history"
    )  # שולח בקשה GET לשרת לקבלת היסטוריית משחקים
    if response.status_code == 200:  # התקבלה בהצלחה
        history = response.json().get("history", [])  # קבלת היסטוריית המשחקים
        wins = sum(
            1 for entry in history if entry.get("won", False)
        )  # חישוב מספר הניצחונות
        losses = len(history) - wins  # חישוב מספר ההפסדים

        print(f"סך הכל משחקים:{len(history)} ניצחונות:, {wins} הפסדים: {losses}")

        if not history:
            print("אין לך היסטוריות. תתחיל לשחק במשחק שלנו ותוכל לצפות במשחקים שלך!!!")
            return

        for entry in history:  # עבור כל היסטוריה
            won_status = "כן✌️" if entry.get("won", False) else "לא🙅‍♀️"
            print(
                f"התאריך:📅{entry['date']}, השעה:🕰️ {entry['time']} ניצחון: {won_status}, המילה:📖 {entry.get('word', 'לא ידוע')}"
            )
    else:
        print(
            Fore.RED
            + "⚠️אזהרה: אין לך היסטוריות. תתחיל לשחק במשחק שלנו ותוכל לצפות במשחקים שלך!!!"
            + Style.RESET_ALL
        )


# עדכון מצב המשחק
def update_game(won, word):
    response = session.post(
        f"{BASE_URL}/update_game", json={"won": won, "word": word}
    )  # שולח בקשת POST לעדכון מצב המשחק
    try:
        response_data = response.json()  # המרה לאובייקט JSON
        if response.status_code == 200:
            print(response_data["message"])
        else:
            print(response_data.get("error", "שגיאה בעדכון מצב המשחק."))
    except ValueError:
        print("שגיאה: התגובה מהשרת: בעיה בהמרה")
    except Exception as e:
        print(f"שגיאה: {str(e)}")


print("בסיעתא דישמיא")

logo = r"""
            _    _
           | |  | |
           | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
           |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
           | |  | | (_| | | | | (_| | | | | | | (_| | | | |
           |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                                __/ |
                               |___/
    """
print(logo)


# אתחול של colorama
init()


text = """שלום הגעתם למשחק החדש שלנו המן תלוי על עץ!
בו תוכלו לצפות בניצחונות וכן בהפסדים שלכם!
ולהנות במשחק מפתיע ומאתגר- 
וכן מרענן באמצע חיי שיגרה----
הוראות המשחק:
ישנם לפניך 5 אופציות.
באופציה ראשונה תוכלו להתחבר אלינו! ולהתחיל לשחק!   
אך זיכרו זה כמובן בתנאי שכבר אתם מכירים אותנו וכנסתם למשחק שלו.
ואם לו ברוכה הבאה!
הינכם יכולים ללחוץ על מקש 2 במיקלדת שלכם ולהגיע להרשמה אלינו ולהיות מחוברים למערכת שלנו-  
ואם אתם נרשמים אלינו בפעם הבאה שתירצו לשחק במשחק המן תלוי על עץ רק תיצטרכו להתחבר אלינו!  
כמובן זיכרו את שם משתמש שעל שמו נרשמתם וכן הסיסמה שלו לפעם הבאה!
אפשרות 3 בו אם תרצו להפסיק כדי לשתות באמצע כוס קפא ומשהו קטן לאכול
תוכלו ללחוץ 3 כדי להתנתק וכדי לחזור אלינו תתחברו אלינו שוב!
ועל מקש 4 בו ממש מתחיל המשחק דעו יש למשחק זמן מוגבל בו תוכלו לשחק!!
המשחק שלכם כולל 10 דקות בדיוק ולאחר מכן המשחק ניגמר!!!!
ובמקש 5 ישנו אפשרות לראות את היסטורית הניצחונות שלך או ח"ו ההפסדים שלך!
הזדרזו והכנסו אלינו עכשיו תהנו----!!!!!!!!!
משחק מהנה התחילו להמריא אלינו🛩️🛩️🛩️🛩️🛩️🛩️🛩️🛩️🛩️"""

print(Fore.MAGENTA + text)

print(Fore.RESET)


# הפעלת המשחק
def play_hangman():
    print("1. להתחברות🪪")
    print("2. להרשמה📝")
    print("3. ליציאה🚶‍♂️")
    print("4. להתחלת משחק🪜")
    print("5. להצגת היסטוריה‍💻")

    while True:
        try:
            choice = int(input("\033[96mבחר אופציה❓: \033[0m"))
            if choice in [1, 2, 3, 4, 5]:  # בדיקה האם המשתמש לחץ על מספר בין 1-5
                break
            else:
                print(
                    Fore.RED
                    + "אזהרה:⚠️ יש להכניס מספר בין 1 ל-5 בלבד."
                    + Style.RESET_ALL
                )
        except ValueError:
            print(Fore.RED + "אזהרה:⚠️ יש להכניס מספר בלבד." + Style.RESET_ALL)

    if choice == 1:
        username = input("הכנס שם משתמש: ")
        password = input("הכנס סיסמה: ")
        login(username, password)  # קריאה לפונקציית התחברות

    elif choice == 2:
        username = input("הכנס שם משתמש: ")
        password = input("הכנס סיסמה: ")
        register(username, password)  # קריאה לפונקציית רישום

    elif choice == 3:
        logout()  # קריאה לפונקציית התנתקות
        return

    elif choice == 4:
        if not session.cookies:  # בדיקה אם אין עוגיות בסשן
            print(
                Fore.RED
                + "⚠️אזהרה: נדרש להרשם ולהתחבר לפני התחלת המשחק"
                + Style.RESET_ALL
            )
            return

        while True:
            try:
                word_choice = int(input("\033[96mהכנס מספר לבחירת מילה👈: \033[0m"))
                break
            except ValueError:
                print(Fore.RED + "אזהרה:⚠️ יש להכניס מספר בלבד." + Style.RESET_ALL)

        word = start_game(word_choice)  # קבלת המילה מהשרת
        if word:
            hidden_word = "_" * len(word)
            print("המילה היא:", hidden_word)

            attempts = 7  # מספר הניסיונות
            guessed_letters = []  # רשימת האותיות שניחשו

            while attempts > 0:
                guess = input("הכנס אות: ").lower()  # ממיר מאותיות גדולות לקטנות

                if not re.match("^[א-ת]$", guess):
                    print(
                        Fore.RED
                        + "אזהרה:⚠️ יש להכניס אות בעברית בלבד."
                        + Style.RESET_ALL
                    )
                    continue  # חזרה להתחלת הלולאה

                if guess in guessed_letters:  # בדיקה אם האות כבר ניחשה
                    print(
                        Fore.RED
                        + "אזהרה:⚠️ כבר ניחשת את האות הזו, נסה אות אחרת."
                        + Style.RESET_ALL
                    )
                    continue  # חזרה להתחלת הלולאה

                guessed_letters.append(guess)  # הוספת האות לרשימת האותיות הניחשות

                if guess in word:  # בדיקה אם הניחוש נכון
                    print(Back.YELLOW + "נכון!" + Style.RESET_ALL)
                else:
                    attempts -= 1  # הפחתת ניסיונות
                    print(
                        Back.BLACK
                        + f"טעית!❌ נותרו לך⌛ {attempts} פסילות."
                        + Style.RESET_ALL
                    )

                    if attempts == 6:
                        print(r"""      🟤🟤🟤🟤🟤🟤🟤   """)
                    elif attempts == 5:
                        print(
                            r"""
                    🟤🟤🟤🟤🟤🟤🟤
                                 🟤
                                 🟤
                                 🟤
                                 🟤
                                 🟤
                                                          """
                        )
                    elif attempts == 4:
                        print(
                            r"""
                    🟤🟤🟤🟤🟤🟤🟤
                    🟤           🟤
                    😊           🟤
                                 🟤
                                 🟤
                                 🟤
                                                              """
                        )
                    elif attempts == 3:
                        print(
                            r"""
                    🟤🟤🟤🟤🟤🟤🟤
                    🟤           🟤
                    😊           🟤
                    🟢           🟤
                                 🟤
                                 🟤
                                 🟤



                                                                                     """
                        )
                    elif attempts == 2:
                        print(
                            r"""
                    🟤🟤🟤🟤🟤🟤🟤
                    🟤           🟤
                    😊           🟤
                  🟢🟢🟢         🟤
                                  🟤
                                  🟤
                                  🟤

     """
                        )
                    elif attempts == 1:
                        print(
                            r"""
                    🟤🟤🟤🟤🟤🟤🟤
                    🟤            🟤
                    😊            🟤
                  🟢🟢🟢          🟤
                      🦵          🟤
                                  🟤
                                  🟤
                                                                                                              """
                        )
                    elif attempts == 0:
                        print(
                            r"""
                    🟤🟤🟤🟤🟤🟤🟤
                    🟤           🟤
                    😊           🟤
                  🟢🟢🟢         🟤
                    🦵🦵         🟤
                                  🟤
                                  🟤
                                                                                                                  """
                        )
                # מציג את המילה המוסתרת עם האותיות הניחשות
                hidden_word = "".join(
                    letter if letter in guessed_letters else "_" for letter in word
                )
                print("המילה היא:", hidden_word)
                if "_" not in hidden_word:  # אם לא נותרו אותיות נסתרות
                    print("ניחשת את המילה! כל הכבוד!👏")
                    print(" המילה היא:" + hidden_word)
                    break

            if attempts == 0:  # אם נגמרו הניסיונות
                print(Fore.BLUE + f"הפסדת!🙁 המילה הייתה: {word}" + Style.RESET_ALL)
                update_game(False, word)  # אם נפסל אז מעדכן FALSE ומעדכן את המילה
            else:
                update_game(True, word)  # אם ניצח אז מעדכן TRUE ומעדכן את המילה

    elif choice == 5:
        show_history()  # קריאה לפונקציית הצגת היסטוריה


if __name__ == "__main__":
    while True:
        play_hangman()  # קריאה לפונקציית הפעלת המשחק
