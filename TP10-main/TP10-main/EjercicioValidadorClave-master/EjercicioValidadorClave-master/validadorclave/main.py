from validadorclave.modelo.validador import Validador
from validadorclave.modelo.errores import (
    NoCumpleLongitudError,
    NoTieneMayusculaError,
    NoTieneMinusculaError,
    NoTieneNumeroError,
    NoTieneCaracterEspecialError,
    NoTienePalabraError
)

def obtener_mensaje_error(regla, excepcion):
    """
    Retorna un mensaje de error específico basado en el tipo de excepción.
    """
    mensajes = {
        NoCumpleLongitudError: "La clave debe tener una longitud de más de {} caracteres",
        NoTieneMayusculaError: "La clave debe tener al menos una letra mayúscula",
        NoTieneMinusculaError: "La clave debe tener al menos una letra minúscula",
        NoTieneNumeroError: "La clave debe tener al menos un número",
        NoTieneCaracterEspecialError: "La clave debe tener al menos un caracter especial (@, _, #, $ o %)",
        NoTienePalabraError: "La palabra calisto debe estar escrita con al menos dos letras en mayúscula"
    }
    
    mensaje_base = mensajes.get(type(excepcion), "Error de validación no especificado")
    
    if isinstance(excepcion, NoCumpleLongitudError):
        longitud = 8 if "Ganimedes" in regla.__class__.__name__ else 6
        return mensaje_base.format(longitud)
    
    return mensaje_base

def validar_clave(clave, reglas):
    """
    Valida una clave contra una lista de reglas de validación.
    
    Args:
        clave (str): La clave a validar
        reglas (list): Lista de clases de reglas de validación
    
    Imprime mensajes de error por cada regla que no se cumpla
    o un mensaje de éxito si la clave pasa todas las validaciones.
    """
    for regla_clase in reglas:
        try:
            # Crear instancia de la regla
            regla = regla_clase()
            # Crear validador con la regla
            validador = Validador(regla)
            # Intentar validar la clave
            if validador.es_valida(clave):
                print(f"La clave es válida para {regla.__class__.__name__}")
        except Exception as e:
            print(f"Error: {regla.__class__.__name__}: {obtener_mensaje_error(regla, e)}")

def main():
    """
    Función principal que demuestra el uso del validador de claves.
    """
    # Ejemplo de uso
    from validadorclave.modelo.validador import ReglaValidacionGanimedes, ReglaValidacionCalisto
    
    # Lista de reglas a validar
    reglas = [ReglaValidacionGanimedes, ReglaValidacionCalisto]
    
    # Ejemplos de claves
    claves_ejemplo = [
        "corta",  # Muy corta para ambas reglas
        "Ab1@calisto",  # Válida para Ganímedes pero no para Calisto (falta mayúscula en calisto)
        "Ab1@cAliStO",  # Válida para ambas reglas
        "abc123456",  # No cumple caracteres especiales para Ganímedes
        "123CALISTO"  # No cumple para Calisto (todas mayúsculas)
    ]
    
    # Probar cada clave
    for i, clave in enumerate(claves_ejemplo, 1):
        print(f"\nProbando clave #{i}: '{clave}'")
        print("-" * 50)
        validar_clave(clave, reglas)

if __name__ == "__main__":
    main()