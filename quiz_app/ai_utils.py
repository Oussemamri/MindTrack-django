from django.core.cache import cache
from django.conf import settings
from typing import List, Tuple
import requests
import random
from datetime import datetime

class RateLimitExceeded(Exception):
    pass

class QuestionGenerator:
    def __init__(self):
        self.api_key = settings.QUIZ_API_KEY
        self.base_url = "https://quizapi.io/api/v1/questions"
        self.MAX_REQUESTS_PER_HOUR = 100

    def generate_questions(self, topic: str, num_questions: int) -> tuple[List[Tuple[str, List[Tuple[str, bool]]]], bool]:
        if self._is_rate_limited():
            raise RateLimitExceeded("API rate limit exceeded. Please try again later.")

        try:
            params = {
                'apiKey': self.api_key,
                'limit': num_questions,
                'category': self._map_topic_to_category(topic),
                'difficulty': 'Medium'
            }
            
            print(f"Making API request with params: {params}")  # Debug log
            response = requests.get(self.base_url, params=params)
            print(f"API Response Status: {response.status_code}")  # Debug log
            print(f"API Response Content: {response.text}")  # Debug log
            
            response.raise_for_status()
            
            questions_data = response.json()
            formatted_questions = self._format_questions(questions_data)
            
            if formatted_questions:
                self._update_rate_limit_counter()
                return formatted_questions, True
            else:
                print("No questions were formatted successfully")  # Debug log
                return self._get_fallback_questions(num_questions, topic), False
            
        except Exception as e:
            print(f"Error generating questions: {str(e)}")
            print(f"Error type: {type(e).__name__}")  # Debug log
            print(f"Full error details: {e.__class__.__name__}")
            return self._get_fallback_questions(num_questions, topic), False

    def _format_questions(self, questions_data: List[dict]) -> List[Tuple[str, List[Tuple[str, bool]]]]:
        formatted_questions = []
        
        for q in questions_data:
            question_text = q.get('question')
            if not question_text:
                continue

            answers = []
            correct_answers = q.get('correct_answers', {})
            answer_options = q.get('answers', {})
            
            for key, text in answer_options.items():
                if text:  # Only add non-null answers
                    answer_key = f"{key}_correct"
                    is_correct = correct_answers.get(answer_key) == 'true'
                    answers.append((text, is_correct))
            
            if answers:  # Only add questions with at least one answer
                formatted_questions.append((question_text, answers))
        
        return formatted_questions

    def _map_topic_to_category(self, topic: str) -> str:
        category_map = {
            'linux': 'linux',
            'devops': 'devops',
            'docker': 'docker',
            'code': 'code',
            'sql': 'sql',
            'cms': 'cms'
        }
        mapped_category = category_map.get(topic.lower())
        print(f"Mapping topic '{topic}' to category '{mapped_category}'")  # Debug log
        return mapped_category or 'code'  # Default to 'code' if no match

    def _is_rate_limited(self) -> bool:
        """Check if we've exceeded our rate limit"""
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        rate_limit_key = f"quizapi_api_calls:{current_hour}"
        
        # Get current count of API calls
        current_count = cache.get(rate_limit_key, 0)
        
        return current_count >= self.MAX_REQUESTS_PER_HOUR

    def _update_rate_limit_counter(self) -> None:
        """Increment the rate limit counter"""
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        rate_limit_key = f"quizapi_api_calls:{current_hour}"
        
        # Get current count
        current_count = cache.get(rate_limit_key, 0)
        
        # Increment counter
        cache.set(rate_limit_key, current_count + 1, timeout=settings.RATE_LIMIT_CACHE_TIMEOUT)

    def _get_fallback_questions(self, num_questions: int, topic: str = None) -> List[Tuple[str, List[Tuple[str, bool]]]]:
        """Return topic-specific fallback questions"""
        question_bank = {
            "History": [
                ("Who was the first President of the United States?", [
                    ("George Washington", True), ("Thomas Jefferson", False), 
                    ("Abraham Lincoln", False), ("John Adams", False),
                ]),
                ("In which year did World War II end?", [
                    ("1945", True), ("1944", False), ("1946", False), ("1943", False),
                ]),
                # Add more history questions
            ],
            "Science": [
                ("What is the chemical symbol for gold?", [
                    ("Au", True), ("Ag", False), ("Fe", False), ("Cu", False),
                ]),
                ("Which planet is closest to the Sun?", [
                    ("Mercury", True), ("Venus", False), ("Earth", False), ("Mars", False),
                ]),
                # Add more science questions
            ],
            "Geography": [
                ("What is the capital of France?", [
                    ("Paris", True), ("London", False), ("Berlin", False), ("Madrid", False),
                ]),
                ("Which is the largest ocean?", [
                    ("Pacific", True), ("Atlantic", False), ("Indian", False), ("Arctic", False),
                ]),
                # Add more geography questions
            ],
            # Add more topics
        }
        
        # Get questions for the specific topic or use general questions
        if topic and topic in question_bank:
            available_questions = question_bank[topic]
        else:
            # Combine all questions if topic not found
            available_questions = [q for questions in question_bank.values() for q in questions]
        
        # Shuffle and return requested number of questions
        random.shuffle(available_questions)
        return available_questions[:num_questions]