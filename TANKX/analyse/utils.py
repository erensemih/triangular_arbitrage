from collections import OrderedDict

def get_triangles_and_symbols(discrepancy_dict, max_symbols):
    # Using a set to keep track of unique elements
    unique_symbols = set()
    # Using an OrderedDict to maintain the order of insertion for the result
    symbol_set = OrderedDict()
    triangles = []

    for triangle in discrepancy_dict.keys():
        A, B, C = triangle.split("_")
        # Create pairs for the triangle
        pairs = [A+B, B+C, A+C]
        import logging

        # Calculate what the new size of unique_symbols would be if current pairs are added
        temp_symbol_set = unique_symbols.union(pairs)

        # Check if adding these pairs would exceed the max_symbols limit
        if len(temp_symbol_set) <= max_symbols:
            unique_symbols.update(pairs)
            for pair in pairs:
                # Update the actual symbol_set with pairs while maintaining order
                symbol_set[pair] = None
            triangles.append(pairs)
        else:
            break  # Stop adding more triangles once we reach the limit

    # Convert OrderedDict keys back to a list to maintain order


    ordered_symbol_set = list(symbol_set.keys())

    return triangles, ordered_symbol_set