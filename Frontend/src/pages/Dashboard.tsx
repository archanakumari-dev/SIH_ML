import React, { useState } from 'react';
import {Upload,BarChart3, PieChart, Network, TrendingUp, AlertTriangle, Eye, Zap, Clock, MapPin } from 'lucide-react';
import Chatbot from './chatbot';

const Dashboard = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [analysisResults, setAnalysisResults] = useState(false);
  const [showChatbot, setShowChatbot] = useState(false);


  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      // Simulate analysis delay
      setTimeout(() => setAnalysisResults(true), 2000);
    }
  };

  const speciesData = [
    { name: 'Bathypelagic Fish', abundance: 35, color: '#06b6d4' },
    { name: 'Unknown Species A', abundance: 28, color: '#3b82f6' },
    { name: 'Deep-sea Crustacean', abundance: 22, color: '#8b5cf6' },
    { name: 'Novel Organism B', abundance: 15, color: '#10b981' }
  ];

  const taxaRichness = [
    { habitat: 'Abyssal Plains', count: 45 },
    { habitat: 'Hydrothermal Vents', count: 38 },
    { habitat: 'Seamounts', count: 52 },
    { habitat: 'Trenches', count: 29 }
  ];

  const biodiversityMetrics = [
    { name: 'Simpson Index', value: '0.82', description: 'High diversity' },
    { name: 'Evenness', value: '0.76', description: 'Well distributed' },
    { name: 'Chao1 Estimator', value: '156', description: 'Estimated total species' },
    { name: 'Good\'s Coverage', value: '94.2%', description: 'Sample completeness' }
  ];

  const environmentalFactors = [
    { factor: 'Temperature', value: '2.1°C', impact: 'Optimal' },
    { factor: 'Depth', value: '3,847m', impact: 'Deep Abyssal' },
    { factor: 'Salinity', value: '34.7 PSU', impact: 'Normal' },
    { factor: 'Oxygen', value: '2.8 mg/L', impact: 'Low' }
  ];

  const novelSpecies = [
    { id: 'NS001', confidence: 95, habitat: 'Hydrothermal Vents', similarity: '12%' },
    { id: 'NS002', confidence: 89, habitat: 'Abyssal Plains', similarity: '8%' },
    { id: 'NS003', confidence: 92, habitat: 'Seamounts', similarity: '15%' },
    { id: 'NS004', confidence: 87, habitat: 'Trenches', similarity: '6%' }
  ];

  const conservationAlerts = [
    { species: 'Deep-sea Coral', status: 'Endangered', trend: 'declining', priority: 'high' },
    { species: 'Abyssal Fish', status: 'Vulnerable', trend: 'stable', priority: 'medium' },
    { species: 'Hydrothermal Vent Fauna', status: 'Critical', trend: 'declining', priority: 'high' }
  ];

  return (
    <div className="min-h-screen text-white py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-cyan-300 to-blue-300 bg-clip-text text-transparent">
            eDNA Analysis Dashboard
          </h1>
          <p className="text-xl text-gray-300">Upload your eDNA sequences for AI-powered biodiversity analysis</p>
        </div>

        {/* Upload Section */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border-2 border-green-400 border-white/20 mb-12 ">
          <h2 className="text-2xl font-bold mb-6 flex items-center">
            <Upload className="mr-3 h-6 w-6 text-cyan-400" />
            Upload eDNA Sample
          </h2>
          
          <div className="border-2 border-dashed border-cyan-400 rounded-xl p-8 text-center">
            <input
              type="file"
              id="file-upload"
              accept=".fasta,.fastq,.txt"
              onChange={handleFileUpload}
              className="hidden"
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer flex flex-col items-center space-y-4"
            >
              <div className="bg-cyan-500/20 rounded-full p-6">
                <Upload className="h-12 w-12 text-cyan-400" />
              </div>
              <div>
                <p className="text-xl font-semibold mb-2">
                  {uploadedFile ? uploadedFile.name : 'Click to upload eDNA file'}
                </p>
                <p className="text-gray-400">Supports FASTA, FASTQ, and TXT formats</p>
              </div>
            </label>
          </div>

          {uploadedFile && !analysisResults && (
            <div className="mt-6 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400 mx-auto mb-4"></div>
              <p className="text-cyan-300">Analyzing sequences...</p>
            </div>
          )}
        </div>

        {/* Results Section */}
        {analysisResults && (
          <>
            {/* Summary Stats */}
            <div className="flex flex-wrap justify-between gap-6 mb-12">
  <div className="flex-1 min-w-[200px] bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 text-center">
    <div className="text-3xl font-bold text-cyan-400 mb-2">127</div>
    <div className="text-gray-300">Total Species</div>
  </div>
  <div className="flex-1 min-w-[200px] bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 text-center">
    <div className="text-3xl font-bold text-green-400 mb-2">23</div>
    <div className="text-gray-300">Novel Taxa</div>
  </div>
  <div className="flex-1 min-w-[200px] bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 text-center">
    <div className="text-3xl font-bold text-blue-400 mb-2">4.2</div>
    <div className="text-gray-300">Shannon Diversity</div>
  </div>
</div>


            {/* Advanced Metrics */}
            <div className="grid lg:grid-cols-2 gap-8 mb-12">
              {/* Biodiversity Indices */}
              <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
                <h3 className="text-xl font-bold mb-6 flex items-center">
                  <TrendingUp className="mr-3 h-5 w-5 text-cyan-400" />
                  Biodiversity Indices
                </h3>
                
                <div className="space-y-4">
                  {biodiversityMetrics.map((metric, index) => (
                    <div key={index} className="flex justify-between items-center p-4 bg-white/5 rounded-lg">
                      <div>
                        <div className="font-semibold text-white">{metric.name}</div>
                        <div className="text-sm text-gray-400">{metric.description}</div>
                      </div>
                      <div className="text-xl font-bold text-cyan-400">{metric.value}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Environmental Context */}
              <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
                <h3 className="text-xl font-bold mb-6 flex items-center">
                  <MapPin className="mr-3 h-5 w-5 text-cyan-400" />
                  Environmental Context
                </h3>
                
                <div className="space-y-4">
                  {environmentalFactors.map((env, index) => (
                    <div key={index} className="flex justify-between items-center p-4 bg-white/5 rounded-lg">
                      <div>
                        <div className="font-semibold text-white">{env.factor}</div>
                        <div className="text-sm text-gray-400">{env.impact}</div>
                      </div>
                      <div className="text-lg font-bold text-blue-400">{env.value}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="grid lg:grid-cols-2 gap-8 mb-12">
              {/* Species Abundance Chart */}
              <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
                <h3 className="text-xl font-bold mb-6 flex items-center">
                  <PieChart className="mr-3 h-5 w-5 text-cyan-400" />
                  Species Abundance Distribution
                </h3>
                
                <div className="space-y-4">
                  {speciesData.map((species, index) => (
                    <div key={index} className="flex items-center space-x-4">
                      <div
                        className="w-4 h-4 rounded-full"
                        style={{ backgroundColor: species.color }}
                      ></div>
                      <div className="flex-1">
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-sm font-medium">{species.name}</span>
                          <span className="text-sm text-gray-400">{species.abundance}%</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div
                            className="h-2 rounded-full transition-all duration-1000"
                            style={{
                              backgroundColor: species.color,
                              width: `${species.abundance}%`
                            }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Taxa Richness Chart */}
              <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
                <h3 className="text-xl font-bold mb-6 flex items-center">
                  <BarChart3 className="mr-3 h-5 w-5 text-cyan-400" />
                  Taxa Richness by Habitat
                </h3>
                
                <div className="space-y-4">
                  {taxaRichness.map((habitat, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium">{habitat.habitat}</span>
                        <span className="text-sm text-cyan-400 font-bold">{habitat.count}</span>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-3">
                        <div
                          className="bg-gradient-to-r from-cyan-500 to-blue-500 h-3 rounded-full transition-all duration-1000"
                          style={{ width: `${(habitat.count / 60) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Novel Species Discovery */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 mb-12">
              <h3 className="text-xl font-bold mb-6 flex items-center">
                <Eye className="mr-3 h-5 w-5 text-cyan-400" />
                Novel Species Discovery
              </h3>
              
              <div className="grid md:grid-cols-2 gap-6">
                {novelSpecies.map((species, index) => (
                  <div key={index} className="bg-white/5 rounded-xl p-6 border border-white/10">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h4 className="font-bold text-green-400 text-lg">{species.id}</h4>
                        <p className="text-gray-400 text-sm">{species.habitat}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-gray-400">Confidence</div>
                        <div className="text-lg font-bold text-green-400">{species.confidence}%</div>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-400">Similarity to known species</span>
                      <span className="text-sm font-semibold text-orange-400">{species.similarity}</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2 mt-3">
                      <div
                        className="bg-gradient-to-r from-green-500 to-cyan-500 h-2 rounded-full transition-all duration-1000"
                        style={{ width: `${species.confidence}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Conservation Alerts */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 mb-12">
              <h3 className="text-xl font-bold mb-6 flex items-center">
                <AlertTriangle className="mr-3 h-5 w-5 text-yellow-400" />
                Conservation Status Alerts
              </h3>
              
              <div className="space-y-4">
                {conservationAlerts.map((alert, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg border-l-4 border-l-yellow-400">
                    <div className="flex items-center space-x-4">
                      <AlertTriangle className={`h-5 w-5 ${alert.priority === 'high' ? 'text-red-400' : 'text-yellow-400'}`} />
                      <div>
                        <div className="font-semibold text-white">{alert.species}</div>
                        <div className="text-sm text-gray-400">Status: {alert.status}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`text-sm font-semibold ${alert.trend === 'declining' ? 'text-red-400' : 'text-green-400'}`}>
                        {alert.trend === 'declining' ? '↓ Declining' : '→ Stable'}
                      </div>
                      <div className={`text-xs ${alert.priority === 'high' ? 'text-red-400' : 'text-yellow-400'}`}>
                        {alert.priority.toUpperCase()} PRIORITY
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Community Structure Network */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 mb-12">
              <h3 className="text-xl font-bold mb-6 flex items-center">
                <Network className="mr-3 h-5 w-5 text-cyan-400" />
                Community Structure Network
              </h3>
              
              <div className="bg-gray-800/50 rounded-xl p-8 text-center">
                <div className="grid grid-cols-3 gap-8 items-center justify-items-center">
                  {/* Mock network visualization */}
                  <div className="relative">
                    <div className="w-16 h-16 bg-cyan-500 rounded-full flex items-center justify-center text-xs font-bold">
                      Hub 1
                    </div>
                    <div className="absolute -top-2 -right-2 w-8 h-8 bg-blue-400 rounded-full opacity-75"></div>
                  </div>
                  
                  <div className="relative">
                    <div className="w-20 h-20 bg-purple-500 rounded-full flex items-center justify-center text-xs font-bold">
                      Hub 2
                    </div>
                    <div className="absolute -bottom-2 -left-2 w-6 h-6 bg-green-400 rounded-full opacity-75"></div>
                    <div className="absolute -top-2 -right-2 w-6 h-6 bg-blue-400 rounded-full opacity-75"></div>
                  </div>
                  
                  <div className="relative">
                    <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center text-xs font-bold">
                      Hub 3
                    </div>
                    <div className="absolute -top-2 -left-2 w-8 h-8 bg-cyan-400 rounded-full opacity-75"></div>
                  </div>
                </div>
                
                <p className="text-gray-400 mt-6">
                  Interactive network showing species interactions and community clusters
                </p>
              </div>
            </div>

            {/* AI Processing Insights */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 mb-12">
              <h3 className="text-xl font-bold mb-6 flex items-center">
                <Zap className="mr-3 h-5 w-5 text-cyan-400" />
                AI Processing Insights
              </h3>
              
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center p-6 bg-white/5 rounded-xl">
                  <Clock className="h-8 w-8 text-cyan-400 mx-auto mb-3" />
                  <div className="text-2xl font-bold text-white mb-2">2.3 min</div>
                  <div className="text-gray-400 text-sm">Processing Time</div>
                </div>
                
                <div className="text-center p-6 bg-white/5 rounded-xl">
                  <BarChart3 className="h-8 w-8 text-green-400 mx-auto mb-3" />
                  <div className="text-2xl font-bold text-white mb-2">15,847</div>
                  <div className="text-gray-400 text-sm">Sequences Analyzed</div>
                </div>
                
                <div className="text-center p-6 bg-white/5 rounded-xl">
                  <Network className="h-8 w-8 text-purple-400 mx-auto mb-3" />
                  <div className="text-2xl font-bold text-white mb-2">97.2%</div>
                  <div className="text-gray-400 text-sm">Model Confidence</div>
                </div>
              </div>
              
              <div className="mt-6 p-4 bg-cyan-500/10 rounded-lg border border-cyan-500/20">
                <h4 className="font-semibold text-cyan-300 mb-2">Key Findings:</h4>
                <ul className="text-gray-300 text-sm space-y-1">
                  <li>• Discovered 4 potentially novel species with high confidence scores</li>
                  <li>• Identified rare deep-sea coral communities in critical conservation status</li>
                  <li>• Detected unusual biodiversity patterns suggesting unique ecosystem dynamics</li>
                  <li>• Found evidence of microplastic impact on deep-sea fauna distribution</li>
                </ul>
              </div>
            </div>

            
           {!showChatbot&&(<button type="button" className="flex  items-center px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg font-semibold hover:from-cyan-600 hover:to-blue-600 transition-all"
             onClick={() => setShowChatbot(prev=>!prev)}
            >
                   
                 {showChatbot ? "Close AI Chatbot" : "AI Chatbot"}
                </button>)} 
                {showChatbot && (
  <div>
    <Chatbot setShowChatbot={setShowChatbot} />
  </div>
)}
          </>
        )}
      </div>
      
    </div>
    
  );
};

export default Dashboard;