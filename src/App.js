import React, { useState, useRef } from 'react';
import './App.css';

// Surrealist color palette
const COLORS = [
  '#ff00cc', '#00ffcc', '#ccff00', '#ffcc00', '#00ccff', '#cc00ff', '#fff700', '#00fff7', '#f700ff', '#ff0077'
];

// Generates a random nonsense poem
function generatePoem() {
  const lines = [
    'The umbrella whispers to the moonlit toaster.',
    'Bananas pirouette on invisible trapezes.',
    'A clock melts into a puddle of giggles.',
    'Clouds wear shoes and tap-dance on spaghetti.',
    'The fish recite Shakespeare backwards.',
    'Cacti sing lullabies to neon jellybeans.',
    'A rubber duck ponders quantum philosophy.',
    'Marshmallow mountains dream of purple rain.',
    'The typewriter composes symphonies for ants.',
    'Invisible cats juggle rainbow pancakes.'
  ];
  let poem = '';
  for (let i = 0; i < 4; i++) {
    poem += lines[Math.floor(Math.random() * lines.length)] + '\n';
  }
  return poem;
}

// Generates a random surreal creature
function SurrealCreature({ seed }) {
  const size = 80 + Math.sin(seed) * 40;
  const color = COLORS[seed % COLORS.length];
  const eyeColor = COLORS[(seed + 3) % COLORS.length];
  const mouthColor = COLORS[(seed + 5) % COLORS.length];
  return (
    <svg width={size} height={size} style={{ margin: 16, filter: 'drop-shadow(0 0 12px ' + color + ')' }}>
      <ellipse cx={size/2} cy={size/2} rx={size/2.2} ry={size/2.7} fill={color} />
      <ellipse cx={size/2 - 15} cy={size/2 - 10} rx={8} ry={12} fill={eyeColor} />
      <ellipse cx={size/2 + 15} cy={size/2 - 10} rx={8} ry={12} fill={eyeColor} />
      <ellipse cx={size/2} cy={size/2 + 15} rx={18} ry={8} fill={mouthColor} />
      <circle cx={size/2 - 15} cy={size/2 - 10} r={3} fill="#222" />
      <circle cx={size/2 + 15} cy={size/2 - 10} r={3} fill="#222" />
      <ellipse cx={size/2} cy={size/2 + 15} rx={8} ry={3} fill="#222" />
      <ellipse cx={size/2} cy={size/2 - 30} rx={10} ry={5} fill={COLORS[(seed+7)%COLORS.length]} opacity="0.7" />
    </svg>
  );
}

function App() {
  const [poem, setPoem] = useState(generatePoem());
  const [creatures, setCreatures] = useState([0,1,2,3,4].map(i=>Math.floor(Math.random()*1000)));
  const [bgColor, setBgColor] = useState(COLORS[Math.floor(Math.random()*COLORS.length)]);
  const [absurdity, setAbsurdity] = useState(0);
  const audioRef = useRef();

  function randomizeAll() {
    setPoem(generatePoem());
    setCreatures([0,1,2,3,4].map(i=>Math.floor(Math.random()*1000)));
    setBgColor(COLORS[Math.floor(Math.random()*COLORS.length)]);
    setAbsurdity(absurdity+1);
    if (audioRef.current) {
      audioRef.current.currentTime = 0;
      audioRef.current.play().catch(() => {});
    }
  }

  return (
    <div className="App" style={{ background: `radial-gradient(circle, ${bgColor} 0%, #222 100%)`, minHeight: '100vh', transition: 'background 1s' }}>
      <header className="App-header">
        <h1 style={{ fontFamily: 'cursive', fontSize: '3rem', letterSpacing: '0.2em', color: COLORS[(absurdity+2)%COLORS.length], textShadow: '0 0 16px #fff' }}>
          Surrealist Playground
        </h1>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', margin: 24 }}>
          {creatures.map((seed, i) => <SurrealCreature key={i} seed={seed} />)}
        </div>
        <pre style={{ background: 'rgba(255,255,255,0.1)', color: '#fff', padding: 16, borderRadius: 12, fontSize: '1.2rem', maxWidth: 500, margin: '0 auto', boxShadow: '0 0 12px #000' }}>{poem}</pre>
        <button onClick={randomizeAll} style={{ marginTop: 32, padding: '16px 32px', fontSize: '1.3rem', borderRadius: 24, border: 'none', background: COLORS[(absurdity+4)%COLORS.length], color: '#222', cursor: 'pointer', boxShadow: '0 0 8px #fff', transition: 'background 0.5s' }}>
          Unleash More Absurdity
        </button>
        <audio ref={audioRef} src="https://cdn.pixabay.com/audio/2022/10/16/audio_12b8b8b6e7.mp3" preload="auto" />
        <p style={{ marginTop: 40, fontSize: '1.1rem', color: COLORS[(absurdity+6)%COLORS.length], textShadow: '0 0 8px #000' }}>
          Click the button to conjure new creatures, poems, and colors!<br/>
          Each click increases the absurdity of your universe.
        </p>
      </header>
    </div>
  );
}

export default App;
