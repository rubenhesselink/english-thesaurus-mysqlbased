from difflib import get_close_matches
import mysql.connector

def connect_db():
    con = mysql.connector.connect(
        user='ardit700_student',
        password='ardit700_student',
        host='108.167.140.122',
        database='ardit700_pm1database'
    )
    return con


def search_word(query, con):
    cursor = con.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def translate(word, con):
    query = "SELECT * FROM Dictionary WHERE EXPRESSION = '%s'" % word
    results = search_word(query, con)
    # MySQL queries are case insensitive. This means we don't have to check for lower, upper and title.

    if results:
        return [result[1] for result in results]
    else:
        # Gather all words and find close matches

        query = "SELECT * FROM Dictionary"
        results = search_word(query, con)
        list_to_compare = [result[0] for result in results]

        if len(get_close_matches(word, list_to_compare)) > 0:
            yn = input("Did you mean %s instead? Enter Y if correct, or N if incorrect."
                       % get_close_matches(word, list_to_compare)[0])
            if yn.upper()[0] == 'Y':
                suggested_word = get_close_matches(word, list_to_compare)[0]
                query = "SELECT * FROM Dictionary WHERE EXPRESSION = '%s'" % suggested_word
                results = search_word(query, con)
                return [result[1] for result in results]
            elif yn.upper()[0] == 'N':
                return "Word not found."
            else:
                return "Word not found."
        else:
            return "Word not found."


word = input("Enter word: ")
con = connect_db()
output = translate(word, con)

if type(output) == list:
    for item in output:
        print(item)
else:
    print(output)