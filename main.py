import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from lexer import lexer, reset_lineno
from parser import build_parser
from tabla_simbolos import SymbolTable
from codigo_intermedio import IntermediateCodeGenerator
from traductor import CodeTranslator

def format_ast_python_style(node, level=0):
    indent = "    " * level
    if isinstance(node, tuple):
        result = f"{indent}(\n"
        result += f"{indent}    {repr(node[0])},\n"
        for child in node[1:]:
            result += f"{format_ast_python_style(child, level + 1)},\n"
        result = result.rstrip(",\n")
        result += f"\n{indent})"
        return result
    elif isinstance(node, list):
        result = f"{indent}[\n"
        for child in node:
            result += f"{format_ast_python_style(child, level + 1)},\n"
        result = result.rstrip(",\n")
        result += f"\n{indent}]"
        return result
    else:
        return f"{indent}{repr(node)}"

def find_line(input_text, token_pos):
    lines = input_text[:token_pos].splitlines()
    return len(lines)  


def compile_code():
    symbols_output.delete("1.0", tk.END)
    ast_output.delete("1.0", tk.END)
    intermediate_output.delete("1.0", tk.END)
    cpp_output.delete("1.0", tk.END)
    errors_output.delete("1.0", tk.END)

    source_code = code_input.get("1.0", tk.END)
    if not source_code.strip():
        errors_output.insert("1.0", "Error: No hay código fuente para compilar.\n")
        return

    lexer.input(source_code)
    lexer.lineno = 1

    symbol_table = SymbolTable()
    parser = build_parser()

    try:
        tokens = []
        while tok := lexer.token():
            tokens.append(f"{tok.type}({tok.value})")
    except SyntaxError as e:
        
        token_pos = lexer.lexpos
        line_number = find_line(source_code, token_pos)
        errors_output.insert("end", f"{e} en la línea {line_number}.\n")
        return
    except Exception as e:
        errors_output.insert("end", f"Error inesperado en análisis léxico: {e}\n")
        return

    try:
        parser.symbol_table = symbol_table
        ast = parser.parse(source_code, lexer=lexer)
        formatted_ast = format_ast_python_style(ast)
        ast_output.insert("1.0", formatted_ast)
    except SyntaxError as e:
        
        token_pos = lexer.lexpos
        line_number = find_line(source_code, token_pos)
        errors_output.insert("end", f"{e} en la línea {line_number}.\n")
        return
    except Exception as e:
        errors_output.insert("end", f"Error inesperado en análisis sintáctico: {e}\n")
        return

    try:
        
        icg = IntermediateCodeGenerator()
        intermediate_code = icg.generate(ast)
        formatted_code = "\n".join(" ".join(map(str, line)) for line in intermediate_code)
        intermediate_output.insert("1.0", formatted_code)
    except Exception as e:
        errors_output.insert("end", f"Error en generación de código intermedio: {e}\n")
        return

    try:
        
        translator = CodeTranslator()
        cpp_code = translator.translate(ast)
        cpp_output.insert("1.0", cpp_code)
    except Exception as e:
        errors_output.insert("end", f"Error en traducción a C++: {e}\n")
        return

    try:
        symbol_table_str = str(symbol_table)
        symbols_output.insert("1.0", symbol_table_str)
    except Exception as e:
        errors_output.insert("end", f"Error en la tabla de símbolos: {e}\n")


def clear_all():
    code_input.delete("1.0", tk.END)
    symbols_output.delete("1.0", tk.END)
    ast_output.delete("1.0", tk.END)
    intermediate_output.delete("1.0", tk.END)
    cpp_output.delete("1.0", tk.END)

def save_cpp_code():
    cpp_code = cpp_output.get("1.0", tk.END).strip()
    if not cpp_code:
        messagebox.showwarning("Guardar", "No hay código traducido a guardar.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".cpp",
        filetypes=[("Archivos C++", "*.cpp"), ("Todos los archivos", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(cpp_code)
        messagebox.showinfo("Guardar", "Código guardado exitosamente.")

def copy_cpp_code():
    cpp_code = cpp_output.get("1.0", tk.END).strip()
    if not cpp_code:
        messagebox.showwarning("Copiar", "No hay código traducido para copiar.")
        return
    app.clipboard_clear()
    app.clipboard_append(cpp_code)
    app.update()
    messagebox.showinfo("Copiar", "Código copiado al portapapeles.")

app = tk.Tk()
app.title("Compilador")
app.geometry("1200x750")
app.resizable(True, True)
app.state("zoomed")
icono = PhotoImage(file="compilador.png")
app.iconphoto(True, icono)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=5)

app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)

code_frame = ttk.LabelFrame(app, text="Código fuente", padding=10)
code_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
code_input = tk.Text(code_frame, wrap="none", font=("Consolas", 10))
code_input.pack(fill="both", expand=True)

button_frame = tk.Frame(app, pady=10)
button_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
ttk.Button(button_frame, text="Compilar", command=compile_code).pack(side="left", padx=10)
ttk.Button(button_frame, text="Limpiar", command=clear_all).pack(side="left", padx=10)
ttk.Button(button_frame, text="Guardar Código", command=save_cpp_code).pack(side="left", padx=10)
ttk.Button(button_frame, text="Copiar Código", command=copy_cpp_code).pack(side="left", padx=10)

symbols_frame = ttk.LabelFrame(app, text="Tabla de símbolos", padding=10)
symbols_frame.grid(row=0, column=1, sticky="nsew")
symbols_output = tk.Text(symbols_frame, wrap="none", font=("Consolas", 10))
symbols_output.pack(fill="both", expand=True)

ast_frame = ttk.LabelFrame(app, text="AST", padding=10)
ast_frame.grid(row=1, column=1, sticky="nsew")
ast_output = tk.Text(ast_frame, wrap="none", font=("Consolas", 10))
ast_output.pack(fill="both", expand=True)

intermediate_frame = ttk.LabelFrame(app, text="Código intermedio", padding=10)
intermediate_frame.grid(row=0, column=2, sticky="nsew")
intermediate_output = tk.Text(intermediate_frame, wrap="none", font=("Consolas", 10))
intermediate_output.pack(fill="both", expand=True)

cpp_frame = ttk.LabelFrame(app, text="Código traducido a C++", padding=10)
cpp_frame.grid(row=1, column=2, sticky="nsew")
cpp_output = tk.Text(cpp_frame, wrap="none", font=("Consolas", 10))
cpp_output.pack(fill="both", expand=True)


errors_frame = ttk.LabelFrame(app, text="Errores", padding=10)
errors_frame.grid(row=1, column=0, sticky="nsew")
errors_output = tk.Text(errors_frame, wrap=tk.WORD, font=("Consolas", 10),fg="red")
errors_output.pack(fill="both", expand=True)


app.mainloop()
