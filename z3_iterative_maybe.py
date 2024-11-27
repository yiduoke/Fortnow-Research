from z3 import *

# Initialize solver
solver = Solver()

# Simulated parameters
num_items = 10  # Number of items
import random
random.seed(42)

items = [f"item_{i}" for i in range(num_items)]
u_A1 = {item: random.randint(1, 20) for item in items}
u_A2 = {item: random.randint(1, 20) for item in items}

# Print utility table
print("\nUtility Table:")
print(f"{'Item':<10}{'Utility A1':<15}{'Utility A2':<15}")
for item in items:
    print(f"{item:<10}{u_A1[item]:<15}{u_A2[item]:<15}")

# Turing machine outputs
tm_A = sorted(items, key=lambda item: u_A1[item], reverse=True)
tm_B = sorted(items, key=lambda item: u_A2[item], reverse=True)

# Merge outputs from TM A and TM B
revealed_items = []
for i in range(max(len(tm_A), len(tm_B))):
    if i < len(tm_A):
        revealed_items.append(tm_A[i])
    if i < len(tm_B):
        revealed_items.append(tm_B[i])

# Variables for allocation
x = {item: Bool(f"x_{item}") for item in items}


# EFX constraints
def add_efx_constraints(solver, revealed, alloc, u_A1, u_A2):
    # Utilities for revealed items
    U_A1 = Sum([If(alloc[item], u_A1[item], 0) for item in revealed])
    U_A2 = Sum([If(Not(alloc[item]), u_A2[item], 0) for item in revealed])

    U_A1_2 = Sum([If(Not(alloc[item]), u_A1[item], 0) for item in revealed])
    U_A2_1 = Sum([If(alloc[item], u_A2[item], 0) for item in revealed])

    # Add EFX constraints for revealed items
    for item in revealed:
        solver.add(U_A1 >= U_A1_2 - If(Not(alloc[item]), u_A1[item], U_A1_2))
        solver.add(U_A2 >= U_A2_1 - If(alloc[item], u_A2[item], U_A2_1))

# Maintain a set of solutions
valid_allocations = []

# Process revealed items
for step in range(len(revealed_items)):
  current_pool = revealed_items[:step + 1]
  solver.push()

  # Add allocation constraints for the current pool
  # for item in current_pool:
  #     solver.add(Or(And(x[item], Not(x[item])), Not(x[item])))
  
  # for item in current_pool:
  #   solver.add(Or(x[item], Not(x[item])))  # Either assigned to A1 or A2


  # Add EFX constraints
  add_efx_constraints(solver, current_pool, x, u_A1, u_A2)

  # Find all valid solutions for the current pool
  current_allocations = []
  while solver.check() == sat:
    model = solver.model()
    # solution = {item: model[x[item]] for item in current_pool}
    solution = {item: model.evaluate(x[item]) for item in current_pool}
    allocation = {item: model[x[item]] for item in items}

    current_allocations.append(allocation)
    solver.add(Not(And([x[item] == solution[item] for item in current_pool])))
    

  # Filter solutions: Keep only subsets of the next step's allocations
  if valid_allocations:
    valid_allocations = [
      prev for prev in valid_allocations
      if any(all(prev[item] == sol.get(item, None) for item in prev) for sol in current_allocations)
    ]
  else:
    valid_allocations = current_allocations

  solver.pop()

  # Debugging output for current step
  print(f"\nStep {step + 1}:")
  print(f"Revealed items: {current_pool}")
  print(f"Number of valid allocations: {len(valid_allocations)}")

  # Print valid allocations with utility values
  for idx, sol in enumerate(valid_allocations, 1):
    print("sol: ", sol)
    A1_items = [item for item in sol if sol[item]]
    A2_items = [item for item in sol if not sol[item]]
    A1_utility = sum(u_A1[item] for item in A1_items)
    A2_utility = sum(u_A2[item] for item in A2_items)
    print(f"\nAllocation {idx}:")
    print(f"  Agent A1 gets: {A1_items} (Utility: {A1_utility})")
    print(f"  Agent A2 gets: {A2_items} (Utility: {A2_utility})")

# Final results
print("\nFinal valid allocations:")
for idx, sol in enumerate(valid_allocations, 1):
    A1_items = [item for item, allocated_to_A1 in sol.items() if allocated_to_A1]
    A2_items = [item for item in sol if item not in A1_items]
    A1_utility = sum(u_A1[item] for item in A1_items)
    A2_utility = sum(u_A2[item] for item in A2_items)
    print(f"\nFinal Allocation {idx}:")
    print(f"  Agent A1 gets: {A1_items} (Utility: {A1_utility})")
    print(f"  Agent A2 gets: {A2_items} (Utility: {A2_utility})")
