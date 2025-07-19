
import random
import string
import secrets
import os
import json
from datetime import datetime
import argparse

class PasswordGenerator:

    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous = "0O1lI" 
        
        
        self.history = []
        self.history_file = "password_history.json"
        self.load_history()
    
    def clear_screen(self):
        
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        
        print("\n" + "=" * 60)
        print(f"🔐 {title.upper()}")
        print("=" * 60)
    
    def print_separator(self):
        
        print("-" * 60)
    
    def get_character_set(self, include_lowercase=True, include_uppercase=True, 
                         include_digits=True, include_symbols=True, 
                         exclude_ambiguous=False):
        
        charset = ""
        
        if include_lowercase:
            charset += self.lowercase
        if include_uppercase:
            charset += self.uppercase
        if include_digits:
            charset += self.digits
        if include_symbols:
            charset += self.symbols
        
        if exclude_ambiguous:
            charset = ''.join(char for char in charset if char not in self.ambiguous)
        
        return charset
    
    def generate_password(self, length=12, include_lowercase=True, include_uppercase=True,
                         include_digits=True, include_symbols=True, exclude_ambiguous=False,
                         ensure_complexity=True):
       
        
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        charset = self.get_character_set(include_lowercase, include_uppercase,
                                       include_digits, include_symbols, exclude_ambiguous)
        
        if not charset:
            raise ValueError("At least one character type must be selected")
        
        
        password = ''.join(secrets.choice(charset) for _ in range(length))
        
        
        if ensure_complexity:
            password = self.ensure_password_complexity(password, length, include_lowercase,
                                                     include_uppercase, include_digits,
                                                     include_symbols, exclude_ambiguous)
        
        return password
    
    def ensure_password_complexity(self, password, length, include_lowercase,
                                 include_uppercase, include_digits, include_symbols,
                                 exclude_ambiguous):
        
        
        required_chars = []
        
        if include_lowercase:
            chars = self.lowercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            required_chars.append(secrets.choice(chars))
        
        if include_uppercase:
            chars = self.uppercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            required_chars.append(secrets.choice(chars))
        
        if include_digits:
            chars = self.digits
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            required_chars.append(secrets.choice(chars))
        
        if include_symbols:
            required_chars.append(secrets.choice(self.symbols))
        
        
        if len(required_chars) < length:
            charset = self.get_character_set(include_lowercase, include_uppercase,
                                           include_digits, include_symbols, exclude_ambiguous)
            
            remaining_length = length - len(required_chars)
            additional_chars = [secrets.choice(charset) for _ in range(remaining_length)]
            required_chars.extend(additional_chars)
        
       
        password_list = required_chars[:length]
        secrets.SystemRandom().shuffle(password_list)
        
        return ''.join(password_list)
    
    def check_password_strength(self, password):
        
        score = 0
        feedback = []
        
     
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
    
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in self.symbols for c in password)
        
        char_types = sum([has_lower, has_upper, has_digit, has_symbol])
        score += char_types
        
        if not has_lower:
            feedback.append("Add lowercase letters")
        if not has_upper:
            feedback.append("Add uppercase letters")
        if not has_digit:
            feedback.append("Add numbers")
        if not has_symbol:
            feedback.append("Add special characters")
        
       
        if len(set(password)) < len(password) * 0.7:
            feedback.append("Avoid repeated characters")
            score -= 1
        
       
        sequential_count = 0
        for i in range(len(password) - 2):
            if (ord(password[i]) + 1 == ord(password[i+1]) and 
                ord(password[i+1]) + 1 == ord(password[i+2])):
                sequential_count += 1
        
        if sequential_count > 0:
            feedback.append("Avoid sequential characters (abc, 123)")
            score -= 1
        
        
        if score >= 7:
            strength = "Very Strong"
            color = "🟢"
        elif score >= 5:
            strength = "Strong"
            color = "🟡"
        elif score >= 3:
            strength = "Medium"
            color = "🟠"
        else:
            strength = "Weak"
            color = "🔴"
        
        return {
            'strength': strength,
            'score': score,
            'color': color,
            'feedback': feedback
        }
    
    def save_password_to_history(self, password, settings):
       
        entry = {
            'password': password,
            'length': len(password),
            'settings': settings,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'strength': self.check_password_strength(password)['strength']
        }
        
        self.history.append(entry)
        
      
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
        self.save_history()
    
    def save_history(self):
       
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Warning: Could not save history: {e}")
    
    def load_history(self):
        
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"⚠️  Warning: Could not load history: {e}")
                self.history = []
        else:
            self.history = []
    
    def generate_multiple_passwords(self, count=5, **kwargs):
       
        passwords = []
        for _ in range(count):
            password = self.generate_password(**kwargs)
            strength = self.check_password_strength(password)
            passwords.append({
                'password': password,
                'strength': strength
            })
        return passwords
    
    def interactive_password_generator(self):
        """Interactive mode for password generation"""
        while True:
            try:
                self.clear_screen()
                self.print_header("Interactive Password Generator")
                
                # Get password length
                while True:
                    try:
                        length = int(input("🔢 Enter password length (4-128, default: 12): ") or "12")
                        if 4 <= length <= 128:
                            break
                        else:
                            print("❌ Length must be between 4 and 128 characters!")
                    except ValueError:
                        print("❌ Please enter a valid number!")
                
                # Get character type preferences
                print("\n🎯 Character Types (y/n):")
                include_lowercase = input("Include lowercase letters? (Y/n): ").lower() != 'n'
                include_uppercase = input("Include uppercase letters? (Y/n): ").lower() != 'n'
                include_digits = input("Include numbers? (Y/n): ").lower() != 'n'
                include_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
                
                # Additional options
                print("\n⚙️  Additional Options:")
                exclude_ambiguous = input("Exclude ambiguous characters (0, O, 1, l, I)? (y/N): ").lower() == 'y'
                ensure_complexity = input("Ensure password complexity? (Y/n): ").lower() != 'n'
                
                # Generate multiple passwords option
                generate_multiple = input("Generate multiple passwords? (y/N): ").lower() == 'y'
                
                if generate_multiple:
                    count = int(input("How many passwords? (1-10, default: 5): ") or "5")
                    count = max(1, min(count, 10))
                else:
                    count = 1
                
                # Generate passwords
                print(f"\n🔐 Generated Password{'s' if count > 1 else ''}:")
                self.print_separator()
                
                settings = {
                    'length': length,
                    'include_lowercase': include_lowercase,
                    'include_uppercase': include_uppercase,
                    'include_digits': include_digits,
                    'include_symbols': include_symbols,
                    'exclude_ambiguous': exclude_ambiguous,
                    'ensure_complexity': ensure_complexity
                }
                
                if count == 1:
                    password = self.generate_password(**settings)
                    strength_info = self.check_password_strength(password)
                    
                    print(f"Password: {password}")
                    print(f"Length: {len(password)} characters")
                    print(f"Strength: {strength_info['color']} {strength_info['strength']}")
                    
                    if strength_info['feedback']:
                        print(f"Suggestions: {', '.join(strength_info['feedback'])}")
                    
                    # Save to history
                    self.save_password_to_history(password, settings)
                    
                else:
                    passwords = self.generate_multiple_passwords(count, **settings)
                    for i, pwd_info in enumerate(passwords, 1):
                        password = pwd_info['password']
                        strength = pwd_info['strength']
                        print(f"{i:2d}. {password} [{strength['color']} {strength['strength']}]")
                        
                        # Save to history
                        self.save_password_to_history(password, settings)
                
                # Options after generation
                print(f"\n{'='*60}")
                print("Options:")
                print("1. 🔄 Generate another password")
                print("2. 📊 Check password strength")
                print("3. 📝 View password history")
                print("4. 💾 Export passwords")
                print("0. 🚪 Exit")
                
                choice = input("\n👉 Select an option (0-4): ").strip()
                
                if choice == '1':
                    continue
                elif choice == '2':
                    self.check_custom_password_strength()
                elif choice == '3':
                    self.show_password_history()
                elif choice == '4':
                    self.export_passwords()
                elif choice == '0':
                    print("\n👋 Thank you for using Password Generator!")
                    break
                else:
                    print("❌ Invalid option!")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")
    
    def check_custom_password_strength(self):
        """Allow user to check strength of their own password"""
        self.print_header("Password Strength Checker")
        
        password = input("🔐 Enter password to check: ")
        
        if not password:
            print("❌ Password cannot be empty!")
            input("Press Enter to continue...")
            return
        
        strength_info = self.check_password_strength(password)
        
        print(f"\n📊 Password Analysis:")
        self.print_separator()
        print(f"Password: {'*' * len(password)}")
        print(f"Length: {len(password)} characters")
        print(f"Strength: {strength_info['color']} {strength_info['strength']}")
        print(f"Score: {strength_info['score']}/8")
        
        if strength_info['feedback']:
            print(f"\n💡 Suggestions for improvement:")
            for suggestion in strength_info['feedback']:
                print(f"  • {suggestion}")
        else:
            print(f"\n✅ Excellent! This password meets all security criteria.")
        
        input("\nPress Enter to continue...")
    
    def show_password_history(self):
        """Display password generation history"""
        self.print_header("Password History")
        
        if not self.history:
            print("📭 No passwords in history!")
            input("Press Enter to continue...")
            return
        
        print(f"📝 Last {len(self.history)} generated passwords:")
        self.print_separator()
        
        for i, entry in enumerate(reversed(self.history[-10:]), 1):
            print(f"{i:2d}. Length: {entry['length']} | "
                  f"Strength: {entry['strength']} | "
                  f"Time: {entry['timestamp']}")
        
        show_details = input(f"\n🔍 Show password details? (y/N): ").lower() == 'y'
        
        if show_details:
            print(f"\n🔐 Detailed History:")
            self.print_separator()
            
            for i, entry in enumerate(reversed(self.history[-5:]), 1):
                print(f"\n{i}. Password: {entry['password']}")
                print(f"   Length: {entry['length']} characters")
                print(f"   Strength: {entry['strength']}")
                print(f"   Generated: {entry['timestamp']}")
                
                settings = entry['settings']
                types = []
                if settings.get('include_lowercase'): types.append('lowercase')
                if settings.get('include_uppercase'): types.append('uppercase')
                if settings.get('include_digits'): types.append('digits')
                if settings.get('include_symbols'): types.append('symbols')
                
                print(f"   Types: {', '.join(types)}")
        
        input("\nPress Enter to continue...")
    
    def export_passwords(self):
        """Export password history to file"""
        self.print_header("Export Passwords")
        
        if not self.history:
            print("📭 No passwords to export!")
            input("Press Enter to continue...")
            return
        
        filename = f"passwords_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("🔐 PASSWORD GENERATOR EXPORT\n")
                f.write("=" * 50 + "\n")
                f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Passwords: {len(self.history)}\n\n")
                
                for i, entry in enumerate(self.history, 1):
                    f.write(f"Password #{i}\n")
                    f.write(f"Password: {entry['password']}\n")
                    f.write(f"Length: {entry['length']} characters\n")
                    f.write(f"Strength: {entry['strength']}\n")
                    f.write(f"Generated: {entry['timestamp']}\n")
                    
                    settings = entry['settings']
                    f.write(f"Settings: Length={settings['length']}, ")
                    f.write(f"Lowercase={settings.get('include_lowercase', True)}, ")
                    f.write(f"Uppercase={settings.get('include_uppercase', True)}, ")
                    f.write(f"Digits={settings.get('include_digits', True)}, ")
                    f.write(f"Symbols={settings.get('include_symbols', True)}\n")
                    f.write("-" * 30 + "\n\n")
            
            print(f"✅ Passwords exported to '{filename}'!")
            
        except Exception as e:
            print(f"❌ Error exporting passwords: {e}")
        
        input("Press Enter to continue...")
    
    def quick_generate(self, length=12):
        """Quick password generation for command line use"""
        password = self.generate_password(length=length)
        strength = self.check_password_strength(password)
        
        print(f"🔐 Generated Password: {password}")
        print(f"📏 Length: {length} characters")
        print(f"💪 Strength: {strength['color']} {strength['strength']}")
        
        return password

def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description='🔐 Password Generator')
    parser.add_argument('--length', '-l', type=int, default=12,
                       help='Password length (default: 12)')
    parser.add_argument('--count', '-c', type=int, default=1,
                       help='Number of passwords to generate (default: 1)')
    parser.add_argument('--no-lowercase', action='store_true',
                       help='Exclude lowercase letters')
    parser.add_argument('--no-uppercase', action='store_true',
                       help='Exclude uppercase letters')
    parser.add_argument('--no-digits', action='store_true',
                       help='Exclude digits')
    parser.add_argument('--no-symbols', action='store_true',
                       help='Exclude symbols')
    parser.add_argument('--exclude-ambiguous', action='store_true',
                       help='Exclude ambiguous characters (0, O, 1, l, I)')
    parser.add_argument('--quick', '-q', action='store_true',
                       help='Quick generation without interactive mode')
    
    args = parser.parse_args()
    
    generator = PasswordGenerator()
    
    # Validate length
    if not (4 <= args.length <= 128):
        print("❌ Password length must be between 4 and 128 characters!")
        return
    
    # Validate count
    if not (1 <= args.count <= 50):
        print("❌ Count must be between 1 and 50!")
        return
    
    # Handle quick generation
    if args.quick or any([args.no_lowercase, args.no_uppercase, args.no_digits, 
                         args.no_symbols, args.exclude_ambiguous, args.count > 1]):
        
        settings = {
            'length': args.length,
            'include_lowercase': not args.no_lowercase,
            'include_uppercase': not args.no_uppercase,
            'include_digits': not args.no_digits,
            'include_symbols': not args.no_symbols,
            'exclude_ambiguous': args.exclude_ambiguous,
            'ensure_complexity': True
        }
        
        try:
            if args.count == 1:
                password = generator.generate_password(**settings)
                strength = generator.check_password_strength(password)
                
                print(f"🔐 Generated Password: {password}")
                print(f"📏 Length: {len(password)} characters")
                print(f"💪 Strength: {strength['color']} {strength['strength']}")
                
                generator.save_password_to_history(password, settings)
                
            else:
                passwords = generator.generate_multiple_passwords(args.count, **settings)
                print(f"🔐 Generated {args.count} Passwords:")
                print("=" * 60)
                
                for i, pwd_info in enumerate(passwords, 1):
                    password = pwd_info['password']
                    strength = pwd_info['strength']
                    print(f"{i:2d}. {password} [{strength['color']} {strength['strength']}]")
                    
                    generator.save_password_to_history(password, settings)
                    
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
        
        return
    
    # Run interactive mode
    generator.interactive_password_generator()

if __name__ == "__main__":
    main()