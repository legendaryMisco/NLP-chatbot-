import os
import warnings
from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText
from openfabric_pysdk.context import OpenfabricExecutionRay
from openfabric_pysdk.loader import ConfigClass
from time import time

import ontology as ont

############################################################
# Callback function called on update config
############################################################
def config(configuration: ConfigClass):
    # TODO Add code here
    pass

def extract_question(text):
    # Use a regular expression or a natural language processing library to extract the question from the input text.
    question_pattern = r"\?\s+(.*)"
    question_match = re.search(question_pattern, text)
    if question_match:
        return question_match.group(1)
    else:
        return None

def search_ontology(ontology, question):
    # Use the ontology client's query API to search for the answer to the question.
    query = ont.Query(question)
    results = ontology.query(query)
    if results:
        return results[0].answer
    else:
        return None

def generate_response(answer):
    # Generate a response based on the retrieved answer using text generation techniques or by retrieving relevant facts from the ontology.
    if answer:
        return f"The answer to your question is: {answer}"
    else:
        return "I'm sorry, I couldn't find an answer to your question in the science ontology."

def execute(request: SimpleText, ray: OpenfabricExecutionRay) -> SimpleText:
    output = []
    for text in request.text:
        response = ''

        try:
            # Initialize the ontology client
            client = ont.Client()

            # Load the ontology from a file
            ontology = client.load_ontology_from_file("science.owl")

            # Extract the question from the input text
            question = extract_question(text)

            # Search for the answer using the ontology
            answer = search_ontology(ontology, question)

            # Generate a response based on the retrieved answer
            response = generate_response(answer)
        except Exception as e:
            print(f"Error processing question: {e}")
            response = "I'm sorry, I'm still learning about science. I can't answer your question yet."

        output.append(response)

    return SimpleText(dict(text=output))
