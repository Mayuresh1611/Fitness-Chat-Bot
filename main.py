import google.generativeai as genai 
import google.generativeai.generative_models as gen
import streamlit as st
import os

class BlockedPromptException(Exception):
    pass


class StopCandidateException(Exception):
    pass


try:
    API = os.environ["API_KEY"]
except KeyError:
    print("Error: API_KEY not found in environment variables.")
    API = None  # Set a default value or handle the missing API key case appropriately

if API:
    print(API)
    genai.configure(api_key=API)
genai.configure(api_key=API)

# Set up the model
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 1,
}

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config)


chat_bg = [
  {
    "role": "user",
    "parts": ["Your name will be fitness-guru and your work is to give advice related to fitness, diet, and sports. You will not answer any queries or give information about any other stuff that is not related to fitness, diet, and sports. Keep anwsers short and simple. Remember their age and talk accordingly with respect to their age. Be more freidnly with teens and kids and be more direct and precise with adults. You will answer only fitness, diet and sports-related querries. You can say \"My domain is fitness and I cannot answer other questions.\". This way you can avoid user's questions that are not related to your field. Do not give plans, information, dietary plans, or workout tips until they give you information such as age, weight, height, medical conditions, desired plans, and goals related to fitness only. Every time user asks queries without providing their information, without answering questions you ask for information. Every time you form a plan for user do include this information, build suitable plan for the user based on the information provided by user. User safety is first priority thus do not give advice until you have information of user and use that information to curate better plans for user. Always Introduce yourself first" ]
  },
  {
    "role": "model",
    "parts": ["I am fitness-guru, and I am here to help you with your fitness, diet, and sports-related questions. To ensure your safety and well-being, I need the following information from you before I can provide you with any specific advice:\n\n* **Age** Your age is important because it can affect your fitness level, metabolism, and risk of certain health conditions\n* **Weight** Your weight is important because it can affect your fitness level and risk of certain health conditions.\n* **Height** For calculating BMI \n* **Any medical conditions you have** so that I can make sure that the plan I create for you is safe and does not aggravate your condition.\n* **Your desired plans and goals related to health** is important so that I can create a plan that is tailored to your specific needs and goals.\nThis information is essential for me to create a safe and effective plan for you.\nPlease provide me with this information so that I can get started on creating a plan for you."]
  },
]
convo = model.start_chat(history=chat_bg)

if "messages" not in st.session_state:
    st.session_state.messages  = [chat_bg[1]]

# Streamlit app
st.title("Fitness Chatbot")

for message in st.session_state.messages:  
    if message['role'] == "model":
        st.chat_message("model").markdown(message['parts'][0] ,  unsafe_allow_html=True )
    else:
        st.chat_message("user").markdown(message['parts'][0])



# Display initial model message
# st.markdown(chat_bg[1]['parts'][0])
        

if prompt := st.chat_input("user: "):
    
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user" , "parts":[prompt]})

    try:
        convo.send_message(prompt)
        response = convo.last.text
    except Exception as e:
        if str(type(e).__name__) == "BlockedPromptException":
            response = "<span style='color:red'>I cannot provide you answer as it is flagged as harmful</span>" 
        else:    
            response = "Sorry! some error occured. Can you please repeat that?"
    st.chat_message("model").markdown(response , unsafe_allow_html=True)
    st.session_state.messages.append({"role":"model" , "parts":[response]})


