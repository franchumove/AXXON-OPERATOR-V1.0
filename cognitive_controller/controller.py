def decide_modules(archetype, emotion):
    # Esta es una lógica simulada. Puedes reemplazarla.
    if archetype == "explorer" and emotion == "curious":
        return ["modulo_inspiración", "modulo_reto"]
    else:
        return ["modulo_reflexión", "modulo_soporte"]

def build_contextual_strategy(message, modules):
    # Crea una estrategia con base en los módulos
    return f"Estrategia basada en el mensaje: '{message}' con módulos: {', '.join(modules)}"