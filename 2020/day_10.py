# Part 1

with open("input_10.txt") as f:
    text = f.read().strip()
adapters = list(map(int, text.split("\n")))
adapters.sort()
adapters.insert(0, 0)
adapters.append(adapters[-1] + 3)

adapter_diff = [abs(j - i) for i, j in zip(adapters, adapters[1:])]
print(
    sum(1 for diff in adapter_diff if diff == 1)
    * sum(1 for diff in adapter_diff if diff == 3)
)


# Part 2


class AdapterTree:
    def __init__(self, joltage, children=None):
        self.joltage = joltage
        self.children = []


def enrich_tree(adapter_tree, adapters_left, count):
    for index, adapter in enumerate(adapters_left):
        if len(adapters_left) == 0:
            return count
        if adapter - adapter_tree.joltage < 4:
            child = AdapterTree(adapter, [])
            if adapter == adapters_left[-1]:
                count += 1
            adapter_tree.children.append(child)
            # print(f"Added child={adapter} to parent={adapter_tree.joltage}")
            count = enrich_tree(child, adapters_left[index + 1 :], count)
        if adapter - adapter_tree.joltage >= 4:
            break
    return count


def count_arrangements(adapters):
    if len(adapters) == 1:
        return 1
    adapters.sort()
    adapter_tree = AdapterTree(adapters[0], [])
    adapters_left = adapters[1:]
    count = 0
    return enrich_tree(adapter_tree, adapters_left, count)


def count_arrangements_efficiently(adapters):
    total_count = 1
    current_part = []
    for adapter in adapters:
        if not current_part or adapter - current_part[-1] < 3:
            current_part.append(adapter)
            continue
        if adapter - current_part[-1] == 3:
            total_count *= count_arrangements(current_part)
            current_part = [adapter]
            continue
    return total_count


print(count_arrangements_efficiently(adapters))
