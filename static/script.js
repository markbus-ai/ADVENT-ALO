document.addEventListener('DOMContentLoaded', async () => {
    console.log('Documento cargado');
    const calendar = document.querySelector('.calendar');
    calendar.innerHTML = ''; // Limpiar el calendario existente

    createSnowfall();
    createProgressTracker();

    try {
        const response = await fetch('/api/gifts');
        console.log('Respuesta de /api/gifts:', response);
        const gifts = await response.json();
        console.log('Regalos recibidos:', gifts);

        gifts.forEach(gift => {
            console.log('Creando tarjeta para el día:', gift.day);
            const dayCard = createDayCard(gift);
            calendar.appendChild(dayCard);
        });
        
        updateProgressTracker();
    } catch (error) {
        console.error('Error cargando los regalos:', error);
    }
});

function createSnowfall() {
    const snowContainer = document.createElement('div');
    snowContainer.className = 'snowfall-container';
    document.body.appendChild(snowContainer);

    const snowflakeCount = window.innerWidth < 768 ? 20 : 50;

    for (let i = 0; i < snowflakeCount; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        snowflake.textContent = '❄';
        
        snowflake.style.left = `${Math.random() * 100}%`;
        snowflake.style.animationDuration = `${10 + Math.random() * 20}s`;
        snowflake.style.fontSize = `${0.5 + Math.random() * 2}rem`;
        
        snowContainer.appendChild(snowflake);
    }
}

function createProgressTracker() {
    const progressContainer = document.createElement('div');
    progressContainer.className = 'progress-tracker';
    
    const progressText = document.createElement('span');
    progressText.textContent = 'Regalos abiertos';
    
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    
    const progressFill = document.createElement('div');
    progressFill.className = 'progress-fill';
    
    progressBar.appendChild(progressFill);
    progressContainer.appendChild(progressText);
    progressContainer.appendChild(progressBar);
    
    document.body.appendChild(progressContainer);
}

function updateProgressTracker() {
    const totalDays = 24;
    const openedDays = document.querySelectorAll('.day.opened').length;
    const progressFill = document.querySelector('.progress-fill');
    
    if (progressFill) {
        const percentage = (openedDays / totalDays) * 100;
        progressFill.style.width = `${percentage}%`;
    }
}

function createDayCard(gift) {
    const dayDiv = document.createElement('div');
    dayDiv.className = `day ${gift.available ? 'available' : 'locked'}`;
    dayDiv.setAttribute('data-day', gift.day);
    
    let contentPreview = '';
    if (gift.available) {
        switch (gift.type) {
            case 'text':
                contentPreview = `<p class="preview-text">${gift.content.substring(0, 30)}...</p>`;
                break;
            case 'image':
                contentPreview = '<i class="fas fa-image"></i>';
                break;
            case 'link':
                contentPreview = '<i class="fas fa-link"></i>';
                break;
            case 'poem':
                contentPreview = '<i class="fas fa-feather-alt"></i>';
                break;
            default:
                contentPreview = '<i class="fas fa-gift"></i>';
        }
    } else {
        contentPreview = '<i class="fas fa-lock"></i>';
    }

    let giftContent = '';
    if (gift.type === 'image') {
        giftContent = `
            <div class="gift-image-container">
                <div class="thumbnail-wrapper">
                    <img src="${gift.content}" class="gift-image" alt="Regalo del día" 
                        onerror="this.onerror=null; this.src='static/images/default.jpg'; console.log('Error cargando imagen, usando default');">
                </div>
                <div class="gift-description-wrapper">
                    <p class="gift-description">${gift.description}</p>
                </div>
            </div>`;
    } else if (gift.type === 'link') {
        giftContent = `
            <div class="link-container">
                <p class="gift-description">${gift.description}</p>
                <a href="${gift.content}" class="btn gift-link" target="_blank">
                    Abrir enlace
                </a>
            </div>`;
    } else if (gift.type === 'poem') {
        const poemContent = Array.isArray(gift.content) 
            ? gift.content 
            : typeof gift.content === 'string'
                ? gift.content.split('\n')
                : [gift.content];
        
        const poemHTML = poemContent
            .map(line => `<p class="poem-line">${line || '&nbsp;'}</p>`)
            .join('');
            
        const modalStyle = {
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: 400,
            backgroundColor: 'var(--color-christmas-red)',
            border: '2px solid var(--color-tinsel)',
            boxShadow: '0 8px 20px rgba(0, 0, 0, 0.4)',
            padding: '20px 30px',
            borderRadius: '12px',
            color: 'var(--color-white)',
            fontFamily: "'Playfair Display', serif",
            textAlign: 'center'
        };

        dayDiv.addEventListener('click', function() {
            if (!this.classList.contains('opened')) {
                this.classList.add('opened');
                const modal = document.createElement('div');
                modal.style.cssText = Object.entries(modalStyle).map(([key, value]) => `${key}: ${value}`).join(';');
                modal.innerHTML = poemHTML;
                
                const modalContainer = document.createElement('div');
                modalContainer.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    backdrop-filter: blur(5px);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    z-index: 1000;
                `;
                
                const closeBtn = document.createElement('button');
                closeBtn.textContent = '×';
                closeBtn.style.cssText = `
                    position: absolute;
                    right: 15px;
                    top: 10px;
                    background: none;
                    border: none;
                    color: var(--color-tinsel);
                    font-size: 30px;
                    cursor: pointer;
                `;
                
                closeBtn.onclick = () => modalContainer.remove();
                modal.appendChild(closeBtn);
                modalContainer.appendChild(modal);
                document.body.appendChild(modalContainer);
                
                modalContainer.onclick = (e) => {
                    if (e.target === modalContainer) modalContainer.remove();
                };
                
                updateProgressTracker();
                createSparkles(this);
            }
        });
    } else {
        giftContent = `<p>${gift.content || gift.description}</p>`;
    }

    dayDiv.innerHTML = `
        <div class="day-content">
            <div class="day-front">
                <span class="day-number">${gift.day}</span>
                <span class="day-label">Diciembre</span>
                <div class="preview-content">
                    ${contentPreview}
                </div>
            </div>
            <div class="gift-content">
                <h2>Día ${gift.day}</h2>
                ${giftContent}
            </div>
        </div>
    `;

    if (gift.available) {
        dayDiv.addEventListener('click', function() {
            const dayNumber = this.getAttribute('data-day');
            const giftContent = this.querySelector('.gift-content');
            const isOpened = this.classList.contains('opened');

            if (!isOpened) {
                this.classList.add('opened');
                giftContent.style.display = 'flex';
                updateProgressTracker();
                createSparkles(this);
            } else {
                this.classList.remove('opened');
                giftContent.style.display = 'none';
                updateProgressTracker();
            }
        });
    }

    return dayDiv;
}

function createSparkles(parent) {
    for (let i = 0; i < 10; i++) {
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle';
        sparkle.style.left = `${Math.random() * 100}%`;
        sparkle.style.top = `${Math.random() * 100}%`;
        parent.appendChild(sparkle);

        setTimeout(() => sparkle.remove(), 1000);
    }
}

const modal = document.getElementById('imageModal');
const modalImg = document.getElementById('modalImage');
const modalDesc = document.getElementById('modalDescription');
const closeModal = document.querySelector('.close-modal');

function openModal(imgSrc, description) {
    modal.style.display = "block";
    
    // Crear el contenido del modal con diseño navideño
    const modalContent = `
        <div class="modal-content christmas-theme">
            <div class="modal-header">
                <h2> Regalo del Día 🎄</h2>
                <span class="close-modal">✖</span>
            </div>
            <div class="modal-body">
                <div class="image-wrapper">
                    <img src="${imgSrc}" id="modalImage" alt="Regalo especial" 
                        onerror="this.onerror=null; this.src='static/images/default.jpg';">
                </div>
                <div class="description-wrapper">
                    <p class="modal-description">${description}</p>
                </div>
            </div>
            <div class="modal-footer">
                <span class="decoration">🎁</span>
                <span class="decoration">⭐</span>
                <span class="decoration">🎄</span>
            </div>
        </div>
    `;
    
    modal.innerHTML = modalContent;
    document.body.style.overflow = 'hidden';
    
    // Agregar efectos de nieve al modal
    addSnowEffect();
    
    // Actualizar los event listeners
    const closeBtn = modal.querySelector('.close-modal');
    closeBtn.onclick = function() {
        modal.style.display = "none";
        document.body.style.overflow = 'auto';
        removeSnowEffect();
    }
    
    modal.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
            document.body.style.overflow = 'auto';
            removeSnowEffect();
        }
    }
}

function addSnowEffect() {
    const snowflakes = 30;
    const modalContent = document.querySelector('.modal-content');
    
    for (let i = 0; i < snowflakes; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'modal-snowflake';
        snowflake.innerHTML = '❄';
        snowflake.style.left = `${Math.random() * 100}%`;
        snowflake.style.animationDuration = `${Math.random() * 3 + 2}s`;
        snowflake.style.animationDelay = `${Math.random() * 2}s`;
        snowflake.style.opacity = Math.random();
        snowflake.style.fontSize = `${Math.random() * 10 + 10}px`;
        modalContent.appendChild(snowflake);
    }
}

function removeSnowEffect() {
    const snowflakes = document.querySelectorAll('.modal-snowflake');
    snowflakes.forEach(snowflake => snowflake.remove());
}

window.onclick = function(event) {
    const modal = document.getElementById('poemModal');
    if (event.target === modal) {
        modal.style.display = "none";
        document.body.style.overflow = 'auto';
    }
}