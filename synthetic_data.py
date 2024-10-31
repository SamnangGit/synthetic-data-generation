import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_aoi_key = os.getenv('GROQ_API_KEY')

responses = []
ranked_response = []


def read_csv(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            csv_content = file.read()
            csv_content = '\n'.join(line.rstrip() for line in csv_content.splitlines())
            return csv_content
            
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path '{path}' was not found.")
    except IOError as e:
        raise IOError(f"Error reading file at path '{path}': {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error reading CSV file: {str(e)}")
    
def write_csv(csv_string, output_path, extract_from_tags=True):
    try:
        if not csv_string or not csv_string.strip():
            raise ValueError("CSV string is empty")
            
        if extract_from_tags:
            start_tag = "<synthetic_data_csv>"
            end_tag = "</synthetic_data_csv>"
            
            start_idx = csv_string.find(start_tag)
            end_idx = csv_string.find(end_tag)
            
            if start_idx != -1 and end_idx != -1:
                csv_string = csv_string[start_idx + len(start_tag):end_idx].strip()
            else:
                print("Warning: Tags not found, using entire string as CSV content")
        
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Write the CSV content to file
        with open(output_path, 'w', encoding='utf-8', newline='') as file:
            cleaned_content = '\n'.join(line for line in csv_string.splitlines() if line.strip())
            file.write(cleaned_content)
            
        print(f"CSV file successfully written to: {output_path}")
            
    except IOError as e:
        raise IOError(f"Error writing to file at path '{output_path}': {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error writing CSV file: {str(e)}")    


prompt_template = """
    Given a real dataset in CSV format, analyze its patterns and generate 100 rows of synthetic data that maintains similar statistical properties and relationships. Your response should ONLY include the synthetic data in CSV format within the specified tags.

    The real data is provided here:
    <real_data_csv>
    {REAL_DATA_CSV}
    </real_data_csv>

    Important:
    - Do NOT provide any code or explanations
    - ONLY output exactly 100 rows of synthetic data
    - Maintain the same column names and order as the original data
    - Keep similar patterns, distributions, and relationships between columns
    - Ensure data types match the original (e.g., integers stay integers)
    - Generate new unique values for any ID columns
    - Respect any business rules or constraints visible in the real data

    Before outputting:
        1. COUNT the number of rows you've generated
        2. VERIFY it is exactly 100
        3. If not 100, regenerate until you have exactly 100 rows

    Provide ONLY the synthetic data in this format:
    <synthetic_data_csv>
    [Generated CSV data here - exactly 100 rows]
    </synthetic_data_csv>
"""

prompt = prompt_template.format(REAL_DATA_CSV=read_csv('./dataset/healthcare_dataset.csv'))

model = 'llama-3.2-11b-text-preview'


def data_generation(prompt, model):
    groq = Groq(api_key=groq_aoi_key)
    response = groq.chat.completions.create(
        messages=[
            {
                'role' : 'user',
                'content' : prompt
            }
        ],
        model=model
    )
    print(prompt)
    print()
    print('====================================')
    print()

    result = response.choices[0].message.content
    write_csv(result, './output/new_two.csv')

    return response.choices[0].message.content


def main():
    result = data_generation(prompt, model=model)
    print(result)


if __name__ == "__main__":
    main()