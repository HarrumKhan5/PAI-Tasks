from flask import Flask, render_template, request, jsonify # type: ignore
import numpy as np

app = Flask(__name__)

N = 4
board = np.zeros((N, N), dtype=int)
queens = 0

def is_safe(board, row, col):
    for i in range(row):
        if board[i][col]:
            return False
    
    i, j = row, col
    while i >= 0 and j >= 0:
        if board[i][j]:
            return False
        i -= 1
        j -= 1
    
    i, j = row, col
    while i >= 0 and j < N:
        if board[i][j]:
            return False
        i -= 1
        j += 1
    
    return True

@app.route('/')
def index():
    return render_template('index.html', board=board)

@app.route('/place_queen', methods=['POST'])
def place_queen():
    global queens
    data = request.json
    row, col = data['row'], data['col']
    
    if board[row][col] == 1:
        return jsonify({"message": "A queen is already placed here!"})
    
    if not is_safe(board, row, col):
        return jsonify({"message": "This move is not safe! Try again."})
    
    board[row][col] = 1
    queens += 1
    
    if queens == N:
        return jsonify({"message": "🎉 Congratulations! You placed all 4 queens correctly! 🎉", "win": True})
    
    return jsonify({"message": "Queen placed successfully!", "win": False})

@app.route('/reset', methods=['POST'])
def reset_board():
    global board, queens
    board = np.zeros((N, N), dtype=int)
    queens = 0
    return jsonify({"message": "Board reset! Start again."})

if __name__ == '__main__':
    app.run(debug=True)
