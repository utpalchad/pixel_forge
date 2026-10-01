import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata={title:"Pixel Forge — Turn Pixels Into Form",description:"Transform images into interactive 3D forms, STL, GLB and lithophanes."};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
