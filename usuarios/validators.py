from django.core.exceptions import ValidationError
import re

class PasswordRobustaValidator:
    def validate(self, password, user=None):
        # 1. Lista negra optimizada de contraseñas comunes que cumplen con el regex (longitud, letras, números y símbolos)
        passwords_prohibidas = [
            'password1!', 'welcome1@', 'admin123*', 'secret1$', '12345678a!', 
            'abc12345*', 'qwerty123!', 'changeme1#', 'letmein12$', '123456789a$'
        ]
        if password.lower() in passwords_prohibidas or 'admin' in password.lower():
            raise ValidationError(
                "🔒 Esta contraseña es extremadamente común o contiene términos restringidos por seguridad. Por favor, elige una clave única.",
                code='password_prohibida',
            )
        
        # 2. Validación integral mediante Regex (longitud, letras, números y símbolos)
        patron = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&._\-#])[A-Za-z\d@$!%*?&._\-#]{8,14}$'
        if not re.match(patron, password):
            raise ValidationError(
                "⚠️ La contraseña no cumple con los requisitos de seguridad: debe tener entre 8 y 14 caracteres, "
                "combinar letras, números y al menos un símbolo especial (ej. @, $, _, !).",
                code='password_invalida',
            )

    def get_help_text(self):
        return (
            "💡 Tu contraseña debe tener una longitud de 8 a 14 caracteres, incluir al menos una letra, un número, "
            "un símbolo especial y no puede ser una clave común (como admin123)."
        )