"use client";

import { motion } from "framer-motion";

const socials = [
  {
    label: "Email",
    value: "desai.aah@northeastern.edu",
    href: "mailto:desai.aah@northeastern.edu",
    external: false,
  },
  {
    label: "GitHub",
    value: "github.com/aahan-rd",
    href: "https://github.com/aahan-rd",
    external: true,
  },
  {
    label: "LinkedIn",
    value: "linkedin.com/in/aahan-desai-",
    href: "https://www.linkedin.com/in/aahan-desai-/",
    external: true,
  },
  {
    label: "Phone",
    value: "+1 510 459 2486",
    href: "tel:+15104592486",
    external: false,
  },
];

export default function Contact() {
  return (
    <section
      id="contact"
      className="py-32 px-6 md:px-16 border-t border-offwhite/6"
    >
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 28 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
        >
          <h2 className="font-display text-5xl md:text-6xl font-bold text-offwhite mb-5">
            Let&apos;s Connect
          </h2>
          <p className="text-offwhite/50 text-lg mb-16 max-w-xl leading-relaxed">
            Open to PM co-op opportunities for May–Dec 2026, research
            collaborations, and conversations about building products,
            conservation, and anything in between.
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-24">
          {socials.map((s, i) => (
            <motion.a
              key={s.label}
              href={s.href}
              target={s.external ? "_blank" : undefined}
              rel={s.external ? "noopener noreferrer" : undefined}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.08 }}
              whileHover={{ y: -3, transition: { duration: 0.18 } }}
              className="block p-5 rounded-2xl border border-offwhite/8 hover:border-copper/35 transition-colors duration-250 group"
              style={{ background: "rgba(255,255,255,0.02)" }}
            >
              <p className="text-xs uppercase tracking-[0.2em] text-copper mb-2.5">
                {s.label}
              </p>
              <p className="text-offwhite/60 text-sm group-hover:text-offwhite/90 transition-colors truncate">
                {s.value}
              </p>
            </motion.a>
          ))}
        </div>

        {/* Footer */}
        <div className="border-t border-offwhite/6 pt-8 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-offwhite/22 text-sm">
            &copy; 2026 Aahan Desai
          </p>
          <p className="text-offwhite/22 text-sm">
            Built with Next.js &amp; Claude Code
          </p>
        </div>
      </div>
    </section>
  );
}
