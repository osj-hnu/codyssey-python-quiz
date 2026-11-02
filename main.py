import json
import random
import os

class Quiz:
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer  # 정답 번호 (1~4)

    def to_dict(self):
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
        """파일에서 데이터를 읽어오거나 초기 데이터를 생성합니다."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
            except (json.JSONDecodeError, KeyError):
                self.set_initial_data()
        else:
            self.set_initial_data()

    def set_initial_data(self):
        """초기 퀴즈 데이터 5개를 설정합니다."""
        initial_quizzes = [
            Quiz("Python에서 리스트에 요소를 추가하는 함수는?", ["add()", "append()", "insert()", "push()"], 2),
            Quiz("Python의 주석 기호는?", ["//", "/* */", "#", "--"], 3),
            Quiz("문자열을 정수로 변환하는 함수는?", ["str()", "int()", "float()", "char()"], 2),
            Quiz("다음 중 불변(Immutable) 자료형은?", ["list", "dict", "set", "tuple"], 4),
            Quiz("리스트의 길이를 구하는 함수는?", ["length()", "size()", "len()", "count()"], 3)
        ]
        self.quizzes = initial_quizzes
        self.high_score = 0
        self.save_data()

    def save_data(self):
        """현재 상태를 state.json에 저장합니다."""
        data = {
            "high_score": self.high_score,
            "quizzes": [q.to_dict() for q in self.quizzes]
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def show_quizzes(self):
        """등록된 모든 퀴즈 목록 출력"""
        print("\n--- 📜 현재 등록된 퀴즈 목록 ---")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"{i}. {quiz.question}")
        print("----------------------------")

    def show_high_score(self):
        """최고 점수 출력"""
        print(f"\n🏆 현재 최고 점수: {self.high_score}점")

    def add_quiz(self):
        """새로운 퀴즈 추가 (요구사항 09, 10, 11)"""
        print("\n--- ➕ 새 퀴즈 추가 ---")
        question = input("질문을 입력하세요: ").strip()
        
        options = []
        for i in range(1, 5):
            opt = input(f"보기 {i}번을 입력하세요: ").strip()
            options.append(opt)
        
        while True:
            try:
                answer = int(input("정답 번호(1~4)를 입력하세요: "))
                if 1 <= answer <= 4:
                    break
                print("❌ 1에서 4 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("❌ 숫자만 입력 가능합니다.")
        
        self.quizzes.append(Quiz(question, options, answer))
        self.save_data()
        print("✅ 퀴즈가 성공적으로 추가되었습니다!")

    def play_quiz(self):
        """퀴즈 풀기 기능"""
        if not self.quizzes:
            print("\n❌ 퀴즈가 없습니다. 먼저 추가해주세요.")
            return

        # 랜덤하게 최대 5문제 선택
        num_to_select = min(len(self.quizzes), 5)
        selected_quizzes = random.sample(self.quizzes, num_to_select)
        
        score = 0
        print(f"\n🚀 퀴즈를 시작합니다! (총 {num_to_select}문제)")

        for i, quiz in enumerate(selected_quizzes, 1):
            print(f"\n[문제 {i}] {quiz.question}")
            for j, option in enumerate(quiz.options, 1):
                print(f"({j}) {option}")
            
            while True:
                try:
                    user_input = input("정답 번호: ").strip()
                    answer_idx = int(user_input)
                    if 1 <= answer_idx <= 4:
                        break
                    print("1~4 사이의 숫자를 입력하세요.")
                except ValueError:
                    print("숫자만 입력 가능합니다.")

            if answer_idx == quiz.answer:
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n🎊 종료! 점수: {score}/{num_to_select}")
        
        if score > self.high_score:
            print(f"🔥 최고 점수 경신! {self.high_score} -> {score}")
            self.high_score = score
            self.save_data()

    def run(self):
        """메인 루프"""
        while True:
            print("\n[ Python 퀴즈 게임 ]")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록 보기")
            print("4. 최고 점수 확인")
            print("5. 종료")
            
            choice = input("원하는 메뉴 번호를 입력하세요: ").strip()

            if choice == '1':
                self.play_quiz()
            elif choice == '2':
                self.add_quiz()
            elif choice == '3':
                self.show_quizzes()
            elif choice == '4':
                self.show_high_score()
            elif choice == '5':
                print("게임을 종료합니다. 안녕히 가세요!")
                break
            else:
                print("\n❌ 잘못된 입력입니다. 1~5 사이의 숫자를 입력해주세요.")

if __name__ == "__main__":
    game = QuizGame()
    game.run()