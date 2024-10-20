<script>
  import { onMount } from 'svelte'
  import * as THREE from 'three'

  let canvasRef
  let scene, camera, renderer, raycaster, cube, mouse

  onMount(() => {
    const canvas = canvasRef
    const { width, height } = canvas.getBoundingClientRect()

    scene = new THREE.Scene()
    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true })
    renderer.setSize(width, height)

    const geometry = new THREE.BoxGeometry(1, 1, 1)
    const material = new THREE.MeshBasicMaterial({ color: '#fff' })
    cube = new THREE.Mesh(geometry, material)
    scene.add(cube)

    camera.position.z = 5

    raycaster = new THREE.Raycaster()
    mouse = new THREE.Vector2()

    window.addEventListener('resize', () => {
      const { width, height } = canvas.getBoundingClientRect()
      camera.aspect = width / height
      camera.updateProjectionMatrix()
      renderer.setSize(width, height)
    })

    function animate() {
      requestAnimationFrame(animate)

      cube.rotation.x += 0.01
      cube.rotation.y += 0.01

      renderer.render(scene, camera)
    }

    animate()
  })
</script>

<div class="container">
  <canvas id="model" bind:this={canvasRef}></canvas>
  <div class="sidebar">
    <p>Рыба</p>
  </div>
</div>

<style>
  .container {
    display: flex;
    height: 100vh;
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
    flex-direction: column;
  }

  .sidebar p {
    font-size: 2rem;
  }
</style>
