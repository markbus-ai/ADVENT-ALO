import asyncio
from flask import Flask, render_template, jsonify, url_for, request
from datetime import datetime
import os
import aiohttp
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Lista de regalos para el calendario de adviento
GIFTS = {
    1: {
        "type": "text",
        "content": "primer dia del calendario, espero te guste lo hice con mucho amor"
    },
    2: {
        "type": "text",
        "content": "De todas las personas en el mundo, mi corazón se quedo con vos. y todos los dias confirmo que fue la mejor decision "
    },
    3: {
        "type": "image",
        "content": "static/images/imgday3.jpg",
        "description": "Nuestra primer foto como novios "
    },
    4: {
        "type": "text",
        "content": "Cupon valido por 10 minutos de masajes "
    },
    5: {
        "type": "link",
        "content": "https://open.spotify.com/intl-es/track/7b9hpzFQJaKUAAKsOeDafS",
        "description": "Cada vez que la escucho, pienso en vos "
    },
    6: {
        "type": "text",
        "content": "Me encanta como me miras, como me haces reír, cómo me cuidas. Me encantas vos"
    },
    7: {
        "type": "image",
        "content": "static/images/imgday7.jpg",
        "description": "Un momento especial juntos Porque cumplimos 1 año juntos"
    },
    8: {
        "type": "text",
        "content": "8 razones por las que te amo: Tu sonrisa, tu bondad, tu fortaleza, tu humor, tu Pelo, tu pasión, tu lealtad y tu forma de amar "
    },
    9: {
        "type": "link",
        "content": "https://open.spotify.com/playlist/40MgWg7bEJYjAaHAKSq8K3",
        "description": "Una playlist especial para vos - Todas las canciones que me hacen acordar a nosotros "
    },
    10: {
        "type": "link",
        "content": "static/love-puzzle.html",
        "description": "Un rompecabezas con nuestra foto favorita - ¡Armalo para ver un mensaje especial! "
    },
    11: {
        "type": "link",
        "content": "https://open.spotify.com/intl-es/track/4J2HLNTxiVxxs6kWgTIN43",
        "description": "Nuestra canción - La primera que te dedique "
    },
    12: {
        "type": "link",
        "content": "static/our_story.html",
        "description": "el dia en el que te conoci "
    },
    13: {
        "type": "text",
        "content": "Sos la persona que me hace sentir completo, que me inspira a ser mejor cada día, y que llena mi vida de amor y alegría. No cambiaría ni un solo momento juntos ",
        "description": "Un pensamiento desde el corazón "
    },
    14: {
        "type": "link",
        "content": "static/memory_lane.html",
        "description": "Un recorrido virtual por nuestros momentos especiales juntos "
    },
    15: {
        "type": "text",
        "content": "Otra cosa que me encanta de vos es tu forma de ser tan auténtica y única. Me haces sentir especial cada día ",
        "description": "Un pensamiento del corazón "
    },
    16: {
        "type": "poem",
        "content": [
            "Cada estrella en el cielo",
            "Es un te amo que te envío",
            "Cada rayo de sol al amanecer",
            "Es mi sonrisa al pensarte",
            "Cada gota de lluvia",
            "Es un beso que guardo para vos",
            "Y cada latido de mi corazón",
            "Tiene grabado tu nombre "
        ],
        "description": "Un poema que escribí pensando en vos "
    },
    17: {
        "type": "link",
        "content": "static/quiz/our_love.html",
        "description": "Un quiz interactivo sobre nuestra historia"
    },
    18: {
        "type": "text",
        "content": "Cada vez que veo tu sonrisa, mi mundo se ilumina. Me encanta cómo tus ojos brillan cuando estás feliz y cómo tu risa puede alegrar hasta el día más gris. Sos mi rayito de sol ",
        "description": "Un pensamiento especial para vos "
    },
    19: {
        "type": "text",
        "content": "Cada vez que veo tu sonrisa, mi mundo se ilumina. Me encanta cómo tus ojos brillan cuando estás feliz y cómo tu risa puede alegrar hasta el día más gris. Sos mi rayito de sol ",
        "description": "Un pensamiento especial para vos "
    },
    20: {
        "type": "link",
        "content": "static/mosaic/collage.html",
        "description": "Un mosaico gigante hecho con cientos de nuestras fotos juntos que forma un corazón "
    },
    21: {
        "type": "text",
        "content": "Hoy me acuerdo cuando te pedi ser novios. Estabamos en el aldrey, nervioso pero seguro, y en ese momento mi vida cambió para siempre. Cada día agradezco habertelo pedido ",
        "description": "Un recuerdo especial de nosotros "
    },
    22: {
        "type": "link",
        "content": "static/garden/jardin_virtual.html", 
        "description": "Un jardín virtual donde cada flor representa un momento especial juntos. ¡Puedes regar las flores y verlas crecer! "
    },
    23: {
        "type": "link",
        "content": "static/christmas_countdown.html",
        "description": "Cuenta regresiva personalizada para Navidad - Con mensajes especiales cada hora "
    },
    24: {
        "type": "text",
        "content": "Cada día que pasa me enamoro más de tu sonrisa, de tu forma de ser, de cómo me haces sentir. Sos mi persona favorita en todo el mundo y no puedo imaginar mi vida sin vos ",
        "description": "Un mensaje desde el corazón "
    },
    25: {
        "type": "link",
        "content": "static/christmas/decorar_arbol.html",
        "description": "¡Feliz Navidad mi amor! Un árbol de Navidad virtual que podés decorar a tu gusto con luces, adornos, guirnaldas y hasta poner regalitos debajo. ¡Guardá tu diseño y compartilo conmigo! "
    }
}

@app.route('/ping')
def ping():
    return 'pong'

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
    current_date = datetime.now()
    current_day = current_date.day
    
    available_gifts = []
    for day in range(1, 26):
        gift = GIFTS.get(day, {})
        is_available = day <= current_day
        #is_available = True  # Desbloquear todos los regalos para depuración
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
    # Manejar el tipo poema
    elif gift['type'] == 'poem':
        # Convertir el contenido del poema en una lista de líneas
        gift['content'] = gift['content'].split('\n')
    
    print(f"Enviando datos del regalo: {gift}")
    return jsonify(gift)

@app.route('/upload_photos', methods=['POST'])
def upload_photos():
    if 'photos[]' not in request.files:
        return jsonify({'error': 'No se encontraron archivos'}), 400
    
    uploaded_files = request.files.getlist('photos[]')
    saved_files = []
    
    upload_folder = os.path.join(app.static_folder, 'mosaic', 'source_images')
    os.makedirs(upload_folder, exist_ok=True)
    
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Asegurar que el nombre del archivo sea único
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(upload_folder, filename)):
                filename = f"{base}_{counter}{ext}"
                counter += 1
            
            file.save(os.path.join(upload_folder, filename))
            saved_files.append(filename)
    
    return jsonify({'files': saved_files})

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def keep_alive():
    """Hace ping al servidor cada 5 minutos para mantenerlo activo"""
    app_url = 'https://advent-alo.onrender.com'
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{app_url}/ping") as response:
                    print(f"Ping status: {response.status}")
            await asyncio.sleep(300)  # 5 minutos
        except aiohttp.ClientError as e:
            print(f"Error en keep_alive: {e}")
        except Exception as e:
            print(f"Unexpected error in keep_alive: {e}")
        await asyncio.sleep(60)  # Espera 1 minuto antes de reintentar

from threading import Thread

def start_keep_alive():
    asyncio.run(keep_alive())

if __name__ == "__main__":
    # Iniciar la tarea en segundo plano
    Thread(target=start_keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=8000, debug=True)
