import Nav from "@/components/Nav";
import Hero from "@/components/Hero";
import About from "@/components/About";
import RocketSection from "@/components/RocketSection";
import Experience from "@/components/Experience";
import Projects from "@/components/Projects";
import Skills from "@/components/Skills";
import Wild from "@/components/Wild";
import Contact from "@/components/Contact";

export default function Home() {
  return (
    <main>
      <Nav />
      <Hero />
      <About />
      <Experience />
      <Projects />
      <RocketSection />
      <Skills />
      <Wild />
      <Contact />
    </main>
  );
}
