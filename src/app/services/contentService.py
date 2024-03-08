# Load a pdf with langchain PyPDFLoader
from langchain.document_loaders import PyPDFLoader
import openai
import matplotlib.pyplot as plt
import seaborn as sns
import asyncio

from audioService import extract_transcript
from scrapeService import ascrape_playwright
from openai import OpenAI
import os
sns.set()
os.environ['OPENAI_API_KEY'] = "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"


def create_qa(context, num=5,perspective = 'data science'):
    # Defining the context for creating the Q&As
    # Prompt to create the questions
    if perspective == 'data science':

        q_a_prompt = (
            f"Imagine you're revisiting the core concepts from a text you read a few days ago. "
            f"Please generate questions that explore the key ideas discussed in the text. "
            f"Avoid referencing specific details from the text itself, but focus on the broader concepts and theories. "
            f"Consider topics related to data science, machine learning, mathematics, and related ones present in the context: {context}. "
            f"Create a set of {num} questions with answers that help reinforce your understanding of the main themes and "
            f"principles covered in the  given context : {context}. "
            f"Separate each block composed of a question and an answer with 3 dashes '---' like this: Q: <question>\n A: <answer> "
            f"--- Q: <question>\n A: <answer>, etc. Let's think step by step. Q:"
        )

    else:
        q_a_prompt = (f"Imagine you are summarizing the main topic and crafting questions based on the passage below:"
            f"\n\n{context}\n\n"
            f"Please create a set of {num} questions along with their respective answers. "
            f"Each question should specifically address key points from the passage. "
            f"Separate each question and answer pair with three dashes '---' as follows:\n"
            f"Q: <question>\nA: <answer>\n---\nQ: <question>\nA: <answer>\n---\n"
            f"Feel free to provide detailed and insightful questions that reflect the essence of the passage. "
            f"Let's begin. Q:")


    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful research and\
            programming assistant"},
                  {"role": "user", "content": q_a_prompt}]
    )
    return response.choices[0].message.content


def run_qa_session(num, context):
    overall_scores = []
    qa_dict = {}

    q_a = create_qa(context, num)
    # Create a list of questions and answers from the output string by leveraging the '---' separator
    q_a_list = q_a.split('---')
    scores_list = []

    for qa in q_a_list:
        question = qa.split("A:")[0].replace("Q:", "")
        answer = qa.split("A:")[1].replace("Q:", "")
        user_answer = input(question)
        qa_dict[f"Round 1"] = {"question": question, "answer": answer, "user_answer": user_answer}
        print("CORRECT ANSWER: ", answer)
        print("***")
        score_feedback = evaluate_answer(question, answer, user_answer)
        print("score feedback",score_feedback)
        score = score_feedback.split("SCORE:")[1].split("FEEDBACK:")[0]
        print("*****SCORE****",score)
    return qa_dict, score


def evaluate_answer(question, true_answer, user_answer):
    # Evaluate the answer
    evaluate_prompt = f"Given this question: {question} for which the correct answer is this: {true_answer}, give a score from 0 to 100 to the following answer given by the user: {user_answer}. The output should be formmated as follows: SCORE: <score number as an integer (e.g 45, 90, etc...)> \n: FEEDBACK: <A one sentence feedback justifying the score.>"
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful research and\
            programming assistant"},
                  {"role": "user", "content": evaluate_prompt}]
    )

    return response.choices[0].message.content


def plot_scores(overall_scores):
    plt.plot(overall_scores)
    plt.xlabel("Round")
    plt.ylabel("Score")
    plt.title("Q&A Session Scores")
    plt.show()


async def scrape_with_playwright(url: str, tags, **kwargs):

    #html_content = await ascrape_playwright(url, tags)
    html_content=extract_transcript(url)
    #print(html_content)
    num = 5
    qa_dict, overall_scores = run_qa_session(num, html_content)
    print("The Q&A data: ", qa_dict)


if __name__ == "__main__":
    asyncio.run(scrape_with_playwright(
        url="https://www.youtube.com/watch?v=pNfElcpgDYo&ab_channel=AutomataLearningLab",
        tags=["p"]
    ))
