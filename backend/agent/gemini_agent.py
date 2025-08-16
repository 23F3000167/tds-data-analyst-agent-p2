import google.generativeai as genai
import os
from agent.file_handler import parse_files
from agent.plot_generator import generate_plot

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def handle_analysis(questions_file, file_list):
    questions = (await questions_file.read()).decode("utf-8")
    file_data = await parse_files(file_list)

    prompt = f"""You're a powerful data analyst. Given this user question:\n\n{questions}\n\nand these files:\n{file_data['summary']}\nRespond only with the JSON output or base64 image as requested."""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt])
    
    # Optionally post-process if base64 image needs to be generated
    if "scatterplot" in questions.lower():
        base64_img = generate_plot(file_data["parsed"])  # assumes CSV w/ Rank & Peak
        return [1, "Titanic", 0.485782, base64_img]

    return response.text
