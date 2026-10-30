import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="위드멤버 - 인스타 피드 원고 자동 생성기",
    page_icon="📸",
    layout="centered"
)

# 세련된 UI 스타일 및 결과 카드 박스 CSS 적용
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
    /* 인스타 피드 스타일을 살린 고급스러운 카드 박스 */
    .insta-card {
        background-color: #FAFAFA;
        border: 1px solid #E0E0E0;
        border-left: 4px solid #D4AF37;
        padding: 24px;
        border-radius: 12px;
        color: #262626;
        font-size: 15px;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-all;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 15px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown("<h2 style='text-align: center; color: #AA771C;'>📸 인스타그램 피드 원고 & 해시태그 생성기</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666666;'>매장명, 지역명, 키워드만 입력하면 최상단 노출 최적화 방문 후기 원고가 완성됩니다.</p>", unsafe_allow_html=True)
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
        store_name = st.text_input("매장명", placeholder="예: 캐치업왁싱 여의도점")
        region = st.text_input("지역명", placeholder="예: 서울 영등포구 여의도동")
    with col2:
        # 요청하신 대로 '업종'을 '키워드'로 변경
        business_type = st.text_input("키워드", placeholder="예: 당산왁싱, 영등포왁싱, 여의도왁싱")
        target_audience = st.text_input("타겟층 (선택사항)", placeholder="예: 데이트 코스 찾는 연인들")

    submit_button = st.form_submit_button(label="✨ 최적화 후기 원고 생성하기")

# 생성 로직
if submit_button:
    if not OPENAI_API_KEY:
        st.error("⚠️ Streamlit Cloud 설정(Secrets)에 OpenAI API 키가 등록되지 않았습니다.")
    elif not store_name or not region or not business_type:
        st.warning("⚠️ 매장명, 지역명, 키워드는 필수 입력 항목입니다.")
    else:
        with st.spinner("🤖 인스타그램 알고리즘 최상단 노출 방문 후기 원고를 작성 중입니다..."):
            try:
                client = OpenAI(api_key=OPENAI_API_KEY)
                
                prompt = f"""
                당신은 인스타그램 체험단 및 인플루언서 마케팅 전문가입니다.
                아래 정보를 바탕으로 인스타그램 피드에 업로드할 **'실제 방문 후기(내돈내산 또는 체험단 솔직 후기)'** 콘셉트의 최상단 노출 최적화 원고를 작성해주세요.

                [입력 정보]
                - 매장명: {store_name}
                - 지역명: {region}
                - 키워드: {business_type}
                - 타겟층: {target_audience if target_audience else '일반 방문객'}

                [작성 가이드라인 및 형식 지정]
                반드시 아래의 양식과 톤앤매너에 맞춰서 작성해주세요. 마크다운 코드 블록(``` 등)은 결과에 절대 포함하지 마세요.

                1. **관점**: 매장 입장이 아니라, **"직접 방문해보고 반해서 남기는 솔직한 후기"** 톤으로 작성할 것 ("~에 다녀왔어요!", "~추천해요!" 등 소비자 시점 사용)
                2. **첫 문장 (후킹 문구)**: 피드를 내리다 멈추게 만드는 감탄사나 궁금증을 유발하는 문구 + 입력된 키워드와 지역명을 자연스럽게 녹여낼 것
                3. **본문 구성**: 매장 분위기, 메뉴나 서비스의 맛/품질과 장점, 친절함 등을 생생한 이모지와 함께 가독성 있게 작성
                4. **위치 안내**: 📍 위치: {region} ({store_name})
                5. **해시태그**: #️⃣ [추천 해시태그 (10개)] 형태로 하단에 나열 (입력된 키워드, 지역명, 인스타 인기 태그 조합)

                순수 텍스트만 출력하세요.
                """

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "당신은 전문 SNS 인플루언서입니다. 매장 홍보글이 아닌 리얼한 방문 후기 톤으로 텍스트만 출력하세요."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )

                result_text = response.choices[0].message.content
                
                # 혹시 포함된 마크다운 백틱 제거
                result_text = result_text.replace("```markdown", "").replace("```", "").strip()

                # 결과 출력 (예쁜 카드 박스 형태로 렌더링)
                st.success("🎉 방문 후기 원고 생성이 완료되었습니다!")
                st.markdown("### 📝 생성된 인스타그램 후기 원고")
                
                # HTML div 박스를 이용해 깔끔하게 출력
                st.markdown(f'<div class="insta-card">{result_text}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {e}")
