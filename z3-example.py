from z3 import *

# Create variables
x = Int('x')
y = Int('y')

# Create a solver instance
solver = Solver()

# Add constraints
solver.add(x + y == 10)
solver.add(x > 0, y > 0)

# Check satisfiability
if solver.check() == sat:
    print("Solution:")
    print(solver.model())
else:
    print("No solution exists.")
