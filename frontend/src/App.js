import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, XCircle, RefreshCw, Brain, Sparkles, Trophy, Target, Type, ListChecks, GitBranch, BookOpen } from 'lucide-react';
import TreeVisualizer from './components/TreeVisualizer';
import TestMode from './components/TestMode';

export default function QuestionApp() {
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [textAnswer, setTextAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [error, setError] = useState(null);
  const [score, setScore] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [answerType, setAnswerType] = useState('multiple');
  const [submitting, setSubmitting] = useState(false);
  const [customMode, setCustomMode] = useState(false);
  const [patternType, setPatternType] = useState('THEORY');
  const [patternInputs, setPatternInputs] = useState({});
  const [showTestMode, setShowTestMode] = useState(false);

  const API_BASE_URL = 'http://localhost:8000';
  const defaultPatternByType = {
    THEORY: 'DESCRIPTION',
    STRATEGY: 'GENERIC',
    CSP: 'FC',
    MINIMAX: 'BASIC',
  };

  const fetchQuestion = async (type) => {
    setLoading(true);
    setError(null);
    setSelectedAnswer(null);
    setTextAnswer('');
    setSubmitted(false);
    setEvaluationResult(null);
    setAnswerType(type);
    setQuestion(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate/strategy`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          answer_type: type
        })
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to generate question');
      }

      const data = await response.json();
      setQuestion(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const submitCustomQuestion = async () => {
    if (!patternType) return;

    const needsInputs = patternType !== 'MINIMAX';
    if (needsInputs && Object.keys(patternInputs).length === 0) return

    setLoading(true);
    setError(null);
    setQuestion(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/custom-question/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pattern_type: patternType,
          pattern_id: defaultPatternByType[patternType],
          inputs: patternInputs,
          answer_type: answerType
        })
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to submit custom question');
      }

      const data = await response.json();
      setQuestion(data);
      setPatternInputs({});

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // fetchQuestion('multiple');
  }, []);

  const handleSubmit = async () => {
    const userAnswer = (question && question.answer_type === 'multiple') ? selectedAnswer : textAnswer;

    if (!userAnswer || userAnswer.trim() === '') {
      return;
    }

    setSubmitting(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/answer/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question_id: question.id,
          user_answer: userAnswer
        })
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to submit answer');
      }

      const result = await response.json();

      if (result.correct_answer) {
        setEvaluationResult({ ...result, correct_answer_text: result.correct_answer });
      } else {
        setEvaluationResult(result);
      }

      setSubmitted(true);
      setTotalQuestions(prev => prev + 1);

      if (result.is_correct) {
        setScore(prev => prev + 1);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleNewQuestion = (type) => {
    setShowTestMode(false);
    fetchQuestion(type);
  };

  const renderHeader = () => (
    <div className="max-w-4xl mx-auto mb-6">
      <div className="flex items-center justify-between bg-white/20 backdrop-blur-lg rounded-2xl p-4 text-white shadow-xl">
        <div className="flex items-center gap-3">
          <Brain className="w-10 h-10" />
          <div>
            <h1 className="text-2xl font-bold">SmarTest AI</h1>
            <p className="text-sm text-purple-100">Învață inteligent</p>
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
  );

  // ===== RENDERARE TEST MODE =====
  if (showTestMode) {
    return <TestMode onBackToHome={() => setShowTestMode(false)} apiBaseUrl={API_BASE_URL} />;
  }

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
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-center text-gray-800 mb-2">Oops! Ceva nu a mers bine</h2>
          <p className="text-center text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => { setError(null); setQuestion(null); }}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-purple-700 hover:to-blue-700 transition-all"
          >
            <RefreshCw className="w-5 h-5 inline mr-2" />
            Mergi la început
          </button>
        </div>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 py-8 px-4">
        {renderHeader()}

        <div className="max-w-4xl mx-auto bg-white rounded-3xl shadow-2xl p-8 text-center">
          {/* SWITCH MOD */}
          <div className="flex justify-center gap-4 mb-8">
            <button
              onClick={() => setCustomMode(false)}
              className={`px-6 py-2 rounded-xl font-semibold transition ${
                !customMode ? 'bg-purple-600 text-white' : 'bg-gray-200'
              }`}
            >
              Întrebare generată
            </button>

            <button
              onClick={() => setCustomMode(true)}
              className={`px-6 py-2 rounded-xl font-semibold transition ${
                customMode ? 'bg-blue-600 text-white' : 'bg-gray-200'
              }`}
            >
              Întrebare pe pattern
            </button>
          </div>

          {/* ================= MOD: ÎNTREBARE PE PATTERN ================= */}
          {customMode ? (
            <>
              <h2 className="text-3xl font-bold text-gray-800 mb-4">
                Creează o întrebare pe pattern
              </h2>
              <p className="text-gray-600 mb-6">
                Completează câmpurile – sistemul va construi întrebarea.
              </p>

              <select
                value={patternType}
                onChange={(e) => {
                  setPatternType(e.target.value);
                  setPatternInputs({});
                }}
                className="p-4 rounded-xl border-2 border-gray-300 mb-6 w-full"
              >
                <option value="THEORY">Teorie</option>
                <option value="STRATEGY">Strategie</option>
                <option value="CSP">CSP</option>
                <option value="MINIMAX">Minimax</option>
              </select>

              {patternType === 'THEORY' && (
                <input
                  type="text"
                  placeholder="Nume strategie (ex: A* Search)"
                  className="w-full p-4 rounded-xl border-2 border-gray-300 mb-6"
                  onChange={(e) =>
                    setPatternInputs({ strategy_name: e.target.value })
                  }
                />
              )}

              {patternType === 'STRATEGY' && (
                <>
                  <input
                    type="text"
                    placeholder="Nume problemă (ex: N-Queens)"
                    className="w-full p-4 rounded-xl border-2 border-gray-300 mb-3"
                    onChange={(e) =>
                      setPatternInputs(prev => ({
                        ...prev,
                        problem_name: e.target.value
                      }))
                    }
                  />
                  <input
                    type="text"
                    placeholder="Instanță (ex: tablă 8x8)"
                    className="w-full p-4 rounded-xl border-2 border-gray-300 mb-6"
                    onChange={(e) =>
                      setPatternInputs(prev => ({
                        ...prev,
                        instance: e.target.value
                      }))
                    }
                  />
                </>
              )}

              {patternType === 'CSP' && (
                <>
                  <input
                    type="text"
                    placeholder="Variabila 1 (ex: X)"
                    className="w-full p-4 rounded-xl border-2 border-gray-300 mb-3"
                    onChange={(e) =>
                      setPatternInputs(prev => ({ ...prev, var1: e.target.value }))
                    }
                  />
                  <input
                    type="text"
                    placeholder="Variabila 2 (ex: Y)"
                    className="w-full p-4 rounded-xl border-2 border-gray-300 mb-3"
                    onChange={(e) =>
                      setPatternInputs(prev => ({ ...prev, var2: e.target.value }))
                    }
                  />
                  <input
                    type="text"
                    placeholder="Domenii (ex: {1,2,3})"
                    className="w-full p-4 rounded-xl border-2 border-gray-300 mb-3"
                    onChange={(e) =>
                      setPatternInputs(prev => ({ ...prev, domains: e.target.value }))
                    }
                  />
                  <input
                    type="text"
                    placeholder="Valoare asignată (ex: 1)"
                    className="w-full p-4 rounded-xl border-2 border-gray-300 mb-6"
                    onChange={(e) =>
                      setPatternInputs(prev => ({ ...prev, assigned_value: e.target.value }))
                    }
                  />
                </>
              )}

              {patternType === 'MINIMAX' && (
                <p className="text-gray-600 mb-6">
                  Pattern Minimax – nu necesită date de intrare.
                </p>
              )}

              <select
                value={answerType}
                onChange={(e) => setAnswerType(e.target.value)}
                className="p-4 rounded-xl border-2 border-gray-300 mb-6 w-full"
              >
                <option value="multiple">Alegere multiplă</option>
                <option value="text">Răspuns text</option>
              </select>

              <button
                onClick={submitCustomQuestion}
                disabled={
                  Object.keys(patternInputs).length === 0 &&
                  patternType !== 'MINIMAX'
                }
                className={`w-full py-4 px-8 rounded-xl font-bold text-lg transition-all transform ${
                  Object.keys(patternInputs).length > 0 || patternType === 'MINIMAX'
                    ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white hover:scale-105'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                }`}
              >
                Generează întrebarea
              </button>
            </>
          ) : (
            <>
              <h2 className="text-3xl font-bold text-gray-800 mb-4">
                Alege tipul de întrebare
              </h2>
              <p className="text-gray-600 mb-8">
                Ce fel de provocare dorești să primești?
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <button
                  onClick={() => setAnswerType('multiple')}
                  className="p-6 border-4 rounded-2xl hover:border-purple-400 hover:bg-purple-50 transition-all"
                >
                  <ListChecks className="w-12 h-12 mx-auto text-purple-600 mb-3" />
                  <p className="font-bold text-gray-800">Răspuns Multiplu</p>
                  <p className="text-sm text-gray-600 mt-2">Alege din variante</p>
                </button>

                <button
                  onClick={() => setAnswerType('text')}
                  className="p-6 border-4 rounded-2xl hover:border-blue-400 hover:bg-blue-50 transition-all"
                >
                  <Type className="w-12 h-12 mx-auto text-blue-600 mb-3" />
                  <p className="font-bold text-gray-800">Răspuns Text</p>
                  <p className="text-sm text-gray-600 mt-2">Scrie răspunsul</p>
                </button>

                <button
                  onClick={() => setShowTestMode(true)}
                  className="p-6 border-4 rounded-2xl border-green-400 hover:bg-green-50 transition-all"
                >
                  <BookOpen className="w-12 h-12 mx-auto text-green-600 mb-3" />
                  <p className="font-bold text-gray-800">Crează Test</p>
                  <p className="text-sm text-gray-600 mt-2">Multiple întrebări</p>
                </button>
              </div>

              <button
                onClick={() => fetchQuestion(answerType)}
                className="mt-10 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 px-12 rounded-xl font-semibold hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-xl"
              >
                Generează întrebarea
              </button>
            </>
          )}
        </div>
      </div>
    );
  }

  const isMultipleChoice = question.answer_type === 'multiple';
  const showCorrectAnswer = !question.protected;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 py-8 px-4">
      {renderHeader()}

      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-3xl shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-8 text-white">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles className="w-6 h-6" />
                  <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">
                    Nivel {question.difficulty}
                  </span>
                  <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1">
                    {isMultipleChoice ? <ListChecks className="w-4 h-4" /> : <Type className="w-4 h-4" />}
                    {isMultipleChoice ? 'Alegere multiplă' : 'Răspuns text'}
                  </span>
                </div>
                <h2 className="text-3xl font-bold mb-2">{question.title}</h2>
                <p className="text-purple-100 text-sm">#{question.question_type}</p>
              </div>
            </div>
          </div>

          <div className="p-8">
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl p-6 mb-8 border-l-4 border-purple-600">
              <p className="text-gray-800 text-lg leading-relaxed">{question.prompt}</p>
            </div>

            {question.question_type === "MINIMAX_TREE" && (
              <div className="mb-8">
                <TreeVisualizer tree={question.problem_instance.tree} />
              </div>
            )}

            {isMultipleChoice && question.options && (
              <div className="space-y-4 mb-8">
                {question.options.map((option, index) => {
                  const isSelected = selectedAnswer === option;
                  const showResult = submitted && evaluationResult;
                  let isThisCorrect = false;
                  if (showResult && evaluationResult.correct_answer === option) {
                    isThisCorrect = true;
                  }

                  let buttonStyle = 'bg-white border-2 border-gray-200 hover:border-purple-400 hover:shadow-lg';

                  if (isSelected && !submitted) {
                    buttonStyle = 'bg-gradient-to-r from-purple-100 to-blue-100 border-2 border-purple-500 shadow-lg scale-105';
                  }
                  if (showResult && isThisCorrect) {
                    buttonStyle = 'bg-gradient-to-r from-green-100 to-emerald-100 border-2 border-green-500 shadow-lg';
                  }
                  if (showResult && isSelected && !isThisCorrect) {
                    buttonStyle = 'bg-gradient-to-r from-red-100 to-pink-100 border-2 border-red-500 shadow-lg';
                  }

                  return (
                    <button
                      key={index}
                      onClick={() => !submitted && setSelectedAnswer(option)}
                      disabled={submitted}
                      className={`w-full text-left p-5 rounded-2xl transition-all duration-300 transform ${buttonStyle} ${
                        submitted ? 'cursor-default' : 'cursor-pointer hover:scale-102'
                      } flex items-center justify-between`}
                    >
                      <div className="flex items-center gap-4">
                        <div
                          className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg ${
                            (isSelected && !submitted) ? 'bg-purple-600 text-white' :
                              (showResult && isThisCorrect) ? 'bg-green-600 text-white' :
                                (showResult && isSelected && !isThisCorrect) ? 'bg-red-600 text-white' :
                                  'bg-gray-100 text-gray-600'
                          }`}>
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
            )}

            {!isMultipleChoice && (
              <div className="mb-8">
                <textarea
                  value={textAnswer}
                  onChange={(e) => setTextAnswer(e.target.value)}
                  disabled={submitted}
                  placeholder="Scrie răspunsul tău aici..."
                  className="w-full p-6 rounded-2xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none text-gray-800 text-lg resize-none disabled:bg-gray-100 disabled:cursor-not-allowed"
                  rows={6}
                />
              </div>
            )}

            {!submitted ? (
              <button
                onClick={handleSubmit}
                disabled={submitting || (isMultipleChoice ? !selectedAnswer : !textAnswer.trim())}
                className={`w-full py-4 px-6 rounded-2xl font-bold text-lg transition-all transform ${
                  (isMultipleChoice ? selectedAnswer : textAnswer.trim()) && !submitting
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:from-purple-700 hover:to-blue-700 shadow-xl hover:shadow-2xl hover:scale-105'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                }`}
              >
                {submitting ? 'Se verifică...' : (isMultipleChoice ? (selectedAnswer ? 'Verifică răspunsul' : 'Selectează un răspuns') : (textAnswer.trim() ? 'Verifică răspunsul 🎯' : 'Scrie un răspuns'))}
              </button>
            ) : (
              <div className="space-y-4">
                {evaluationResult && (
                  <div
                    className={`p-6 rounded-2xl border-2 ${
                      evaluationResult.is_correct
                        ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-400'
                        : evaluationResult.score >= 50
                          ? 'bg-gradient-to-r from-yellow-50 to-orange-50 border-yellow-400'
                          : 'bg-gradient-to-r from-red-50 to-pink-50 border-red-400'
                    }`}
                  >
                    <div className="flex items-center mb-3">
                      {evaluationResult.is_correct ? (
                        <>
                          <CheckCircle className="w-8 h-8 text-green-600 mr-3" />
                          <span className="font-bold text-2xl text-gray-800">Excelent!</span>
                        </>
                      ) : evaluationResult.score >= 50 ? (
                        <>
                          <AlertCircle className="w-8 h-8 text-yellow-600 mr-3" />
                          <span className="font-bold text-2xl text-gray-800">Bine!</span>
                        </>
                      ) : (
                        <>
                          <XCircle className="w-8 h-8 text-red-600 mr-3" />
                          <span className="font-bold text-2xl text-gray-800">Încearcă din nou!</span>
                        </>
                      )}
                      <span className="ml-auto text-3xl font-bold text-gray-800">
                        {Math.round(evaluationResult.score)}%
                      </span>
                    </div>

                    {!isMultipleChoice && evaluationResult.details && (
                      <div className="bg-white/60 rounded-xl p-4 mb-3">
                        {evaluationResult.details.keywords_found && evaluationResult.details.keywords_found.length > 0 && (
                          <div className="mb-2">
                            <p className="font-semibold text-green-700 mb-1">✓ Cuvinte cheie găsite:</p>
                            <p className="text-gray-700">{evaluationResult.details.keywords_found.join(', ')}</p>
                          </div>
                        )}
                        {evaluationResult.details.keywords_missed && evaluationResult.details.keywords_missed.length > 0 && (
                          <div>
                            <p className="font-semibold text-red-700 mb-1">✗ Cuvinte cheie lipsă:</p>
                            <p className="text-gray-700">{evaluationResult.details.keywords_missed.join(', ')}</p>
                          </div>
                        )}
                      </div>
                    )}

                    <div className="bg-white/60 rounded-xl p-4">
                      <p className="font-semibold text-gray-800 mb-2">Soluție de referință:</p>
                      <p className="text-gray-700 leading-relaxed">{evaluationResult.reference_solution}</p>
                    </div>
                  </div>
                )}

                <div className="flex gap-4">
                  <button
                    onClick={() => handleNewQuestion('multiple')}
                    className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 px-6 rounded-2xl font-bold text-lg hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-xl flex items-center justify-center gap-2"
                  >
                    <ListChecks className="w-6 h-6" />
                    Alegere multiplă
                  </button>
                  <button
                    onClick={() => handleNewQuestion('text')}
                    className="flex-1 bg-gradient-to-r from-cyan-600 to-teal-600 text-white py-4 px-6 rounded-2xl font-bold text-lg hover:from-cyan-700 hover:to-teal-700 transition-all transform hover:scale-105 shadow-xl flex items-center justify-center gap-2"
                  >
                    <Type className="w-6 h-6" />
                    Răspuns text
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}