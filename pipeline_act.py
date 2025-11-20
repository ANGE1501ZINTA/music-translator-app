import whisper
import re
from langdetect import detect
from deep_translator import GoogleTranslator

dict_lang = {
    
    "en" : "anglais",
     "fr": "français",
     "es" : "espagnol" ,
    "de" : "allmend",
    "it" : "Italien",
    "pt" : "portuguais"
}

trans_lang = {
    
    "Français": "fr",
    "Anglais": "en",
    "Espagnol": "es",
    "Allemand": "de",
    "Italien": "it",
    "Portugais": "pt"
    
}

def trans_audio(fichier_mp3):
    model = whisper.load_model("base")
    result = model.transcribe(fichier_mp3, fp16=False)
    print(result["segments"])
    return result["segments"]

    
    #  Netoyer
    
def clean_text(t):
    t = re.sub(r"\s+", " ", t)  # enlever espaces multiples
    t = t.strip()
    return t
def extract(segments):
    lines = [clean_text(seg["text"]) for seg in segments if seg.get("text") and seg["text"].strip()]
    ignore_list = ["factory", "usine", "music"]
    lines_cleaned = [line for line in lines if line.lower() not in ignore_list]
    return lines_cleaned

def detect_lang(texte) :
    code = detect(texte)
    langue_complete = dict_lang.get(code, "Langue inconnue") 
    
    return code, langue_complete

def traduct_text(texte , target_full_name) :
    
    print(f" traduction en : {target_full_name} ....")
    
    target_code = trans_lang[target_full_name]
    
    trad = GoogleTranslator(source="auto", target=target_code).translate(texte)
    
    print("traduction terminer")
    
    return trad

# pipeline global

def pipeline(mp3_file, langue_cible="Français"):
    segments = trans_audio(mp3_file)           # Transcription
    lines_cleaned = extract(segments)          # Nettoyage et filtrage
    texte_clean = "\n".join(lines_cleaned)  # chaque segment sur sa propre ligne
    # Texte final pour détection/traduction
    code, langue_detectee = detect_lang(texte_clean)
    traduction_finale = traduct_text(texte_clean, langue_cible)

    # Sauvegarde
    with open("resultat_final.txt", "w", encoding="utf-8") as f:
        f.write("===== PAROLES ORIGINALES =====\n")
        f.write(f"Langue  : {langue_detectee}\n\n")
        f.write(texte_clean)
        f.write("\n\n===== TRADUCTION =====\n")
        f.write(f"Langue  : {langue_cible}\n\n")
        f.write(traduction_finale)

    print("\n FICHIER TXT GÉNÉRÉ \n")
    return texte_clean, traduction_finale
