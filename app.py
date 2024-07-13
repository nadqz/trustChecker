from flask import Flask, request, jsonify
import hashlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def calculate_file_hash(file):
    hash_func = hashlib.sha256()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_func.update(chunk)
    file.seek(0)  # Reset file pointer to the beginning after reading
    return hash_func.hexdigest()

@app.route('/compare', methods=['POST'])
def compare_files():
    try:
        file1 = request.files['file1']
        file2 = request.files['file2']

        hash1 = calculate_file_hash(file1)
        hash2 = calculate_file_hash(file2)

        result = {
            "file1": {
                "filename": file1.filename,
                "content_type": file1.content_type,
                "size": len(file1.read()),  # Calculate file size correctly
                "hash": hash1,
                "source_of_origin": "Uploaded from user's device"
            },
            "file2": {
                "filename": file2.filename,
                "content_type": file2.content_type,
                "size": len(file2.read()),  # Calculate file size correctly
                "hash": hash2,
                "source_of_origin": "Uploaded from user's device"
            },
            "are_files_identical": hash1 == hash2
        }

        # Reset file pointers to the beginning after reading
        file1.seek(0)
        file2.seek(0)

        return jsonify(result), 200
    except KeyError:
        return jsonify({"error": "Please provide 'file1' and 'file2' in the request."}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
