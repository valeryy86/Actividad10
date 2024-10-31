from abc import ABC, abstractmethod
from validadorclave.modelo.errores import (
    NoCumpleLongitudError,
    NoTieneMayusculaError,
    NoTieneMinusculaError,
    NoTieneNumeroError,
    NoTieneCaracterEspecialError,
    NoTienePalabraError
)

class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    def _validar_longitud(self, clave):
        if len(clave) <= self._longitud_esperada:
            raise NoCumpleLongitudError()
        return True

    def _contiene_mayuscula(self, clave):
        if not any(c.isupper() for c in clave):
            raise NoTieneMayusculaError()
        return True

    def _contiene_minuscula(self, clave):
        if not any(c.islower() for c in clave):
            raise NoTieneMinusculaError()
        return True

    def _contiene_numero(self, clave):
        if not any(c.isdigit() for c in clave):
            raise NoTieneNumeroError()
        return True

    @abstractmethod
    def es_valida(self, clave):
        pass

class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(8)

    def contiene_caracter_especial(self, clave):
        caracteres_especiales = {'@', '_', '#', '$', '%'}
        if not any(c in caracteres_especiales for c in clave):
            raise NoTieneCaracterEspecialError()
        return True

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self.contiene_caracter_especial(clave)
        return True

class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(6)

    def contiene_calisto(self, clave):
        # Convertir la clave a minúsculas para buscar 'calisto'
        clave_lower = clave.lower()
        pos = clave_lower.find('calisto')
        
        if pos == -1:
            raise NoTienePalabraError()
            
        # Obtener el fragmento 'calisto' de la clave original
        palabra = clave[pos:pos+7]
        
        # Contar mayúsculas en la palabra
        mayusculas = sum(1 for c in palabra if c.isupper())
        
        # Debe tener al menos 2 mayúsculas pero no todas
        if mayusculas < 2 or mayusculas == len('calisto'):
            raise NoTienePalabraError()
            
        return True

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_numero(clave)
        self.contiene_calisto(clave)
        return True

class Validador:
    def __init__(self, regla):
        self._regla = regla

    def es_valida(self, clave):
        return self._regla.es_valida(clave)