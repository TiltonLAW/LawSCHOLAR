import os
import openai
import requests

# search.py

os.environ['OPENAI_API_KEY'] = 'sk-insert-your-openai-api-key-here'
os.environ['SERPAPI_KEY'] = 'insert-your-serp-api-key-here'

def generate_query(prompt):
    openai.api_key = os.environ['OPENAI_API_KEY']
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"What are the best search terms to use to find search results for this legal question: \"{prompt}\"? Please provide the term, do not answer in a narrative form. Do not include words like law, court, legal, or defendant",
        temperature=0.6,
        max_tokens=30,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    term = response.choices[0].text.strip().replace('"', '')
    print(f"Generated legal term for the prompt '{prompt}': {term}")
    return term

def get_search_results(query):
    serpapi_key = os.environ['SERPAPI_KEY']
    query_encoded = requests.utils.quote(query)
    response = requests.get(f'https://serpapi.com/search?engine=google_scholar&q={query_encoded}&as_sdt=4%2C46&api_key={serpapi_key}')
    search_results = response.json()
    
    print(f"Search results for query '{query}':")
    for i, result in enumerate(search_results.get('organic_results', [])):
        # print(f"Result {i + 1}: {result['title']}")    
    

        return search_results

