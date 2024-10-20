<script>
    let canvasRef;
</script>

<style>
    .container {
        display: flex;
        height: 100%;
    }

    canvas {
        width: 65%;
        height: 100%;
        background-color: #222;
    }

    .sidebar {
        width: 35%;
        background-color: #333;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .sidebar p {
        font-size: 2rem;
    }
</style>

<div class="container">
    <canvas bind:this={canvasRef}></canvas>
    <div class="sidebar">
        <p>Рыба</p>
    </div>
</div>