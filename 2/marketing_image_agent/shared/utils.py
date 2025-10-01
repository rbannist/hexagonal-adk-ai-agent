class DataManipulationUtils:
    @staticmethod
    def get_list_of_dict_values(self, list_of_dicts: list, key: str) -> list:
        return [a_dict[key] for a_dict in list_of_dicts]

    @staticmethod
    def get_list_of_dict_values_as_str(self, list_of_dicts: list, key: str) -> str:
        return ', '.join(self.get_list_of_dict_values(list_of_dicts, key))

    @staticmethod
    def snake_to_camel_case(snake_str: str) -> str:
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    @staticmethod
    def camel_to_snake_case(camel_str: str) -> str:
        snake_str = ""
        for i, char in enumerate(camel_str): # type: ignore
            if char.isupper():
                if i > 0:
                    snake_str += "_"
                snake_str += char.lower()
            else:
                snake_str += char
        return snake_str
    
    @staticmethod
    def snake_case_to_hyphenated_compounds(snake_str):
        return '-'.join(part.capitalize() for part in snake_str.split('_'))

    @staticmethod
    def convert_keys_snake_to_camel_case(data):
        if isinstance(data, dict):
            return {DataManipulationUtils.snake_to_camel_case(k): DataManipulationUtils.convert_keys_snake_to_camel_case(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [DataManipulationUtils.convert_keys_snake_to_camel_case(item) for item in data]
        return data