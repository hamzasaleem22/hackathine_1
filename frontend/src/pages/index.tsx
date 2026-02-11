import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import { BookOpen, GraduationCap, Code, BarChart3, Target, Globe } from 'lucide-react';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className={styles.heroButton}
            to="/docs/module-0/">
            Get Started with Module 0 →
          </Link>
        </div>
      </div>
    </header>
  );
}

type FeatureCardProps = {
  icon: React.ReactNode;
  title: string;
  description: string;
};

function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <div className={styles.featureCard}>
      <div className={styles.featureIcon} role="img" aria-label={title}>
        {icon}
      </div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
    </div>
  );
}

function HomepageFeatures() {
  const features = [
    {
      icon: <BookOpen />,
      title: '6 Comprehensive Modules',
      description: 'From Physical AI fundamentals to advanced topics including ROS 2, simulation (Gazebo/Unity), NVIDIA Isaac SDK, and Vision-Language-Action models.',
    },
    {
      icon: <GraduationCap />,
      title: 'University-Level Content',
      description: 'Rigorous academic standards with IEEE-style citations, technical accuracy, and content appropriate for upper-division undergraduate or graduate students.',
    },
    {
      icon: <Code />,
      title: 'Interactive Code Playgrounds',
      description: 'Execute Python code examples directly in your browser. Learn ROS 2, robotics simulation, and AI integration through hands-on experimentation.',
    },
    {
      icon: <BarChart3 />,
      title: 'Rich Visualizations',
      description: '3-5 diagrams per chapter including Mermaid flowcharts, architecture diagrams, and technical illustrations to enhance understanding of complex concepts.',
    },
    {
      icon: <Target />,
      title: 'Practical Assessments',
      description: 'Self-assessment projects including ROS 2 package development, Gazebo simulation, Isaac perception pipelines, and a comprehensive capstone integration project.',
    },
    {
      icon: <Globe />,
      title: 'Open Access',
      description: '100% open-access citations ensuring every student can verify sources. No paywalls, no institutional access required - knowledge for everyone.',
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.featuresGrid}>
          {features.map((feature, idx) => (
            <FeatureCard key={idx} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
}

type ModuleCardProps = {
  title: string;
  description: string;
  duration: string;
  moduleNumber: number;
};

function ModuleCard({ title, description, duration, moduleNumber }: ModuleCardProps) {
  return (
    <div className={styles.moduleCard}>
      <div className={styles.moduleHeader}>
        <div className={styles.moduleNumber} aria-label={`Module ${moduleNumber}`}>
          {moduleNumber}
        </div>
        <h3 className={styles.moduleTitle}>{title}</h3>
      </div>
      <div className={styles.moduleBody}>
        <p className={styles.moduleDescription}>{description}</p>
        <p className={styles.moduleDuration}>⏱️ {duration}</p>
      </div>
    </div>
  );
}

function HomepageModules() {
  const modules = [
    {
      title: 'Module 0: Introduction to Physical AI',
      description: 'Physical AI principles, embodied intelligence, humanoid robotics landscape, sensor systems (LIDAR, cameras, IMUs)',
      duration: '2 weeks',
    },
    {
      title: 'Module 1: ROS 2 & Robotics Middleware',
      description: 'ROS 2 architecture, Python (rclpy), URDF for humanoids, nodes, topics, services, actions',
      duration: '3 weeks',
    },
    {
      title: 'Module 2: Gazebo & Unity Simulation',
      description: 'Physics simulation, URDF/SDF, Unity rendering, sensor simulation, HRI',
      duration: '3 weeks',
    },
    {
      title: 'Module 3: NVIDIA Isaac SDK',
      description: 'Isaac SDK, Isaac Sim, Isaac ROS, sim-to-real transfer, perception pipelines',
      duration: '3 weeks',
    },
    {
      title: 'Module 4: Vision-Language-Action (VLA)',
      description: 'LLM integration (OpenAI GPT), voice recognition (Whisper), NLP to ROS 2 action translation',
      duration: '2 weeks',
    },
    {
      title: 'Module 5: Humanoid Development & Capstone',
      description: 'Humanoid design principles, integration capstone: voice + path planning + vision + manipulation',
      duration: '2 weeks',
    },
  ];

  return (
    <section className={styles.modules}>
      <div className="container">
        <Heading as="h2" className={styles.modulesHeading}>
          Course Structure
        </Heading>
        <div className={styles.modulesGrid}>
          {modules.map((module, idx) => (
            <ModuleCard key={idx} {...module} moduleNumber={idx} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="University-level interactive textbook on Physical AI and Humanoid Robotics covering ROS 2, simulation, NVIDIA Isaac, and Vision-Language-Action models">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <HomepageModules />
      </main>
    </Layout>
  );
}
