

def display(foods):
    display_list = {}
    for food in foods:
        display_list[food.title]
    children = food.children.all()
    if len(children) > 0:
        display_list.append(display(food.children.all()))
    return display_list
