# Function to read and process data from the file
def read_flashcards(file_path):
    vocals = []  # List to store all vocabularies
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Remove any extra whitespace or newline characters
            if line:
                # Split the line into 3 parts based on the underscore separator
                parts = line.split('_')
                
                # Ensure the line is correctly formatted before processing
                if len(parts) == 3:
                    eng_word = parts[0]  # The English word
                    word_type = parts[1]  # The part of speech (n, v, adj, adv)
                    viet_mean = parts[2]  # The Vietnamese meaning

                    # Create a dictionary for this word
                    vocal = {
                        'eng_word': eng_word,
                        'type': word_type,
                        'vie_mean': viet_mean
                    }

                    # Append the dictionary to the list of vocals
                    vocals.append(vocal)
    return vocals

# Example usage:
file_path = "vocal1.txt"  # Path to the flashcards file
vocals = read_flashcards(file_path)  # Process and store the data

# Output the result
for vocal in vocals:
    print(vocal)
