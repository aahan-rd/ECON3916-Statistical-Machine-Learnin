"use client";

import { motion } from "framer-motion";
import Image from "next/image";

type Photo = { src: string; species: string; location: string };

const row1: Photo[] = [
  { src: "/images/wildlife/little-spiderhunter.png", species: "Little Spiderhunter", location: "Bangalore, India" },
  { src: "/images/wildlife/oriental-white-eye.png",  species: "Oriental White-Eye",  location: "Bangalore, India" },
  { src: "/images/wildlife/mottled-wood-owl.png",    species: "Mottled Wood Owl",    location: "Western Ghats, India" },
];

const row2: Photo[] = [
  { src: "/images/wildlife/jerdons-leafbird.png", species: "Jerdon's Leafbird", location: "Western Ghats, India" },
  { src: "/images/wildlife/bengal-tiger.png",     species: "Bengal Tiger",      location: "Kabini, Karnataka" },
];

function LeafIcon() {
  return (
    <svg
      width="32"
      height="32"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="text-forest-light"
    >
      <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" />
      <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12" />
    </svg>
  );
}

export default function Wild() {
  return (
    <section id="nature" className="py-32 px-6 md:px-16">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 28 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
          className="mb-14"
        >
          <h2 className="font-display text-5xl md:text-6xl font-bold text-offwhite flex items-center gap-4">
            Nature
            <LeafIcon />
          </h2>
          <p className="mt-6 text-offwhite/60 text-lg leading-relaxed max-w-2xl">
            I&apos;ve been a wildlife photographer since I was 14 — 300+ bird
            species documented across India and counting. I use my camera to
            tell stories about the ecosystems we share, and why protecting them
            matters.
          </p>
          <a
            href="https://www.instagram.com/aahandesai/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 mt-5 text-sm text-offwhite/50 hover:text-copper transition-colors duration-200"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" />
            </svg>
            Follow my wildlife photography on Instagram
          </a>
        </motion.div>

        {/* Photo grid */}
        <div className="flex flex-col gap-[10px] mb-24">
          {/* Row 1 — 3 equal columns */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-[10px]">
            {row1.map((photo, i) => (
              <motion.div
                key={photo.species}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ duration: 0.5, delay: i * 0.07 }}
                className="relative group rounded-2xl overflow-hidden"
                style={{ aspectRatio: "4/3" }}
              >
                <Image
                  src={photo.src}
                  alt={photo.species}
                  fill
                  className="object-cover transition-transform duration-500 group-hover:scale-105"
                  style={{ objectPosition: "center" }}
                />
                <div
                  className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                  style={{ background: "rgba(13,13,13,0.62)" }}
                />
                <div className="absolute bottom-0 left-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <p className="text-offwhite font-medium text-sm">{photo.species}</p>
                  <p className="text-offwhite/55 text-xs mt-0.5">{photo.location}</p>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Row 2 — 2 equal columns, wider */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-[10px]">
            {row2.map((photo, i) => (
              <motion.div
                key={photo.species}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ duration: 0.5, delay: (i + 3) * 0.07 }}
                className="relative group rounded-2xl overflow-hidden"
                style={{ aspectRatio: "16/9" }}
              >
                <Image
                  src={photo.src}
                  alt={photo.species}
                  fill
                  className="object-cover transition-transform duration-500 group-hover:scale-105"
                  style={{ objectPosition: "center" }}
                />
                <div
                  className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                  style={{ background: "rgba(13,13,13,0.62)" }}
                />
                <div className="absolute bottom-0 left-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <p className="text-offwhite font-medium text-sm">{photo.species}</p>
                  <p className="text-offwhite/55 text-xs mt-0.5">{photo.location}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Conservation */}
        <motion.div
          initial={{ opacity: 0, y: 28 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
        >
          <h3 className="font-display text-3xl md:text-4xl font-bold text-offwhite mb-10">
            Conservation
          </h3>

          <div className="grid md:grid-cols-2 gap-5">
            {/* Film card */}
            <div
              className="p-7 rounded-2xl border border-forest/30 hover:border-forest-light/40 transition-colors duration-300"
              style={{ background: "rgba(45, 80, 22, 0.06)" }}
            >
              <p className="text-xs uppercase tracking-[0.2em] text-forest-light font-semibold mb-4">
                Film
              </p>
              <h4 className="font-display text-xl font-semibold text-offwhite mb-3 leading-snug">
                Bengaluru, Let&apos;s Fly Together
              </h4>
              <p className="text-offwhite/55 text-sm leading-relaxed mb-5">
                Award-winning documentary selected for Bangalore International
                Centre&apos;s B&bull;LORE festival. The film explores
                Bengaluru&apos;s urban bird ecosystems across locations like
                Jakkur Lake, Thimmasandra Lake, and Devanahalli — documenting
                rare species and the cost of habitat encroachment.
              </p>
              <a
                href="https://bangaloreinternationalcentre.org/blore/bengaluru-lets-fly-together-b%e2%80%a2lore-by-bic/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-copper hover:text-copper-dark transition-colors inline-flex items-center gap-1.5"
              >
                Watch at BIC
                <svg
                  width="11"
                  height="11"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
                  <polyline points="15,3 21,3 21,9" />
                  <line x1="10" y1="14" x2="21" y2="3" />
                </svg>
              </a>
            </div>

            {/* WWF card */}
            <div
              className="p-7 rounded-2xl border border-forest/30 hover:border-forest-light/40 transition-colors duration-300"
              style={{ background: "rgba(45, 80, 22, 0.06)" }}
            >
              <p className="text-xs uppercase tracking-[0.2em] text-forest-light font-semibold mb-4">
                WWF India
              </p>
              <h4 className="font-display text-xl font-semibold text-offwhite mb-3 leading-snug">
                Model COP — Karnataka Representative
              </h4>
              <p className="text-offwhite/55 text-sm leading-relaxed">
                Selected as one of two state representatives for Karnataka in
                WWF India&apos;s Model COP program. Led ground-level plastic
                pollution audits in my locality and developed actionable policy
                recommendations for local government officials.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
