import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="위드멤버 - 인스타 피드 원고 자동 생성기",
    page_icon="📸",
    layout="centered"
)

# 깔끔하고 세련된 UI 스타일 적용 (입력창 및 가독성 오류 해결)
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #D4AF37;
        border-radius: 8px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA771C 100%);
        color: #FFFFFF;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #F3E5AB 0%, #D4AF37 100%);
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown("<h2 style='text-align: center; color: #AA771C;'>📸 인스타그램 피드 원고 & 해시태그 생성기</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666666;'>매장명, 지역명, 업종만 입력하면 최상단 노출 최적화 원고가 완성됩니다.</p>", unsafe_allow_html=True)
st.markdown("---")

# 안전하게 Streamlit Secrets에서 API 키 가져오기
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    OPENAI_API_KEY = ""

# 입력 폼
with st.form(key="instagram_form"):
    col1, col2 = st.columns(2)
    with col1:
        store_name = st.text_input("매장명", placeholder="예: 온도네일스튜디오")
        region = st.text_input("지역명", placeholder="예: 세종 반곡동")
    with col2:
        business_type = st.text_input("업종", placeholder="예: 네일아트")
        target_audience = st.text_input("타겟층 (선택사항)", placeholder="예: 트렌디한 2030 여성")

    submit_button = st.form_submit_button(label="✨ 최적화 원고 생성하기")

# 생성 로직
if submit_button:
    if not OPENAI_API_KEY:
        st.error("⚠️ Streamlit Cloud 설정(Secrets)에 OpenAI API 키가 등록되지 않았습니다.")
    elif not store_name or not region or not business_type:
        st.warning("⚠️ 매장명, 지역명, 업종은 필수 입력 항목입니다.")
    else:
        with st.spinner("🤖 인스타그램 알고리즘 최상단 노출 원고를 작성 중입니다..."):
            try:
                client = OpenAI(api_key=OPENAI_API_KEY)
                
                prompt = f"""
                당신은 인스타그램 SEO 전문가이자 소상공인 마케팅 전문가입니다.
                아래 정보를 바탕으로 인스타그램 피드 게시물에 사용할 최상단 노출 최적화 원고와 해시태그를 작성해주세요.

                [입력 정보]
                - 매장명: {store_name}
                - 지역명: {region}
                - 업종: {business_type}
                - 타겟층: {target_audience if target_audience else '일반 방문객'}

                [작성 가이드라인]
                1. **첫 문장 (후킹 문구)**: 사용자가 피드를 내리다가 멈추도록 시선을 사로잡는 강력한 후킹 문구를 최상단에 배치하세요. (지역명 + 업종 키워드 자연스럽게 포함)
                2. **본문 구성**: 매장의 매력 포인트, 방문해야 하는 이유, 이벤트나 서비스 특징을 가독성 있게 이모지와 함께 작성하세요.
                3. **콜 투 액션 (CTA)**: 프로필 링크 클릭, 예약, 방문 유도를 위한 문구를 포함하세요.
                4. **해시태그**: 지역 키워드, 업종 키워드, 인스타 인기 태그를 조합하여 **최소 10개 이상** 엄선해 주세요.

                ※ 주의: 결과물에 ```markdown 같은 코드 블록 기호는 절대 넣지 말고, 순수 마케팅 텍스트만 출력해주세요.
                """

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "당신은 전문 소셜미디어 마케터입니다. 코드 블록 기호 없이 깔끔하게 텍스트를 출력하세요."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )

                result_text = response.choices[0].message.content
                
                # 혹시 포함된 마크다운 백틱 제거
                result_text = result_text.replace("```markdown", "").replace("```", "").strip()

                # 결과 출력 (Streamlit 기본 컨테이너를 사용하여 글씨 깨짐 방지)
                st.success("🎉 원고 생성이 완료되었습니다!")
                st.markdown("### 📝 생성된 인스타그램 원고")
                st.info(result_text)

            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {e}")
