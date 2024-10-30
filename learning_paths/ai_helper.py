class SimpleAI:
    RESPONSES = {
        'hello': [
            "👋 Hey there, Learning Superhero!\n\n"
            "I'm your AI Learning Buddy, ready to help you conquer the world of knowledge! 🌟\n\n"
            "What can I help you with today?\n"
            "🎯 Creating epic learning paths\n"
            "🎮 Designing fun quizzes\n"
            "🧠 Learning strategies\n"
            "💪 Motivation boosters\n\n"
            "Let's make learning awesome together! ✨"
        ],
        
        'bye': [
            "🌟 Keep Being Awesome!\n\n"
            "Remember:\n"
            "🚀 Every step forward is progress\n"
            "🎮 Learning is your superpower\n"
            "✨ You're doing great!\n\n"
            "Come back anytime for more learning adventures! 👋"
        ],
        
        'create path': [
            "🚀 Master Path Creation Like a Pro!\n\n"
            "1. 🎯 Choose Your Epic Topic\n"
            "   - Pick something you're passionate about\n"
            "   - Think about what others want to learn\n"
            "   - Make it unique and exciting\n\n"
            "2. 🧩 Break It Down (Like a DJ Breaking Beats)\n"
            "   - Start with fundamentals\n"
            "   - Build up to advanced concepts\n"
            "   - Create natural progression\n\n"
            "3. 🎮 Gamify Your Path\n"
            "   - Add interactive quizzes\n"
            "   - Include progress milestones\n"
            "   - Create achievement badges\n\n"
            "4. 🎨 Make It Engaging\n"
            "   - Use multimedia content\n"
            "   - Add real-world examples\n"
            "   - Include practical exercises\n\n"
            "Pro Tip: Think of your learning path as a video game - each topic is a new level to conquer! 🎮✨"
        ],
        
        'quiz tips': [
            "🎯 Level Up Your Quiz Game!\n\n"
            "1. 🧠 Design Mind-Blowing Questions\n"
            "   - Mix multiple choice with open-ended\n"
            "   - Use real-world scenarios\n"
            "   - Add some humor and personality\n\n"
            "2. 🎚️ Balance the Challenge\n"
            "   - 40% Easy (Build confidence)\n"
            "   - 40% Medium (Test understanding)\n"
            "   - 20% Hard (Push boundaries)\n\n"
            "3. 🎭 Add Plot Twists\n"
            "   - Include trick questions\n"
            "   - Add 'What would happen if...?' scenarios\n"
            "   - Make them think outside the box\n\n"
            "4. 🎪 Make It Fun!\n"
            "   - Use memes and pop culture references\n"
            "   - Add encouraging feedback\n"
            "   - Include fun facts with answers\n\n"
            "Remember: The best quizzes are like potato chips - you can't stop at just one! 🎪✨"
        ],
        
        'learning': [
            "🚀 Supercharge Your Learning Journey!\n\n"
            "1. 🧠 The Power of Pomodoro\n"
            "   - 25 minutes focused learning\n"
            "   - 5 minutes dancing break\n"
            "   - Repeat and conquer!\n\n"
            "2. 🎮 Gamify Everything\n"
            "   - Set daily XP goals\n"
            "   - Create learning streaks\n"
            "   - Challenge friends\n\n"
            "3. 🎯 Master the Basics First\n"
            "   - Build strong foundations\n"
            "   - Practice regularly\n"
            "   - Teach others to reinforce\n\n"
            "4. 🎨 Mix It Up\n"
            "   - Try different learning styles\n"
            "   - Use visual aids\n"
            "   - Create mind maps\n\n"
            "Pro Tip: Learning is like a RPG - every day you're leveling up! 🎮✨"
        ],
        
        'motivation': [
            "🚀 Time to Get FIRED UP!\n\n"
            "1. 🎯 Set Epic Goals\n"
            "   - Break big dreams into mini-quests\n"
            "   - Track your progress\n"
            "   - Celebrate small wins\n\n"
            "2. 🎮 Build Your Streak\n"
            "   - Don't break the chain\n"
            "   - Share progress with friends\n"
            "   - Compete with yourself\n\n"
            "3. 🎨 Visualize Success\n"
            "   - Picture yourself mastering topics\n"
            "   - Create a learning vision board\n"
            "   - Share your knowledge\n\n"
            "Remember: You're not just learning, you're becoming a knowledge superhero! 💪✨"
        ],
        
        'default': [
            "🚀 Welcome to Your Learning Adventure!\n\n"
            "I'm your AI Learning Buddy, here to make learning FUN! Ask me about:\n\n"
            "🎯 Creating Epic Learning Paths\n"
            "🎮 Designing Engaging Quizzes\n"
            "🧠 Super-Powered Learning Strategies\n"
            "💪 Motivation Boosters\n\n"
            "Just type what you need help with, and let's make learning awesome! ✨"
        ]
    }

    @staticmethod
    def get_response(user_input):
        user_input = user_input.lower()
        
        # Check for greetings
        greetings = ['hi', 'hello', 'hey', 'greetings', 'sup']
        goodbyes = ['bye', 'goodbye', 'see you', 'cya', 'farewell']
        
        for greeting in greetings:
            if greeting in user_input:
                return SimpleAI.RESPONSES['hello'][0]
                
        for goodbye in goodbyes:
            if goodbye in user_input:
                return SimpleAI.RESPONSES['bye'][0]
        
        # Check other keywords
        for key in SimpleAI.RESPONSES:
            if key in user_input and key not in ['hello', 'bye']:
                return SimpleAI.RESPONSES[key][0]
        
        return SimpleAI.RESPONSES['default'][0] 