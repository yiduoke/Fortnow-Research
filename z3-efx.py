# from z3 import *
# import random

# # Simulated parameters
# num_items = 10  # Simulate with a finite subset of items
# items = [f"item_{i}" for i in range(num_items)]

# # Utility functions for agents A1 and A2
# # Replace these with your Turing machine outputs or any dynamic computation
# u_A1 = {f"item_{i}": random.randint(1, num_items) for i in range(num_items)}  # Example utility for A1
# u_A2 = {f"item_{i}": random.randint(1, num_items) for i in range(num_items)}  # Example utility for A2

# # Z3 variables for allocation
# # x[item] = 0 if assigned to A1, 1 if assigned to A2
# x = {item: Int(f"x_{item}") for item in items}

# # Initialize solver
# solver = Solver()

# # Fixed assignment constraint: Every item must be assigned to one agent
# for item in items:
#     solver.add(Or(x[item] == 0, x[item] == 1))

# # Compute utilities for each agent
# U_A1 = Sum([If(x[item] == 0, u_A1[item], 0) for item in items])
# U_A2 = Sum([If(x[item] == 1, u_A2[item], 0) for item in items])

# # EFX Constraints: No envy up to any single item
# for item in items:
#     # Envy-free up to any single item for A1
#     solver.add(Or(
#         U_A1 >= U_A2,  # No envy
#         U_A1 >= U_A2 - If(x[item] == 1, u_A2[item], 0)  # Removing item resolves envy
#     ))
#     # Envy-free up to any single item for A2
#     solver.add(Or(
#         U_A2 >= U_A1,  # No envy
#         U_A2 >= U_A1 - If(x[item] == 0, u_A1[item], 0)  # Removing item resolves envy
#     ))

# # Solve the allocation problem
# if solver.check() == sat:
#     model = solver.model()
#     # Extract allocation and compute utilities
#     allocation = {item: model[x[item]].as_long() for item in items}
#     assigned_A1 = [item for item in items if allocation[item] == 0]
#     assigned_A2 = [item for item in items if allocation[item] == 1]
#     total_utility_A1 = sum(u_A1[item] for item in assigned_A1)
#     total_utility_A2 = sum(u_A2[item] for item in assigned_A2)
    
#     # Print results
#     print("Allocation:")
#     print("Agent A1:", assigned_A1, "| Total Utility:", total_utility_A1)
#     print("Agent A2:", assigned_A2, "| Total Utility:", total_utility_A2)
# else:
#     print("No EFX allocation found under these constraints.")


from z3 import *
import random

# Simulated parameters
num_items = 10  # Number of items to simulate
items = [f"item_{i}" for i in range(num_items)]

# Random utility values for each agent
random.seed(42)  # Set seed for reproducibility
u_A1 = {item: random.randint(1, 20) for item in items}  # Random utilities for A1
u_A2 = {item: random.randint(1, 20) for item in items}  # Random utilities for A2

# Print generated utilities
print("Agent A1's utilities:", u_A1)
print("Agent A2's utilities:", u_A2)

# Z3 variables for allocation
# x[item] = 0 if assigned to A1, 1 if assigned to A2
x = {item: Int(f"x_{item}") for item in items}

# Initialize solver
solver = Solver()

# Fixed assignment constraint: Every item must be assigned to one agent
for item in items:
    solver.add(Or(x[item] == 0, x[item] == 1))

# Compute utilities for each agent
U_A1 = Sum([If(x[item] == 0, u_A1[item], 0) for item in items])
U_A2 = Sum([If(x[item] == 1, u_A2[item], 0) for item in items])

# EFX Constraints: No envy up to any single item
for item in items:
    # Envy-free up to any single item for A1
    solver.add(Or(
        U_A1 >= U_A2,  # No envy
        U_A1 >= U_A2 - If(x[item] == 1, u_A2[item], 0)  # Removing item resolves envy
    ))
    # Envy-free up to any single item for A2
    solver.add(Or(
        U_A2 >= U_A1,  # No envy
        U_A2 >= U_A1 - If(x[item] == 0, u_A1[item], 0)  # Removing item resolves envy
    ))

# Solve the allocation problem
if solver.check() == sat:
    model = solver.model()
    # Extract allocation and compute utilities
    allocation = {item: model[x[item]].as_long() for item in items}
    assigned_A1 = [item for item in items if allocation[item] == 0]
    assigned_A2 = [item for item in items if allocation[item] == 1]
    total_utility_A1 = sum(u_A1[item] for item in assigned_A1)
    total_utility_A2 = sum(u_A2[item] for item in assigned_A2)
    
    # Print results
    print("\nAllocation:")
    print("Agent A1:", assigned_A1, "| Total Utility:", total_utility_A1)
    print("Agent A2:", assigned_A2, "| Total Utility:", total_utility_A2)
else:
    print("No EFX allocation found under these constraints.")
