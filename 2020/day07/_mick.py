import re


class Bag:
    def __init__(self, color, children):
        self.color = color
        self.children = children

    def __repr__(self):
        return f"Bag({self.color})"

    @staticmethod
    def from_string(data):
        bag_color = re.match(r'(.*) bags contain', data)[1]
        bag_children = re.findall(r'(\d+?) (.+?) bags?', data)
        return Bag(bag_color, bag_children)

    def contains(self, all_bags, color):
        try:
            next(filter(lambda x: x[1] == color, self.children))
            return True
        except StopIteration:
            pass
        for child in self.children:
            next_bag = all_bags[child[1]]
            if next_bag.check_gold(all_bags, color):
                return True

        return False

    def count_children(self, all_bags):
        num_of_children = 0
        for num, color in self.children:
            num_of_children += int(num)
            num_of_children += int(num) * all_bags[color].count_children(all_bags)
        return num_of_children



def get_data():
    my_dict = {}
    with open("2020/day07/data.txt") as f:
        for bags in f.read().split("\n"):
            new_bag = Bag.from_string(bags)
            my_dict[new_bag.color] = new_bag
    return my_dict


def bags_with_gold():
    bag_dict = get_data()
    gold_bags = [bag_dict[bag].check_gold(bag_dict, 'shiny gold') for bag in bag_dict]
    return sum(gold_bags)

def count_bags(current_bag, all_bags ):
    children = current_bag.children
    count = 0
    for child in children:
        current_amount = int(child[0])
        count += current_amount
        next_bag = all_bags[child[1]]
        count += count_bags(next_bag, all_bags) * int(child[0]) 
    return count

bag_dict = get_data()

print(f"There are {bags_with_gold()} bags that can contain a shiny gold bag")
print(f"There are {count_bags(bag_dict['shiny gold'], bag_dict)} individual bags in one shiny gold bag")