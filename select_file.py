import os

def list_directories_and_count(directory):
    directories = [d for d in os.listdir(directory) if os.path.isfile(os.path.join(directory, d))]
    directories_split = [f.split('#')[0] for f in directories]

    counts = {}
    for item in directories_split:
        counts[item] = counts.get(item, 0) + 1

    unique_list = []
    for item, count in counts.items():
        unique_list.append((item, count))

    return unique_list

def select_category(categories):
    page = 1

    while True:
        start_index = (page - 1) * 10
        end_index = min(len(categories), start_index + 10)
        print("Select a category:")

        for i in range(start_index, end_index):
            print(f"{i + 1}. {categories[i][0]}")
        
        choice = input(f"Enter the number ({start_index + 1}-{end_index}) or 'n' for next page, 'p' for previous page, or 'q' to quit: ")
        if choice.isdigit():
            category_index = int(choice) - 1
            if start_index <= category_index < end_index:
                return categories[category_index]
            else:
                print("\n！！！Invalid choice! Please enter a number within the range.！！！\n")
                continue
        elif choice.lower() == 'n':
            if end_index < len(categories):
                page += 1
                continue
            else:
                print("\n！！！No more files.！！！\n")
                continue
        elif choice.lower() == 'p':
            if start_index > 0:
                page -= 1
                continue
            else:
                print("\n！！！Already at the first page.！！！\n")
                continue
        elif choice.lower() == 'q':
            return None
        else:
            print("\n！！！Invalid choice! Please enter a valid option.！！！\n")
            continue

def select_again(selected_directory):
    if selected_directory is not None:
        page = 1
        name = selected_directory[0]
        num = selected_directory[1]

        while True:
            start_index = (page - 1) * 10
            end_index = min(num, start_index + 10)
            print(f"Files in '{name}':")

            for i in range(start_index, end_index):
                print(f"{i + 1 - start_index}. {name}#{i + 1}.json")

            choice = input(f"Enter the number ({start_index + 1}-{end_index}) or 'n' for next page, 'p' for previous page, or 'q' to quit: ")
            if choice.isdigit():
                file_index = int(choice)
                if start_index < file_index <= end_index:
                    return f"{name}#{file_index}.json"
                else:
                    print("\n！！！Invalid choice! Please enter a number within the range.！！！\n")
                    continue
            elif choice.lower() == 'n':
                if end_index < num:
                    page += 1
                    continue
                else:
                    print("\n！！！No more files.！！！\n")
                    continue
            elif choice.lower() == 'p':
                if start_index > 0:
                    page -= 1
                    continue
                else:
                    print("\n！！！Already at the first page.！！！\n")
                    continue
            elif choice.lower() == 'q':
                return None
            else:
                print("\nInvalid choice! Please enter a valid option.\n")
                continue

def select_file_in_category(directory):
    directories = list_directories_and_count(directory)
    selected_directory = select_category(directories)

    input1 = select_again(selected_directory)
    print(f"\nYou selected: {input1}\n\nNow select next file in category:\n")
    input2 = select_again(selected_directory)

    return (input1, input2)


# if __name__ == "__main__":
#     directory = './put'
#     selected_file = select_file_in_category(directory)
#     if selected_file:
#         print(f"You selected: {selected_file}")