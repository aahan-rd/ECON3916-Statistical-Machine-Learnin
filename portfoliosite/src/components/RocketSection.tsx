"use client";

import { motion } from "framer-motion";

const stats = [
  { label: "Peak Altitude", value: "3,000 ft" },
  { label: "Max Speed", value: "230 m/s" },
  { label: "Motor", value: "J420" },
  { label: "Build Time", value: "5 months" },
];

export default function RocketSection() {
  return (
    <div
      className="relative w-full overflow-hidden"
      style={{ minHeight: "88vh" }}
    >
      {/* ── Solid dark base ── */}
      <div className="absolute inset-0" style={{ background: "#0d0d0d" }} />

      {/* ── Video: sized by height, full rocket visible nose-to-flame, pinned right ── */}
      <div className="absolute right-0 top-0 h-full hidden md:flex items-center">
        <video
          autoPlay
          muted
          loop
          playsInline
          poster="/images/aeronu/rocket-launch.png"
          style={{ height: "100%", width: "auto", display: "block" }}
        >
          <source src="/videos/rocket-launch.mp4" type="video/mp4" />
        </video>
      </div>

      {/* Mobile: contained static image */}
      <div
        className="absolute inset-0 md:hidden"
        style={{
          backgroundImage: "url('/images/aeronu/rocket-launch.png')",
          backgroundSize: "contain",
          backgroundRepeat: "no-repeat",
          backgroundPosition: "center 60%",
        }}
      />

      {/* ── Top fade ── */}
      <div
        className="absolute top-0 left-0 right-0 pointer-events-none"
        style={{
          height: 120,
          background: "linear-gradient(to bottom, #0d0d0d 0%, transparent 100%)",
        }}
      />

      {/* ── Bottom fade ── */}
      <div
        className="absolute bottom-0 left-0 right-0 pointer-events-none"
        style={{
          height: 120,
          background: "linear-gradient(to top, #0d0d0d 0%, transparent 100%)",
        }}
      />

      {/* ── Content ── */}
      <div
        className="relative z-10 flex items-center px-6 md:px-16 py-36"
        style={{ minHeight: "88vh" }}
      >
        <motion.div
          initial={{ opacity: 0, y: 28 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.8 }}
          className="max-w-lg"
        >
          {/* Small caps label */}
          <p
            className="text-copper font-semibold mb-5"
            style={{
              fontSize: "0.65rem",
              letterSpacing: "0.3em",
              fontVariant: "small-caps",
              textTransform: "uppercase",
            }}
          >
            To anyone who shares the love for flight
          </p>

          <h3
            className="font-display font-bold text-offwhite leading-tight mb-6"
            style={{ fontSize: "clamp(2.2rem, 4.5vw, 3.4rem)" }}
          >
            Obsessed with flight even before I could walk.
          </h3>

          <p className="text-offwhite/65 leading-relaxed mb-8 text-[1.05rem]">
            From memorizing every system in an F-14 cockpit as a kid to building
            a 6-foot rocket from scratch with AeroNU — aerospace has been my
            longest-running obsession. Our rocket hit 3,000&nbsp;ft and
            230&nbsp;m/s. I&apos;m not here because aerospace seems like a good
            career move — I&apos;m here because a two-year-old watched Maverick
            take off and never got over it.
          </p>

          {/* Stats pills */}
          <div className="flex flex-wrap gap-3">
            {stats.map((s) => (
              <div
                key={s.label}
                className="px-4 py-2 rounded-full"
                style={{
                  background: "rgba(196,149,106,0.08)",
                  border: "1px solid rgba(196,149,106,0.25)",
                  backdropFilter: "blur(6px)",
                }}
              >
                <span className="text-offwhite/40 text-xs mr-1.5">{s.label}</span>
                <span className="text-copper text-sm font-medium">{s.value}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
