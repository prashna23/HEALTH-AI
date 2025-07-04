# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ew07wdq3hnwtoK4-BAU5LwVsOZS0pQSA
"""

# Install dependencies
!pip install transformers huggingface_hub gradio accelerate --quiet

# Import libraries
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login
import gradio as gr

# Login to Hugging Face (don't share your token publicly)
login("replace with your own token")  # Replace with your own token

# Load IBM Granite model
model_id = "ibm-granite/granite-3.3-2b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Function 1: Predict disease from symptoms
def predict_disease(symptoms):
    prompt = f"A patient reports: {symptoms}. What is the possible illness and recommendation?"
    result = pipe(prompt, max_new_tokens=300)[0]["generated_text"]
    return result

# Function 2: Suggest home remedies for a disease
def home_remedy(disease_name):
    prompt = f"What are some natural home remedies for {disease_name}?"
    result = pipe(prompt, max_new_tokens=300)[0]["generated_text"]
    return result

# Create Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 HealthAI - Healthcare Assistant")

    with gr.Tab("1️⃣ Symptoms Identifier"):
        symptom_input = gr.Textbox(label="Enter symptoms", placeholder="e.g. I have cough, cold, and fever")
        symptom_output = gr.Textbox(label="HealthAI Suggestion")
        symptom_btn = gr.Button("Analyze")
        symptom_btn.click(fn=predict_disease, inputs=symptom_input, outputs=symptom_output)

    with gr.Tab("2️⃣ Home Remedies"):
        disease_input = gr.Textbox(label="Enter disease name", placeholder="e.g. cold, diabetes")
        remedy_output = gr.Textbox(label="Suggested Home Remedies")
        remedy_btn = gr.Button("Get Remedies")
        remedy_btn.click(fn=home_remedy, inputs=disease_input, outputs=remedy_output)

# Launch the app
demo.launch()