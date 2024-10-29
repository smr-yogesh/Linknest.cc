const canvas = document.createElement('canvas');
document.body.appendChild(canvas);
const ctx = canvas.getContext('2d');

// Set canvas to cover the entire viewport
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

const dots = [];
const mouse = { x: 0, y: 0 };

window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

for (let i = 0; i < 100; i++) {
    dots.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 4,
        vx: Math.random() * 2 - 1,
        vy: Math.random() * 2 - 1
    });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#006600';

    for (let i = 0; i < dots.length; i++) {
        const dot = dots[i];

        ctx.beginPath();
        ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
        ctx.fillStyle = '#006600';
        ctx.fill();

        dot.x += dot.vx;
        dot.y += dot.vy;

        if (dot.x > canvas.width || dot.x < 0) {
            dot.vx = -dot.vx;
        }

        if (dot.y > canvas.height || dot.y < 0) {
            dot.vy = -dot.vy;
        }

        const dx = mouse.x - dot.x;
        const dy = mouse.y - dot.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
            ctx.beginPath();
            ctx.moveTo(dot.x, dot.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.stroke();
        }
    }

    requestAnimationFrame(draw);
}
draw();
