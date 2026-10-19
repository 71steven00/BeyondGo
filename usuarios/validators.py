from django.core.exceptions import ValidationError
import re

class PasswordRobustaValidator:
    def validate(self, password, user=None):
        # 1. Prohibir contraseñas específicas como admin123
        passwords_prohibidas = ['admin123', 'password123', '12345678', 'admin', 'holamundo']
        if password.lower() in passwords_prohibidas or 'admin' in password.lower():
            raise ValidationError(
                "Esta contraseña es demasiado común o contiene términos prohibidos por seguridad.",
                code='password_prohibida',
            )
        
        # 2. Exigir longitud entre 8 y 14 caracteres
        if not (8 <= len(password) <= 14):
            raise ValidationError(
                "La contraseña debe tener una longitud mínima de 8 y máxima de 14 caracteres.",
                code='password_longitud_invalida',
            )

        # 3. Exigir robustez (letras, números y al menos un carácter especial / símbolo como @, %, $, etc.)
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[@$!%*?&._\-#]', password):
            raise ValidationError(
                "La contraseña debe ser más robusta: debe incluir letras, números y al menos un carácter especial (ej. @, $, %, !).",
                code='password_poco_robusta',
            )

    def get_help_text(self):
        return (
            "Tu contraseña debe tener entre 8 y 14 caracteres, combinar letras, números y símbolos especiales, "
            "y no puede ser una clave débil o común como admin123."
        )