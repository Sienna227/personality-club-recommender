# 개인 성향 분석 기반 개인 맞춤형 교내활동 추천 시스템
# 문제해결과컴퓨팅사고 11조 [말차중조]

import time

# 시작 화면
print("=" * 70)
print("🎓 개인 맞춤형 교내활동 추천 시스템")
print("🎓 Personalized Campus Activity Recommendation System")
print("=" * 70)
print("\n안녕하세요!")
print("간단한 성향 검사를 통해 당신에게 맞는 교내활동을 추천해드립니다.")
print("자신에게 가장 맞는 선택지를 골라주세요.")
input("👉 시작하려면 Enter 키를 누르세요...")

scores = {"S": 0,"G": 0,"P": 0,"T": 0,"I": 0,"O": 0,"PL": 0,"C": 0}

# 질문 데이터
questions = [{"question": "1. 새로운 사람들과 친해질 수 있는 활동이 더 좋다.","positive": "S","negative": "G"},
    {"question": "2. 활동을 선택할 때 재미보다 결과와 성과가 중요하다.","positive": "G","negative": "S"},
    {"question": "3. 사람들과 어울리는 활동이 혼자 하는 활동보다 좋다.","positive": "S","negative": "G"},
    {"question": "4. 혼자 집중해서 하는 활동이 편하다.","positive": "P","negative": "T"},
    {"question": "5. 팀 프로젝트나 단체 활동이 재미있다.","positive": "T","negative": "P"},
    {"question": "6. 다른 사람들과 역할을 나누는 활동이 좋다.","positive": "T","negative": "P"},
    {"question": "7. 실내 활동이 더 편하다.","positive": "I","negative": "O"},
    {"question": "8. 몸을 움직이는 활동을 좋아한다.","positive": "O","negative": "I"},
    {"question": "9. 조용한 공간에서 활동하는 것이 좋다.","positive": "I","negative": "O"},
    {"question": "10. 계획이 잘 정리된 활동이 좋다.","positive": "PL","negative": "C"},
    {"question": "11. 새로운 도전을 하는 활동이 재미있다.","positive": "C","negative": "PL"},
    {"question": "12. 익숙한 방식보다 새로운 경험을 선호한다.","positive": "C","negative": "PL"}]

# 16가지 성향 유형 데이터
type_details = {"SPIN": {"name": "조용한 자기계발형","activity": "정적","relation": "개인몰입","focus": "취미향유","style": "표현창작","clubs": ["성균서도회", "서예부"]},
    "SPIC": {"name": "몰입형 탐구가","activity": "정적","relation": "개인몰입","focus": "취미향유","style": "탐구실천","clubs": ["SAPA"]},
    "SPON": {"name": "독립적 실천가","activity": "정적","relation": "개인몰입","focus": "역량성장","style": "표현창작","clubs": ["그린나래", "성미회", "행소문화회", "글터"]},
    "SPOC": {"name": "자유로운 개척자","activity": "정적","relation": "개인몰입","focus": "역량성장","style": "탐구실천","clubs": ["TIME", "GNC"]},
    "STIN": {"name": "따뜻한 실내교류형","activity": "정적","relation": "교류협업","focus": "취미향유","style": "표현창작","clubs": ["겟세마네", "반촌", "성불회", "CCC", "UBF", "다정"]},
    "STIC": {"name": "창의적 협업가","activity": "정적","relation": "교류협업","focus": "취미향유","style": "탐구실천","clubs": ["별누리", "팀선비", "다정"]},
    "STON": {"name": "꾸준한 공동체형","activity": "정적","relation": "교류협업","focus": "역량성장","style": "표현창작","clubs": ["심산한누리", "호우회", "KUSA", "HERA"]},
    "STOC": {"name": "활기찬 팀플레이어","activity": "정적","relation": "교류협업","focus": "역량성장","style": "탐구실천","clubs": ["멋쟁이 사자처럼", "SKFC", "삼은사과", "패거리","풍물패 얼", "SWAY", "꼬", "능라촌","대동악회", "사후", "CT", "엘세데아","애송이", "GROOV", "JDA", "TuNA","수선관 그 밴드", "헤게모니", "파란"]},
    "GPIN": {"name": "계획적 성장형","activity": "활동","relation": "개인몰입","focus": "취미향유","style": "표현창작","clubs": ["KCC"]},
    "GPIC": {"name": "집중형 문제해결가","activity": "활동","relation": "개인몰입","focus": "취미향유","style": "탐구실천","clubs": ["기우회", "Equal", "Re:Skku"]},
    "GPON": {"name": "성실한 실행가","activity": "활동","relation": "개인몰입","focus": "역량성장","style": "표현창작","clubs": ["Be-Nay", "AIESEC"]},
    "GPOC": {"name": "독립형 도전자","activity": "활동","relation": "개인몰입","focus": "역량성장","style": "탐구실천","clubs": ["태권도부", "벽걸강산", "검도부"]},
    "GTIN": {"name": "전략적 협력가","activity": "활동","relation": "교류협업","focus": "취미향유","style": "표현창작","clubs": ["SKKIP", "SKKUO", "영숨촌"]},
    "GTIC": {"name": "프로젝트 추진형","activity": "활동","relation": "교류협업","focus": "취미향유","style": "탐구실천","clubs": ["성균극회", "성균합창단"]},
    "GTON": {"name": "책임감 있는 실무형","activity": "활동","relation": "교류협업","focus": "역량성장","style": "표현창작","clubs": ["UNSA", "AIESEC"]},
    "GTOC": {"name": "도전형 리더형","activity": "활동","relation": "교류협업","focus": "역량성장","style": "탐구실천","clubs": ["농성회", "라켓챌린지", "성균축구단","킹고야구반", "FC어우락", "SCOOP","MANIA", "STC", "제사포","아가리", "Ecos", "MIDAS","Bizball", "SIGMA FC", "클래스","천종", "글로벌"]}}

# 관심 분야 입력
print("\n" + "=" * 70)
print("📌 관심 분야 선택")
print("=" * 70)
print("1. 스포츠")
print("2. 학술")
print("3. 예술")
print("4. 봉사")
print("5. 친목")
print("6. 전체")

field_choice = input("\n👉 관심 분야 번호 입력: ")
field_map = {"1": "스포츠","2": "학술","3": "예술","4": "봉사","5": "친목","6": "전체"}
selected_field = field_map.get(field_choice, "전체")
print(f"\n선택한 분야: {selected_field}")
time.sleep(1)

# 성향 검사 시작
print("\n" + "=" * 70)
print("🧠 성향 분석 시작")
print("=" * 70)
for q in questions:
    print("\n" + q["question"])
    print("A. 매우 그렇다")
    print("B. 그렇다")
    print("C. 보통이다")
    print("D. 아니다")
    print("E. 매우 아니다")
    answer = input("👉 입력(A~E): ").upper()
    while answer not in ["A", "B", "C", "D", "E"]:
        answer = input("👉 다시 입력하세요(A~E): ").upper()
    if answer == "A":
        scores[q["positive"]] += 2
        scores[q["negative"]] -= 2
    elif answer == "B":
        scores[q["positive"]] += 1
        scores[q["negative"]] -= 1
    elif answer == "C":
        scores[q["positive"]] += 0
        scores[q["negative"]] += 0
    elif answer == "D":
        scores[q["positive"]] -= 1
        scores[q["negative"]] += 1
    elif answer == "E":
        scores[q["positive"]] -= 2
        scores[q["negative"]] += 2

# 최종 성향 결과 계산
result = ""
if scores["S"] >= scores["G"]:
    result += "S"
else:
    result += "G"
if scores["P"] >= scores["T"]:
    result += "P"
else:
    result += "T"
if scores["I"] >= scores["O"]:
    result += "I"
else:
    result += "O"
if scores["PL"] >= scores["C"]:
    result += "N"
else:
    result += "C"

# 결과 출력
print("\n" + "=" * 70)
print("🎯 성향 분석 결과")
print("=" * 70)
print(f"\n당신의 성향 유형은 [{result}] 입니다.")
if result in type_details:
    user_type = type_details[result]
    print(f"\n📌 유형 이름 : {user_type['name']}")
    print("\n📖 유형 특징")
    print(f"- 활동강도 : {user_type['activity']}")
    print(f"- 관계방식 : {user_type['relation']}")
    print(f"- 지향점 : {user_type['focus']}")
    print(f"- 활동성격 : {user_type['style']}")

# 분석
print("\n" + "=" * 70)
print("🔍 성향 코드 설명")
print("=" * 70)
print("S = Social (친목 중심)")
print("G = Goal (목표 중심)")
print("P = Personal (개인 중심)")
print("T = Team (팀 중심)")
print("I = Indoor (실내형)")
print("O = Outdoor (활동형)")
print("N = Normal / Planned (안정형)")
print("C = Challenging (도전형)")

print("\n" + "=" * 70)
print("📊 세부 성향 분석")
print("=" * 70)
if result[0] == "S":
    print("- 사람들과 어울리는 활동을 선호합니다.")
else:
    print("- 목표와 성과 중심 활동을 선호합니다.")
if result[1] == "P":
    print("- 혼자 몰입하는 활동에 강점이 있습니다.")
else:
    print("- 협업과 팀 활동에 강점이 있습니다.")
if result[2] == "I":
    print("- 실내 활동 환경을 선호합니다.")
else:
    print("- 활동적이고 야외 활동을 좋아합니다.")
if result[3] == "N":
    print("- 안정적이고 계획적인 활동을 선호합니다.")
else:
    print("- 새로운 도전과 변화를 좋아합니다.")

# 추천 동아리 출력
print("\n" + "=" * 70)
print("🏆 추천 동아리")
print("=" * 70)
if result in type_details:
    clubs = user_type["clubs"]
    for i, club in enumerate(clubs, start=1):
        print(f"\n[{i}] {club}")
        print("추천 이유:")
        if user_type["relation"] == "개인몰입":
            print("- 혼자 몰입하며 활동 가능")
        else:
            print("- 다양한 사람들과 협업 가능")

        if user_type["focus"] == "역량성장":
            print("- 자기계발 및 성장 가능")
        else:
            print("- 취미와 재미 중심 활동 가능")

        if user_type["style"] == "탐구실천":
            print("- 새로운 경험과 도전 가능")
        else:
            print("- 창의성과 표현 활동 가능")

# 세부 점수 출력
print("\n" + "=" * 70)
print("📈 세부 성향 점수")
print("=" * 70)

print(f"Social(S): {scores['S']}")
print(f"Goal(G): {scores['G']}")

print(f"Personal(P): {scores['P']}")
print(f"Team(T): {scores['T']}")

print(f"Indoor(I): {scores['I']}")
print(f"Outdoor(O): {scores['O']}")

print(f"Planned(N): {scores['PL']}")
print(f"Challenging(C): {scores['C']}")

# 전체 16유형 출력
print("\n" + "=" * 70)
print("📚 전체 16유형 요약")
print("=" * 70)
for code, info in type_details.items():
    print(f"\n[{code}] {info['name']}")
    print(f"활동강도 : {info['activity']}")
    print(f"관계방식 : {info['relation']}")
    print(f"지향점 : {info['focus']}")
    print(f"활동성격 : {info['style']}")
    print("대표 동아리 : ", end="")
    for club in info["clubs"][:3]:
        print(club, end=" / ")
    print()

# 종료
print("\n" + "=" * 70)
print("✅ 프로그램 종료")
print("감사합니다 😊")
print("=" * 70)
