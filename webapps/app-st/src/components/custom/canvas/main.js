import { Streamlit } from 'https://cdn.jsdelivr.net/npm/streamlit-component-lib@2.0.0/+esm'


const submitBtn = document.getElementById("submit");
submitBtn.addEventListener("click", sendDrawingValue);

const clearBtn = document.getElementById("clear");
clearBtn.addEventListener("click", clearCanvas)

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
ctx.lineWidth = 15;
ctx.lineCap = "round";
ctx.strokeStyle = "white";

let drawing = false;
let lastX = 0;
let lastY = 0;

canvas.addEventListener("mousedown", start);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stop);
canvas.addEventListener("mouseout", stop);

canvas.addEventListener("touchstart", handleTouchStart);
canvas.addEventListener("touchmove", handleTouchMove);
canvas.addEventListener("touchend", stop);

clearCanvas();

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, render);
Streamlit.setComponentReady();


function render(event) {
    Streamlit.setFrameHeight(document.documentElement.scrollHeight);
}

function clearCanvas() {
    console.log('clearing')
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function draw(e) {
    if (!drawing) return;
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

function getCanvasImageBase64() {
    const dataUrl = canvas.toDataURL("image/png");
    const imageBase64 = dataUrl.split(',')[1];

    return imageBase64;
}

function handleTouchMove(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    draw({ offsetX: touch.clientX - rect.left, offsetY: touch.clientY - rect.top });
}

function handleTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    start({ offsetX: touch.clientX - rect.left, offsetY: touch.clientY - rect.top });
}

function sendDrawingValue() {
    const value = JSON.stringify({
        image_base64: getCanvasImageBase64(),
    })
    Streamlit.setComponentValue(value);
}

function start(e) {
    drawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

function stop() {
    drawing = false;
}
