import random
import os

class RockPaperScissors:
    def __init__(self):
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.choices = ['rock', 'paper', 'scissors']
        self.choice_emojis = {
            'rock': '🪨',
            'paper': '📄',
            'scissors': '✂️'
        }
        
    def clear_screen(self):
        """Clear the console screen for better UI"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self):
        """Display welcome message and game rules"""
        print("=" * 50)
        print("🎮 WELCOME TO ROCK PAPER SCISSORS! 🎮")
        print("=" * 50)
        print("\n📋 GAME RULES:")
        print("• Rock beats Scissors")
        print("• Scissors beat Paper")
        print("• Paper beats Rock")
        print("\n💡 HOW TO PLAY:")
        print("• Type 'rock', 'paper', or 'scissors'")
        print("• You can also use shortcuts: 'r', 'p', 's'")
        print("• Type 'quit' to exit the game")
        print("=" * 50)
    
    def get_user_choice(self):
        """Get and validate user input"""
        while True:
            user_input = input("\n🎯 Enter your choice (rock/paper/scissors or r/p/s): ").lower().strip()
            
            if user_input in ['quit', 'exit', 'q']:
                return 'quit'
            
            # Handle shortcuts
            if user_input in ['r', 'rock']:
                return 'rock'
            elif user_input in ['p', 'paper']:
                return 'paper'
            elif user_input in ['s', 'scissors']:
                return 'scissors'
            else:
                print("❌ Invalid choice! Please enter rock, paper, scissors (or r, p, s)")
    
    def get_computer_choice(self):
        """Generate random computer choice"""
        return random.choice(self.choices)
    
    def determine_winner(self, user_choice, computer_choice):
        """Determine the winner based on game rules"""
        if user_choice == computer_choice:
            return 'tie'
        
        winning_combinations = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }
        
        if winning_combinations[user_choice] == computer_choice:
            return 'user'
        else:
            return 'computer'
    
    def display_choices(self, user_choice, computer_choice):
        """Display both choices with emojis"""
        print(f"\n🎭 CHOICES:")
        print(f"You chose: {user_choice.upper()} {self.choice_emojis[user_choice]}")
        print(f"Computer chose: {computer_choice.upper()} {self.choice_emojis[computer_choice]}")
    
    def display_result(self, winner, user_choice, computer_choice):
        """Display the result of the round"""
        print("\n" + "=" * 30)
        
        if winner == 'tie':
            print("🤝 IT'S A TIE!")
        elif winner == 'user':
            print("🎉 YOU WIN!")
            self.user_score += 1
        else:
            print("💻 COMPUTER WINS!")
            self.computer_score += 1
        
        self.rounds_played += 1
        print("=" * 30)
    
    def display_score(self):
        """Display current score"""
        print(f"\n📊 SCORE AFTER {self.rounds_played} ROUND(S):")
        print(f"You: {self.user_score} | Computer: {self.computer_score}")
        
        if self.user_score > self.computer_score:
            print("🌟 You're leading!")
        elif self.computer_score > self.user_score:
            print("🤖 Computer is leading!")
        else:
            print("⚖️ It's tied!")
    
    def play_again(self):
        """Ask if user wants to play another round"""
        while True:
            choice = input("\n🔄 Do you want to play again? (yes/no or y/n): ").lower().strip()
            if choice in ['yes', 'y']:
                return True
            elif choice in ['no', 'n']:
                return False
            else:
                print("❌ Please enter 'yes' or 'no' (or 'y' or 'n')")
    
    def display_final_stats(self):
        """Display final game statistics"""
        print("\n" + "=" * 40)
        print("📈 FINAL GAME STATISTICS")
        print("=" * 40)
        print(f"Total rounds played: {self.rounds_played}")
        print(f"Your wins: {self.user_score}")
        print(f"Computer wins: {self.computer_score}")
        print(f"Ties: {self.rounds_played - self.user_score - self.computer_score}")
        
        if self.user_score > self.computer_score:
            print("🏆 CONGRATULATIONS! YOU WON OVERALL!")
        elif self.computer_score > self.user_score:
            print("🤖 Computer won overall. Better luck next time!")
        else:
            print("🤝 Overall tie! Great game!")
        
        win_rate = (self.user_score / self.rounds_played * 100) if self.rounds_played > 0 else 0
        print(f"Your win rate: {win_rate:.1f}%")
        print("=" * 40)
    
    def play_game(self):
        """Main game loop"""
        self.clear_screen()
        self.display_welcome()
        
        while True:
            # Get user choice
            user_choice = self.get_user_choice()
            
            if user_choice == 'quit':
                break
            
            # Get computer choice
            computer_choice = self.get_computer_choice()
            
            # Display choices
            self.display_choices(user_choice, computer_choice)
            
            # Determine winner
            winner = self.determine_winner(user_choice, computer_choice)
            
            # Display result
            self.display_result(winner, user_choice, computer_choice)
            
            # Display score
            self.display_score()
            
            # Ask if user wants to play again
            if not self.play_again():
                break
        
        # Display final statistics
        if self.rounds_played > 0:
            self.display_final_stats()
        
        print("\n👋 Thanks for playing Rock Paper Scissors!")
        print("See you next time!")

def main():
    """Main function to start the game"""
    game = RockPaperScissors()
    game.play_game()

if __name__ == "__main__":
    main()