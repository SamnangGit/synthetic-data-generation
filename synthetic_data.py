import os
from groq import Groq
from dotenv import load_dotenv
import cohere
import pandas as pd
from datetime import datetime, timedelta
import random

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
cohere_api_key = os.getenv('COHERE_API_KEY')

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
    groq = Groq(api_key=groq_api_key)
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

def generate_mock_data(sample_size: int = 100, output_path: str = './output/mock_data.csv') -> None:
    """
    Generate mock healthcare data and save it to a CSV file.

    Args:
        sample_size (int): Number of records to generate.
        output_path (str): Path where the CSV file will be saved.
    """
    
    distributions = {
        'gender': {'Male': 0.49, 'Female': 0.51},
        'blood_type': {
            'O+': 0.38, 'A+': 0.34, 'B+': 0.09, 'AB+': 0.03,
            'O-': 0.07, 'A-': 0.06, 'B-': 0.02, 'AB-': 0.01
        },
        'medical_conditions': {
            'None': 0.4, 'Hypertension': 0.2, 'Diabetes': 0.15,
            'Asthma': 0.1, 'Heart Disease': 0.08, 'Arthritis': 0.07
        },
        'age_groups': {
            '18-30': 0.2, '31-50': 0.35, '51-70': 0.3, '71-90': 0.15
        }
    }
    
    mock_data = []
    try:
        for i in range(sample_size):
            # Generate age based on age group distribution
            age_group = random.choices(
                list(distributions['age_groups'].keys()),
                list(distributions['age_groups'].values())
            )[0]
            min_age, max_age = map(int, age_group.split('-'))
            age = random.randint(min_age, max_age)
            
            record = {
                'PatientID': f'P{i+1000:04d}',
                'Gender': random.choices(
                    list(distributions['gender'].keys()),
                    list(distributions['gender'].values())
                )[0],
                'Age': age,
                'BloodType': random.choices(
                    list(distributions['blood_type'].keys()),
                    list(distributions['blood_type'].values())
                )[0],
                'MedicalCondition': random.choices(
                    list(distributions['medical_conditions'].keys()),
                    list(distributions['medical_conditions'].values())
                )[0],
                'LastCheckup': (
                    datetime.now() - timedelta(days=random.randint(0, 365))
                ).strftime('%Y-%m-%d'),
                'BMI': round(random.uniform(18.5, 35.0), 1),
                'BloodPressure': f"{random.randint(90, 140)}/{random.randint(60, 90)}"
            }
            mock_data.append(record)
        
        df_mock = pd.DataFrame(mock_data)
        
        df_mock.to_csv(output_path, index=False)
        print(f"Mock data successfully saved to {output_path}")
        
    except Exception as e:
        raise Exception(f"Error generating mock data: {str(e)}")

def rerank_response():
    real_data = """
        Bobby JacksOn	30	Male	B-	Cancer	1/31/2024	Matthew Smith	Sons and Miller	Blue Cross	18856.28131	328	Urgent	2/2/2024	Paracetamol	Normal
        LesLie TErRy	62	Male	A+	Obesity	8/20/2019	Samantha Davies	Kim Inc	Medicare	33643.32729	265	Emergency	8/26/2019	Ibuprofen	Inconclusive
        DaNnY sMitH	76	Female	A-	Obesity	9/22/2022	Tiffany Mitchell	Cook PLC	Aetna	27955.09608	205	Emergency	10/7/2022	Aspirin	Normal
    """
    
    mock_data = """"
        P1000	Male	19	A-	None	2024-07-16	29.2	101/88
        P1001	Male	70	B+	Asthma	2024-08-07	29.2	134/71
        P1002	Female	46	AB+	None	2023-11-13	23.5	109/68
    """

    synthetic_data = """
        Elijah Reed	59	Female	O-	Hypertension	2/5/2021	Rebecca Torres	Johnson-Fletcher	Aetna	27865.33052	425	Emergency	2/15/2021	Simvastatin	Inconclusive
        Cody Morris	11	Male	A+	Diabetes	1/24/2024	Thomas Martin	 "Hernandez-Rogers and Vang"	 "UnitedHealthcare"	51214.41121	142	Urgent	2/10/2024	Paracetamol	Abnormal
        Aileen Carroll	52	Female	AB-	Obesity	12/26/2023	Lisa Castillo	 "Smith-Neal and Larsen"	 "Cigna"	18424.49454	465	Elective	1/3/2024	Aspirin	Normal
    """

    doc = [mock_data, synthetic_data]

    cohere_obj = cohere.ClientV2(cohere_api_key)
    cohere_result = cohere_obj.rerank(
        model='rerank-english-v3.0',
        query=real_data,
        documents=doc,
        top_n=3

    )
    return cohere_result


def main():
    result = data_generation(prompt, model=model)
    print(result)
    generate_mock_data()
    result = rerank_response()
    print(result)


if __name__ == "__main__":
    main()