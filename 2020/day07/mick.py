import re


class Bag:
    def __init__(self, color, children):
        self.color = color
        self.children = children
        self.num_of_children = 0

    def __repr__(self):
        return f"Bag({self.color})"

    @staticmethod
    def clean_data(data):
        bag_color = re.match(r'(.*) bags contain', data)[1]
        bag_children = re.findall(r'(\d+?) (.+?) bags?', data)
        return [bag_color, bag_children]

    def check_gold(self, all_bags):
        try:
            next(filter(lambda x: x[1] == "shiny gold", self.children))
            return True
        except StopIteration:
            pass
        for child in self.children:
            next_bag = all_bags[child[1]]
            if next_bag.check_gold(all_bags):
                return True

        return False

    def count_children(self, all_bags):
        num_of_children = 0
        for child in self.children:
            num_of_children += int(child[0])
            next_bag = all_bags[child[1]]
            print(next_bag)
            num_of_children += int(child[0]) * next_bag.count_children(all_bags)
        return num_of_children



def get_data():
    my_dict = {}
    with open("2020/day07/data.txt") as f:
        for bags in f.read().split("\n"):
            color, children = Bag.clean_data(bags)
            new_bag = Bag(color, children)
            my_dict[new_bag.color] = new_bag
    return my_dict


def bags_with_gold():
    bag_dict = get_data()
    gold_bags = [bag_dict[bag].check_gold(bag_dict) for bag in bag_dict]
    return sum(gold_bags)

print(f"There are {bags_with_gold()} bags that can contain a shiny gold bag")
print(f"There are {get_data()['shiny gold'].count_children(get_data())} individual bags in one shiny gold bag")