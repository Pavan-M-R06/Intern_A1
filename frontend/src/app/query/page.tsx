"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, Brain, Loader2, Send, Sparkles, BookOpen } from "lucide-react";
import { api } from "@/lib/api";

export default function QueryPage() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const commonQuestions = [
    "Explain JWT Authentication to me",
    "What should I learn next?",
    "Summarize my progress this week",
    "Help me understand async/await",
  ];

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setResponse("");

    try {
      // Detect question type and call appropriate API
      if (question.toLowerCase().includes("explain") || question.toLowerCase().includes("what is")) {
        // Extract concept name
        const conceptMatch = question.match(/explain\s+(.+?)(?:\s+to\s+me)?$/i) || 
                           question.match(/what\s+is\s+(.+?)(?:\?)?$/i);
        const concept = conceptMatch ? conceptMatch[1] : question;
        
        const result = await api.explainConcept(concept);
        setResponse(result.explanation);
      } else if (question.toLowerCase().includes("should i learn") || question.toLowerCase().includes("what next")) {
        const result = await api.getLearningGuidance();
        setResponse(result.guidance);
      } else {
        // Default to concept explanation
        const result = await api.explainConcept(question);
        setResponse(result.explanation);
      }
    } catch (err: any) {
      setError(err.message || "Failed to get response");
    } finally {
      setLoading(false);
    }
  };

  const askCommon = (q: string) => {
    setQuestion(q);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="glass border-b border-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <Link href="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Dashboard</span>
          </Link>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        <div className="space-y-8">
          {/* Title */}
          <div className="space-y-2 text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-600/20 to-cyan-600/20 border border-purple-500/20 mb-4">
              <Brain className="w-8 h-8 gradient-text" />
            </div>
            <h1 className="text-4xl font-bold gradient-text">Ask Your AI Mentor</h1>
            <p className="text-muted-foreground">Get personalized explanations based on your learning history</p>
          </div>

          {/* Common Questions */}
          {!response && (
            <div className="card-glass space-y-4">
              <p className="text-sm font-medium flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-primary" />
                Try asking:
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {commonQuestions.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => askCommon(q)}
                    className="p-4 rounded-lg bg-muted/50 hover:bg-muted text-left transition-all hover:scale-[1.02] border border-transparent hover:border-primary/30"
                  >
                    <p className="text-sm">{q}</p>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div className="card-glass space-y-4">
            <div className="flex gap-3">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAsk()}
                placeholder="Ask me anything about your learning..."
                className="input flex-1"
              />
              <button
                onClick={handleAsk}
                disabled={loading || !question.trim()}
                className="btn-primary px-6 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>
            
            {error && (
              <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive">
                <p className="text-sm font-medium">{error}</p>
              </div>
            )}
          </div>

          {/* Response */}
          {loading && (
            <div className="card-glass">
              <div className="flex items-center gap-3 text-primary">
                <Brain className="w-6 h-6 animate-pulse" />
                <p className="text-sm font-medium">AI Mentor is thinking...</p>
              </div>
            </div>
          )}

          {response && (
            <div className="card-glass space-y-4 animate-in">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-600 to-cyan-500 flex items-center justify-center flex-shrink-0">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1 space-y-3">
                  <div className="prose prose-invert max-w-none">
                    <div className="whitespace-pre-wrap leading-relaxed">
                      {response}
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-3 pt-4 border-t border-border">
                <button
                  onClick={() => {
                    setQuestion("");
                    setResponse("");
                  }}
                  className="btn-secondary text-sm px-4 py-2"
                >
                  Ask Another Question
                </button>
                <button
                  onClick={() => navigator.clipboard.writeText(response)}
                  className="btn-ghost text-sm px-4 py-2"
                >
                  Copy Response
                </button>
              </div>
            </div>
          )}

          {/* Info Card */}
          {!response && !loading && (
            <div className="card-glass">
              <div className="flex items-start gap-4">
                <div className="p-3 rounded-lg bg-primary/10">
                  <BookOpen className="w-6 h-6 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold mb-2">Personalized Teaching</h3>
                  <p className="text-sm text-muted-foreground">
                    Your AI Mentor knows what you've already learned and adapts explanations to your level.
                    It references your past mistakes and learning patterns to give you the most relevant guidance.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
