import openai
import os

def generate_response(prompt, relevant_cases, case_infos):
    openai.api_key = os.environ['OPENAI_API_KEY']
    case_info = " ".join([f"{case['case_title']} ({case['citation']}): {', '.join(case['helpful_quotes'])}" for case in case_infos])
    
    print("Case info:", case_info)  # Add this line to print case_info
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Based on the following case information, answer the legal question: \"{prompt}\".\n\nCases: {case_info}\n\nProviding citations and relavant quotes, if any, Please provide an accurate and thorough answer: ",
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    answer = response.choices[0].text.strip()
    return answer

