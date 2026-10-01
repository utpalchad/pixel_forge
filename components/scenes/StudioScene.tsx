"use client";
import {Canvas,useFrame} from "@react-three/fiber";
import {Grid,OrbitControls} from "@react-three/drei";
import {useRef} from "react";
import * as THREE from "three";

function Model({depth,wire}:{depth:number,wire:boolean}){
  const m=useRef<THREE.Mesh>(null);
  useFrame((s,d)=>{
    if(m.current){
      m.current.rotation.y+=d*.08;
      m.current.rotation.x=THREE.MathUtils.lerp(m.current.rotation.x,-.25+s.pointer.y*.08,.04);
    }
  });
  return <mesh ref={m} scale={[1,1,.65+depth/140]} rotation={[-.25,.3,0]}>
    <icosahedronGeometry args={[1.5,5]}/>
    <meshPhysicalMaterial color={wire?"#5ff7ff":"#8a4dff"} roughness={.26} metalness={.12} clearcoat={1} wireframe={wire}/>
  </mesh>
}

export default function StudioScene({depth,wire}:{depth:number,wire:boolean}){
  return <Canvas camera={{position:[0,1,5],fov:42}} dpr={[1,1.5]}>
    <color attach="background" args={["#0d0d16"]}/>
    <ambientLight intensity={1.0}/>
    <directionalLight position={[4,5,3]} intensity={2.2} color="#ffffff"/>
    <pointLight position={[-3,2,2]} intensity={26} distance={8} color="#ff4fd8"/>
    <pointLight position={[3,0,2]} intensity={24} distance={8} color="#57e6ff"/>
    <pointLight position={[0,-1,3]} intensity={18} distance={7} color="#ff8a3d"/>
    <Model depth={depth} wire={wire}/>
    <Grid position={[0,-1.9,0]} args={[10,10]} cellSize={.4} cellThickness={.4} cellColor="#31264a" sectionColor="#5ff7ff" fadeDistance={8}/>
    <OrbitControls enablePan={false} minDistance={3} maxDistance={8}/>
  </Canvas>
}
