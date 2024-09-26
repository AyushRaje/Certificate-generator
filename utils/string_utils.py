class StringUtils:
    
    def capitalize_string(text_to_capitalize: str):
        modified_string = text_to_capitalize.lower()
        modified_string = modified_string.capitalize()

        for i in range(len(modified_string)):
            if modified_string[i] == ' ' and i + 1 < len(modified_string):
                modified_string = modified_string[:i + 1] + modified_string[i + 1].upper() + modified_string[i + 2:]

        return modified_string

if __name__=='__main__':
    # Example usage
    input_string = "hELLO WoRLD HOW ARE YOU"
    output_string = StringUtils.capitalize_string(input_string)
    print(output_string) 