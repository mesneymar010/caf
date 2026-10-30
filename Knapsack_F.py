def knapsack(weights, values, capacity):
    n = len(weights)

    # Create DP table
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    # Find selected items
    selected = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]

    selected.reverse()

    print("DP Table:")
    for row in dp:
        print(*row)

    print("\nMaximum Value:", dp[n][capacity])
    print("Selected Items (item number, weight, value):")

    for i in selected:
        print(i + 1, weights[i], values[i])


if __name__ == "__main__":
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7

    print("Weights:", weights)
    print("Values:", values)
    print("Knapsack Capacity:", capacity)

    knapsack(weights, values, capacity)
