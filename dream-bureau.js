// The Interdimensional Cat Dream Bureau - JavaScript Engine
// Where chaos meets bureaucracy in the most delightful way

class CosmicCatBureau {
    constructor() {
        this.cats = [
            {
                name: "Sir Whiskers McPurrington III",
                role: "Chief Dream Architect",
                department: "Nightmare Debugging Division",
                speciality: "Recursive anxiety loops",
                mood: "Contemplatively caffeinated"
            },
            {
                name: "Professor Mittens von Fluffenstein",
                role: "Senior Lucidity Inspector",
                department: "Reality Compliance Department",
                speciality: "Physics violation reports",
                mood: "Perpetually perplexed"
            },
            {
                name: "Captain Snuggles the Magnificent",
                role: "Dream Quality Assurance Manager",
                department: "Surreal Experience Optimization",
                speciality: "Impossible geometry validation",
                mood: "Majestically judgmental"
            },
            {
                name: "Dr. Pawsworth Dreamweaver",
                role: "Interdimensional Therapist",
                department: "Subconscious Maintenance",
                speciality: "Existential crisis resolution",
                mood: "Zen-like but slightly annoyed"
            },
            {
                name: "Admiral Fluffytail Stardust",
                role: "Cosmic Dream Navigator",
                department: "Astral Projection Logistics",
                speciality: "Getting lost in space-time",
                mood: "Cosmically confused"
            },
            {
                name: "Baroness Whiskertons the Wise",
                role: "Ancient Dream Archivist",
                department: "Memory Palace Maintenance",
                speciality: "Forgetting where she put things",
                mood: "Mysteriously knowing"
            }
        ];
        
        this.dreamPoetryTemplates = [
            "In the {adjective} realm of {noun}, where {creature} {verb} through {place}, the {emotion} of {concept} {action} like {metaphor}.",
            "Behold! The {adjective} {noun} {verb} {adverb} while {creature} {action} in the {place} of {concept}.",
            "When {time} {verb} the {adjective} {noun}, {creature} {action} {emotion} through {place} like {metaphor}.",
            "In {number} dimensions of {concept}, the {adjective} {creature} {verb} {emotion} until {noun} {action}.",
            "The {adjective} {noun} whispers {emotion} to {creature} who {verb} through {place} seeking {concept}.",
            "Beyond the {adjective} {place}, where {creature} {action} {emotion}, the {noun} {verb} like {metaphor}.",
            "In the bureaucracy of {concept}, {creature} {verb} {adjective} {noun} while {emotion} {action} through {place}."
        ];
        
        this.wordBank = {
            adjective: ["ethereal", "bureaucratic", "luminescent", "paradoxical", "whimsical", "cosmic", "ineffable", "surreal", "transcendent", "absurd", "magnificent", "bewildering", "iridescent", "temporal", "quantum"],
            noun: ["paperwork", "dreams", "regulations", "consciousness", "reality", "forms", "procedures", "existence", "bureaucracy", "infinity", "protocols", "dimensions", "committees", "meetings", "deadlines"],
            creature: ["interdimensional cats", "cosmic kittens", "bureaucratic felines", "astral cats", "quantum kitties", "dream cats", "celestial felines", "administrative cats", "mystical kittens", "temporal cats"],
            verb: ["process", "file", "approve", "contemplate", "transcend", "organize", "categorize", "validate", "optimize", "harmonize", "synchronize", "bureaucratize", "mystify", "quantify", "purr at"],
            place: ["filing cabinets of eternity", "cosmic break rooms", "interdimensional offices", "astral meeting rooms", "quantum cubicles", "celestial archives", "bureaucratic voids", "temporal waiting rooms", "infinite hallways", "dream processing centers"],
            emotion: ["existential dread", "bureaucratic bliss", "cosmic confusion", "administrative anxiety", "transcendent boredom", "mystical frustration", "quantum uncertainty", "temporal melancholy", "infinite patience", "surreal satisfaction"],
            concept: ["proper procedure", "cosmic order", "administrative efficiency", "universal harmony", "bureaucratic perfection", "interdimensional compliance", "quantum regulations", "astral protocols", "temporal deadlines", "infinite paperwork"],
            action: ["meow mysteriously", "purr bureaucratically", "nap transcendentally", "file complaints", "stamp documents", "schedule meetings", "process applications", "validate existence", "organize chaos", "contemplate infinity"],
            metaphor: ["a cosmic hairball", "interdimensional yarn", "bureaucratic catnip", "quantum fish", "astral laser pointers", "temporal scratching posts", "celestial cardboard boxes", "mystical tuna cans", "infinite litter boxes", "cosmic cat treats"],
            time: ["yesterday's tomorrow", "next week's yesterday", "the eternal now", "bureaucratic time", "cosmic lunch break", "interdimensional Monday", "quantum weekend", "astral overtime", "temporal coffee break", "infinite deadline"],
            number: ["seventeen", "forty-two", "infinity minus one", "a bureaucratic dozen", "cosmic seven", "quantum eleven", "interdimensional nine", "astral thirteen", "temporal eight", "mystical twenty-three"],
            adverb: ["bureaucratically", "cosmically", "mysteriously", "efficiently", "transcendentally", "quantumly", "interdimensionally", "astrally", "temporally", "infinitely"]
        };
        
        this.dreamCounter = 42847;
        this.nightmaresProcessed = 1337;
        this.lucidDreams = 888;
        this.catNaps = 9999;
        
        this.init();
    }
    
    init() {
        this.createStars();
        this.createCatCards();
        this.startCosmicAnimations();
        this.updateCounters();
        this.spawnFloatingCats();
    }
    
    createStars() {
        const starsContainer = document.getElementById('stars');
        for (let i = 0; i < 100; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.width = star.style.height = (Math.random() * 3 + 1) + 'px';
            star.style.animationDelay = Math.random() * 2 + 's';
            starsContainer.appendChild(star);
        }
    }
    
    createCatCards() {
        const bureau = document.getElementById('catBureau');
        
        this.cats.forEach((cat, index) => {
            const card = document.createElement('div');
            card.className = 'cat-card';
            card.innerHTML = `
                <div class="cat-name">${cat.name}</div>
                <div class="cat-role">${cat.role}</div>
                <div class="cat-role" style="color: #4ecdc4; font-size: 0.8rem;">${cat.department}</div>
                <div class="cat-role" style="color: #ff6b6b; font-size: 0.8rem; margin-bottom: 10px;">Speciality: ${cat.speciality}</div>
                <div class="cat-role" style="color: #ffd700; font-size: 0.8rem; margin-bottom: 20px;">Current Mood: ${cat.mood}</div>
                <div class="dream-poem" id="poem-${index}">Click to generate a cosmic dream report...</div>
                <button class="generate-btn" onclick="bureau.generateDreamPoetry(${index})">Process Dream</button>
            `;
            bureau.appendChild(card);
        });
    }
    
    generateDreamPoetry(catIndex) {
        const poemElement = document.getElementById(`poem-${catIndex}`);
        const cat = this.cats[catIndex];
        
        // Add loading animation
        poemElement.innerHTML = "<div style='animation: pulse 1s infinite;'>🐱 Processing cosmic bureaucracy... 🌟</div>";
        
        setTimeout(() => {
            const template = this.getRandomElement(this.dreamPoetryTemplates);
            const poem = this.fillTemplate(template);
            
            poemElement.innerHTML = `
                <div style="font-style: italic; margin-bottom: 10px; color: #4ecdc4;">Dream Report #${Math.floor(Math.random() * 999999)}</div>
                <div style="margin-bottom: 10px;">${poem}</div>
                <div style="font-size: 0.8rem; color: #b0b0b0; margin-top: 15px;">— Processed by ${cat.name}</div>
                <div style="font-size: 0.7rem; color: #888; margin-top: 5px;">Status: ${this.getRandomElement(['Approved', 'Pending Review', 'Requires More Catnip', 'Cosmically Compliant', 'Mysteriously Valid'])}</div>
            `;
            
            this.updateCounters();
            this.createFloatingEmoji();
        }, 1500);
    }
    
    fillTemplate(template) {
        let filledTemplate = template;
        
        // Replace all placeholders with random words
        Object.keys(this.wordBank).forEach(category => {
            const regex = new RegExp(`{${category}}`, 'g');
            filledTemplate = filledTemplate.replace(regex, () => {
                return this.getRandomElement(this.wordBank[category]);
            });
        });
        
        return filledTemplate;
    }
    
    getRandomElement(array) {
        return array[Math.floor(Math.random() * array.length)];
    }
    
    updateCounters() {
        this.dreamCounter += Math.floor(Math.random() * 50) + 1;
        this.nightmaresProcessed += Math.floor(Math.random() * 5) + 1;
        this.lucidDreams += Math.floor(Math.random() * 3) + 1;
        this.catNaps += Math.floor(Math.random() * 10) + 1;
        
        document.getElementById('dreamCounter').textContent = this.dreamCounter.toLocaleString();
        document.getElementById('nightmaresProcessed').textContent = this.nightmaresProcessed.toLocaleString();
        document.getElementById('lucidDreams').textContent = this.lucidDreams.toLocaleString();
        document.getElementById('catNaps').textContent = this.catNaps.toLocaleString();
    }
    
    createFloatingEmoji() {
        const emojis = ['🐱', '😸', '😺', '😻', '🙀', '😿', '😾', '🌟', '✨', '🌙', '💫', '🔮', '🎭', '📋', '📝'];
        const emoji = document.createElement('div');
        emoji.textContent = this.getRandomElement(emojis);
        emoji.style.position = 'fixed';
        emoji.style.left = Math.random() * window.innerWidth + 'px';
        emoji.style.top = window.innerHeight + 'px';
        emoji.style.fontSize = (Math.random() * 20 + 20) + 'px';
        emoji.style.zIndex = '1000';
        emoji.style.pointerEvents = 'none';
        emoji.style.animation = 'floatUp 3s ease-out forwards';
        
        document.body.appendChild(emoji);
        
        setTimeout(() => {
            emoji.remove();
        }, 3000);
    }
    
    spawnFloatingCats() {
        setInterval(() => {
            const catEmojis = ['🐱', '😸', '😺', '😻', '🙀', '😿', '😾'];
            const cat = document.createElement('div');
            cat.className = 'floating-cat';
            cat.textContent = this.getRandomElement(catEmojis);
            cat.style.top = Math.random() * (window.innerHeight - 100) + 'px';
            cat.style.animationDuration = (Math.random() * 10 + 10) + 's';
            
            document.body.appendChild(cat);
            
            setTimeout(() => {
                cat.remove();
            }, 25000);
        }, 8000);
    }
    
    startCosmicAnimations() {
        // Add floating animation keyframes
        const style = document.createElement('style');
        style.textContent = `
            @keyframes floatUp {
                0% {
                    transform: translateY(0px) rotate(0deg);
                    opacity: 1;
                }
                100% {
                    transform: translateY(-${window.innerHeight + 100}px) rotate(360deg);
                    opacity: 0;
                }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
        `;
        document.head.appendChild(style);
        
        // Random counter updates
        setInterval(() => {
            this.updateCounters();
        }, 5000);
        
        // Random cosmic events
        setInterval(() => {
            this.triggerCosmicEvent();
        }, 15000);
    }
    
    triggerCosmicEvent() {
        const events = [
            () => this.createCosmicNotification("🌟 Interdimensional coffee break initiated"),
            () => this.createCosmicNotification("📋 New regulation: All dreams must now include cats"),
            () => this.createCosmicNotification("🔮 Quantum entanglement detected in filing cabinet B-42"),
            () => this.createCosmicNotification("😸 Sir Whiskers has approved 847 dreams in 0.3 seconds"),
            () => this.createCosmicNotification("🌙 Night shift cats reporting for duty"),
            () => this.createCosmicNotification("✨ Reality.exe has stopped working, restarting..."),
            () => this.createCosmicNotification("🎭 Drama detected in Sector 7, dispatching therapy cats"),
            () => this.temporarilyChangeTitle()
        ];
        
        const randomEvent = this.getRandomElement(events);
        randomEvent();
    }
    
    createCosmicNotification(message) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            padding: 15px 20px;
            color: #e0e0e0;
            font-family: 'Comfortaa', cursive;
            font-size: 0.9rem;
            z-index: 10000;
            animation: slideInRight 0.5s ease-out, fadeOut 0.5s ease-in 4.5s forwards;
            max-width: 300px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        `;
        notification.textContent = message;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
            style.remove();
        }, 5000);
    }
    
    temporarilyChangeTitle() {
        const titleElement = document.querySelector('.title');
        const originalTitle = titleElement.textContent;
        const funnyTitles = [
            "The Interdimensional Cat Nap Bureau",
            "The Intergalactic Feline Filing Department",
            "The Cosmic Kitty Complaint Center",
            "The Astral Cat Administrative Agency",
            "The Quantum Purr Processing Plant",
            "The Mystical Meow Management Ministry"
        ];
        
        titleElement.textContent = this.getRandomElement(funnyTitles);
        
        setTimeout(() => {
            titleElement.textContent = originalTitle;
        }, 3000);
    }
}

// Initialize the cosmic cat bureau when the page loads
let bureau;
window.addEventListener('DOMContentLoaded', () => {
    bureau = new CosmicCatBureau();
});

// Add some extra cosmic interactions
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('cat-card') || e.target.closest('.cat-card')) {
        // Create sparkle effect on click
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                const sparkle = document.createElement('div');
                sparkle.textContent = '✨';
                sparkle.style.cssText = `
                    position: fixed;
                    left: ${e.clientX + (Math.random() - 0.5) * 100}px;
                    top: ${e.clientY + (Math.random() - 0.5) * 100}px;
                    font-size: ${Math.random() * 20 + 10}px;
                    z-index: 10000;
                    pointer-events: none;
                    animation: sparkleFloat 2s ease-out forwards;
                `;
                document.body.appendChild(sparkle);
                
                setTimeout(() => sparkle.remove(), 2000);
            }, i * 100);
        }
    }
});

// Add sparkle animation
const sparkleStyle = document.createElement('style');
sparkleStyle.textContent = `
    @keyframes sparkleFloat {
        0% {
            transform: translateY(0px) scale(1) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) scale(0) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(sparkleStyle);

// Konami code easter egg for extra absurdity
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.code);
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    
    if (JSON.stringify(konamiCode) === JSON.stringify(konamiSequence)) {
        activateUltraCosmicMode();
        konamiCode = [];
    }
});

function activateUltraCosmicMode() {
    document.body.style.animation = 'rainbow 0.5s infinite';
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes rainbow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
    
    // Spawn many cats
    for (let i = 0; i < 20; i++) {
        setTimeout(() => {
            bureau.createFloatingEmoji();
        }, i * 200);
    }
    
    bureau.createCosmicNotification("🌈 ULTRA COSMIC MODE ACTIVATED! 🌈");
    
    setTimeout(() => {
        document.body.style.animation = '';
        style.remove();
    }, 10000);
}