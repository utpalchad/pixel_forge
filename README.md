# Pixel Forge

> Turn pixels into form.

Pixel Forge is an image-to-3D creation platform that transforms ordinary JPG and PNG images into **STL**, **GLB**, and **3D-printable lithophane** outputs. It combines Cloudinary-powered media processing with a custom geometry pipeline and an interactive 3D experience so users can move from an image to a usable 3D asset without traditional CAD skills.

## ✨ What Pixel Forge Does

Upload an image, choose how you want it interpreted, adjust the geometry, preview the result in 3D, and export it.

- **Image → STL** for 3D-printable reliefs and geometry
- **Image → GLB** for portable 3D assets and web experiences
- **Image → Lithophane** using image brightness to generate printable depth
- **Interactive 3D preview** with rotation, zoom, lighting, and live visual feedback
- **Custom controls** for depth, detail, smoothing, dimensions, base thickness, and inversion
- **Optional natural-language guidance** so users can describe the result they want
- **Cloudinary media pipeline** for upload, transformation, enhancement, optimization, and standardized reconstruction inputs

## 🧠 How It Works

```text
JPG / PNG
    │
    ▼
Cloudinary Media Processing
    │
    ├── optimization
    ├── resize / crop
    ├── background processing
    └── standardized input
    │
    ▼
Pixel Forge Conversion Engine
    │
    ├── grayscale / depth mapping
    ├── height generation
    ├── mesh construction
    ├── smoothing & optimization
    └── scale / base / geometry processing
    │
    ▼
Interactive 3D Preview
    │
    ├── STL
    ├── GLB
    └── Lithophane
```

For relief and lithophane modes, Pixel Forge can construct geometry directly from image data. More advanced reconstruction modes can use AI-assisted depth or 3D generation while keeping the core workflow and post-processing inside Pixel Forge.

## 🎨 Experience

Pixel Forge is designed as a spatial, interactive creation experience rather than a conventional upload form.

The interface is being built around:

**Image → Depth → Wireframe → Mesh → Object**

The goal is for users to actually *see* their image becoming geometry. The 3D model is the center of the interface, surrounded by lightweight controls for editing and export.

## 🛠️ Planned Tech Stack

### Frontend
- Next.js / React
- TypeScript
- Tailwind CSS
- Three.js
- React Three Fiber
- Drei
- GSAP / motion-based interactions

### Media
- Cloudinary

### Conversion & Geometry
- Python
- NumPy
- Pillow / OpenCV
- trimesh / Open3D
- Custom image-to-height-map and mesh-generation logic

### Backend
- FastAPI

## 🧩 Conversion Engine

A simplified relief conversion follows this pipeline:

```text
Image
  ↓
Resize & normalize
  ↓
Grayscale / depth map
  ↓
Pixel intensity → height
  ↓
Generate vertices
  ↓
Connect vertices into faces
  ↓
Add walls + base
  ↓
Repair / smooth / simplify mesh
  ↓
Export STL / GLB
```

A basic height mapping can be represented as:

```text
height = min_thickness + (brightness / 255) × depth
```

Lithophane mode can invert this relationship so darker regions produce thicker geometry.

## 🚀 Project Goals

Pixel Forge aims to make basic 3D asset creation accessible to people who do not know Blender, CAD, mesh modeling, or traditional 3D workflows.

The project focuses on three ideas:

1. **Accessibility** — start with an ordinary image.
2. **Interactivity** — preview and customize geometry visually.
3. **Practical output** — export files that can be used on the web or prepared for 3D printing.

## 🗺️ Roadmap

- [ ] Interactive landing experience
- [ ] Drag-and-drop JPG/PNG upload
- [ ] Cloudinary preprocessing pipeline
- [ ] Custom relief conversion engine
- [ ] Lithophane generator
- [ ] STL export
- [ ] GLB export
- [ ] Three.js / React Three Fiber model viewer
- [ ] Live depth and smoothing controls
- [ ] Model dimensions and scaling
- [ ] Mesh repair / optimization
- [ ] Natural-language parameter input
- [ ] Advanced AI-assisted 3D reconstruction
- [ ] Responsive mobile experience

## 💻 Local Development

The implementation is currently under active development. Once the application scaffold is committed, the typical development flow will be:

```bash
git clone https://github.com/utpalchad/pixel_forge.git
cd pixel_forge
npm install
npm run dev
```

Backend setup instructions and required environment variables will be documented as those modules are added.

> Never commit API secrets or Cloudinary credentials directly to the repository. Use environment variables and keep local secret files out of version control.

## ☁️ Cloudinary

Cloudinary is intended to be a core part of the Pixel Forge media workflow rather than only file storage. It prepares image assets before geometry generation and can provide optimized variants for previews and downstream processing.

## 🏗️ Status

**Pixel Forge is currently in active hackathon development.** Features described above include both the target product experience and components currently being implemented.

## 📄 License

This project is licensed under the **MIT License**. See the repository's `LICENSE` file for details.

---

### Pixel Forge

**From image to geometry. From pixels to form.**
