import ast
import re


def absolute_fixer(filename="generated_app.py"):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        # Step 1: Fix unclosed single quotes
        if line.count("'") % 2 != 0 and "'''" not in line:
            # Agar line ke end mein comma hai (dictionary style), toh quote comma se pehle lagao
            if line.strip().endswith(","):
                line = line.rstrip().rstrip(",") + "'" + ",\n"
            else:
                line = line.rstrip() + "'\n"

        # Step 2: Fix unclosed double quotes
        if line.count('"') % 2 != 0 and '"""' not in line:
            if line.strip().endswith(","):
                line = line.rstrip().rstrip(",") + '"' + ",\n"
            else:
                line = line.rstrip() + '"\n'

        fixed_lines.append(line)

    fixed_code = "".join(fixed_lines)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(fixed_code)

    try:
        ast.parse(fixed_code)
        return True, "Code Healed Successfully"
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    absolute_fixer()