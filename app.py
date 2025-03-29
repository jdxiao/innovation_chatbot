from flask import Flask, request, jsonify, render_template
import json
from openai import OpenAI

app = Flask(__name__)

# initialize the OpenAI client for DeepSeek
API_KEY = "placeholder"
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

# load data for RAG
with open('documents/data.json', 'r') as file:
    data = json.load(file)

# categories list for RAG
categories = ["overview", "ICT", "manufacturing", "clean energy", "creative industries"]

# function to analyze user input using DeepSeek
def analyze_user_input(user_input):
    # define the system message for the analysis prompt
    system_message = """
    Please analyze the following user input and classify it into one of the following categories: "overview", "ICT", "manufacturing", "clean energy", "creative industries".
    Also, classify whether the query is about "background", "proposal", or both. If the query is about both, specify that. Please return the results in the following format:
    {
        "category": "overview",  # one of the categories: overview, ICT, manufacturing, clean energy, creative industries
        "type": "background"    # one of the types: background, proposal, both
    }
    """
    
    # API call for user input
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    
    # parse result as dictionary
    analysis_result = response.choices[0].message.content.strip()
    try:
        return json.loads(analysis_result)
    except json.JSONDecodeError:
        return {"error": "Unable to parse response from DeepSeek"}

# retrieve context from the data.json based on identified category and type of query
def retrieve_context(identified_category, is_background, is_proposal):
    context_data = data.get(identified_category, {})
    context = ""

    # always include the 'name' and 'ranking' fields for context
    context += f"Category: {context_data.get('name', '')}\n"
    context += f"Ranking: {context_data.get('ranking', '')}\n\n"

    # add background info if requested
    if is_background and "background" in context_data:
        context += context_data["background"] + "\n\n"

    # add proposal info if requested
    if is_proposal and "proposal" in context_data:
        context += context_data["proposal"]

    # default to overview background if no relevant data is found
    if not context:
        context = data.get("overview", {}).get("background", "")

    return context

# function to generate the final response using DeepSeek
def chat_with_ai(user_input, context):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": """
                You are an expert advisor on Canada’s innovation strategy. Provide concise,
                fact-based insights based on Canada’s innovation reports and global best practices.

                Focus on key sectors where Canada is lagging:
                - Information and Communication Technology (ICT): 5G deployment, broadband expansion, cloud adoption.
                - High-Tech Manufacturing: Commercialization, R&D incentives, industrial-scale innovation.
                - Clean Energy & Sustainability: Green investments, carbon capture, industrial decarbonization.
                - Creative Industries: Gaming, digital content exports, global market competitiveness.

                Prioritize:
                - Actionable policy recommendations.
                - Investment strategies.
                - Technology-driven solutions.
                       
                Your response should be in full sentences, conversational, and informative, unless explicitly requested otherwise.
                Avoid jargon and overly technical language. Use simple, clear language.
                Avoid markdown formatting with the exception of bold text.
                Use bullet points only when necessary.
                Explicitly reference the information given as context whenever relevant.
                Suggest 1 or 2 follow-up questions for the user to ask.
                Limit your full response to 100 words or less.
            """},
            {"role": "user", "content": user_input},
            {"role": "system", "content": context}],
            temperature=0.7
        )
        result = response.choices[0].message.content.split("(Word count:")[0].strip()
        return result
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    # analyze the user input and classify it
    classification = analyze_user_input(user_input)

    # retrieve the relevant context based on the classification (RAG)
    identified_category = classification.get("category", "overview")
    is_background = classification.get("type") == "background"
    is_proposal = classification.get("type") == "proposal" or classification.get("type") == "both"

    context = retrieve_context(identified_category, is_background, is_proposal)

    # generate the response with context
    response = chat_with_ai(user_input, context)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)