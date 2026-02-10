import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'index', // Textbook overview
    {
      type: 'category',
      label: 'Module 0: Introduction to Physical AI',
      link: {
        type: 'doc',
        id: 'module-0/index',
      },
      collapsed: false,
      items: [
        'module-0/principles',
        'module-0/embodied-intelligence',
        'module-0/humanoid-landscape',
        'module-0/sensor-systems',
        'module-0/assessment',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 & Robotics Middleware',
      link: {
        type: 'generated-index',
        title: 'Module 1: ROS 2 & Robotics Middleware',
        description: 'Comprehensive coverage of ROS 2 architecture, Python (rclpy), and URDF for humanoids.',
      },
      collapsed: true,
      items: [],
    },
    {
      type: 'category',
      label: 'Module 2: Gazebo & Unity Simulation',
      link: {
        type: 'generated-index',
        title: 'Module 2: Gazebo & Unity Simulation',
        description: 'Physics simulation, URDF/SDF, Unity rendering, and sensor simulation.',
      },
      collapsed: true,
      items: [],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac SDK',
      link: {
        type: 'generated-index',
        title: 'Module 3: NVIDIA Isaac SDK',
        description: 'Isaac SDK, Isaac Sim, Isaac ROS, and sim-to-real transfer.',
      },
      collapsed: true,
      items: [],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      link: {
        type: 'generated-index',
        title: 'Module 4: Vision-Language-Action Models',
        description: 'LLM integration, voice recognition (OpenAI Whisper), and NLP to ROS 2 action translation.',
      },
      collapsed: true,
      items: [],
    },
    {
      type: 'category',
      label: 'Module 5: Humanoid Development & Capstone',
      link: {
        type: 'generated-index',
        title: 'Module 5: Humanoid Development & Capstone Project',
        description: 'Humanoid robot development theory and comprehensive integration capstone project.',
      },
      collapsed: true,
      items: [],
    },
  ],
};

export default sidebars;
