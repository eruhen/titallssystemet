# Titallstrening – Streamlit
# Kjør med: streamlit run titallstrening_streamlit.py
import random
import streamlit as st
from decimal import Decimal, getcontext

getcontext().prec = 28

FACTORS = [Decimal(10), Decimal(100), Decimal(1000)]

def fmt(n: Decimal) -> str:
    s = format(n, 'f').rstrip('0').rstrip('.')
    s = s.replace('.', ',')
    return s if s else '0'

def parse_user(s: str) -> Decimal:
    s = s.strip().replace(' ', '').replace(',', '.')
    return Decimal(s)

def random_number(difficulty: str) -> Decimal:
    if difficulty == 'Hele tall':
        choices = [random.randint(1, 9999), random.choice([10,20,30,40,50,60,70,80,90,100,200,500,1000])]
        n = Decimal(random.choice(choices))
    elif difficulty == 'Desimaltall':
        whole = random.randint(0, 999)
        frac_places = random.choice([1,2,3])
        frac = random.randint(1, 9*(10**(frac_places-1)))
        n = Decimal(f"{whole}.{str(frac).zfill(frac_places)}")
    else:
        return random_number(random.choice(['Hele tall','Desimaltall']))
    if random.random() < 0.2:
        frac_places = random.choice([1,2,3])
        frac = random.randint(1, 9*(10**(frac_places-1)))
        n = Decimal(f"0.{str(frac).zfill(frac_places)}")
    return n

def new_task():
    a = random_number(st.session_state.difficulty)
    op = random.choice(st.session_state.ops)  # '*' or '/'
    f = random.choice(st.session_state.factors)
    if op == '*':
        correct = a * f
        text = f"{fmt(a)} · {fmt(f)} = ?"
    else:
        correct = a / f
        text = f"{fmt(a)} : {fmt(f)} = ?"
    st.session_state.task_text = text
    st.session_state.correct = correct
    st.session_state.user_answer = ""

st.set_page_config(page_title="Titallstrening", page_icon="🧮")
st.title("Titallstrening – 10, 100, 1000")

with st.sidebar:
    st.header("Innstillinger")
    ops = st.multiselect("Operasjon", ["Gange (·)","Dele (:)"], default=["Gange (·)","Dele (:)"])
    st.session_state.ops = ['*' if o.startswith("Gange") else '/' for o in ops] or ['*','/']
    factors = st.multiselect("Faktorer", ["10","100","1000"], default=["10","100","1000"])
    st.session_state.factors = [Decimal(f) for f in factors] or FACTORS
    st.session_state.difficulty = st.selectbox("Talltype", ["Hele tall","Desimaltall","Blandet"], index=2)
    qcount = st.number_input("Antall oppgaver i økt", min_value=1, max_value=200, value=20, step=1)
    if "remaining" not in st.session_state:
        st.session_state.remaining = qcount
    # Reset
    if st.button("Start/Nullstill økt"):
        st.session_state.correct_count = 0
        st.session_state.tried = 0
        st.session_state.remaining = qcount
        new_task()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Riktige", st.session_state.get("correct_count", 0))
with col2:
    st.metric("Forsøkt", st.session_state.get("tried", 0))
with col3:
    st.metric("Igjen", st.session_state.get("remaining", 0))

st.divider()

if "task_text" not in st.session_state:
    new_task()

st.subheader("Oppgave")
st.write(st.session_state.task_text)

ans = st.text_input("Svar (bruk komma eller punktum):", value=st.session_state.get("user_answer",""))
colA, colB = st.columns([1,1])
with colA:
    if st.button("Sjekk svar", type="primary", use_container_width=True):
        try:
            u = parse_user(ans)
            st.session_state.tried = st.session_state.get("tried", 0) + 1
            if u == st.session_state.correct:
                st.success("Riktig! ✅")
                st.session_state.correct_count = st.session_state.get("correct_count", 0) + 1
            else:
                st.error(f"Feil. Riktig svar: **{fmt(st.session_state.correct)}**")
            st.session_state.remaining = max(0, st.session_state.get("remaining", 0) - 1)
        except Exception as e:
            st.warning("Kunne ikke tolke svaret. Bruk tall med komma eller punktum.")
with colB:
    if st.button("Ny oppgave", use_container_width=True):
        new_task()

st.caption("Desimaltall vises med komma. Du kan skrive svar med komma eller punktum.")
