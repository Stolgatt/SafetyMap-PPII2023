const canvas = document.createElement('canvas');
canvas.width = window.innerWidth * 0.8;
canvas.height = window.innerHeight * 0.6;
canvas.style.position = 'absolute';
canvas.style.left = '50%';
canvas.style.top = '70%';
canvas.style.transform = 'translate(-50%, -50%)';
const ctx = canvas.getContext('2d');
document.body.appendChild(canvas);

let squareX = 50;
let squareY = canvas.height;
const squareSize = 50;
let squareVelocityY = 0;

let obstacleX = canvas.width;
const obstacleY = canvas.height - squareSize;
const obstacleSize = 50;
let obstacleSpeed = 5;
const obstacleSpeedIncrease = 10;

document.addEventListener('keydown', (event) => {
    if ((event.code === 'Space' || event.code === 'ArrowUp') && squareY === canvas.height - squareSize) {
        squareVelocityY = -20;
    }
    if (event.code === 'ArrowDown' && squareY < canvas.height - squareSize) {
        squareVelocityY = 20;
    }
});

let score = 0;
let gameRunning = true;
let lastTime = Date.now();

function resetGame() {
    if (score > 0) {
        fetch('/scores', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": document.getElementById('csrf_token').value
            },
            body: JSON.stringify({ score: score })
        }).then(response => response.json())
          .then(data => console.log(data));
    }

    squareX = 50;
    squareY = canvas.height;
    squareVelocityY = 0;
    obstacleSpeed = 5;

    obstacleX = canvas.width;

    score = 0;

    gameRunning = true;
    gameLoop();
}

function gameLoop() {
    const currentTime = Date.now();
    const deltaTime = (currentTime - lastTime) / 1000;

    squareY += squareVelocityY;
    squareVelocityY += 1;

    if (squareY > canvas.height - squareSize) {
        squareY = canvas.height - squareSize;
        squareVelocityY = 0;
    }

    obstacleSpeed += obstacleSpeedIncrease * deltaTime;
    obstacleX -= obstacleSpeed;

    if (obstacleX < -obstacleSize) {
        obstacleX = canvas.width;
    }

    if (obstacleX + obstacleSize < squareX) {
        score++;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = 'blue';
    ctx.fillRect(squareX, squareY, squareSize, squareSize);

    ctx.fillStyle = 'red';
    ctx.fillRect(obstacleX, obstacleY, obstacleSize, obstacleSize);

    ctx.fillStyle = 'black';
    ctx.font = '20px Arial';
    ctx.fillText(`Score: ${score}`, 10, 30);

    if (
        squareX < obstacleX + obstacleSize &&
        squareX + squareSize > obstacleX &&
        squareY < obstacleY + obstacleSize &&
        squareY + squareSize > obstacleY
    ) {
        gameRunning = false;
        setTimeout(resetGame, 1000);
    } else {
        if (gameRunning) {
            requestAnimationFrame(gameLoop);
        }
    }

    lastTime = currentTime;
}

gameLoop();