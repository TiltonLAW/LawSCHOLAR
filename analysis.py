import os
import openai
import requests
from bs4 import BeautifulSoup
import re

# analysis.py

def download_full_case(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Print the entire structure of the webpage
    print(soup.prettify())

    # Get all text within the body tag
    body = soup.find('body')
    case_text = body.get_text(separator=' ', strip=True) # get_text() function returns all the text in a document or beneath a tag

    print(f"Full case text 1st: {case_text[:100]}...")
    
    return case_text


def split_text(text, chunk_size):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def get_relevance_score(prompt, case_text):
    openai.api_key = os.environ['OPENAI_API_KEY']
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"On a scale of 1 (not help) to 10 (highly helpful), how helpful is the following case text for answering the legal question: \"{prompt}\"?\n\nCase text: \"{case_text}\".\n\nRelevance score: ",
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    score_text = response.choices[0].text.strip()
    score = int(''.join(filter(str.isdigit, score_text)))  # Extract only digits and convert to int
    return score

def filter_and_rank_cases(prompt, search_results):
    if 'organic_results' not in search_results:
        return [], []

    organic_results = search_results['organic_results']

    case_info = []

    # Calculate relevance scores for each case
    for case in organic_results:
        # Download the full case text using the "link" element in the SERP API JSON output
        case_text = download_full_case(case['link'])

        # Find the citation and case name
        citation = re.search(r'(\d{1,4}\s\w{1,4}\s\d{1,4}\s\(\d{4}\))', case_text)
        citation = citation.group(0) if citation else 'Citation not found'

        case_name = re.search(r'((?:\b[A-Z]+\b\s)+v\.(?:\s\b[A-Z]+\b)+)', case_text)
        case_name = case_name.group(0) if case_name else 'Case name not found'
        case_name_short = re.sub(r'([A-Z]+)', lambda m: m.group(0).capitalize(), case_name)

        # Split the case into chunks if it's too long
        case_chunks = split_text(case_text, 2048)  # GPT-3 token limit is 4096, reserve some tokens for the prompt

        print(f"Case title: {case['title']}")
        print(f"Full case text 2nd: {case_text[:100]}...")  # Print the first 100 characters of the case text
        print(f"Number of chunks: {len(case_chunks)}")

        # Process each chunk separately and calculate the relevance score
        relevance_scores = []
        helpful_quotes = []
        for chunk in case_chunks:
            score = get_relevance_score(prompt, chunk)
            if score >= 5:  # A threshold of 5 to consider a quote helpful
                sentences = re.findall(r'(?:^|[.!?])\s*([^?!.]*?{prompt}[^?!.\n]*[.?!])', chunk)
                if sentences:
                    helpful_quotes.append(sentences[0])
            relevance_scores.append(score)

        if helpful_quotes:
            case_info.append({
                'case_name': case_name_short,
                'citation': citation,
                'helpful_quotes': helpful_quotes
            })

        case['relevance_score'] = max(relevance_scores) if relevance_scores else 0
        print(f"Final relevance score: {case['relevance_score']}\n")

    # Rank cases based on their relevance score
    ranked_cases = sorted(organic_results, key=lambda x: x['relevance_score'], reverse=True)
    return ranked_cases, case_info


