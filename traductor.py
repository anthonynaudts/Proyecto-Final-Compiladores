class CodeTranslator:
    def __init__(self):
        self.output = []
        self.symbol_table = set() 

    def translate(self, ast):
        self.visit(ast)
        return "\n".join(self.output)

    def visit(self, node):
        """Visitar nodos del AST de forma recursiva."""
        if isinstance(node, tuple):
            if node[0] == "program":
                self.output.append("#include <iostream>")
                self.output.append("using namespace std;")
                self.output.append("")
                self.output.append("int main() {")
                for stmt in node[1]:
                    self.visit(stmt)
                self.output.append("    return 0;")
                self.output.append("}")
            elif node[0] == "declaration":
                self.symbol_table.add(node[2])
                self.output.append(f"    {node[1]} {node[2]};")
            elif node[0] == "declaration_assignment":
                self.symbol_table.add(node[2])
                self.output.append(f"    {node[1]} {node[2]} = {self.visit(node[3])};")
            elif node[0] == "assignment":
                if node[1] not in self.symbol_table:
                    raise ValueError(f"Error: La variable '{node[1]}' no está declarada.")
                self.output.append(f"    {node[1]} = {self.visit(node[2])};")
            elif node[0] == "print":
                value = self.visit(node[1])
                self.output.append(f"    cout << {value} << endl;")
            elif node[0] == "binary_op":
                left = self.visit(node[2])
                right = self.visit(node[3])
                return f"({left} {node[1]} {right})"
            elif node[0] == "if":
                condition = self.visit(node[1])
                self.output.append(f"    if ({condition}) {{")
                for stmt in node[2]:
                    self.visit(stmt)
                self.output.append("    }")
            elif node[0] == "if_else":
                condition = self.visit(node[1])
                self.output.append(f"    if ({condition}) {{")
                for stmt in node[2]:
                    self.visit(stmt)
                self.output.append("    } else {")
                for stmt in node[3]:
                    self.visit(stmt)
                self.output.append("    }")
        elif isinstance(node, str):
            if node in self.symbol_table:
                return node
            else:
                return f'"{node}"'
        else:
            return str(node)
