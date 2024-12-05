from flask import Flask, render_template, jsonify, url_for
from datetime import datetime
import os

app = Flask(__name__)

# Lista de regalos para el calendario de adviento
GIFTS = {
    1: {
        "type": "text",
        "content": "primer dia del calendario, espero te guste lo hice con mucho amor✨"
    },
    2: {
        "type": "text",
        "content": "De todas las personas en el mundo, mi corazón se quedo con vos. y todos los dias confirmo que fue la mejor decision ❤️"
    },
    3: {
        "type": "image",
        "content": "static/images/imgday3.jpg",
        "description": "Nuestra primer foto como novios 📸"
    },
    4: {
        "type": "text",
        "content": "Cupon valido por 10 minutos de masajes 💆‍♂️"
    },
    5: {
        "type": "link",
        "content": "https://open.spotify.com/intl-es/track/7b9hpzFQJaKUAAKsOeDafS",
        "description": "Cada vez que la escucho, pienso en vos 🎵"
    },
    6: {
        "type": "text",
        "content": "Me encanta como me miras, como me haces reír, cómo me cuidas. Me encantas vos💝"
    },
    7: {
        "type": "image",
        "content": "static/images/imgday7.jpg",
        "description": "Un momento especial juntos Porque cumplimos 1 año juntos"
    },
    8: {
        "type": "text",
        "content": "8 razones por las que te amo: Tu sonrisa, tu bondad, tu fortaleza, tu humor, tu Pelo, tu pasión, tu lealtad y tu forma de amar 💫"
    },
    9: {
        "type": "link",
        "content": "https://open.spotify.com/playlist/40MgWg7bEJYjAaHAKSq8K3",
        "description": "Una playlist especial para vos - Todas las canciones que me hacen acordar a nosotros 🎵"
    },
    10: {
        "type": "link",
        "content": "static/love-puzzle.html",
        "description": "Un rompecabezas digital con nuestra foto favorita - ¡Armalo para ver un mensaje especial! 🧩"
    },
    11: {
        "type": "link",
        "content": "https://open.spotify.com/intl-es/track/4J2HLNTxiVxxs6kWgTIN43",
        "description": "Nuestra canción - La primera que te dedique 🎵"
    },
    12: {
        "type": "link",
        "content": "static/stories/our_story.html",
        "description": "el dia en el que te conoci - Con fotos, música y animaciones 📖✨"
    },
    13: {
        "type": "link",
        "content": "static/games/memory.html",
        "description": "Un juego de memoria personalizado con nuestros momentos favoritos 🎮"
    },
    14: {
        "type": "art",
        "content": "static/art/digital_drawing.jpg",
        "description": "Un dibujo de kitty que hice de vos"
    },
    15: {
        "type": "text",
        "content": "Otra cosa que me encanta de vos es tu forma de ser tan auténtica y única. Me haces sentir especial cada día 💫",
        "description": "Un pensamiento del corazón 💝"
    },
    16: {
        "type": "poem",
        "content": [
            "Cada estrella en el cielo",
            "Es un te amo que te envío",
            "Cada rayo de sol al amanecer",
            "Es mi sonrisa al pensarte",
            "Cada gota de lluvia",
            "Es un beso que guardo para ti",
            "Y cada latido de mi corazón",
            "Tiene grabado tu nombre ✨"
        ],
        "description": "Un poema que escribí pensando en vos 📝"
    },
    17: {
        "type": "link",
        "content": "static/quiz/our_love.html",
        "description": "Un quiz interactivo sobre nuestra historia - ¡Con premios sorpresa! 🎯"
    },
    18: {
        "type": "link",
        "content": "static/hunt/clues.json",
        "description": "Una búsqueda del tesoro digital - Cada pista te lleva a un recuerdo especial 🗺️"
    },
    19: {
        "type": "animation",
        "content": "static/animations/love_story.gif",
        "description": "Una animación que creé de nuestra historia de amor 🎬"
    },
    20: {
        "type": "photo_mosaic",
        "content": "static/mosaic/collage.jpg",
        "description": "Un mosaico gigante hecho con cientos de nuestras fotos juntos que forma un corazón ❤️📸"
    },
    21: {
        "type": "link",
        "content": "static/letters/carta_especial.html",
        "description": "Una carta digital con todas las razones por las que te amo 💌"
    },
    22: {
        "type": "text",
        "content": "Cada día que pasa me enamoro más de tu sonrisa, de tu forma de ser, de cómo me haces sentir. Sos mi persona favorita en todo el mundo y no puedo imaginar mi vida sin vos ❤️",
        "description": "Un mensaje desde el corazón 💝"
    },
    23: {
        "type": "link",
        "content": "static/christmas_countdown.html",
        "description": "Cuenta regresiva personalizada para Navidad - Con mensajes especiales cada hora 🎄"
    },
    24: {
        "type": "link",
        "content": "static/garden/jardin_virtual.html", 
        "description": "Un jardín virtual donde cada flor representa un momento especial juntos. ¡Puedes regar las flores y verlas crecer! 🌸🌺"
    },
    25: {
        "type": "link",
        "content": "static/christmas/decorar_arbol.html",
        "description": "¡Feliz Navidad mi amor! Un árbol de Navidad virtual que podés decorar a tu gusto con luces, adornos, guirnaldas y hasta poner regalitos debajo. ¡Guardá tu diseño y compartilo conmigo! 🎄🎁✨"
    }
}

# Función helper para verificar imágenes
def verify_image_path(image_path):
    """Verifica y corrige la ruta de la imagen."""
    # Normalizar la ruta
    image_path = image_path.replace('\\', '/')
    
    # Si la ruta comienza con 'static/', quitarlo para la verificación
    check_path = image_path
    if check_path.startswith('static/'):
        check_path = check_path[7:]
    elif check_path.startswith('/static/'):
        check_path = check_path[8:]

    # Verificar si el archivo existe
    if os.path.exists(os.path.join('static', check_path)):
        return image_path
    
    print(f"Imagen no encontrada: {image_path}")
    print(f"Ruta completa intentada: {os.path.join('static', check_path)}")
    return 'static/images/default.jpg'  # Ruta por defecto

@app.route('/')
def index():
    return render_template('index.html', gifts=GIFTS)

@app.route('/api/gifts')
def get_all_gifts():
    # current_date = datetime.now()
    # current_day = current_date.day
    
    available_gifts = []
    for day in range(1, 26):
        gift = GIFTS.get(day, {})
        # is_available = day <= current_day
        is_available = True  # Desbloquear todos los regalos para depuración
        gift_info = {
            "day": day,
            "available": is_available,
            "type": gift.get("type") if is_available else "locked",
            "content": gift.get("content") if is_available else None,
            "description": gift.get("description", gift.get("content")) if is_available else "Aún no disponible"
        }
        available_gifts.append(gift_info)
    
    return jsonify(available_gifts)

@app.route('/api/gift/<int:day>')
def get_gift(day):
    current_date = datetime.now()
    current_day = current_date.day
    
    if day > current_day:
        return jsonify({"error": "Este regalo aún no está disponible"}), 403
    
    gift = GIFTS.get(day)
    if not gift:
        return jsonify({"error": "Regalo no encontrado"}), 404
    
    # Verificar la ruta de la imagen si es de tipo imagen
    if gift['type'] == 'image':
        print(f"Directorio actual: {os.getcwd()}")
        print(f"Contenido de static/images/: {os.listdir('static/images/')}")
        original_path = gift['content']
        gift['content'] = verify_image_path(gift['content'])
        print(f"Original path: {original_path}")
        print(f"Verified path: {gift['content']}")
    
    print(f"Enviando datos del regalo: {gift}")
    return jsonify(gift)

if __name__ == '__main__':
    app.run(debug=True)