"use client";
import {Canvas,useFrame} from "@react-three/fiber";
import {Grid,OrbitControls} from "@react-three/drei";
import {useRef} from "react";
import * as THREE from "three";
function Model({depth,wire}:{depth:number,wire:boolean}){const m=useRef<THREE.Mesh>(null);useFrame((_,d)=>{if(m.current)m.current.rotation.y+=d*.08});return <mesh ref={m} scale={[1,1,.65+depth/140]} rotation={[-.25,.3,0]}><icosahedronGeometry args={[1.5,5]}/><meshStandardMaterial color="#d9ff43" roughness={.32} metalness={.08} wireframe={wire}/></mesh>}
export default function StudioScene({depth,wire}:{depth:number,wire:boolean}){return <Canvas camera={{position:[0,1,5],fov:42}} dpr={[1,1.5]}><color attach="background" args={["#10110e"]}/><ambientLight intensity={1.5}/><directionalLight position={[4,5,3]} intensity={3}/><Model depth={depth} wire={wire}/><Grid position={[0,-1.9,0]} args={[10,10]} cellSize={.4} cellThickness={.4} cellColor="#34362d" sectionColor="#555947" fadeDistance={8}/><OrbitControls enablePan={false} minDistance={3} maxDistance={8}/></Canvas>}
