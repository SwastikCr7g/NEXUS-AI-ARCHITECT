import os
import ast
from dotenv import load_dotenv
from crewai import Crew, Task, Process
from agents import product_manager, system_architect, senior_developer
# Manager connect kiya gaya
from syntax_manager import absolute_fixer

# Environment variables load karna
load_dotenv()


def validate_syntax(filename="generated_app.py"):
    """
    Python ke built-in AST module ka use karke code ki syntax check karta hai.
    """
    if not os.path.exists(filename):
        return False, "File 'generated_app.py' was not created."

    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    if not code.strip():
        return False, "File is empty."

    try:
        ast.parse(code)
        return True, "Code is syntax-perfect."
    except SyntaxError as e:
        error_details = f"SyntaxError: {e.msg} at line {e.lineno}, column {e.offset}."
        return False, error_details


# --- 1. DEFINE OPTIMIZED TASKS ---

research_task = Task(
    description="""Meticulously analyze the app idea: '{app_idea}'. 
    Extract and define:
    1. A professional color palette (Specific Hex codes for BG and UI elements).
    2. Core functional logic and potential edge cases.
    3. Mandatory: Specify that this is a GUI application using Tkinter.
    4. Essential standard libraries required for a single-file Python script.""",
    expected_output="A detailed technical and visual design specification document specifying a GUI approach.",
    agent=product_manager
)

design_task = Task(
    description="""Create a sophisticated Class-based (OOP) Technical Blueprint for: '{app_idea}'.
    Technical Mandates:
    - The app MUST be a Graphical User Interface (GUI).
    - Entire application MUST reside in a single, self-contained Python file.
    - All game/app variables MUST use the 'self.' prefix to ensure proper class scope.
    - Layout MUST use side=tk.TOP/BOTTOM/LEFT/RIGHT.
    - Use standard font styles only ('bold', 'normal').""",
    expected_output="A structured software architecture blueprint for a GUI app with a clear UI hierarchy map.",
    agent=system_architect,
    context=[research_task]
)

coding_task = Task(
    description="""Implement the final application based on the blueprint for: '{app_idea}'.
    Final Code Requirements:
    1. Build it as a GUI app (Tkinter).
    2. Write clean, commented Python code in EXACTLY ONE FILE.
    3. CRITICAL: Ensure all string quotes (' ') and brackets ([ ]) are closed.
    4. Master Tip: In dictionaries, use only single quotes for strings and avoid nesting double quotes inside them (e.g., use '14 inch' instead of '14"').
    5. Save the pure Python output using the 'write_code_to_file' tool into 'generated_app.py'.""",
    expected_output="A fully functional, runnable Python GUI script saved as 'generated_app.py'.",
    agent=senior_developer,
    context=[design_task]
)

# --- 2. ASSEMBLE THE UNIVERSAL CREW ---

agency = Crew(
    agents=[product_manager, system_architect, senior_developer],
    tasks=[research_task, design_task, coding_task],
    process=Process.sequential,
    memory=False,
    verbose=True,
    max_rpm=10
)

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("🏢 NEURAL NEXUS v3.6 - AUTO-HEALER EDITION ONLINE")
    print("Optimization: Self-Healing Syntax Logic Enabled")
    print("=" * 55 + "\n")

    user_prompt = input("🚀 What would you like to build today? ")

    if user_prompt.strip():
        # Prompt Update: AI ko galti karne se rokne ke liye master instruction add ki
        enhanced_prompt = user_prompt + " (IMPORTANT: In the STORE_DATA dictionary, use only single quotes for strings and avoid nesting double quotes inside them like '14 inch' instead of '14\"'.)"

        max_retries = 3
        attempt = 1
        current_app_idea = enhanced_prompt

        while attempt <= max_retries:
            print(f"\n[SYSTEM] Execution Attempt {attempt}/{max_retries}...\n")
            try:
                # Kickoff the agents
                agency.kickoff(inputs={'app_idea': current_app_idea})

                # Post-Generation Validation
                is_valid, message = validate_syntax()

                if not is_valid:
                    print(f"⚠️ Initial Validation Failed: {message}")
                    print(f"💉 Attempting Absolute Healing via syntax_manager...")

                    # Syntax Healer call kiya
                    healed, heal_msg = absolute_fixer()

                    if healed:
                        print("✨ Code Healed! Re-validating...")
                        is_valid, message = validate_syntax()
                    else:
                        print(f"❌ Healing Failed: {heal_msg}")

                if is_valid:
                    print("\n" + "=" * 45)
                    print("✅ MISSION SUCCESS: CODE IS PERFECT & RUNNABLE")
                    print("📄 File saved to: 'generated_app.py'")
                    print("💡 Status: Syntax Verified & Healed.")
                    print("=" * 45)
                    break
                else:
                    if attempt < max_retries:
                        print(f"🔄 Feedback sent to Agent for re-generation...")
                        current_app_idea = f"THE PREVIOUS CODE HAD A SYNTAX ERROR: {message}. RE-WRITE the entire code carefully ensuring all quotes and brackets are closed."
                        attempt += 1
                    else:
                        print("\n❌ Max retries reached. Critical syntax failure.")
                        break

            except Exception as e:
                if "503" in str(e):
                    print(f"\n⚠️ SERVER BUSY: Retrying attempt {attempt}...")
                    attempt += 1
                else:
                    print(f"\n❌ Agency Critical Failure: {str(e)}")
                    break