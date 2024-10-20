<script>
  import { onMount } from 'svelte';
  import * as THREE from 'three';
  import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

  let canvasRef;
  let scene, camera, renderer, raycaster, cube, mouse, controls;

  onMount(() => {
    const canvas = canvasRef;
    const { width, height } = canvas.getBoundingClientRect();

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(width, height);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.rotateSpeed = 0.5;
    controls.enablePan = true;
    controls.minDistance = 1;
    controls.maxDistance = 10;

    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: '#fff' });
    cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    camera.position.z = 5;

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    window.addEventListener('resize', () => {
      const width = window.innerWidth * 0.65;
      const height = window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    });

    canvasRef.addEventListener('click', onClick, false);

    function onClick(event) {
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);

      const intersects = raycaster.intersectObjects([cube]);

      if (intersects.length > 0) {
        console.log('Cube clicked!');
      }
    }

    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }

    animate();
  });
</script>

<div class="container">
  <canvas id="model" bind:this={canvasRef}></canvas>
  <div class="sidebar">
    <p>This is a sidebar</p>
  </div>
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