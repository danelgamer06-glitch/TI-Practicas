"""ai_simple.py

Chatbot sencillo tipo "IA" basado en reglas y aprendizaje básico.

Uso: python ai_simple.py
"""
import json
import re
import os


KB_PATH = "ai_kb.json"


DEFAULT_KB = {
    "greetings": ["hola", "buenos días", "buenas", "buenas tardes", "buenas noches"],
    "farewells": ["adiós", "hasta luego", "nos vemos", "chao"],
    "qa": {
        "¿cómo estás?": "Estoy bien, gracias. ¿Y tú?",
        "qué puedes hacer": "Puedo responder preguntas simples, aprender respuestas nuevas y chatear." 
    }
}


def load_kb():
    if os.path.exists(KB_PATH):
        try:
            with open(KB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_KB.copy()


def save_kb(kb):
    with open(KB_PATH, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)


def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9áéíóúñ¿?¡! ]+", "", text)
    return text


def get_response(kb, text):
    text_n = normalize(text)

    # greetings
    for g in kb.get("greetings", []):
        if g in text_n:
            return "¡Hola!"

    # farewells
    for f in kb.get("farewells", []):
        if f in text_n:
            return "¡Hasta luego!"

    # exact Q/A
    for q, a in kb.get("qa", {}).items():
        if normalize(q) == text_n:
            return a

    # partial match: contains keywords from questions
    for q, a in kb.get("qa", {}).items():
        qn = normalize(q)
        if all(word in text_n for word in qn.split() if len(word) > 2):
            return a

    # fallback
    return None


def teach(kb, question, answer):
    kb.setdefault("qa", {})[question] = answer
    save_kb(kb)


def main():
    kb = load_kb()
    print("Chatbot sencillo — escribe 'salir' para terminar. Escribe 'enseñar' para añadir una respuesta.")
    while True:
        try:
            text = input("Tú: ")
        except EOFError:
            print()
            break

        if not text:
            continue

        t = normalize(text)
        if t in ("salir", "adios", "exit", "quit"):
            print("Bot: ¡Nos vemos!")
            break

        if t.startswith("enseñar") or t.startswith("enseñar:") or t.startswith("enseñar "):
            # formato: enseñar pregunta | respuesta
            rest = text.partition(" ")[2] if " " in text else ""
            if "|" in rest:
                q, _, a = rest.partition("|")
                q = q.strip()
                a = a.strip()
                if q and a:
                    teach(kb, q, a)
                    print("Bot: Enseñado.")
                    continue
            print("Bot: Para enseñar usa: enseñar pregunta | respuesta")
            continue

        resp = get_response(kb, text)
        if resp:
            print("Bot:", resp)
        else:
            print("Bot: No sé responder. Puedes enseñarme usando: enseñar pregunta | respuesta")


if __name__ == "__main__":
    main()
