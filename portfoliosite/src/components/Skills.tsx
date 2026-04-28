"use client";

import { motion } from "framer-motion";

type SkillCategory = {
  label: string;
  color: string;
  skills: string[];
};

const categories: SkillCategory[] = [
  {
    label: "Languages",
    color: "#c4956a",
    skills: ["Python", "Java", "Kotlin", "SQL", "HTML", "CSS"],
  },
  {
    label: "ML & Data",
    color: "#c4956a",
    skills: [
      "scikit-learn",
      "Pandas",
      "NumPy",
      "Matplotlib",
      "Seaborn",
      "Statsmodels",
      "Random Forest",
      "Gradient Boosting",
      "OLS Regression",
      "Classification",
      "Cross-validation",
      "NLP",
      "Sentiment Analysis",
      "Time Series",
    ],
  },
  {
    label: "Product",
    color: "#c4956a",
    skills: [
      "Figma",
      "PRDs",
      "User Research",
      "Wireframing",
      "Sprint Planning",
      "MoSCoW Prioritization",
      "A/B Testing",
      "Google Looker Studio",
      "Competitive Analysis",
    ],
  },
  {
    label: "Tools",
    color: "#c4956a",
    skills: [
      "Git / GitHub",
      "Google Cloud",
      "Azure Kubernetes",
      "Loveable.AI",
      "Claude",
      "Claude Code",
      "Streamlit",
      "yfinance",
      "DaVinci Resolve",
      "Adobe Lightroom",
      "Blender",
    ],
  },
  {
    label: "Languages Spoken",
    color: "#2d5016",
    skills: [
      "English (Advanced)",
      "Hindi (Fluent)",
      "French (Classroom)",
      "Gujarati (Basic)",
    ],
  },
];

export default function Skills() {
  return (
    <section id="skills" className="py-32 px-6 md:px-16">
      <div className="max-w-6xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 28 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
          className="font-display text-5xl md:text-6xl font-bold text-offwhite mb-16"
        >
          Skills
        </motion.h2>

        <div className="space-y-11">
          {categories.map((cat, ci) => (
            <motion.div
              key={cat.label}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.55, delay: ci * 0.08 }}
            >
              <h3
                className="text-xs font-semibold uppercase tracking-[0.22em] mb-4"
                style={{ color: cat.color }}
              >
                {cat.label}
              </h3>
              <div className="flex flex-wrap gap-2.5">
                {cat.skills.map((skill, si) => (
                  <motion.span
                    key={skill}
                    initial={{ opacity: 0, scale: 0.92 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{
                      duration: 0.3,
                      delay: ci * 0.04 + si * 0.025,
                    }}
                    className="px-4 py-2 rounded-full border border-offwhite/12 text-offwhite/62 text-sm tracking-wide cursor-default hover:border-copper/40 hover:text-offwhite/90 hover:bg-copper/5 transition-all duration-200"
                  >
                    {skill}
                  </motion.span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
