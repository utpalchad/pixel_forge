"use client";
import dynamic from "next/dynamic";
import {ArrowDown,Move3d} from "lucide-react";
import {useEffect,useRef} from "react";
import gsap from "gsap";
const ForgeScene=dynamic(()=>import("./scenes/ForgeScene"),{ssr:false});

export default function Hero(){
  const root=useRef<HTMLElement>(null);
  useEffect(()=>{
    const ctx=gsap.context(()=>{
      gsap.from(".heroWord",{y:120,opacity:0,rotateX:-28,stagger:.11,duration:1.15,ease:"power4.out"});
      gsap.from(".heroCopy p",{y:28,opacity:0,duration:.8,delay:.5,ease:"power3.out"});
      gsap.from(".primary",{scale:.88,opacity:0,duration:.7,delay:.7,ease:"back.out(1.8)"});
      gsap.from(".eyebrow,.dragHint,.scrollHint,.heroIndex",{opacity:0,y:12,stagger:.08,duration:.6,delay:.9});
      gsap.to(".heroScene",{y:-14,duration:3.8,ease:"sine.inOut",repeat:-1,yoyo:true});
    },root);
    return()=>ctx.revert();
  },[]);

  return <section className="hero" ref={root}>
    <div className="heroGrid"/>
    <div className="colorOrb orbOne"/>
    <div className="colorOrb orbTwo"/>
    <div className="colorOrb orbThree"/>
    <div className="eyebrow"><span className="pulse"/>IMAGE → GEOMETRY / 001</div>
    <div className="heroCopy">
      <h1>
        <span className="heroLine"><span className="heroWord">TURN</span></span>
        <span className="heroLine"><span className="heroWord chroma">PIXELS</span></span>
        <span className="heroLine"><span className="heroWord">INTO <b>FORM.</b></span></span>
      </h1>
      <p>Transform ordinary images into tactile digital geometry. Shape depth, explore the mesh, export the object.</p>
      <a href="#studio" className="primary">ENTER THE FORGE <span>↗</span></a>
    </div>
    <div className="heroScene"><ForgeScene/></div>
    <div className="dragHint"><Move3d size={17}/><span>DRAG TO EXPLORE</span></div>
    <div className="scrollHint"><ArrowDown size={16}/><span>SCROLL TO DECONSTRUCT</span></div>
    <div className="heroIndex">PF<br/><span>01—04</span></div>
    <div className="heroTicker"><span>PIXEL FORGE · IMAGE TO DEPTH · DEPTH TO MESH · MESH TO FORM · </span><span>PIXEL FORGE · IMAGE TO DEPTH · DEPTH TO MESH · MESH TO FORM · </span></div>
  </section>
}
