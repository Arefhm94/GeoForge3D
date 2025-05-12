import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function EarthBackground() {
  const containerRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (!containerRef.current) return;
    
    // Setup scene
    const scene = new THREE.Scene();
    
    // Setup camera
    const camera = new THREE.PerspectiveCamera(
      60, 
      window.innerWidth / window.innerHeight, 
      0.1, 
      1000
    );
    camera.position.z = 2.5;
    
    // Setup renderer
    const renderer = new THREE.WebGLRenderer({ 
      antialias: true,
      alpha: true 
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    // Clear any existing canvas
    if (containerRef.current.firstChild) {
      containerRef.current.removeChild(containerRef.current.firstChild);
    }
    
    containerRef.current.appendChild(renderer.domElement);
    
    // Create Earth
    const geometry = new THREE.SphereGeometry(1, 64, 64);
    
    // Earth materials
    const material = new THREE.MeshPhongMaterial({
      color: 0x0077be,
      emissive: 0x112244,
      specular: 0x99ccff,
      shininess: 30,
      transparent: true,
      opacity: 0.8
    });
    
    const earth = new THREE.Mesh(geometry, material);
    scene.add(earth);
    
    // Add glow effect
    const glowGeometry = new THREE.SphereGeometry(1.1, 64, 64);
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: 0x0088ff,
      transparent: true,
      opacity: 0.1,
      side: THREE.BackSide
    });
    const glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
    scene.add(glowMesh);
    
    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0x444444);
    scene.add(ambientLight);
    
    // Add directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 3, 5);
    scene.add(directionalLight);
    
    // Handle window resize
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    
    window.addEventListener('resize', handleResize);
    
    // Animation loop
    let animationFrameId: number;
    
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      
      earth.rotation.y += 0.001;
      glowMesh.rotation.y += 0.001;
      
      renderer.render(scene, camera);
    };
    
    animate();
    
    // Clean up on unmount
    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      scene.remove(earth);
      scene.remove(glowMesh);
      geometry.dispose();
      glowGeometry.dispose();
      material.dispose();
      glowMaterial.dispose();
      renderer.dispose();
      
      if (containerRef.current && containerRef.current.contains(renderer.domElement)) {
        containerRef.current.removeChild(renderer.domElement);
      }
    };
  }, []);
  
  return (
    <div 
      ref={containerRef}
      className="fixed inset-0 z-0 bg-gradient-to-b from-black to-blue-950"
    />
  );
}