import pandas as pd
import openai
import time

openai.api_key = 'your-api-key-here'

def modify_text_with_gpt(text):
    MAX_RETRIES = 5
    RETRY_DELAY = 10
    prompt = (
        "You are an expert system in oncology, specifically in the field of nuclear medicine imaging and hemato-oncology. "
        "You are trained to determine the initial Ann Arbor stage for therapy planning based on PET scan reports in lymphoma patients. "
        "Please identify the lesions primarily attributable to lymphoma for the following patient and state the most likely Ann Arbor stage. "
        "Use a chain-of-thought approach to explain each step of your analysis, so the reasoning behind your conclusion is clear. "
        "Here are the staging options available: "
        "1 = Ann Arbor stage I, "
        "2 = Ann Arbor stage II, "
        "3 = Ann Arbor stage III, "
        "4 = Ann Arbor stage IV. "
        "After summarizing the lesions related to lymphoma and explaining each step, please state the number of the stage that you believe is most likely, without suggesting any additional possible stages. "
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
    return None  # If max retries exceeded, return None

input_excel_file_path = "your-input-excel-file-path-here"
input_column_name = "Written PET/CT Report"
output_column_name = "Ann Arbor Stage – As Determined by GPT-4 Based on PET/CT Report Text"
output_excel_file_path = "your-output-excel-file-path-here"

df = pd.read_excel(input_excel_file_path)
df[output_column_name] = df[input_column_name].apply(modify_text_with_gpt)
df.to_excel(output_excel_file_path, index=False)
