# 🍳 Recetify

Recetify es una aplicación web tipo red social pensada para amantes de la cocina, donde los usuarios pueden compartir, descubrir y guardar recetas.

🌐 **Demo en vivo:** https://www.recetify.online/

---

## 🚀 Sobre el proyecto

Este proyecto ha sido desarrollado como parte del **módulo de Django** dentro de mi **máster en desarrollo full stack**.

El objetivo principal era construir una aplicación funcional de principio a fin utilizando Django, aplicando buenas prácticas y entendiendo cómo estructurar un proyecto real.

---

## ✨ Funcionalidades

- 👤 Registro e inicio de sesión de usuarios  
- 🍽️ Crear y publicar recetas  
- ⭐ Puntuar recetas de otros usuarios  
- 🔖 Guardar recetas favoritas  
- 📋 Visualizar recetas de la comunidad  

---

## 🛠️ Tecnologías utilizadas

- **Backend:** Django  
- **Frontend:** HTML + Tailwind CSS  
- **Base de datos:** SQLite (por defecto en desarrollo)  

---

## 📚 Aprendizajes

Este proyecto me ha permitido:

- Entender mejor la arquitectura de aplicaciones con Django  
- Trabajar con modelos, vistas y templates (MTV)  
- Gestionar autenticación de usuarios  
- Mejorar en el uso de Tailwind para maquetación rápida  

💡 Como punto de mejora, eché en falta utilizar un framework moderno de frontend como **React** para aportar mayor interactividad y dinamismo a la aplicación. No se implementó porque no era un requisito del proyecto.

---

## ⚙️ Instalación local

Si quieres ejecutar el proyecto en local:

```bash
# Clonar el repositorio
git clone https://github.com/Gpasadasfj/recetify.git

# Entrar en la carpeta
cd recetify

# Crear entorno virtual
python -m venv venv

# Activarlo
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Ejecutar servidor
python manage.py runserver
