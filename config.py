import os
import subprocess
import sys
import re
from dotenv import load_dotenv
from crewai.tools import BaseTool

# Load environment variables
load_dotenv()

# --- 1. LLM CONFIGURATION (GEMINI 2.5 FLASH) ---
llm_config = "gemini/gemini-2.5-flash"


# --- 2. UNIVERSAL LIBRARY INSTALLER (Final Optimized) ---
class LibraryInstallerTool(BaseTool):
    name: str = "install_library"
    description: str = "Installs missing python libraries. Input: JUST the package name string."

    def _run(self, package_name: str) -> str:
        """Installs the package while skipping problematic and standard libs."""
        try:
            pkg = str(package_name).lower().strip().replace("'", "").replace('"', "")
            if ":" in pkg:
                pkg = pkg.split(":")[-1].replace("{", "").replace("}", "").strip()

            blacklist = ["playsound", "pygame", "pydub", "simpleaudio"]
            if any(b in pkg for b in blacklist):
                return f"⚠️ Skipping {pkg}. Please use native Tkinter logic for maximum stability."

            standard_libs = ["tkinter", "sqlite3", "os", "sys", "json", "re", "datetime", "math", "random", "time",
                             "collections"]
            if any(lib == pkg for lib in standard_libs):
                return f"✅ {pkg} is a standard library. No pip install needed."

            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            return f"✅ Successfully installed: {pkg}"
        except Exception as e:
            return f"❌ Failed to install {package_name}: {str(e)}"


# --- 3. STABILIZED CODE EXTRACTOR & WRITER (With Auto-Correct Guard) ---
class FileWriterTool(BaseTool):
    name: str = "write_code_to_file"
    description: str = "SAVES PURE PYTHON CODE TO generated_app.py. Input: The raw AI response string."

    def _run(self, content: str) -> str:
        """Strictly extracts, validates and saves Python code to generated_app.py."""
        try:
            filename = "generated_app.py"
            raw_text = str(content).strip()

            # Step 1: Intelligent Extraction
            if "```python" in raw_text:
                clean_content = raw_text.split("```python")[1].split("```")[0].strip()
            elif "```" in raw_text:
                clean_content = raw_text.split("```")[1].split("```")[0].strip()
            else:
                if "import " in raw_text:
                    clean_content = "import " + raw_text.split("import ", 1)[1]
                else:
                    clean_content = raw_text

            # Step 2: Syntax Guard (Auto-fix basic quote/bracket issues)
            # Fix for 'p004' type errors (unterminated strings in dictionaries)
            lines = clean_content.splitlines()
            fixed_lines = []
            for line in lines:
                # Agar line mein odd number of quotes hain, toh ek quote add kar do end mein
                if line.count("'") % 2 != 0 and "'''" not in line:
                    line = line.rstrip() + "'"
                if line.count('"') % 2 != 0 and '"""' not in line:
                    line = line.rstrip() + '"'
                fixed_lines.append(line)

            clean_content = "\n".join(fixed_lines)

            # Step 3: Write to file
            with open(filename, "w", encoding="utf-8") as f:
                f.write(clean_content)

            return f"✅ MISSION SUCCESS: {filename} saved. Syntax Guard checked for unclosed quotes."
        except Exception as e:
            return f"❌ Save error: {str(e)}"


# Tool instances for Agents
file_tool = FileWriterTool()
command_tool = LibraryInstallerTool()

if __name__ == "__main__":
    print(f"🚀 Universal Engine Initialized | Model: {llm_config}")