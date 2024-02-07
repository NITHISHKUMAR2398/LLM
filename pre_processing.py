import re

class PreprocessModule:
    def __init__(self):
        pass

    def remove_speaker_names(self, text):
        # Define a regex pattern to match names with the format "Dr.[Name]:"
        pattern = re.compile(r"Dr\.[A-Za-z]+:")

        # Remove the matched names
        processed_text = re.sub(pattern, "", text)
        
        return processed_text
