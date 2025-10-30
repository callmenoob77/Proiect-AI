import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, XCircle, RefreshCw, Brain, Sparkles, Trophy, Target } from 'lucide-react';

export default function QuestionApp() {
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState(null);
  const [score, setScore] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(0);

  const API_BASE_URL = 'http://localhost:8000';

  const fetchQuestion = async () => {
    setLoading(true);
    setError(null);
    setSelectedAnswer(null);
    setSubmitted(false);

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate/strategy`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to generate question');
      }

      const data = await response.json();
      setQuestion(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestion();
  }, []);

  const extractOptions = (prompt) => {
    const match = prompt.match(/menţionate: (.+)\?/);
    if (match) {
      return match[1].split(', ').map(opt => opt.trim());
    }
    return [];
  };

  const handleSubmit = () => {
    if (selectedAnswer) {
      setSubmitted(true);
      setTotalQuestions(prev => prev + 1);
      if (isCorrect()) {
        setScore(prev => prev + 1);
      }
    }
  };

  const isCorrect = () => {
    return selectedAnswer === question?.correct_answer?.answer;
  };

  const handleNewQuestion = () => {
    fetchQuestion();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="relative">
            <Brain className="w-20 h-20 text-white mx-auto mb-6 animate-pulse" />
            <Sparkles className="w-8 h-8 text-yellow-300 absolute top-0 right-0 animate-bounce" />
          </div>
          <p className="text-white text-xl font-semibold">Se generează întrebarea...</p>
          <p className="text-purple-200 mt-2">Pregătește-te să gândești strategic!</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full transform hover:scale-105 transition-transform">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-center text-gray-800 mb-2">Oops! Ceva nu a mers bine</h2>
          <p className="text-center text-gray-600 mb-6">{error}</p>
          <button
            onClick={fetchQuestion}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-lg"
          >
            <RefreshCw className="w-5 h-5 inline mr-2" />
            Încearcă din nou
          </button>
        </div>
      </div>
    );
  }

  if (!question) return null;

  const options = extractOptions(question.prompt);
  const showCorrectAnswer = !question.protected;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 py-8 px-4">
      {/* Header cu statistici */}
      <div className="max-w-4xl mx-auto mb-6">
        <div className="flex items-center justify-between bg-white/20 backdrop-blur-lg rounded-2xl p-4 text-white shadow-xl">
          <div className="flex items-center gap-3">
            <Brain className="w-10 h-10" />
            <div>
              <h1 className="text-2xl font-bold">AI Strategy Quiz</h1>
              <p className="text-sm text-purple-100">Testează-ți cunoștințele algoritmice</p>
            </div>
          </div>
          <div className="flex gap-6">
            <div className="text-center bg-white/20 rounded-xl px-4 py-2">
              <Trophy className="w-6 h-6 mx-auto mb-1" />
              <p className="text-2xl font-bold">{score}</p>
              <p className="text-xs">Scor</p>
            </div>
            <div className="text-center bg-white/20 rounded-xl px-4 py-2">
              <Target className="w-6 h-6 mx-auto mb-1" />
              <p className="text-2xl font-bold">{totalQuestions}</p>
              <p className="text-xs">Întrebări</p>
            </div>
          </div>
        </div>
      </div>

      {/* Card principal */}
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-3xl shadow-2xl overflow-hidden transform hover:shadow-3xl transition-shadow">
          {/* Header gradient */}
          <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-8 text-white">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles className="w-6 h-6" />
                  <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">
                    Nivel {question.difficulty}
                  </span>
                </div>
                <h2 className="text-3xl font-bold mb-2">{question.title}</h2>
                <p className="text-purple-100 text-sm">#{question.question_type}</p>
              </div>
            </div>
          </div>

          {/* Conținut */}
          <div className="p-8">
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl p-6 mb-8 border-l-4 border-purple-600">
              <p className="text-gray-800 text-lg leading-relaxed">{question.prompt}</p>
            </div>

            {/* Opțiuni */}
            <div className="space-y-4 mb-8">
              {options.map((option, index) => {
                const isSelected = selectedAnswer === option;
                const showResult = submitted && showCorrectAnswer;
                const isThisCorrect = option === question.correct_answer?.answer;

                let buttonStyle = 'bg-white border-2 border-gray-200 hover:border-purple-400 hover:shadow-lg';
                let iconColor = 'text-gray-400';

                if (isSelected && !submitted) {
                  buttonStyle = 'bg-gradient-to-r from-purple-100 to-blue-100 border-2 border-purple-500 shadow-lg scale-105';
                  iconColor = 'text-purple-600';
                }
                if (showResult && isThisCorrect) {
                  buttonStyle = 'bg-gradient-to-r from-green-100 to-emerald-100 border-2 border-green-500 shadow-lg';
                  iconColor = 'text-green-600';
                }
                if (showResult && isSelected && !isThisCorrect) {
                  buttonStyle = 'bg-gradient-to-r from-red-100 to-pink-100 border-2 border-red-500 shadow-lg';
                  iconColor = 'text-red-600';
                }

                return (
                  <button
                    key={index}
                    onClick={() => !submitted && setSelectedAnswer(option)}
                    disabled={submitted}
                    className={`w-full text-left p-5 rounded-2xl transition-all duration-300 transform ${buttonStyle} ${
                      submitted ? 'cursor-default' : 'cursor-pointer hover:scale-102'
                    } flex items-center justify-between group`}
                  >
                    <div className="flex items-center gap-4">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg ${
                        isSelected && !submitted ? 'bg-purple-600 text-white' : 'bg-gray-100 text-gray-600'
                      } ${showResult && isThisCorrect ? 'bg-green-600 text-white' : ''} 
                      ${showResult && isSelected && !isThisCorrect ? 'bg-red-600 text-white' : ''}`}>
                        {String.fromCharCode(65 + index)}
                      </div>
                      <span className="font-medium text-gray-800 text-lg">{option}</span>
                    </div>
                    {showResult && isThisCorrect && (
                      <CheckCircle className="w-7 h-7 text-green-600" />
                    )}
                    {showResult && isSelected && !isThisCorrect && (
                      <XCircle className="w-7 h-7 text-red-600" />
                    )}
                  </button>
                );
              })}
            </div>

            {/* Butoane acțiune */}
            {!submitted ? (
              <button
                onClick={handleSubmit}
                disabled={!selectedAnswer}
                className={`w-full py-4 px-6 rounded-2xl font-bold text-lg transition-all transform ${
                  selectedAnswer
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:from-purple-700 hover:to-blue-700 shadow-xl hover:shadow-2xl hover:scale-105'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                }`}
              >
                {selectedAnswer ? 'Verifică răspunsul 🎯' : 'Selectează un răspuns'}
              </button>
            ) : (
              <div className="space-y-4">
                {showCorrectAnswer && (
                  <div
                    className={`p-6 rounded-2xl border-2 ${
                      isCorrect()
                        ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-400'
                        : 'bg-gradient-to-r from-red-50 to-pink-50 border-red-400'
                    }`}
                  >
                    <div className="flex items-center mb-3">
                      {isCorrect() ? (
                        <>
                          <CheckCircle className="w-8 h-8 text-green-600 mr-3" />
                          <span className="font-bold text-2xl text-gray-800">Excelent! 🎉</span>
                        </>
                      ) : (
                        <>
                          <XCircle className="w-8 h-8 text-red-600 mr-3" />
                          <span className="font-bold text-2xl text-gray-800">Aproape! 💪</span>
                        </>
                      )}
                    </div>
                    <div className="bg-white/60 rounded-xl p-4 mt-3">
                      <p className="text-gray-700 leading-relaxed">{question.reference_solution}</p>
                    </div>
                  </div>
                )}

                {!showCorrectAnswer && (
                  <div className="p-6 rounded-2xl bg-gradient-to-r from-blue-50 to-cyan-50 border-2 border-blue-300">
                    <div className="flex items-center mb-2">
                      <Brain className="w-6 h-6 text-blue-600 mr-2" />
                      <span className="font-bold text-lg text-gray-800">Răspuns înregistrat!</span>
                    </div>
                    <p className="text-gray-700">
                      Ai ales: <span className="font-semibold text-blue-600">{selectedAnswer}</span>
                    </p>
                  </div>
                )}

                <button
                  onClick={handleNewQuestion}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 px-6 rounded-2xl font-bold text-lg hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-xl flex items-center justify-center gap-2"
                >
                  <RefreshCw className="w-6 h-6" />
                  Întrebare Nouă
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Footer info */}
        <div className="text-center mt-6 text-white/80 text-sm">
          <p>Proiect AI - Algoritmi și Strategii</p>
        </div>
      </div>
    </div>
  );
}