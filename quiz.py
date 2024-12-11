import random
import ollama

# Global set to track asked questions
asked_questions = set()

# Function to fetch a trivia question
def get_trivia_question():
    global asked_questions  # Declare the global set
    seed = random.randint(1000, 9999)  # Random seed to promote diversity
    prompt = (
        f"You are a trivia question generator. Generate a unique trivia question every time you are asked, "
        f"with seed {seed}. Format the response exactly like this:\n"
        "Question: <A clear trivia question>\n"
        "Options: A) <First option> B) <Second option> C) <Third option> D) <Fourth option>\n"
        "Answer: <The correct option letter (A, B, C, or D)>.\n"
        "Avoid repetition or previous topics in any questions."
    )
    try:
        response = ollama.generate(prompt=prompt, model="mistral")
        if response and 'response' in response:
            text = response['response']
            lines = text.split("\n")
            if len(lines) >= 3:
                question = lines[0].replace("Question: ", "").strip()
                options = lines[1].replace("Options: ", "").strip()
                answer = lines[2].replace("Answer: ", "").strip()
                
                # Avoid duplicate questions
                if question in asked_questions:
                    print("Duplicate detected. Regenerating...")
                    return get_trivia_question()
                
                asked_questions.add(question)
                return question, options, answer
    except Exception as e:
        print(f"Error fetching question: {e}")

    # Fallback static question
    return "What is the capital of France?", "A) Paris B) Berlin C) Rome D) Madrid", "A"

# Function to play the trivia game
def play_trivia_game():
    print("Welcome to the Trivia Game!")
    print("Answer the questions by typing the letter corresponding to your choice (A, B, C, or D).\n")

    score = 0

    for round_number in range(1, 11):
        print(f"Round {round_number}")
        question, options, correct_answer = get_trivia_question()

        print(question)
        print(options)

        user_answer = input("Your answer: ").strip().upper()

        if user_answer == correct_answer:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was {correct_answer}.\n")

    print(f"Game Over! Your final score is {score}/10.")
    print("Thanks for playing!")

# Main function
def main():
    while True:
        play_trivia_game()
        replay = input("Do you want to play again? (yes/no): ").strip().lower()
        if replay not in ('yes', 'y'):
            print("Goodbye! Come back soon!")
            break

if __name__ == "__main__":
    main()
