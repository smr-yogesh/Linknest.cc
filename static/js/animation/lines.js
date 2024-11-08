document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.createElement('canvas');
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const dots = [];

    // Initialize dots with random positions and velocities
    for (let i = 0; i < 100; i++) {
        dots.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 2,
            vx: Math.random() * 2 - 1,
            vy: Math.random() * 2 - 1
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = 'rgba(0, 102, 0, 0.2)'; // Dark green color with low opacity for lines
        ctx.fillStyle = 'rgba(0, 102, 0, 0.2)';   // Dark green color with low opacity for dots

        // Draw dots and lines between nearby dots
        for (let i = 0; i < dots.length; i++) {
            const dot = dots[i];

            // Draw each dot
            ctx.beginPath();
            ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
            ctx.fill();

            // Update dot position
            dot.x += dot.vx;
            dot.y += dot.vy;

            // Reverse direction if dot hits the canvas edge
            if (dot.x > canvas.width || dot.x < 0) dot.vx = -dot.vx;
            if (dot.y > canvas.height || dot.y < 0) dot.vy = -dot.vy;

            // Check distance to other dots and draw lines between close ones
            for (let j = i + 1; j < dots.length; j++) {
                const otherDot = dots[j];
                const dx = otherDot.x - dot.x;
                const dy = otherDot.y - dot.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) { // Adjust this distance for more/less connection density
                    ctx.beginPath();
                    ctx.moveTo(dot.x, dot.y);
                    ctx.lineTo(otherDot.x, otherDot.y);
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(draw);
    }

    draw();
});