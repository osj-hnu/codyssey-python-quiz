import json
import os

class Quiz:
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

    def to_dict(self):
        """객체 데이터를 딕셔너리로 변환 (JSON 저장용)"""
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.answer
        }

class QuizGame:
    def __init__(self):
        self.file_path = 'state.json'
        self.quizzes = []
        self.high_score = 0
        self.load_data()

    def load_data(self):
        """데이터 로드 (요구사항 05, 11)"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.high_score = data.get("high_score", 0)
                self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
        else:
            # 초기 데이터 5개 설정 (요구사항 05)
            self.high_score = 0
            initial_data = [
                {"question": "Python의 창시자는?", "options": ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], "answer": 1},
                {"question": "리스트에 요소를 추가하는 메서드는?", "options": ["add()", "append()", "push()", "insert_end()"], "answer": 2},
                {"question": "Python의 확장자는?", "options": [".py", ".python", ".pyt", ".pyc"], "answer": 1},
                {"question": "출력에 사용하는 함수는?", "options": ["input()", "write()", "print()", "display()"], "answer": 3},
                {"question": "정수형 데이터 타입은?", "options": ["str", "float", "int", "bool"], "answer": 3}
            ]
            self.quizzes = [Quiz(**q) for q in initial_data]
            self.save_data()

    def save_data(self):
        """데이터 저장 (요구사항 11)"""
        data = {
            "high_score": self.high_score,
            "quizzes": [q.to_dict() for q in self.quizzes]
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def run(self):
        """메인 루프 (요구사항 02)"""
        print("=== 퀴즈 게임에 오신 것을 환영합니다! ===")
        # 여기에 메뉴 선택 로직(while문)이 들어갈 예정입니다.

if __name__ == "__main__":
    game = QuizGame()
    game.run()