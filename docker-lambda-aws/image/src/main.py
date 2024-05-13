import os
import logging
import openai
import gradio as gr
import pickle
from datetime import datetime
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from mangum import Mangum

from curriebot import get_agent_executor

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

intro_message = """**Meet Curriebot, your personal career companion! 
Curriebot is here to help you navigate through my professional journey/"Curri"culum vitae, 
answering all your questions about my resume or personal projects. 
Whether you're curious about the details of my project or want insights into my skill set, 
Curriebot is ready to chat. Friendly and knowledgeable, 
Curriebot makes learning about my professional life both easy and enjoyable. 
Let's get the conversation started!**"""

assitant_initial_message = """Hi, my name is Curriebot. Thank you for stopping by. 
I'm here to assist you with any questions about Patrick's resume or projects. How can I help you today?"""

css = """
#image-container {
    display: flex;
    justify-content: center;  # Centers the child horizontally
    width: 100%;  # Ensures the container takes full width
}
img {
    max-width: 100%;  # Ensures the image scales down if it's too wide
}
"""

CUSTOM_PATH = "/"

app = FastAPI()
handler = Mangum(app)

def clear_memory_agent():
    global agent_executor
    agent_executor = get_agent_executor()

def start_chat(api_key):
    global agent_executor
    try:
        os.environ["OPENAI_API_KEY"] = api_key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
        print(llm.invoke("hi"))
        gr.Info("openai api key authentication successful!")
        
        agent_executor = get_agent_executor()
        return {
            start_col: gr.Column(visible=False),
            chat_col : gr.Column(visible=True),
        }
    except Exception as e:
        raise gr.Error("Please double check your openai api key!")

def respond(message, chat_history):
        result = agent_executor.invoke({"input": message})
        chat_history.append((result["input"], result["output"]))
        
        return "", chat_history

with gr.Blocks(
    theme=gr.themes.Default(
        font=gr.themes.GoogleFont("Source Sans Pro"),
        font_mono=gr.themes.GoogleFont("Source Sans Pro"),
    ),
    css=css
) as demo:
    agent_executor = None
    
    with gr.Row():
        with gr.Column():
            gr.Image("banner_resize.png", elem_id="image-container")
        
    gr.Markdown(intro_message)
    gr.Markdown("Before we begin. Please enter your openai api key. Don't worry I will not save it for personal use")
    
    with gr.Row(visible=True) as start_row:
        with gr.Column(visible=True) as start_col:
            api_key = gr.Textbox(label="Enter openai api key here", type="password")
            start_button = gr.Button("Start Chat!")

    with gr.Row(visible=True) as chat_row:
        with gr.Column(visible=False) as chat_col:
            chatbot = gr.Chatbot([(None, assitant_initial_message)]).style(height=500)
            msg = gr.Textbox()
            clear = gr.ClearButton([msg, chatbot])
    
    start_button.click(
        fn=start_chat, inputs=[api_key], outputs=[start_col, chat_col]
    )

    api_key.submit(
        fn=start_chat, inputs=[api_key], outputs=[start_col, chat_col]
    )

    clear.click(fn=clear_memory_agent)
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])


app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)
