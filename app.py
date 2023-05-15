from flask import Flask, render_template, request, jsonify
import search
import analysis
import output

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    prompt = data['prompt']
    query = search.generate_query(prompt)
    search_results = search.get_search_results(query)


    relevant_cases, case_infos = analysis.filter_and_rank_cases(prompt, search_results)
    answer = output.generate_response(prompt, relevant_cases, case_infos)
    return jsonify(answer)

if __name__ == '__main__':
    app.run()
