from flask import Flask, request, jsonify
from symspellpy import SymSpell, Verbosity
import os

app = Flask(__name__)

# 1. Create SymSpell object and load dictionary
max_edit_distance_dictionary = 2
prefix_length = 7
sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)

# Path to your frequency dictionary
dictionary_path = "frequency_dictionary_az_80k.txt"

# Check if dictionary file exists
if not os.path.exists(dictionary_path):
    raise FileNotFoundError(f"Dictionary file not found: {dictionary_path}")

# Load dictionary
term_index = 0  # Column index for terms
count_index = 1  # Column index for frequencies
if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
    raise Exception("Failed to load dictionary")

# 2. Define API endpoint for word correction
@app.route('/correct', methods=['GET'])
def correct():
    # Get word or phrase from query parameters
    input_term = request.args.get('text', '')
    if not input_term:
        return jsonify({'error': 'Parameter "text" is missing'}), 400

    # Perform lookup for suggestions
    max_edit_distance_lookup = 2
    suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST, max_edit_distance_lookup)

    # Format response
    results = []
    for suggestion in suggestions:
        results.append({
            'term': suggestion.term,
            'distance': suggestion.distance,
            'count': suggestion.count
        })

    if results:
        return jsonify({'suggestions': results})
    else:
        return jsonify({'message': 'No suggestions found'}), 200

if __name__ == '__main__':
    # Run server on port 5000
    app.run(host='0.0.0.0', port=5000)