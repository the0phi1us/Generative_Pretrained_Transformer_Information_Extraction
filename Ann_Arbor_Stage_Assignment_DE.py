import pandas as pd
import openai
import time

openai.api_key = 'your-api-key-here'

def modify_text_with_gpt(text):
    MAX_RETRIES = 5
    RETRY_DELAY = 10
    prompt = (
        "Du bist ein Experten-System für Onkologie, speziell für das Gebiet der nuklearmedizinischen Bildgebung und Hämato-Onkologie. "
        "Du wurdest darauf trainiert, auf Grundlage von schriftlichen PET-Befunden bei Lymphom-Patienten zur Therapieplanung das initiale Ann-Arbor-Stadium festzulegen. "
        "Nun möchte ich, dass du die primär dem Lymphom zuzuordnenden Läsionen des folgenden Patienten definierst und mir das wahrscheinlichste Ann-Arbor-Stadium nennst. "
        "Dabei möchte ich, dass du in einem Chain-of-Thought-Ansatz jeden Schritt deiner Analyse erläuterst, um nachzuvollziehen, wie du zu deiner Schlussfolgerung kommst. "
        "Folgende Auswahlmöglichkeiten für das Stadium stehen dir zur Verfügung: "
        "1 = Ann-Arbor-Stadium I, "
        "2 = Ann-Arbor-Stadium II, "
        "3 = Ann-Arbor-Stadium III, "
        "4 = Ann-Arbor-Stadium IV, "
        "Nachdem du die primär dem Lymphom zuzuordnenden Läsionen zusammengefasst und jeden Schritt erläutert hast, gib bitte die Nummer des Stadiums an, das deiner Meinung nach am wahrscheinlichsten vorliegt ohne dabei zusätzlich die Zahl eines weiteren Stadiums aufzuführen, das ebenso möglich wäre. "
        f"{text}"
    ) 

    for attempt in range(MAX_RETRIES):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            print(f"Processed: {text} -> {response['choices'][0]['message']['content']}")
            return response['choices'][0]['message']['content']
        except openai.error.RateLimitError as e:
            print(f"RateLimitError encountered: {e}. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
            RETRY_DELAY += 10
            continue
        except (Timeout, ConnectionError) as e:
            print(f"Error encountered: {e}. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
            continue
    return None

input_excel_file_path = "your-input-excel-file-path-here"
input_column_name = "your-input-column-name-here"
output_column_name = "your-output-column-name-here"
output_excel_file_path = "your-output-excel-file-path-here"

df = pd.read_excel(input_excel_file_path)
df[output_column_name] = df[input_column_name].apply(modify_text_with_gpt)
df.to_excel(output_excel_file_path, index=False)