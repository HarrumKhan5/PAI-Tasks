from flask import Flask, render_template, request
from collections import deque

app = Flask(__name__)

def water_jug_solver_dfs(jug1_capacity, jug2_capacity, target):
    visited = set()
    stack = [(0, 0)]  
    solution_steps = []

    while stack:
        state = stack.pop()
        jug1, jug2 = state

        if state in visited:
            continue
        
        visited.add(state)
        solution_steps.append(f"Jug1: {jug1}L, Jug2: {jug2}L")

        if jug1 == target or jug2 == target:
            solution_steps.append("Solution found!")
            return solution_steps
        possible_moves = [
            (jug1_capacity, jug2),  
            (jug1, jug2_capacity),  
            (0, jug2),              
            (jug1, 0),              
            (jug1 - min(jug1, jug2_capacity - jug2), jug2 + min(jug1, jug2_capacity - jug2)),  
            (jug1 + min(jug2, jug1_capacity - jug1), jug2 - min(jug2, jug1_capacity - jug1))   
        ]

        for move in possible_moves:
            if move not in visited:
                stack.append(move)
    
    solution_steps.append("No solution found.")
    return solution_steps

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    if request.method == 'POST':
        jug1_capacity = int(request.form['jug1_capacity'])
        jug2_capacity = int(request.form['jug2_capacity'])
        target = int(request.form['target'])
        result = water_jug_solver_dfs(jug1_capacity, jug2_capacity, target)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

