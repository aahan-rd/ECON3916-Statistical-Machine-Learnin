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
    <section id="wild" className="py-32 px-6 md:px-16">
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
            Wild
            <LeafIcon />
          </h2>
          <p className="mt-6 text-offwhite/60 text-lg leading-relaxed max-w-2xl">
            I&apos;ve been a wildlife photographer since I was 14 — 300+ bird
            species documented across India and counting. I use my camera to
            tell stories about the ecosystems we share, and why protecting them
            matters.
          </p>
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
