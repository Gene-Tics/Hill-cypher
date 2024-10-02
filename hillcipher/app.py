import numpy as np
from flask import Flask, render_template, request
from math import gcd

app = Flask(__name__)


def mod_inverse(a, m):
    """Compute the modular inverse of a under modulo m."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None  # Return None if no inverse exists


def compute_determinant(matrix):
    """Compute the determinant of a matrix (works for 2x2 and 3x3)."""
    if matrix.shape[0] == 2:
        return matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]
    elif matrix.shape[0] == 3:
        return (matrix[0, 0] * (matrix[1, 1] * matrix[2, 2] - matrix[1, 2] * matrix[2, 1]) -
                matrix[0, 1] * (matrix[1, 0] * matrix[2, 2] - matrix[1, 2] * matrix[2, 0]) +
                matrix[0, 2] * (matrix[1, 0] * matrix[2, 1] - matrix[1, 1] * matrix[2, 0]))
    else:
        raise ValueError("Unsupported matrix size for determinant calculation.")


def is_coprime(a, b):
    """Check if two numbers are coprime."""
    return gcd(a, b) == 1


def matrix_mod_inv(matrix, modulus):
    """Compute the modular inverse of a matrix under modulo m."""
    det = compute_determinant(matrix) % modulus
    print(f"Determinant: {det}")  # Debugging line
    if det == 0 or not is_coprime(det, modulus):
        raise ValueError("The key matrix is not invertible or suitable for decryption.")

    det_inv = mod_inverse(det, modulus)
    if det_inv is None:
        raise ValueError("Determinant has no modular inverse.")

    # Calculate the adjugate matrix
    if matrix.shape[0] == 2:
        matrix_adj = np.array([
            [matrix[1, 1], -matrix[0, 1]],
            [-matrix[1, 0], matrix[0, 0]]
        ])
    elif matrix.shape[0] == 3:
        matrix_adj = np.array([
            [(matrix[1, 1] * matrix[2, 2] - matrix[1, 2] * matrix[2, 1]) % modulus,
             -(matrix[0, 1] * matrix[2, 2] - matrix[0, 2] * matrix[2, 1]) % modulus,
             (matrix[0, 1] * matrix[1, 2] - matrix[0, 2] * matrix[1, 1]) % modulus],
            [-(matrix[1, 0] * matrix[2, 2] - matrix[1, 2] * matrix[2, 0]) % modulus,
             (matrix[0, 0] * matrix[2, 2] - matrix[0, 2] * matrix[2, 0]) % modulus,
             -(matrix[0, 0] * matrix[1, 2] - matrix[0, 2] * matrix[1, 0]) % modulus],
            [(matrix[1, 0] * matrix[2, 1] - matrix[1, 1] * matrix[2, 0]) % modulus,
             -(matrix[0, 0] * matrix[2, 1] - matrix[0, 1] * matrix[2, 0]) % modulus,
             (matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]) % modulus]
        ])

    matrix_inv = (det_inv * matrix_adj) % modulus
    return matrix_inv % modulus


def hill_encrypt(plaintext, key_matrix):
    """Encrypt the plaintext using the Hill cipher."""
    n = key_matrix.shape[0]

    # Clean up and prepare plaintext
    plaintext = plaintext.upper().replace(" ", "")

    # Validate input: Only allow uppercase letters
    if not all(char.isalpha() for char in plaintext):
        raise ValueError("Plaintext must contain only uppercase letters (A-Z).")

    # Split plaintext into n-grams and pad with 'Z' if necessary
    while len(plaintext) % n != 0:
        plaintext += 'Z'  # Padding with 'Z'

    # Convert plaintext to numbers (A = 0, B = 1, ..., Z = 25)
    plaintext_vector = [ord(char) - ord('A') for char in plaintext]

    # Reshape plaintext vector for matrix multiplication
    plaintext_vector = np.array(plaintext_vector).reshape(-1, n).T

    # Matrix multiplication and mod 26
    encrypted_vector = np.dot(key_matrix, plaintext_vector) % 26

    # Convert numbers back to letters
    encrypted_text = ''.join(chr(num + ord('A')) for num in encrypted_vector.T.flatten())

    return encrypted_text


def hill_decrypt(ciphertext, key_matrix):
    """Decrypt the ciphertext using the Hill cipher."""
    n = key_matrix.shape[0]
    ciphertext = ciphertext.upper().replace(" ", "")

    # Validate input: Only allow uppercase letters
    if not all(char.isalpha() for char in ciphertext):
        raise ValueError("Ciphertext must contain only uppercase letters (A-Z).")

    ciphertext_vector = [ord(char) - ord('A') for char in ciphertext]
    ciphertext_vector = np.array(ciphertext_vector).reshape(-1, n).T

    key_matrix_inv = matrix_mod_inv(key_matrix, 26)
    decrypted_vector = np.dot(key_matrix_inv, ciphertext_vector) % 26
    decrypted_text = ''.join(chr(num + ord('A')) for num in decrypted_vector.T.flatten())

    return decrypted_text


@app.route('/', methods=['GET', 'POST'])
def index():
    ciphertext = ""
    decrypted_message = ""
    error = ""
    matrix_size = 3  # Default to 3x3 matrix

    if request.method == 'POST':
        try:
            operation = request.form['operation']
            matrix_size = int(request.form['matrix_size'])

            # Convert key matrix inputs into numpy array based on matrix size
            key_matrix = np.array(
                [[int(request.form[f'key_{i}_{j}']) for j in range(matrix_size)] for i in range(matrix_size)])

            # Validate key matrix elements
            if not all(0 <= value < 26 for value in key_matrix.flatten()):
                raise ValueError("All key matrix values must be integers between 0 and 25.")

            if operation == 'encrypt':
                plaintext = request.form['plaintext']
                ciphertext = hill_encrypt(plaintext, key_matrix)
            else:
                ciphertext = request.form['ciphertext']
                decrypted_message = hill_decrypt(ciphertext, key_matrix)

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = "An unexpected error occurred."

    return render_template('index.html', ciphertext=ciphertext, decrypted_message=decrypted_message, error=error,
                           matrix_size=matrix_size)


if __name__ == '__main__':
    app.run(debug=True)
