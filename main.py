
# 개인 성향 분석 기반 개인 맞춤형 교내활동 추천 시스템
# 문제해결과컴퓨팅사고 11조 [말차중조]

import csv
import time
from pathlib import Path


# ============================================================
# 1. 동아리 데이터 읽기
# ============================================================

clubs_file = Path(__file__).with_name("clubs.csv")

if not clubs_file.exists():
    print("오류: clubs.csv 파일을 찾을 수 없습니다.")
    print("main.py와 clubs.csv를 같은 폴더에 넣어주세요.")
    raise SystemExit

with open(clubs_file, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    clubs_data = list(reader)

required_columns = [
    "동아리명", "세부 소속", "분야", "활성여부",
    "활동강도", "관계방식", "지향점", "활동성격"
]

if not reader.fieldnames or not all(
    column in reader.fieldnames for column in required_columns
):
    print("오류: clubs.csv의 열 이름을 확인해주세요.")
    print("엑셀에서 내보낸 CSV 파일이 올바른지 확인해주세요.")
    raise SystemExit

print(f"동아리 데이터 로드 완료: {len(clubs_data)}개")


# ============================================================
# 2. 관심 분야별 동아리 필터링
# ============================================================

def matches_field(club, selected_field):
    if selected_field == "전체":
        return True

    category = club.get("세부 소속", "")
    field = club.get("분야", "")
    text = category + " " + field

    keywords_by_field = {
        "스포츠": [
            "스포츠동아리", "농구", "배드민턴", "축구", "야구",
            "태권도", "택견", "무술", "스노보드", "테니스",
            "검도", "e스포츠", "댄스스포츠", "헬스"
        ],
        "학술": [
            "학술동아리", "인문사회동아리", "프로그래밍",
            "웹 프로그래밍", "토론", "영어회화", "시사",
            "경영/경제", "천문학", "국제리더십", "방송 청취",
            "글쓰기", "문학", "영화 연구"
        ],
        "예술": [
            "연행예술동아리", "평면예술동아리",
            "밴드", "댄스", "연극", "국악", "합창",
            "음악", "오케스트라", "만화", "미술",
            "영화", "글쓰기", "서예", "사진", "마술",
            "순수미술", "동양화", "음악 창작"
        ],
        "봉사": [
            "봉사동아리", "봉사", "환경", "장애인권"
        ],
        "친목": [
            "취미교양동아리", "종교동아리",
            "커피", "차 및 카페", "친목"
        ]
    }

    keywords = keywords_by_field.get(selected_field)

    if keywords is None:
        return True

    return any(keyword in text for keyword in keywords)


# ============================================================
# 3. 성향 매칭 점수 계산
# 현재 데이터에서 명확하게 대응되는 P/T 차원만 사용
# ============================================================

def calculate_match_score(club, result):
    relationship = club.get("관계방식", "")

    if result[1] == "P" and relationship == "개인몰입":
        return 1

    if result[1] == "T" and relationship == "교류협업":
        return 1

    return 0


# ============================================================
# 4. 추천 이유 생성
# ============================================================

def generate_match_reason(club, result, selected_field):
    reasons = []

    relationship = club.get("관계방식", "")

    if result[1] == "P" and relationship == "개인몰입":
        reasons.append(
            "개인적으로 집중하며 활동하는 성향과 잘 맞습니다."
        )
    elif result[1] == "T" and relationship == "교류협업":
        reasons.append(
            "팀원들과 교류하고 협력하는 성향과 잘 맞습니다."
        )
    else:
        reasons.append(
            "관계 방식이 성향과 완전히 일치하지는 않지만, "
            "선택한 관심 분야를 바탕으로 추천합니다."
        )

    field = club.get("분야", "").strip()

    if selected_field != "전체":
        reasons.append(
            f"선택한 관심 분야는 {selected_field}이며, "
            f"이 동아리의 주요 활동 분야는 {field}입니다."
        )
    else:
        reasons.append(
            f"주요 활동 분야는 {field}입니다."
        )

    return " ".join(reasons)


# ============================================================
# 5. 시작 화면
# ============================================================

print("=" * 70)
print("🎓 개인 맞춤형 교내활동 추천 시스템")
print("🎓 Personalized Campus Activity Recommendation System")
print("=" * 70)

print("\n안녕하세요!")
print("간단한 성향 검사를 통해 당신에게 맞는 교내활동을 추천해드립니다.")
print("자신에게 가장 맞는 선택지를 골라주세요.")

input("👉 시작하려면 Enter 키를 누르세요...")


# ============================================================
# 6. 성향 검사 질문
# ============================================================

scores = {
    "S": 0, "G": 0,
    "P": 0, "T": 0,
    "I": 0, "O": 0,
    "PL": 0, "C": 0
}

questions = [
    {
        "question": "1. 새로운 사람들과 친해질 수 있는 활동이 더 좋다.",
        "positive": "S", "negative": "G"
    },
    {
        "question": "2. 활동을 선택할 때 재미보다 결과와 성과가 중요하다.",
        "positive": "G", "negative": "S"
    },
    {
        "question": "3. 사람들과 어울리는 활동이 혼자 하는 활동보다 좋다.",
        "positive": "S", "negative": "G"
    },
    {
        "question": "4. 혼자 집중해서 하는 활동이 편하다.",
        "positive": "P", "negative": "T"
    },
    {
        "question": "5. 팀 프로젝트나 단체 활동이 재미있다.",
        "positive": "T", "negative": "P"
    },
    {
        "question": "6. 다른 사람들과 역할을 나누는 활동이 좋다.",
        "positive": "T", "negative": "P"
    },
    {
        "question": "7. 실내 활동이 더 편하다.",
        "positive": "I", "negative": "O"
    },
    {
        "question": "8. 몸을 움직이는 활동을 좋아한다.",
        "positive": "O", "negative": "I"
    },
    {
        "question": "9. 조용한 공간에서 활동하는 것이 좋다.",
        "positive": "I", "negative": "O"
    },
    {
        "question": "10. 계획이 잘 정리된 활동이 좋다.",
        "positive": "PL", "negative": "C"
    },
    {
        "question": "11. 새로운 도전을 하는 활동이 재미있다.",
        "positive": "C", "negative": "PL"
    },
    {
        "question": "12. 익숙한 방식보다 새로운 경험을 선호한다.",
        "positive": "C", "negative": "PL"
    }
]


# ============================================================
# 7. 16가지 성향 유형 데이터
# ============================================================

type_names = {
    "SPIN": "조용한 자기계발형",
    "SPIC": "몰입형 탐구가",
    "SPON": "독립적 실천가",
    "SPOC": "자유로운 개척자",
    "STIN": "따뜻한 실내교류형",
    "STIC": "창의적 협업가",
    "STON": "꾸준한 공동체형",
    "STOC": "활기찬 팀플레이어",
    "GPIN": "계획적 성장형",
    "GPIC": "집중형 문제해결가",
    "GPON": "성실한 실행가",
    "GPOC": "독립형 도전자",
    "GTIN": "전략적 협력가",
    "GTIC": "프로젝트 추진형",
    "GTON": "책임감 있는 실무형",
    "GTOC": "도전형 리더형"
}

type_details = {}

for code, name in type_names.items():
    type_details[code] = {
        "name": name,

        # 첫 번째 문자: 관심 지향점
        "focus": "취미향유" if code[0] == "S" else "역량성장",

        # 두 번째 문자: 관계 방식
        "relation": "개인몰입" if code[1] == "P" else "교류협업",

        # 세 번째 문자: 활동 환경 및 강도
        "activity": "정적" if code[2] == "I" else "활동",

        # 네 번째 문자: 활동 성격
        "style": "표현창작" if code[3] == "N" else "탐구실천"
    }


# ============================================================
# 8. 관심 분야 선택
# ============================================================

print("\n" + "=" * 70)
print("📌 관심 분야 선택")
print("=" * 70)
print("1. 스포츠")
print("2. 학술")
print("3. 예술")
print("4. 봉사")
print("5. 친목")
print("6. 전체")

field_map = {
    "1": "스포츠",
    "2": "학술",
    "3": "예술",
    "4": "봉사",
    "5": "친목",
    "6": "전체"
}

field_choice = input("\n👉 관심 분야 번호 입력: ").strip()

while field_choice not in field_map:
    field_choice = input(
        "👉 다시 입력하세요(1~6): "
    ).strip()

selected_field = field_map[field_choice]
print(f"\n선택한 분야: {selected_field}")
time.sleep(1)


# ============================================================
# 9. 성향 검사 진행
# ============================================================

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

    answer = input("👉 입력(A~E): ").strip().upper()

    while answer not in ["A", "B", "C", "D", "E"]:
        answer = input("👉 다시 입력하세요(A~E): ").strip().upper()

    if answer == "A":
        scores[q["positive"]] += 2
        scores[q["negative"]] -= 2
    elif answer == "B":
        scores[q["positive"]] += 1
        scores[q["negative"]] -= 1
    elif answer == "C":
        pass
    elif answer == "D":
        scores[q["positive"]] -= 1
        scores[q["negative"]] += 1
    elif answer == "E":
        scores[q["positive"]] -= 2
        scores[q["negative"]] += 2


# ============================================================
# 10. 최종 성향 유형 계산
# ============================================================

result = ""

result += "S" if scores["S"] >= scores["G"] else "G"
result += "P" if scores["P"] >= scores["T"] else "T"
result += "I" if scores["I"] >= scores["O"] else "O"
result += "N" if scores["PL"] >= scores["C"] else "C"

user_type = type_details[result]


# ============================================================
# 11. 성향 분석 결과 출력
# ============================================================

print("\n" + "=" * 70)
print("🎯 성향 분석 결과")
print("=" * 70)
print(f"\n당신의 성향 유형은 [{result}] 입니다.")
print(f"\n📌 유형 이름 : {user_type['name']}")
print("\n📖 유형 특징")

if result[0] == "S":
    print("- 관계와 교류를 중요하게 생각합니다.")
else:
    print("- 목표 달성과 성과를 중요하게 생각합니다.")

if result[1] == "P":
    print("- 혼자 집중하며 활동하는 것을 선호합니다.")
else:
    print("- 팀원들과 협력하며 활동하는 것을 선호합니다.")

if result[2] == "I":
    print("- 실내에서 집중할 수 있는 활동을 선호합니다.")
else:
    print("- 몸을 움직이며 활동적인 경험을 선호합니다.")

if result[3] == "N":
    print("- 계획적이고 안정적인 활동을 선호합니다.")
else:
    print("- 새로운 경험과 도전적인 활동을 선호합니다.")


# ============================================================
# 12. 성향 코드 설명
# ============================================================

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


# ============================================================
# 13. 세부 성향 분석
# ============================================================

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


# ============================================================
# 14. 동아리 추천
# ============================================================

print("\n" + "=" * 70)
print("🏆 추천 동아리")
print("=" * 70)
print(f"선택한 관심 분야: {selected_field}")
print(f"성향 유형: {result} - {user_type['name']}")

filtered_clubs = [
    club for club in clubs_data
    if club.get("활성여부", "").strip() == "활성"
    and matches_field(club, selected_field)
]

for club in filtered_clubs:
    club["매칭점수"] = calculate_match_score(club, result)

filtered_clubs.sort(
    key=lambda club: club["매칭점수"],
    reverse=True
)

if not filtered_clubs:
    print("\n선택한 분야에 해당하는 활성 동아리가 없습니다.")
    print("관심 분야를 '전체'로 선택해 다시 확인해 보세요.")
else:
    print(f"\n검색된 활성 동아리: {len(filtered_clubs)}개")
    print("※ 매칭 점수는 현재 관계 방식(P/T) 기준입니다.")

    for i, club in enumerate(filtered_clubs, start=1):
        print(f"\n[{i}] {club.get('동아리명', '이름 없음')}")
        print(f"- 성향 매칭 점수: {club['매칭점수']}/1점")
        print(
            "- 추천 이유: "
            + generate_match_reason(club, result, selected_field)
        )
        print(f"- 소속: {club.get('세부 소속', '')}")
        print(f"- 활동 분야: {club.get('분야', '')}")
        print(f"- 활동 강도: {club.get('활동강도', '')}")
        print(f"- 관계 방식: {club.get('관계방식', '')}")
        print(f"- 지향점: {club.get('지향점', '')}")
        print(f"- 활동 성격: {club.get('활동성격', '')}")


# ============================================================
# 15. 세부 성향 점수
# ============================================================

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


# ============================================================
# 16. 전체 16유형 요약
# ============================================================

print("\n" + "=" * 70)
print("📚 전체 16유형 요약")
print("=" * 70)

for code, info in type_details.items():
    matching_clubs = [
        club.get("동아리명", "").strip()
        for club in clubs_data
        if club.get("활성여부", "").strip() == "활성"
        and club.get("활동강도", "").strip() == info["activity"]
        and club.get("관계방식", "").strip() == info["relation"]
        and club.get("지향점", "").strip() == info["focus"]
        and club.get("활동성격", "").strip() == info["style"]
    ]

    print(f"\n[{code}] {info['name']}")
    print(f"활동강도 : {info['activity']}")
    print(f"관계방식 : {info['relation']}")
    print(f"지향점 : {info['focus']}")
    print(f"활동성격 : {info['style']}")

    if matching_clubs:
        print("대표 동아리 : " + " / ".join(matching_clubs[:3]))
    else:
        print("대표 동아리 : 현재 CSV에 네 가지 속성이 모두 일치하는 동아리가 없습니다.")

# ============================================================
# 17. 종료
# ============================================================

print("\n" + "=" * 70)
print("✅ 프로그램 종료")
print("감사합니다 😊")
print("=" * 70)
print("=" * 70)
