<script>
  import { onMount } from 'svelte'
  import * as THREE from 'three'
  import { OrbitControls } from 'three/addons/controls/OrbitControls.js'

  const canvasRatio = 0.65

  let testModel = {
    voxels: [[0, 0, 0, [255, 255, 255]], [1, 0, 0, [255, 0, 0]], [1, 1, 0, [0, 255, 0]]],
    data: {}
  }

  let canvasRef
  let scene, camera, renderer, raycaster, mouse, controls
  let voxelsData = []
  let textData = []

  onMount(() => {
    const canvas = canvasRef
    const { width, height } = canvas.getBoundingClientRect()

    scene = new THREE.Scene()
    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true })
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

    voxelsData = testModel.voxels
    textData = Object.values(testModel.data)

    renderVoxels()

    function animate() {
      requestAnimationFrame(animate)
      controls.update()
      renderer.render(scene, camera)
    }

    animate()
  })

  function renderVoxels() {
    voxelsData.forEach((voxel) => {
      const [x, y, z, rgb] = voxel
      const geometry = new THREE.BoxGeometry(1, 1, 1)
      const material = new THREE.MeshBasicMaterial({
        color: new THREE.Color(`rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`),
      })
      const mesh = new THREE.Mesh(geometry, material)
      mesh.position.set(x, y, z)
      scene.add(mesh)
    })
  }
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