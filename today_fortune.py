"""띠별 오늘의 운세 Streamlit 앱."""

from datetime import datetime
import hashlib
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx


ZODIAC = ["쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양", "원숭이", "닭", "개", "돼지"]

FORTUNES = [
    "작은 계획을 실천하기 좋은 날입니다. 미뤄 둔 일 하나부터 시작해 보세요.",
    "주변 사람과 나누는 대화에서 좋은 생각을 얻을 수 있습니다.",
    "속도를 조금 늦추면 놓쳤던 기회가 보일 수 있습니다.",
    "새로운 일에 도전해 보세요. 첫걸음이 뜻밖의 즐거움을 줄 수 있습니다.",
    "차분하게 우선순위를 정하면 하루가 한결 수월해집니다.",
    "평소의 노력이 빛을 볼 수 있는 날입니다. 자신감을 가져 보세요.",
    "가까운 사람에게 고마움을 전하면 기분 좋은 일이 생길 수 있습니다.",
    "익숙한 방법에 작은 변화를 주면 좋은 결과를 얻을 수 있습니다.",
    "오늘은 쉬어 가는 시간도 중요합니다. 몸과 마음을 돌봐 주세요.",
    "중요한 결정은 정보를 한 번 더 확인한 뒤 내리면 좋겠습니다.",
    "우연한 만남이나 소식이 하루에 활기를 더해 줄 수 있습니다.",
    "해야 할 일을 하나씩 마치면 만족스러운 하루가 될 것입니다.",
]

ADVICE = [
    "행운의 색: 초록색", "행운의 색: 파란색", "행운의 색: 노란색",
    "행운의 색: 주황색", "행운의 색: 보라색", "행운의 색: 하늘색",
]


def daily_pick(date_text, zodiac, choices, salt):
    """날짜와 띠가 같으면 언제나 같은 결과를 고른다."""
    value = f"{date_text}|{zodiac}|{salt}".encode("utf-8")
    index = int(hashlib.sha256(value).hexdigest(), 16) % len(choices)
    return choices[index]


def main():
    st.set_page_config(page_title="오늘의 띠별 운세", page_icon="🍀", layout="centered")
    today = datetime.now(ZoneInfo("Asia/Seoul")).date()
    date_text = today.isoformat()

    st.title("🍀 오늘의 띠별 운세")
    st.caption(f"{today:%Y년 %m월 %d일} · 재미로 보는 운세")

    zodiac = st.selectbox("띠를 선택하세요", ZODIAC, index=None, placeholder="띠 선택")
    if zodiac:
        fortune = daily_pick(date_text, zodiac, FORTUNES, "fortune")
        color = daily_pick(date_text, zodiac, ADVICE, "color")
        st.subheader(f"{zodiac}띠의 오늘의 운세")
        st.success(fortune)
        st.info(color)
    else:
        st.write("띠를 선택하면 오늘의 운세가 나타납니다.")


if __name__ == "__main__":
    if get_script_run_ctx() is None:
        # PyCharm의 일반 Python 실행 버튼으로 시작한 경우 Streamlit 서버를 띄운다.
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run",
                str(Path(__file__).resolve()), "--server.address", "127.0.0.1"
            ], check=False)
        except KeyboardInterrupt:
            pass
    else:
        main()
