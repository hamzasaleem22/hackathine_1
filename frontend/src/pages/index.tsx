import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Get Started with Module 0 →
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>🤖 6 Comprehensive Modules</h3>
              <p>
                From Physical AI fundamentals to advanced topics including ROS 2,
                simulation (Gazebo/Unity), NVIDIA Isaac SDK, and Vision-Language-Action models.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>📖 University-Level Content</h3>
              <p>
                Rigorous academic standards with IEEE-style citations, technical accuracy,
                and content appropriate for upper-division undergraduate or graduate students.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>💻 Interactive Code Playgrounds</h3>
              <p>
                Execute Python code examples directly in your browser. Learn ROS 2, robotics
                simulation, and AI integration through hands-on experimentation.
              </p>
            </div>
          </div>
        </div>
        <div className="row" style={{marginTop: '2rem'}}>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>📊 Rich Visualizations</h3>
              <p>
                3-5 diagrams per chapter including Mermaid flowcharts, architecture diagrams,
                and technical illustrations to enhance understanding of complex concepts.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>🎯 Practical Assessments</h3>
              <p>
                Self-assessment projects including ROS 2 package development, Gazebo simulation,
                Isaac perception pipelines, and a comprehensive capstone integration project.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>🌐 Open Access</h3>
              <p>
                100% open-access citations ensuring every student can verify sources.
                No paywalls, no institutional access required - knowledge for everyone.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
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
        <Heading as="h2" className="text--center margin-bottom--lg">
          Course Structure
        </Heading>
        <div className="row">
          {modules.map((module, idx) => (
            <div className="col col--6" key={idx} style={{marginBottom: '2rem'}}>
              <div className="card">
                <div className="card__header">
                  <h3>{module.title}</h3>
                </div>
                <div className="card__body">
                  <p>{module.description}</p>
                  <p><strong>Duration:</strong> {module.duration}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
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
