"use client";

import { motion } from "framer-motion";

const viewport = { once: true, margin: "-60px" } as const;

type ProjectLink = { label: string; href: string; accent?: boolean };

type Project = {
  title: string;
  role: string;
  bullets: string[];
  tags: string[];
  github?: string;
  links?: ProjectLink[];
};

const projects: Project[] = [
  {
    title: "Oil Shock Radar — Live Geopolitical Volatility Predictor",
    role: "Developer · ECON 3916 Final Project · Spring 2026",
    bullets: [
      "Built a live ML system predicting large WTI crude oil price moves (|daily return| > 2%) from geopolitical risk, market volatility, and real-time NYT headline sentiment.",
      "Engineered 8 time-lagged features from the Caldara & Iacoviello AI-GPR Index, FRED oil prices, and CBOE VIX. Custom phrase-aware bigram NLP scorer for live NYT RSS headlines.",
      "Deployed a Streamlit dashboard with three prediction modes, live yfinance quotes, and a user-adjustable precision/recall threshold.",
    ],
    tags: ["Python", "scikit-learn", "Streamlit", "Gradient Boosting", "NLP", "Sentiment Analysis", "Time Series", "yfinance"],
    github: "https://github.com/aahan-rd/ECON3916-Statistical-Machine-Learnin",
    links: [
      { label: "Live Dashboard", href: "https://livenews-oil-shock-radar.streamlit.app/", accent: true },
    ],
  },
  {
    title: "Agricultural Yield Predictor",
    role: "Horizon Academic Research Program · May–Jul 2024",
    bullets: [
      "Built an end-to-end ML tool helping farmers in developing markets maximize crop yields and profits.",
      "Defined the product from scratch — identified the problem, scoped the solution, built data pipelines, and delivered a Flask web app.",
      "Achieved 96.8% accuracy on a 22-class crop recommendation classifier with a parallel yield regression model.",
      "Mentored by Dr. Maria Konte at Georgia Institute of Technology.",
    ],
    tags: ["Python", "scikit-learn", "Flask", "Linear Regression", "Decision Tree"],
    github:
      "https://github.com/aahan-rd/Agricultural-Research-ML--Horizon-Academic-Research-Program",
  },
  {
    title: "Cook Your Books — Full-Stack Desktop App",
    role: "Developer & Lead Planner · CS Course Project · Spring 2026",
    bullets: [
      "Leading a team to build a full-stack desktop application in Java and JavaFX following the MVVM architecture pattern.",
      "Features four integrated modules: a recipe library browser, a recipe editor, a search system with advanced filtering and debounced queries, and an import interface powered by Gemini's OCR API for adding recipes via photos.",
    ],
    tags: ["Java", "JavaFX", "MVVM", "Gemini API", "OCR", "JUnit", "Full-Stack"],
    github: "https://github.com/aahan-rd",
  },
  {
    title: "SnugLine — CVC Patient Sleeve",
    role: "Design & Engineering Consultant · ENTR 3330 · Spring 2026",
    bullets: [
      "Co-designed a lightweight sleeve to secure external CVC lines for patients undergoing treatment.",
      "Led technical design focused on comfort, mobility, and a quick-access mechanism for providers.",
    ],
    tags: ["Product Design", "Design Thinking", "Medical Device", "User-Centered Design", "Entrepreneurship"],
  },
  {
    title: "Orthodontist AI — Google Code2Learn",
    role: "Developer · Apr–Jul 2020",
    bullets: [
      "Developed a computer vision model to diagnose orthodontic treatment severity and recommend treatment plans — validated against clinical data from India's leading prosthodontist, Dr. Sadashiv Shetty.",
      "Trained and deployed on Google Cloud with a Python client for inference.",
    ],
    tags: ["Google Cloud", "Computer Vision", "Python", "ML"],
  },
  {
    title: "Mroz (1987) Econometric Modeling",
    role: "Statistical ML Course Project · Spring 2026",
    bullets: [
      "Full EDA on real-world data — log-wage transformations, Tukey fence outlier detection, and bivariate plots across all treatment variables.",
      "Built 4 OLS models with HC1 robust standard errors justified by Breusch-Pagan test.",
      "Documented omitted variable bias from two unobserved confounders.",
    ],
    tags: ["Python", "OLS Regression", "Econometrics", "EDA", "Statsmodels"],
    github:
      "https://github.com/aahan-rd/ECON3916-Statistical-Machine-Learnin/tree/main/Economics%20Final%20Project",
  },
];

function ExternalLinkIcon() {
  return (
    <svg
      width="12" height="12" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
    >
      <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
      <polyline points="15,3 21,3 21,9" />
      <line x1="10" y1="14" x2="21" y2="3" />
    </svg>
  );
}

function GitHubIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
    </svg>
  );
}

export default function Projects() {
  return (
    <section id="projects" className="py-32 px-6 md:px-16">
      <div className="max-w-6xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 28 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
          className="font-display text-5xl md:text-6xl font-bold text-offwhite mb-16"
        >
          Projects
        </motion.h2>

        <div className="grid md:grid-cols-2 gap-[20px]">
          {projects.map((project, i) => (
            <motion.div
              key={project.title}
              initial={{ opacity: 0, y: 36 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={viewport}
              transition={{ duration: 0.55, delay: i * 0.08 }}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className="group relative rounded-2xl border border-offwhite/8 hover:border-copper/35 transition-colors duration-300 flex flex-col"
              style={{ background: "rgba(255,255,255,0.025)" }}
            >
              {/* Hover glow */}
              <div
                className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                style={{ boxShadow: "0 0 40px rgba(196,149,106,0.07)" }}
              />

              <div className="p-7 flex flex-col flex-1">
                {/* Header */}
                <div className="flex items-start justify-between gap-4 mb-1.5">
                  <h3 className="font-display text-xl font-semibold text-offwhite leading-snug">
                    {project.title}
                  </h3>
                  <div className="flex items-center gap-3 shrink-0 mt-0.5">
                    {project.github && (
                      <a
                        href={project.github}
                        target="_blank"
                        rel="noopener noreferrer"
                        aria-label={`GitHub — ${project.title}`}
                        className="text-offwhite/30 hover:text-copper transition-colors duration-200"
                      >
                        <GitHubIcon />
                      </a>
                    )}
                  </div>
                </div>

                <p className="text-sm text-copper mb-4">{project.role}</p>

                {/* Bullets — grow to fill available space */}
                <ul className="space-y-2 flex-1">
                  {project.bullets.map((b, bi) => (
                    <li key={bi} className="text-sm text-offwhite/60 leading-relaxed">
                      {b}
                    </li>
                  ))}
                </ul>

                {/* Tags — always at the bottom */}
                <div className="flex flex-wrap gap-2 mt-5">
                  {project.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-xs px-2.5 py-1 rounded-full border border-offwhite/10 text-offwhite/35 tracking-wide"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                {project.links && (
                  <div className="flex flex-wrap gap-2 mt-4">
                    {project.links.map((link) => (
                      <a
                        key={link.label}
                        href={link.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs tracking-wide transition-all duration-200 ${
                          link.accent
                            ? "border border-copper/50 text-copper hover:border-copper hover:bg-copper/10"
                            : "border border-offwhite/15 text-offwhite/50 hover:border-copper/40 hover:text-copper"
                        }`}
                      >
                        {link.label}
                        <ExternalLinkIcon />
                      </a>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
