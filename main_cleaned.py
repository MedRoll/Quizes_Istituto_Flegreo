from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

app = FastAPI()

# dizionario che contiene tutti i quiz caricati
quizzes = {}

def load_data():
    """
    Carica tutti i quiz base (1-5) e tutti i quiz extra (X-2, X-3) in modo dinamico.
    """
    global quizzes
    quizzes.clear()
    
    # 1. Caricamento quiz base 1 → 5
    for i in range(1, 6):
        path = Path(f"ordered_questions{i}.json")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                quizzes[str(i)] = json.load(f)

    # 2. Caricamento di tutti i quiz extra (es: 1-2, 1-3, 2-2, 2-3, 3-2, ...)
    # Definizione degli ID che devono avere un sottomenu con Base, Approfondimento e Vero/Falso
    extra_quiz_ids = [
        "1-2", "1-3",
        "2-2", "2-3",
        "3-2", "3-3",
        "4-2", "4-3",
        "5-2", "5-3",
    ]

    for quiz_id in extra_quiz_ids:
        # Il file si aspetta nomi come 'ordered_questions1-2.json', 'ordered_questions1-3.json', etc.
        path_extra = Path(f"ordered_questions{quiz_id}.json")
        if path_extra.exists():
            with open(path_extra, "r", encoding="utf-8") as f:
                quizzes[quiz_id] = json.load(f)
# carico subito i dati all'avvio
load_data()

@app.get("/quiz/{quiz_id}/{index}")
def get_quiz_question(quiz_id: str, index: int):
    """
    Restituisce la domanda 'index' del quiz 'quiz_id'
    quiz_id può essere "1", "2", "3", "3-2", "3-3", "4", "4-2", "4-3", "5", "5-2", "5-3"
    """
    if quiz_id not in quizzes:
        return {"errore": "Quiz non trovato"}
    if 0 <= index < len(quizzes[quiz_id]):
        return quizzes[quiz_id][index]
    return {"errore": "Indice non valido"}

@app.get("/quiz_all/{quiz_id}")
def get_quiz_all(quiz_id: str):
    """
    Restituisce tutte le domande di un quiz
    """
    if quiz_id not in quizzes:
        return {"errore": "Quiz non trovato"}
    return quizzes[quiz_id]

@app.get("/", response_class=HTMLResponse)
def index():
    """
    Restituisce la pagina HTML del quiz
    """
    with open("template.html", encoding="utf-8") as f:
        return f.read()
