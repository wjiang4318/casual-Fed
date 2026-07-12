from datetime import datetime
from app.db.database import SessionLocal
from app.db.models import Meeting
import re
from diff_match_patch import diff_match_patch

def _tokenize(text:str) -> list[str]:
    return re.findall(r"\w+(?:[-/]\w+)*|[^\w\s]", text) #

def get_prior_statement(date:str):
    date_obj = datetime.strptime(date, "%Y%m%d") 
    session = SessionLocal()
    existing = session.query(Meeting).filter(Meeting.date<date_obj).order_by(Meeting.date.desc()).first()
    session.close()
    if existing: 
        return existing.statement_text
    else:
        return None
    

def diff_statements(prior_text: str, current_text: str) -> list[dict]:
    prior_words = _tokenize(prior_text)
    current_words = _tokenize(current_text)

    # Step 2: every unique word across BOTH texts gets one shared placeholder char.
    # Shared vocabulary is what lets diff_main recognize "same word in both texts".
    all_words = set(prior_words) | set(current_words)
    word_to_char = {word: chr(0xE000 + i) for i, word in enumerate(all_words)} # dictionary comprehension
    #{"The": chr(0xE000),
    #"Committee": chr(0XE001)}
    char_to_word = {char: word for word, char in word_to_char.items()} # reverse mapping of word_to_char

    # Step 3: re-encode each word list as one placeholder-character string.
    prior_encoded = "".join(word_to_char[w] for w in prior_words)
    current_encoded = "".join(word_to_char[w] for w in current_words)

    # Step 4: diff the two short placeholder strings, not the original text.
    dmp = diff_match_patch()
    diffs = dmp.diff_main(prior_encoded, current_encoded)
    dmp.diff_cleanupSemantic(diffs)

    # Step 5: decode each placeholder char back to its real word, and build output.
    op_names = {-1: "delete", 0: "equal", 1: "insert"}
    result = []
    for op, chars in diffs:
        words = [char_to_word[c] for c in chars]
        result.append({"type": op_names[op], "text": " ".join(words)})

    return result


if __name__ == "__main__":
    prior = "The Committee decided to maintain rates"
    current = "The Committee decided to lower rates"
    for chunk in diff_statements(prior, current):
        print(chunk)
