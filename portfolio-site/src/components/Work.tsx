"use client";

import { motion } from "framer-motion";

type Project = {
  title: string;
  role: string;
  date: string;
  description: string;
  tags: string[];
  link?: string;
};

const projects: Project[] = [
  {
    title: "Center for Teacher Accreditation",
    role: "Product Team Intern",
    date: "May–Jul 2025",
    description:
      "Redesigned user flows across B2B and B2C platforms serving 2M+ teachers in 100 countries. Authored PRDs, designed wireframes in Figma, built analytics dashboards in Looker Studio, and championed a net-new product validated through user interviews.",
    tags: ["Product Management", "Figma", "Looker Studio", "PRDs", "User Research"],
  },
  {
    title: "Agricultural Yield Predictor",
    role: "Research Project — Horizon Academic Program",
    date: "",
    description:
      "Built an end-to-end ML tool to help farmers in developing markets maximize crop yields. 22-class crop classifier with 96.8% accuracy + yield regression model. Mentored by Dr. Maria Konte at Georgia Tech.",
    tags: ["Python", "scikit-learn", "Flask", "Random Forest", "Research"],
  },
  {
    title: "Mroz (1987) Econometric Modeling",
    role: "Statistical ML Course Project",
    date: "Spring 2026",
    description:
      "Full econometric analysis of female labor supply. Built 4 OLS models with robust standard errors, conducted residual diagnostics, and documented omitted variable bias.",
    tags: ["Python", "OLS Regression", "Econometrics", "EDA"],
  },
  {
    title: "Orthodontist AI — Google Code2Learn",
    role: "Developer",
    date: "2020",
    description:
      "Trained a computer vision model on Google Cloud to diagnose braces treatment severity, validated against clinical data from India's leading orthodontists.",
    tags: ["Google Cloud", "Computer Vision", "ML"],
  },
  {
    title: "Graphene AI",
    role: "Backend Software Intern",
    date: "Apr–May 2023",
    description:
      "Built automated data pipeline in Python (Scrapy + Selenium) to extract customer review data for Fortune 500 clients including Costco. Deployed on Azure Kubernetes.",
    tags: ["Python", "Scrapy", "Selenium", "Azure Kubernetes"],
  },
];

function ExternalLinkIcon() {
  return (
    <svg
      width="14"
      height="14"
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
  );
}

export default function Work() {
  return (
    <section id="work" className="py-32 px-6 md:px-16">
      <div className="max-w-6xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 28 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
          className="font-display text-5xl md:text-6xl font-bold text-offwhite mb-16"
        >
          Work
        </motion.h2>

        <div className="grid md:grid-cols-2 gap-5">
          {projects.map((project, i) => (
            <motion.div
              key={project.title}
              initial={{ opacity: 0, y: 36 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.55, delay: i * 0.07 }}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className="group relative rounded-2xl p-7 border border-offwhite/8 hover:border-copper/35 transition-colors duration-300 cursor-default"
              style={{ background: "rgba(255,255,255,0.025)" }}
            >
              {/* Hover glow */}
              <div
                className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-400 pointer-events-none"
                style={{ boxShadow: "0 0 40px rgba(196,149,106,0.07)" }}
              />

              <div className="flex items-start justify-between gap-4 mb-3">
                <div>
                  <h3 className="font-display text-xl font-semibold text-offwhite leading-snug">
                    {project.title}
                  </h3>
                  <p className="text-sm text-copper mt-1.5">
                    {project.role}
                    {project.date ? ` · ${project.date}` : ""}
                  </p>
                </div>
                {project.link && (
                  <a
                    href={project.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="shrink-0 text-offwhite/25 hover:text-copper transition-colors mt-0.5"
                    aria-label={`View ${project.title}`}
                  >
                    <ExternalLinkIcon />
                  </a>
                )}
              </div>

              <p className="text-offwhite/55 text-sm leading-relaxed mb-5">
                {project.description}
              </p>

              <div className="flex flex-wrap gap-2">
                {project.tags.map((tag) => (
                  <span
                    key={tag}
                    className="text-xs px-2.5 py-1 rounded-full border border-offwhite/10 text-offwhite/35 tracking-wide"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
