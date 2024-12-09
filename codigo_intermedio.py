class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self):
        """Generar una nueva variable temporal."""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def new_label(self):
        """Generar una nueva etiqueta."""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def generate(self, ast):
        """Generar código intermedio a partir del AST."""
        self.visit(ast)
        return self.code

    def visit(self, node):
        """Visitar nodos del AST de forma recursiva."""
        if isinstance(node, tuple):
            if node[0] == "program":
                for stmt in node[1]:
                    self.visit(stmt)
            elif node[0] == "declaration":
                
                pass
            elif node[0] == "declaration_assignment":
                result = node[2]
                expr = self.visit(node[3])
                self.code.append((result, "=", expr))
            elif node[0] == "assignment":
                result = node[1]
                expr = self.visit(node[2])
                self.code.append((result, "=", expr))
            elif node[0] == "binary_op":
                left = self.visit(node[2])
                right = self.visit(node[3])
                temp = self.new_temp()
                self.code.append((temp, "=", left, node[1], right))
                return temp
            elif node[0] == "print":
                value = self.visit(node[1])
                self.code.append(("PRINT", value))
            elif node[0] == "if":
                condition = self.visit(node[1])
                true_label = self.new_label()
                false_label = self.new_label()
                self.code.append(("IF", condition, "GOTO", true_label))
                self.code.append(("GOTO", false_label))
                self.code.append((f"{true_label}:",))
                for stmt in node[2]:
                    self.visit(stmt)
                self.code.append((f"{false_label}:",))
            elif node[0] == "if_else":
                condition = self.visit(node[1])
                true_label = self.new_label()
                false_label = self.new_label()
                end_label = self.new_label()
                self.code.append(("IF", condition, "GOTO", true_label))
                self.code.append(("GOTO", false_label))
                self.code.append((f"{true_label}:",))
                for stmt in node[2]:
                    self.visit(stmt)
                self.code.append(("GOTO", end_label))
                self.code.append((f"{false_label}:",))
                for stmt in node[3]:
                    self.visit(stmt)
                self.code.append((f"{end_label}:",))
        elif isinstance(node, str):
            return node  
        else:
            return str(node)  
