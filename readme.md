# Introducing LawSCHOLAR - a legal assistant chat bot

This relies on ChatGPT, SerpAPI, LandChain, and Google Scholar to create useful legal content.

https://serpapi.com/google-scholar-api

https://openai.com/

https://python.langchain.com/en/latest/index.html

https://scholar.google.com/

The HTML WebUI takes an input and submits {PROMT} with javeascript and passes it to the python code. The python code then employs the following reasoning method:

## app.py: 

This is the main Flask application. It creates a web server that listens for requests. The '/' route serves the main index.html page, and the '/submit' route takes a legal question as input, uses the other modules to find and analyze relevant legal cases, and then generates a response to the question.

## search.py: 

This module handles the initial search for legal cases. It first uses OpenAI's GPT model to generate a legal query term based on the input prompt. It then uses the SerpAPI (a service for querying Google Search) to search Google Scholar for relevant legal cases. The search results are returned as JSON.

## langchain.py: 

This module processes the search results using LangChain, a text similarity search library. It uses LangChain's Language Model Mediator (LLM) and ConversationChain to create a conversational context and process the search results. It then splits the case texts into smaller chunks and indexes them for similarity search. It ranks the cases based on their similarity to the query.

## analysis.py: 

This module analyzes the search results in more detail. It first downloads the full text of each case, then extracts the citation and case name. It splits the case text into smaller chunks and calculates a relevance score for each chunk using OpenAI's GPT model. The relevance score is used to rank the cases. It also extracts helpful quotes from the cases and returns those as part of the case information.

## output.py: 

This module generates the final output, which is a response to the legal question. It uses OpenAI's GPT model to generate a response based on the case information and the initial prompt. The generated response is then returned to the Flask application.

-----

The system is designed to work in a conversational manner, which means it processes the input question, conducts a search, analyzes the results, and generates a response all in the context of a conversation.

Please note that this system relies heavily on the capabilities of OpenAI's GPT model and the LangChain library for generating search terms, ranking search results, calculating relevance scores, and generating the final response. It also uses SerpAPI for querying Google Scholar and Beautiful Soup for parsing the downloaded case texts.

Currently the project is stalled because google has blocked me for making too many web requests. Another API access method or caselaw database will be required to complete the project.  Please write me with suggestions.  The project should work on your local machine until you get blocked too.  I could try to use a rotating VPN to get around google, but I prefer to use methods acceptable to the project third-party resources. Other options include https://www.law.cornell.edu/search/site; https://case.law/search/#/; or my own state's https://www.vermontjudiciary.org/opinions-decisions.  So far, I have not been able to implement these sites as host databases.
