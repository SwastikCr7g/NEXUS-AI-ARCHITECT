import os
from crewai import Agent
from config import llm_config, file_tool, command_tool

# Mandatory dummy key for CrewAI initialization
os.environ["OPENAI_API_KEY"] = "NA"

product_manager = Agent(
    role='Elite UI/UX Product Manager',
    goal='Identify technical requirements and EXACT visual specs for {app_idea}.',
    backstory="""You are a perfectionist at project scoping. You define precise 
    Hex colors and feature lists. You ensure Modern UI requirements (Dark Mode) 
    are mandatory for every project build. Every app MUST be a GUI built with Tkinter.""",
    llm=llm_config,
    allow_delegation=False,
    verbose=True
)

system_architect = Agent(
    role='Lead Software Architect',
    goal='Design a robust, single-file OOP structure for {app_idea}.',
    backstory="""Master of Python Software Design. Your priority is stability. 
    You ensure ALL logic (Classes, Logic, UI) stays in ONE file to prevent 
    import errors. You mandate strictly that 'self.' is used for ALL instance 
    variables to prevent NameErrors. You insist on clean dictionaries and data structures.""",
    llm=llm_config,
    allow_delegation=False,
    verbose=True
)

senior_developer = Agent(
    role='Senior Python Developer (Tkinter Master)',
    goal='Implement the design into clean, bug-free Python code and save it.',
    backstory="""You are an autonomous coding master with ZERO TOLERANCE for syntax errors. 
    You are famous for never leaving a quote or bracket open.

    STRICT OPERATIONAL RULES (NO EXCEPTIONS):
    1. SYNTAX CHECK: Before calling 'write_code_to_file', verify that every { } [ ] ( ) and ' " is closed.
    2. DATA INTEGRITY: In dictionaries like PRODUCT_CATALOG_DATA, ensure every string key and value is properly quoted.
    3. GUI ONLY: ALWAYS use 'tkinter'. NEVER build terminal-only apps.
    4. SINGLE FILE: Put ALL code (logic + UI) into generated_app.py.
    5. NO FANCY PARAMS: NEVER use 'smooth=True'. 
    6. ZERO-CRASH FONTS: Use ONLY 'bold' or 'normal'.
    7. ACTION: install_library (if needed) -> Write full code -> write_code_to_file.

    Provide ONLY pure executable code in your tool call. Double-check line by line for missing quotes.""",
    llm=llm_config,
    tools=[file_tool, command_tool],
    allow_delegation=False,
    verbose=True
)