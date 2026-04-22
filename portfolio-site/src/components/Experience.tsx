"use client";

import { motion } from "framer-motion";

const viewport = { once: true, margin: "-60px" } as const;

type LiveLink = { label: string; href: string };

type Job = {
  title: string;
  role: string;
  date: string;
  location: string;
  bullets: string[];
  tags: string[];
  liveWork?: LiveLink[];
};

const jobs: Job[] = [
  {
    title: "Center for Teacher Accreditation (CENTA)",
    role: "Product Team Intern",
    date: "May 2025 – Jul 2025",
    location: "Bangalore, India",
    bullets: [
      "Owned product features end-to-end across B2B and B2C platforms serving 2M+ teachers in 100 countries.",
      "Identified product gaps through competitive analysis and user research, then authored PRDs defining requirements, specs, and rollout phases.",
      "Designed wireframes in Figma and built live production pages using Loveable.AI.",
      "Built user analytics dashboards in Google Looker Studio — including one for a statewide government teacher upskilling initiative.",
      "Championed a net-new product initiative and validated it through the company's first formal user interviews.",
    ],
    tags: ["Product Management", "Figma", "Loveable.AI", "Wireframing", "User Research", "Looker Studio"],
    liveWork: [
      { label: "Teacher Certification", href: "https://centa.org/centa-for-schools/teacher-certification" },
      { label: "Teacher Training", href: "https://centa.org/centa-for-schools/teacher-training" },
      { label: "Teacher Recruitment", href: "https://centa.org/centa-for-schools/teacher-recruitment" },
    ],
  },
  {
    title: "Graphene AI",
    role: "Backend Software Intern",
    date: "Apr 2023 – May 2023",
    location: "Bangalore, India",
    bullets: [
      "Built an automated data pipeline in Python (Scrapy, Selenium, Beautiful Soup) to extract and structure large volumes of customer review data for Fortune 500 clients including Costco.",
      "Transformed raw data into actionable business insights and deployed the pipeline on Azure Kubernetes for scalable execution.",
    ],
    tags: ["Python", "Scrapy", "Selenium", "Beautiful Soup", "Azure Kubernetes"],
  },
];

function ExternalLinkIcon() {
  return (
    <svg
      width="11" height="11" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
    >
      <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
      <polyline points="15,3 21,3 21,9" />
      <line x1="10" y1="14" x2="21" y2="3" />
    </svg>
  );
}

export default function Experience() {
  return (
    <section id="experience" className="py-32 px-6 md:px-16">
      <div className="max-w-3xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 28 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
          className="font-display text-5xl md:text-6xl font-bold text-offwhite mb-20"
        >
          Experience
        </motion.h2>

        {/* Timeline */}
        <div className="relative">
          {/* Vertical spine */}
          <div
            className="absolute left-[18px] top-3 bottom-3 w-px"
            style={{
              background:
                "linear-gradient(to bottom, rgba(196,149,106,0.55) 0%, rgba(196,149,106,0.12) 100%)",
            }}
          />

          {jobs.map((job, i) => (
            <div key={job.title}>
              {/* Time-gap indicator between entries */}
              {i > 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  whileInView={{ opacity: 1 }}
                  viewport={viewport}
                  transition={{ duration: 0.5 }}
                  className="relative pl-14 py-7 flex items-center gap-3"
                >
                  {/* dots on the spine */}
                  {[0, 1, 2].map((d) => (
                    <span
                      key={d}
                      className="absolute rounded-full bg-offwhite/15"
                      style={{
                        left: 14,
                        width: 4,
                        height: 4,
                        top: `calc(${28 + d * 14}px)`,
                        transform: "translateX(-50%)",
                      }}
                    />
                  ))}
                  <span className="text-xs tracking-[0.2em] uppercase text-offwhite/22">
                    · 2 years prior ·
                  </span>
                </motion.div>
              )}

              {/* Entry */}
              <motion.div
                initial={{ opacity: 0, x: -16 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={viewport}
                transition={{ duration: 0.55, delay: i * 0.1 }}
                className="relative pl-14 mb-2"
              >
                {/* Timeline dot */}
                <div
                  className="absolute left-0 top-6 flex items-center justify-center"
                  style={{ width: 36, height: 36 }}
                >
                  <div
                    className="rounded-full border flex items-center justify-center"
                    style={{
                      width: 36,
                      height: 36,
                      borderColor:
                        i === 0
                          ? "rgba(196,149,106,0.5)"
                          : "rgba(245,240,235,0.15)",
                      background: "#0d0d0d",
                    }}
                  >
                    <div
                      className="rounded-full"
                      style={{
                        width: 10,
                        height: 10,
                        background:
                          i === 0 ? "#c4956a" : "rgba(245,240,235,0.3)",
                      }}
                    />
                  </div>
                </div>

                {/* Card */}
                <div
                  className="rounded-2xl p-7 border border-offwhite/8 hover:border-copper/30 transition-colors duration-300"
                  style={{ background: "rgba(255,255,255,0.025)" }}
                >
                  {/* Header */}
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-1 mb-1.5">
                    <h3 className="font-display text-xl font-semibold text-offwhite leading-snug">
                      {job.title}
                    </h3>
                    <span className="text-xs text-offwhite/60 shrink-0 sm:mt-1">
                      {job.location}
                    </span>
                  </div>
                  <p className="text-sm text-copper mb-5">
                    {job.role} · {job.date}
                  </p>

                  {/* Bullet points */}
                  <ul className="space-y-2.5 mb-5">
                    {job.bullets.map((b, bi) => (
                      <li key={bi} className="flex gap-3 text-sm text-offwhite/62 leading-relaxed">
                        <span className="text-copper/50 mt-1 shrink-0">–</span>
                        <span>{b}</span>
                      </li>
                    ))}
                  </ul>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-2">
                    {job.tags.map((tag) => (
                      <span
                        key={tag}
                        className="text-xs px-2.5 py-1 rounded-full border border-offwhite/20 text-offwhite/65 tracking-wide"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  {/* Live work links */}
                  {job.liveWork && (
                    <div className="mt-6 pt-5 border-t border-offwhite/8">
                      <p className="text-xs uppercase tracking-[0.18em] text-offwhite/65 mb-3">
                        Live Work
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {job.liveWork.map((link) => (
                          <a
                            key={link.label}
                            href={link.href}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-copper/25 text-copper/70 hover:border-copper/60 hover:text-copper text-xs tracking-wide transition-all duration-200 hover:bg-copper/5"
                          >
                            {link.label}
                            <ExternalLinkIcon />
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </motion.div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
