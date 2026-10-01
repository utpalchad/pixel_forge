"use client";
import {Canvas,useFrame} from "@react-three/fiber";
import {Environment,Float,OrbitControls} from "@react-three/drei";
import {useRef} from "react";
import * as THREE from "three";
function Form(){const group=useRef<THREE.Group>(null);useFrame((s,d)=>{if(group.current){group.current.rotation.y+=d*.08;group.current.rotation.x=THREE.MathUtils.lerp(group.current.rotation.x,s.pointer.y*.18,.04);}});return <group ref={group}><Float speed={1.4} rotationIntensity={.22} floatIntensity={.45}><mesh castShadow><torusKnotGeometry args={[1.42,.46,180,28,2,3]}/><meshStandardMaterial color="#d9ff43" roughness={.2} metalness={.15}/></mesh><mesh scale={1.015}><torusKnotGeometry args={[1.42,.46,80,16,2,3]}/><meshBasicMaterial color="#10120d" wireframe transparent opacity={.14}/></mesh></Float></group>}
export default function ForgeScene(){return <Canvas camera={{position:[0,0,5.8],fov:42}} dpr={[1,1.6]}><ambientLight intensity={1.1}/><directionalLight position={[3,4,4]} intensity={3}/><Form/><Environment preset="studio"/><OrbitControls enablePan={false} enableZoom={false} autoRotate autoRotateSpeed={.35}/></Canvas>}
