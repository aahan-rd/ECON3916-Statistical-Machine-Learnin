"use client";

import { motion } from "framer-motion";
import Image from "next/image";

export default function Hero() {
  return (
    <section className="relative h-screen overflow-hidden flex items-center justify-center">
      {/* Ken Burns background — Aahan's own wildlife photo */}
      <div className="absolute inset-0 ken-burns">
        <Image
          src="/images/hero/DSC_2712.jpg"
          alt="Green leafbird on a mossy branch — wildlife photography by Aahan Desai"
          fill
          priority
          className="object-cover"
          style={{ objectPosition: "center 68%" }}
        />
      </div>

      {/* Gradient overlay — bright open top, fades dark toward text */}
      <div
        className="absolute inset-0"
        style={{
          background:
            "linear-gradient(to bottom, rgba(13,13,13,0.08) 0%, rgba(13,13,13,0.10) 35%, rgba(13,13,13,0.52) 60%, rgba(13,13,13,0.88) 100%)",
        }}
      />

      {/* Content */}
      <div className="relative z-10 text-center px-6 max-w-5xl mx-auto">
        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut", delay: 0.1 }}
          className="text-copper text-xs tracking-[0.3em] uppercase mb-6 font-body"
        >
          Boston, MA · Bangalore, India
        </motion.p>

        <motion.h1
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.25 }}
          className="font-display font-bold text-offwhite leading-none tracking-tight"
          style={{ fontSize: "clamp(3.5rem, 12vw, 9rem)" }}
        >
          Aahan Desai
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, ease: "easeOut", delay: 0.65 }}
          className="mt-6 text-offwhite/60 tracking-[0.2em] uppercase text-sm md:text-base font-light"
        >
          Product Manager &nbsp;·&nbsp; Data Science &nbsp;·&nbsp; Conservation
        </motion.p>
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.6, duration: 0.8 }}
        className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 scroll-indicator"
      >
        <span className="text-offwhite/30 text-[10px] tracking-[0.25em] uppercase">
          Scroll
        </span>
        <svg
          width="14"
          height="22"
          viewBox="0 0 14 22"
          fill="none"
          className="text-offwhite/30"
        >
          <line
            x1="7"
            y1="0"
            x2="7"
            y2="16"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
          />
          <path
            d="M1 11l6 6 6-6"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </motion.div>
    </section>
  );
}
