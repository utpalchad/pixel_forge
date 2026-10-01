"use client";
import dynamic from "next/dynamic";
import {ArrowDown,Move3d} from "lucide-react";
const ForgeScene=dynamic(()=>import("./scenes/ForgeScene"),{ssr:false});
export default function Hero(){return <section className="hero"><div className="heroGrid"/><div className="eyebrow"><span className="pulse"/>IMAGE → GEOMETRY / 001</div><div className="heroCopy"><h1>TURN<br/><span>PIXELS</span><br/>INTO FORM.</h1><p>Transform ordinary images into tactile digital geometry. Shape depth, explore the mesh, export the object.</p><a href="#studio" className="primary">ENTER THE FORGE <span>↗</span></a></div><div className="heroScene"><ForgeScene/></div><div className="dragHint"><Move3d size={17}/><span>DRAG TO EXPLORE</span></div><div className="scrollHint"><ArrowDown size={16}/><span>SCROLL TO DECONSTRUCT</span></div><div className="heroIndex">PF<br/><span>01—04</span></div></section>}
