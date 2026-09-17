# 🗺️ BeyondGo

> **BeyondGo** es una plataforma web de reservas turísticas diseñada para la promoción y gestión integral de tours, alojamientos y experiencias.

---

## 🛠️ Convención de Commits

En este repositorio seguimos el estándar de [Conventional Commits](https://www.conventionalcommits.org/) para mantener un historial de cambios claro, estructurado y profesional.
### 🏷️ Convención de Commits

| Tipo | Categoría | Descripción | Ejemplo de Uso |
| :---: | :--- | :--- | :--- |
| 🚀 | **`feat`** | Nueva funcionalidad o módulo | `feat(login): initialize login app and add UI templates` |
| 🐛 | **`fix`** | Corrección de un error o bug | `fix(auth): correct 6-digit code expiration logic` |
| 🎨 | **`style`** | Estilos, CSS, formato (sin afectar lógica) | `style(ui): adjust responsiveness of reset password form` |
| ♻️ | **`refactor`** | Reestructuración limpia de código | `refactor(templates): move base.html to project root` |
| 📝 | **`docs`** | Documentación (README, notas) | `docs: update setup instructions and commit guidelines` |
| 🔧 | **`chore`** | Configuración, tareas o paquetes | `chore(deps): add django-cors-headers to requirements` |
| 🧪 | **`test`** | Pruebas unitarias o de integración | `test(reservas): add unit tests for tour booking flow` |
| ⚡ | **`perf`** | Optimizaciones de rendimiento/DB | `perf(tours): optimize querysets for destination listings` |
| 📦 | **`build`** | Sistema de construcción o Docker | `build: update Dockerfile and environment setup` |
| 👷 | **`ci`** | Flujos de integración continua | `ci: configure GitHub Actions workflow` |
| ⏪ | **`revert`** | Revertir un commit previo | `revert: "feat: add social auth endpoints"` |

### 📐 Formato del Mensaje

```text
<tipo>(<módulo opcional>): <descripción breve en minúsculas y presente>
