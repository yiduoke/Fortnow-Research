import pandas as pd
import sys
import contextlib
import io
from tabulate import tabulate


def generate_release_order(df):
    """
    Generate the item release order based on two Turing Machines (TM1 and TM2).
    - TM1 releases items in decreasing order of Alice's valuation.
    - TM2 releases items in decreasing order of Bob's valuation.
    - Items may be released more than once.
    """
    tm1_sorted = sorted(df.values, key=lambda x: x[1], reverse=True)  # Sort by A1 value
    tm2_sorted = sorted(df.values, key=lambda x: x[2], reverse=True)  # Sort by A2 value

    release_order = []
    seen_items = set()
    tm1_index, tm2_index = 0, 0

    while tm1_index < len(tm1_sorted) or tm2_index < len(tm2_sorted):
        if tm1_index < len(tm1_sorted):
            item = tm1_sorted[tm1_index][0]
            if item not in seen_items:
                release_order.append((item, "TM1"))
                seen_items.add(item)
            tm1_index += 1

        if tm2_index < len(tm2_sorted):
            item = tm2_sorted[tm2_index][0]
            if item not in seen_items:
                release_order.append((item, "TM2"))
                seen_items.add(item)
            tm2_index += 1

    return release_order

def check_EFX(u1_A1, u1_A2, u2_A2, u2_A1, least_fav_A1, least_fav_A2, step):
    """
    Checks if the current allocation maintains EFX at each step.
    EFX conditions:
      - u1(A1) ≥ u1(A2) - min u1(A2)
      - u2(A2) ≥ u2(A1) - min u2(A1)
    """
    if u1_A1 < u1_A2 - least_fav_A1:
        print(f"⚠️ Step {step}: EFX violated for A1! u1(A1) = {u1_A1}, u1(A2) = {u1_A2}, "
              f"Least favorite item in A2's bundle = {least_fav_A1}")
        return True

    if u2_A2 < u2_A1 - least_fav_A2:
        print(f"⚠️ Step {step}: EFX violated for A2! u2(A2) = {u2_A2}, u2(A1) = {u2_A1}, "
              f"Least favorite item in A1's bundle = {least_fav_A2}")
        return True
    
    return False


def efx_allocation(df):
    """
    Implements an online EFX allocation algorithm that assigns items dynamically
    while maintaining EFX at each step.
    """
    release_order = generate_release_order(df)

    A1_alloc, A2_alloc = [], []
    A1_total, A2_total = 0, 0
    allocation_map = {}

    # Tracking for utilities at each step
    A1_total_values, A2_total_values = [], []
    A1_envy_values, A2_envy_values = [], []
    A1_least_fav_in_A2, A2_least_fav_in_A1 = [], []

    for step, (item, released_by) in enumerate(release_order, start=1):
        item_value_A1 = df[df["Item"] == item]["A1 Value"].values[0]
        item_value_A2 = df[df["Item"] == item]["A2 Value"].values[0]

        # Compute values using the actual allocated items instead of df
        u1_A2 = sum(v for _, v in A2_alloc)  # Alice's valuation of Bob's bundle
        u2_A1 = sum(v for _, v in A1_alloc)  # Bob's valuation of Alice's bundle

        # Compute least favorite items from allocated bundles
        least_fav_A1 = min((v for _, v in A2_alloc), default=0)
        least_fav_A2 = min((v for _, v in A1_alloc), default=0)

        # Try assigning to A1 while maintaining EFX
        new_A1_total = A1_total + item_value_A1
        new_u2_A1 = u2_A1 + item_value_A2  # Bob's updated valuation of Alice's bundle
        new_least_fav_A2 = min([v for _, v in A1_alloc] + [item_value_A2], default=0)

        with contextlib.redirect_stdout(io.StringIO()):
            efx_violation = check_EFX(new_A1_total, u1_A2, A2_total, new_u2_A1, least_fav_A1, new_least_fav_A2, step)

        if not efx_violation:
            A1_alloc.append((item, item_value_A1))
            A1_total = new_A1_total
            u2_A1 = new_u2_A1  # Update Bob's valuation of Alice's bundle
            least_fav_A2 = new_least_fav_A2  # Update least favorite item in Alice's bundle
            allocation_map[item] = "1️⃣"
        
        else:
            # Try assigning to A2 while maintaining EFX
            new_A2_total = A2_total + item_value_A2
            new_u1_A2 = u1_A2 + item_value_A1  # Alice's updated valuation of Bob's bundle
            new_least_fav_A1 = min([v for _, v in A2_alloc] + [item_value_A1], default=0)

            with contextlib.redirect_stdout(io.StringIO()):
                efx_violation = check_EFX(A1_total, new_u1_A2, new_A2_total, u2_A1, new_least_fav_A1, least_fav_A2, step)

            if not efx_violation:
                A2_alloc.append((item, item_value_A2))
                A2_total = new_A2_total
                u1_A2 = new_u1_A2  # Update Alice's valuation of Bob's bundle
                least_fav_A1 = new_least_fav_A1  # Update least favorite item in Bob's bundle
                allocation_map[item] = "2️⃣"
            else:
                allocation_map[item] = "❌"  # Skipped item



        # Compute utilities
        u1_A2 = sum(df[df["Item"] == it]["A1 Value"].values[0] for it, _ in A2_alloc)
        u2_A1 = sum(df[df["Item"] == it]["A2 Value"].values[0] for it, _ in A1_alloc)

        # Compute least favorite items at the current step
        least_fav_A1 = min([df[df["Item"] == it]["A1 Value"].values[0] for it, _ in A2_alloc], default=0)
        least_fav_A2 = min([df[df["Item"] == it]["A2 Value"].values[0] for it, _ in A1_alloc], default=0)

        # Store values
        A1_total_values.append(A1_total)
        A2_total_values.append(A2_total)
        A1_envy_values.append(u1_A2)
        A2_envy_values.append(u2_A1)
        A1_least_fav_in_A2.append(least_fav_A1)
        A2_least_fav_in_A1.append(least_fav_A2)

        # **Check EFX at this step**
        check_EFX(A1_total, u1_A2, A2_total, u2_A1, least_fav_A1, least_fav_A2, step)
    

    # Create final DataFrame for display
    df_efx_allocation = pd.DataFrame({
        "Step": list(range(1, len(release_order) + 1)),
        "Item": [item for item, _ in release_order],
        "TM": [released_by for _, released_by in release_order],
        "To": [allocation_map[item] for item, _ in release_order],
        "u1(A1)": A1_total_values,
        "u1(A2)": A1_envy_values,
        "u2(A2)": A2_total_values,
        "u2(A1)": A2_envy_values,
        "u1(A2) least": A1_least_fav_in_A2,
        "u2(A1) least": A2_least_fav_in_A1
    })

    return df_efx_allocation


df = pd.DataFrame({
    "Item": ["g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8", "g9", "g10"],
    "A1 Value": [9, 1, 18, 2, 17, 19, 3, 8, 12, 6],  # Alice's values
    "A2 Value": [9, 18, 17, 14, 2, 19, 7, 5, 1, 11]  # Bob's values
})


df_final = efx_allocation(df)

print(tabulate(df_final, headers='keys', tablefmt='psql'))


