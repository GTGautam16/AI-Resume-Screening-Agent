from services.llm import ask_llm

def parse_resume(resume_text):

    prompt = f"""
        You are an expert Resume Parser.

        Extract the important information from this resume.

        Resume:
        {resume_text}

        Return a clean structured summary.
        """

    return ask_llm(prompt)