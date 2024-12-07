import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

# Загружаем модель и токенайзер
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Функция для генерации ответа от модели
def ask(prompt: str) -> str:
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    gen_tokens = model.generate(
        input_ids,
        do_sample=True,
        temperature=0.5,
        max_length=100,
    )
    gen_text = tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)[0]
    return gen_text

# Интерфейс Streamlit
st.title("GPT-2 Chatbot with Streamlit")
st.write("Введите сообщение для взаимодействия с моделью:")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Как я могу вам помочь?"}
    ]

# Отображаем предыдущие сообщения
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле для ввода текста
if question := st.chat_input("Ваше сообщение"):
    st.session_state.messages.append({"role": "human", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Генерируем ответ от модели
    response = ask(question)
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
