import React, { useState } from 'react';
import { CheckCircle, XCircle, AlertCircle, Trophy, Clock, BookOpen, ArrowRight, Home } from 'lucide-react';
import TreeVisualizer from './TreeVisualizer';
import GameMatrixVisualizer from './GameMatrixVisualizer';

export default function TestMode({ onBackToHome, apiBaseUrl }) {
  const [testState, setTestState] = useState('setup'); // setup, taking, results
  const [numQuestions, setNumQuestions] = useState(5);
  const [testData, setTestData] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [testResults, setTestResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateTest = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${apiBaseUrl}/api/test/generate?num_questions=${numQuestions}`, {
        method: 'POST'
      });

      if (!response.ok) throw new Error('Nu s-a putut genera testul');

      const data = await response.json();
      setTestData(data);
      setTestState('taking');
      setCurrentQuestionIndex(0);
      setAnswers({});
    } catch (err) {
      alert('Eroare: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const submitTest = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${apiBaseUrl}/api/test/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(answers)
      });

      if (!response.ok) throw new Error('Nu s-a putut trimite testul');

      const results = await response.json();
      setTestResults(results);
      setTestState('results');
    } catch (err) {
      alert('Eroare: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const selectAnswer = (questionId, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const goToQuestion = (index) => {
    setCurrentQuestionIndex(index);
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < testData.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const previousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  // ========== SETUP SCREEN ==========
  if (testState === 'setup') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-8">
            <BookOpen className="w-16 h-16 mx-auto text-purple-600 mb-4" />
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Creează Test</h1>
            <p className="text-gray-600">Testează-ți cunoștințele cu întrebări multiple choice</p>
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 font-semibold mb-3">
              Câte întrebări dorești?
            </label>
            <input
              type="range"
              min="3"
              max="15"
              value={numQuestions}
              onChange={(e) => setNumQuestions(parseInt(e.target.value))}
              className="w-full h-2 bg-purple-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-sm text-gray-600 mt-2">
              <span>3</span>
              <span className="text-2xl font-bold text-purple-600">{numQuestions}</span>
              <span>15</span>
            </div>
          </div>

          <button
            onClick={generateTest}
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-2xl font-bold text-lg hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-xl disabled:opacity-50"
          >
            {loading ? 'Se generează...' : 'Generează Test 🎯'}
          </button>

          <button
            onClick={onBackToHome}
            className="w-full mt-4 bg-gray-200 text-gray-700 py-3 rounded-2xl font-semibold hover:bg-gray-300 transition-all"
          >
            <Home className="w-5 h-5 inline mr-2" />
            Înapoi
          </button>
        </div>
      </div>
    );
  }

  // ========== TAKING TEST ==========
  if (testState === 'taking' && testData) {
    const currentQuestion = testData.questions[currentQuestionIndex];
    const progress = ((currentQuestionIndex + 1) / testData.questions.length) * 100;
    const answeredCount = Object.keys(answers).length;

    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 py-8 px-4">
        {/* Progress Bar */}
        <div className="max-w-4xl mx-auto mb-6">
          <div className="bg-white rounded-2xl p-4 shadow-xl">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-700 font-semibold">
                Întrebarea {currentQuestionIndex + 1} / {testData.questions.length}
              </span>
              <span className="text-gray-600">
                Răspuns: {answeredCount} / {testData.questions.length}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-gradient-to-r from-purple-600 to-blue-600 h-3 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        </div>

        {/* Question Card */}
        <div className="max-w-4xl mx-auto bg-white rounded-3xl shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-6 text-white">
            <h2 className="text-2xl font-bold">{currentQuestion.title}</h2>
            <p className="text-purple-100 mt-1">#{currentQuestion.question_type}</p>
          </div>

          <div className="p-8">
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl p-6 mb-6 border-l-4 border-purple-600">
              <p className="text-gray-800 text-lg">{currentQuestion.prompt}</p>
            </div>

            {/* Tree Visualizer for MINIMAX */}
            {currentQuestion.question_type === "MINIMAX_TREE" && currentQuestion.problem_instance?.tree && (
              <div className="mb-6">
                <TreeVisualizer tree={currentQuestion.problem_instance.tree} />
              </div>
            )}

            {/* Game Matrix Visualizer for NASH */}
            {currentQuestion.question_type === "GAME_MATRIX" && currentQuestion.problem_instance?.matrix && (
              <div className="mb-6">
                <GameMatrixVisualizer matrix={currentQuestion.problem_instance.matrix} />
              </div>
            )}

            {/* Options */}
            <div className="space-y-4 mb-6">
              {currentQuestion.options.map((option, index) => {
                const isSelected = answers[currentQuestion.id] === option;
                return (
                  <button
                    key={index}
                    onClick={() => selectAnswer(currentQuestion.id, option)}
                    className={`w-full text-left p-5 rounded-2xl transition-all duration-300 transform hover:scale-102 ${isSelected
                        ? 'bg-gradient-to-r from-purple-100 to-blue-100 border-2 border-purple-500 shadow-lg scale-105'
                        : 'bg-white border-2 border-gray-200 hover:border-purple-400 hover:shadow-lg'
                      }`}
                  >
                    <div className="flex items-center gap-4">
                      <div
                        className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg ${isSelected ? 'bg-purple-600 text-white' : 'bg-gray-100 text-gray-600'
                          }`}
                      >
                        {String.fromCharCode(65 + index)}
                      </div>
                      <span className="font-medium text-gray-800 text-lg">{option}</span>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Navigation */}
            <div className="flex gap-4">
              <button
                onClick={previousQuestion}
                disabled={currentQuestionIndex === 0}
                className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-2xl font-semibold hover:bg-gray-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                ← Înapoi
              </button>

              {currentQuestionIndex === testData.questions.length - 1 ? (
                <button
                  onClick={submitTest}
                  disabled={answeredCount !== testData.questions.length || loading}
                  className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 rounded-2xl font-semibold hover:from-green-700 hover:to-emerald-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Se trimite...' : 'Finalizează Test ✓'}
                </button>
              ) : (
                <button
                  onClick={nextQuestion}
                  className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-2xl font-semibold hover:from-purple-700 hover:to-blue-700 transition-all"
                >
                  Următoarea →
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Question Navigator */}
        <div className="max-w-4xl mx-auto mt-6">
          <div className="bg-white rounded-2xl p-4 shadow-xl">
            <p className="text-gray-700 font-semibold mb-3">Navigare Întrebări:</p>
            <div className="flex flex-wrap gap-2">
              {testData.questions.map((q, index) => {
                const isAnswered = answers[q.id] !== undefined;
                const isCurrent = index === currentQuestionIndex;
                return (
                  <button
                    key={q.id}
                    onClick={() => goToQuestion(index)}
                    className={`w-12 h-12 rounded-lg font-bold transition-all ${isCurrent
                        ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white scale-110 shadow-lg'
                        : isAnswered
                          ? 'bg-green-100 text-green-700 border-2 border-green-400'
                          : 'bg-gray-100 text-gray-600 border-2 border-gray-300'
                      }`}
                  >
                    {index + 1}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ========== RESULTS SCREEN ==========
  if (testState === 'results' && testResults) {
    const { results, summary } = testResults;
    const percentage = summary.percentage;

    let gradeColor = 'red';
    let gradeText = 'Încearcă din nou';
    let gradeIcon = XCircle;

    if (percentage >= 90) {
      gradeColor = 'green';
      gradeText = 'Excelent!';
      gradeIcon = Trophy;
    } else if (percentage >= 70) {
      gradeColor = 'blue';
      gradeText = 'Foarte bine!';
      gradeIcon = CheckCircle;
    } else if (percentage >= 50) {
      gradeColor = 'yellow';
      gradeText = 'Bine!';
      gradeIcon = AlertCircle;
    }

    const GradeIcon = gradeIcon;

    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 py-8 px-4">
        {/* Summary Card */}
        <div className="max-w-4xl mx-auto mb-6">
          <div className={`bg-gradient-to-r from-${gradeColor}-500 to-${gradeColor}-600 rounded-3xl p-8 text-white shadow-2xl`}>
            <div className="text-center">
              <GradeIcon className="w-20 h-20 mx-auto mb-4" />
              <h1 className="text-4xl font-bold mb-2">{gradeText}</h1>
              <p className="text-2xl mb-6">Scor: {summary.correct_answers} / {summary.total_questions}</p>
              <div className="bg-white/20 rounded-2xl p-6 inline-block">
                <p className="text-5xl font-bold">{Math.round(percentage)}%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Detailed Results */}
        <div className="max-w-4xl mx-auto space-y-4">
          {testData.questions.map((question, index) => {
            const result = results[question.id];
            if (!result) return null;

            const isCorrect = result.is_correct;

            return (
              <div key={question.id} className="bg-white rounded-2xl shadow-xl overflow-hidden">
                <div className={`p-6 ${isCorrect ? 'bg-green-50' : 'bg-red-50'}`}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        {isCorrect ? (
                          <CheckCircle className="w-6 h-6 text-green-600" />
                        ) : (
                          <XCircle className="w-6 h-6 text-red-600" />
                        )}
                        <h3 className="text-xl font-bold text-gray-800">
                          Întrebarea {index + 1}
                        </h3>
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${isCorrect ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
                          }`}>
                          {Math.round(result.score)}%
                        </span>
                      </div>
                      <p className="text-gray-700 mb-4">{question.prompt}</p>

                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-gray-700">Răspunsul tău:</span>
                          <span className={isCorrect ? 'text-green-700' : 'text-red-700'}>
                            {result.user_answer}
                          </span>
                        </div>

                        {!isCorrect && (
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-gray-700">Răspuns corect:</span>
                            <span className="text-green-700">{result.correct_answer}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {result.reference_solution && (
                    <div className="mt-4 p-4 bg-white rounded-xl border-l-4 border-purple-600">
                      <p className="font-semibold text-gray-800 mb-1">Explicație:</p>
                      <p className="text-gray-700">{result.reference_solution}</p>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Action Buttons */}
        <div className="max-w-4xl mx-auto mt-8 flex gap-4">
          <button
            onClick={() => {
              setTestState('setup');
              setTestData(null);
              setTestResults(null);
              setAnswers({});
            }}
            className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-2xl font-bold text-lg hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-xl"
          >
            Test Nou 🎯
          </button>

          <button
            onClick={onBackToHome}
            className="flex-1 bg-white text-gray-700 py-4 rounded-2xl font-bold text-lg hover:bg-gray-100 transition-all shadow-xl"
          >
            <Home className="w-5 h-5 inline mr-2" />
            Acasă
          </button>
        </div>
      </div>
    );
  }

  return null;
}