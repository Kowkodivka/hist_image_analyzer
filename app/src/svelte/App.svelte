<script>
  import { onMount } from 'svelte'
  import * as THREE from 'three'
  import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
  import { OBJLoader } from 'three/addons/loaders/OBJLoader.js'

  const canvasRatio = 0.65

  let path = '/home/kowkodivka/Документы/hist_image_analyzer/backend/output.obj'

  let canvasRef
  let loader, scene, camera, renderer, raycaster, mouse, controls

  onMount(() => {
    const canvas = canvasRef
    const { width, height } = canvas.getBoundingClientRect()

    scene = new THREE.Scene()
    scene.background = new THREE.Color(0x222222)

    loader = new OBJLoader()
    loader.load(
      path,
      (model) => {
        model.position.set(0, 0, 0)
        scene.add(model)
      },
      (xhr) => {
        console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
      },
      (error) => {
        console.log('An error happened: ' + error)
      }
    )

    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)

    renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true })
    renderer.setSize(width, height)

    controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.05
    controls.rotateSpeed = 0.5
    controls.enablePan = true
    controls.minDistance = 1
    controls.maxDistance = 100

    camera.position.z = 5

    raycaster = new THREE.Raycaster()
    mouse = new THREE.Vector2()

    window.addEventListener('resize', () => {
      const width = window.innerWidth * canvasRatio
      const height = window.innerHeight
      camera.aspect = width / height
      camera.updateProjectionMatrix()
      renderer.setSize(width, height)
    })

    canvasRef.addEventListener('click', onClick, false)

    function onClick(event) {
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1

      raycaster.setFromCamera(mouse, camera)
    }

    function animate() {
      requestAnimationFrame(animate)
      controls.update()
      renderer.render(scene, camera)
    }

    animate()
  })
</script>

<div class="container">
  <canvas bind:this={canvasRef}></canvas>
  <div class="sidebar"></div>
</div>

<style>
  .container {
    display: flex;
    height: 100vh;
  }

  canvas {
    width: 65%;
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
    color: #fff;
  }
</style>
