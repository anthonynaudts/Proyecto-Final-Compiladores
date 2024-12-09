class SymbolTable:
    def __init__(self):
        self.symbols = []

    def add(self, name, type, value=None, scope="global"):
        """Agregar una nueva variable a la tabla de símbolos."""
        for symbol in self.symbols:
            if symbol["Nombre"] == name and symbol["Alcance"] == scope:
                raise ValueError(f"Error: La variable '{name}' ya fue declarada en el alcance '{scope}'.")

        self.symbols.append({
            "Nombre": name,
            "Tipo": type,
            "Valor": value,
            "Alcance": scope
        })

    def update(self, name, value, scope="global"):
        """Actualizar el valor de una variable existente."""
        for symbol in self.symbols:
            if symbol["Nombre"] == name and symbol["Alcance"] == scope:
                symbol["Valor"] = value
                return
        raise ValueError(f"Error: La variable '{name}' no está declarada en el alcance '{scope}'.")

    def exists(self, name, scope="global"):
        """Verificar si una variable existe en el alcance dado."""
        return any(symbol["Nombre"] == name and symbol["Alcance"] == scope for symbol in self.symbols)

    def get(self, name, scope="global"):
        """Obtener una variable de la tabla de símbolos."""
        for symbol in self.symbols:
            if symbol["Nombre"] == name and symbol["Alcance"] == scope:
                return symbol
        raise ValueError(f"Error: La variable '{name}' no está declarada en el alcance '{scope}'.")

    def __str__(self):
        """Representación en formato de tabla."""
        header = f"{'Nombre':<15}{'Tipo':<10}{'Valor':<15}{'Alcance':<10}"
        rows = [header, "-" * len(header)]
        for symbol in self.symbols:
            rows.append(f"{symbol['Nombre']:<15}{symbol['Tipo']:<10}{str(symbol['Valor']):<15}{symbol['Alcance']:<10}")
        return "\n".join(rows)
