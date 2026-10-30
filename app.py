import streamlit as st
from openai import OpenAI

# 페이지 설정 (다크모드 및 넓은 화면 레이아웃)
st.set_page_config(
    page_title="위드멤버 - 인스타 피드 원고 자동 생성기",
    page_icon="📸",
    layout="centered"
)

# 커스텀 CSS (블랙 & 골드 콘셉트의 세련된 UI 적용)
st.markdown("""
    <style>
    .main {
        background-color: #121212;
        color: #E0E0E0;
    }
    .stTextInput>div>div>input {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border: 1px solid #333333;
        border-radius: 8px;
    }
    .stSelectbox>div>div>select {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA771C 100%);
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #F3E5AB 0%, #D4AF37 100%);
    }
    .result-box {
        background-color: #1E1E1E;
        border-left: 4px solid #D4AF37;
        padding: 20px;
        border-radius: 4px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown("<h2 style='text-align: center; color: #D4AF37;'>📸 인스타그램 피드 원고 & 해시태그 생성기</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>매장명, 지역명, 업종만 입력하면 최상단 노출 최적화 원고가 완성됩니다.</p>", unsafe_allow_html=True)
st.markdown("---")

# API 키 입력 (사이드바 또는 메인 입력)
st.sidebar.header("🔑 설정")
api_key_input = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# 입력 폼
with st.form(key="instagram_form"):
    col1, col2 = st.columns(2)
    with col1:
        store_name = st.text_input("매장명", placeholder="예: 부평 파스타 맛집")
        region = st.text_input("지역명", placeholder="예: 인천 부평구")
    with col2:
        business_type = st.text_input("업종", placeholder="예: 이탈리안 레스토랑")
        target_audience = st.text_input("타겟층 (선택사항)", placeholder="예: 데이트 코스 찾는 연인들")

    submit_button = st.form_submit_button(label="✨ 최적화 원고 생성하기")

# 생성 로직
if submit_button:
    if not api_key_input:
        st.error("⚠️ OpenAI API 키를 사이드바에 입력해주세요.")
    elif not store_name or not region or not business_type:
        st.warning("⚠️ 매장명, 지역명, 업종은 필수 입력 항목입니다.")
    else:
        with st.spinner("🤖 인스타그램 알고리즘 최상단 노출 원고를 작성 중입니다..."):
            try:
                client = OpenAI(api_key=api_key_input)
                
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
                2. **본문 구성**: 매장의 매력 포인트, 방문해야 하는 이유, 이벤트나 서비스 특징을 가독성 있게 이모지와 함께 작성하세요. (지나치게 길지 않고 릴스나 피드에서 가독성이 좋게)
                3. **콜 투 액션 (CTA)**: 프로필 링크 클릭, 예약, 방문 유도를 위한 문구를 포함하세요.
                4. **해시태그**: 지역 키워드, 업종 키워드, 인스타 인기 태그를 조합하여 **최소 10개 이상** 엄선해 주세요.

                결과는 깔끔하게 Markdown 형식으로 출력해주세요.
                """

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "당신은 전문 소셜미디어 마케터입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )

                result_text = response.choices[0].message.content

                # 결과 출력
                st.success("🎉 원고 생성이 완료되었습니다!")
                st.markdown("### 📝 생성된 인스타그램 원고")
                st.markdown(f"<div class='result-box'>{result_text}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {e}")