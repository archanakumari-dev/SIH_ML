import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Brain, Database, BarChart3, FileText, Microscope, Globe } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: <Brain className="h-8 w-8" />,
      title: "AI-Powered Taxonomy Detection",
      description: "Advanced machine learning algorithms for accurate species identification"
    },
    {
      icon: <Microscope className="h-8 w-8" />,
      title: "Novel Taxa Discovery",
      description: "Unsupervised learning pipeline to discover unknown species"
    },
    {
      icon: <BarChart3 className="h-8 w-8" />,
      title: "Real-time Dashboard",
      description: "Interactive visualizations for biodiversity insights"
    },
    {
      icon: <Database className="h-8 w-8" />,
      title: "Database-Independent",
      description: "Works without relying on incomplete reference databases"
    },
    {
      icon: <FileText className="h-8 w-8" />,
      title: "Report Generation",
      description: "Comprehensive PDF and CSV reports for stakeholders"
    },
    {
      icon: <Globe className="h-8 w-8" />,
      title: "Conservation Impact",
      description: "Supporting marine conservation with accurate data"
    }
  ];

  return (
    <div className="text-white">
      {/* Hero Section */}
      <section className="relative py-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-cyan-500/20 to-blue-600/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-cyan-300 to-blue-300 bg-clip-text text-transparent">
            AI-driven Deep-Sea eDNA
            <br />
            Biodiversity Analyzer
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto">
            Revolutionizing Deep-Sea Biodiversity Monitoring with AI + eDNA
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/dashboard"
              className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg font-semibold text-white hover:from-cyan-600 hover:to-blue-600 transition-all transform hover:scale-105 shadow-lg"
            >
              Try Demo
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
            <button className="inline-flex items-center px-8 py-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg font-semibold text-white hover:bg-white/20 transition-all">
              Download Report
              <FileText className="ml-2 h-5 w-5" />
            </button>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="py-20 bg-white/5 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-cyan-300 to-blue-300 bg-clip-text text-transparent">
              About Our Solution
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <h3 className="text-2xl font-bold mb-4 text-cyan-300">The Problem</h3>
              <p className="text-gray-300 leading-relaxed">
                Deep-sea biodiversity monitoring faces critical challenges due to incomplete reference databases 
                and limited taxonomic expertise. Traditional methods struggle with novel species discovery and 
                accurate abundance estimation in these unexplored ecosystems.
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <h3 className="text-2xl font-bold mb-4 text-cyan-300">Our Solution</h3>
              <p className="text-gray-300 leading-relaxed">
                Our AI-driven pipeline combines unsupervised learning with advanced classification algorithms 
                to discover novel taxa, classify sequences, and estimate abundance without relying on 
                incomplete reference databases.
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <h3 className="text-2xl font-bold mb-4 text-cyan-300">The Impact</h3>
              <p className="text-gray-300 leading-relaxed">
                Faster, more accurate biodiversity insights that support marine conservation efforts, 
                enable better policy decisions, and advance our understanding of deep-sea ecosystems 
                critical for global ocean health.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-cyan-300 to-blue-300 bg-clip-text text-transparent">
              Key Features
            </h2>
            <p className="text-xl text-gray-300">Advanced capabilities for comprehensive biodiversity analysis</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all transform hover:scale-105"
              >
                <div className="text-cyan-400 mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-3 text-white">{feature.title}</h3>
                <p className="text-gray-300">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-cyan-600/20 to-blue-600/20">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold mb-4">Ready to Explore Deep-Sea Biodiversity?</h2>
          <p className="text-xl text-gray-300 mb-8">
            Experience the future of marine biodiversity monitoring with our AI-powered platform
          </p>
          <Link
            to="/dashboard"
            className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg font-semibold text-white hover:from-cyan-600 hover:to-blue-600 transition-all transform hover:scale-105 shadow-lg"
          >
            Start Analysis
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;