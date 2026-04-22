"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

const links = [
  { label: "Experience", href: "#experience" },
  { label: "Projects", href: "#projects" },
  { label: "About", href: "#about" },
  { label: "Skills", href: "#skills" },
  { label: "Wild", href: "#wild" },
  { label: "Contact", href: "#contact" },
];

export default function Nav() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () =>
      setVisible(window.scrollY > window.innerHeight * 0.7);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <AnimatePresence>
      {visible && (
        <motion.nav
          initial={{ y: -60, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -60, opacity: 0 }}
          transition={{ duration: 0.28, ease: "easeOut" }}
          className="fixed top-0 left-0 right-0 z-50 px-8 py-4 flex items-center justify-between"
          style={{
            background: "rgba(13, 13, 13, 0.88)",
            backdropFilter: "blur(14px)",
            borderBottom: "1px solid rgba(245, 240, 235, 0.06)",
          }}
        >
          <a
            href="#"
            className="font-display text-offwhite font-semibold tracking-wide text-sm hover:text-copper transition-colors"
          >
            Aahan Desai
          </a>
          <ul className="hidden sm:flex gap-8">
            {links.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  className="text-sm text-offwhite/60 hover:text-copper transition-colors duration-200 tracking-wide"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </motion.nav>
      )}
    </AnimatePresence>
  );
}
