/**
 * Swizzled Docusaurus Layout component
 *
 * Wraps the original Layout and injects the ChatbotWidget
 * This allows the chatbot to appear on all pages
 */
import React from 'react';
import Layout from '@theme-original/Layout';
import ChatbotWidget from '@site/src/components/Chatbot/ChatbotWidget';

export default function LayoutWrapper(props: any) {
  return (
    <>
      <Layout {...props} />
      <ChatbotWidget />
    </>
  );
}
