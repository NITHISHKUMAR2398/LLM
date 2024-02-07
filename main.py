# main_script.py
from input_module import input_text
from pre_processing import remove_speaker_names

processed_text = remove_speaker_names(input_text)

# Print the processed text
print(processed_text)


