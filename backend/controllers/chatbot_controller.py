# controllers/chatbot_controller.py

from utils.processing import fn_generate_response,fn_get_chroma_client
from utils.classifier import get_static_intent_response
from prompt import get_prompt
import re
import json



def help_fn_format_chat_history(chat_history, limit=5):
    """
    Convert chat history into formatted string.

    Args:
        chat_history (list): Previous messages
        limit (int): Max history size

    Returns:
        str
    """
    if not chat_history:
        return ""

    history = ""

    for msg in chat_history[-limit:]:
        role = msg.get("role")
        text = msg.get("text")

        if role == "user":
            history += f"User: {text}\n"
        elif role == "model":
            history += f"Assistant: {text}\n"

    return history

def help_fn_retrieve_context(question, k=4):
    """
    Retrieve relevant chunks from vector DB.

    Args:
        question (str)
        k (int)

    Returns:
        tuple: (context, source_url)
    """
    vector_store = fn_get_chroma_client()
    retriever = vector_store.as_retriever(search_kwargs={"k": k})

    docs = retriever.invoke(question)

    if not docs:
        return "", ""

    context = "\n\n".join([doc.page_content[:500] for doc in docs])
    source_url = docs[0].metadata.get("url", "")

    return context, source_url




def help_fn_generate_chat_response(question: str, chat_history: list = None):
    """
    Execute RAG pipeline.

    Args:
        question (str)
        chat_history (list)

    Returns:
        dict
    """
    try:
        static_answer = get_static_intent_response(question)
        
        if static_answer:
            return {
                "answer": static_answer,
                "source": "https://sagex.io/" # Provide the base URL as the source
            }
    
        context, source_url = help_fn_retrieve_context(question)

        if not context:
                    return {
                        "answer": "I'd love to give you specific details on that, but I need a bit more information. Generally, Sagex helps businesses through cutting-edge software and engineering. Would you like to schedule a free consultation to speak with our team directly?",
                        "source": "https://sagex.io/contact"
                    }

        history = help_fn_format_chat_history(chat_history)

        prompt = get_prompt()

        formatted_prompt = prompt.format_prompt(
            context=context,
            question=question,
            chat_history=history
        )

        messages = formatted_prompt.to_messages()

        response_text = fn_generate_response(messages)
        final_response =response_text # Default fallback
        try:
            match = re.search(r'\{.*\}',response_text, re.DOTALL)
            if match:
                parsed_response = json.loads(match.group(0))
                # Grab ONLY the text inside the "answer" key
                final_response = parsed_response.get("answer",response_text)
        except Exception as e:
            print(f"JSON Parsing failed, using raw text: {e}")
            pass

        return {
            "answer": final_response,
            "source": source_url
        }

    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "source": ""
        }