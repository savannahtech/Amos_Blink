import json
import yaml
import os

class FormComponent:
    def __init__(self):
        self.forms = {}
        self.current_form = None

    def import_form(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension == '.json':
            with open(file_path, 'r') as file:
                self.forms = json.load(file)
        elif file_extension == '.yaml' or file_extension == '.yml':
            with open(file_path, 'r') as file:
                self.forms = yaml.safe_load(file)
        else:
            raise ValueError("Unsupported file format. Only JSON and YAML are supported.")

        print("Form imported.")
        self.choose_action()

    def fill_form(self):
        if not self.forms:
            print("No form imported. Please import a form first.")
            return

        print("Choose a form:")
        for index, form in enumerate(self.forms, 1):
            print(f"{index}. {form['name']}")

        try:
            choice = int(input()) - 1
            self.current_form = self.forms[choice]
            filled_form = {}
            for question in self.current_form['questions']:
                response = self.ask_question(question)
                filled_form[question['question'].split(' (')[0].strip()] = response

            print("Thank you for filling the form! Here is the filled form:")
            print(json.dumps(filled_form, indent=4, ensure_ascii=False))

            self.choose_action()

        except (ValueError, IndexError):
            print("Invalid choice. Please choose a valid form.")

    def ask_question(self, question):
        q_type = question.get('type', 'string')
        q_options = question.get('options', None)

        while True:
            print(question['question'])
            answer = input()

            if q_type == 'integer':
                try:
                    answer = int(answer)
                    break
                except ValueError:
                    print("Please enter an integer.")
            elif q_type == 'string':
                break
            elif q_type == 'options':
                if answer in q_options:
                    break
                else:
                    print(f"Please choose from the options: {', '.join(q_options)}")
            elif q_type == 'multichoice':
                answer_list = [x.strip() for x in answer.split(',')]
                if all(option in q_options for option in answer_list):
                    break
                else:
                    print(f"Please choose from the options: {', '.join(q_options)}")

        return answer

    def choose_action(self):
        print("Choose an action:")
        print("1. Import a form")
        print("2. Fill in a form")
        print("3. Exit")

        action = input()
        if action == '1':
            print("Enter the path to the form:")
            file_path = input()
            self.import_form(file_path)
        elif action == '2':
            self.fill_form()
        elif action == '3':
            print("Exiting the program.")
            exit()
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    form_component = FormComponent()
    form_component.choose_action()
