import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Timer, CheckCircle, RotateCcw, AlertCircle, Award, 
  Code2, Layout, Palette, ChevronRight, Play, ArrowLeft, 
  Check, X, HelpCircle, BookOpen, Coffee, Terminal, Sparkles,
  Trophy, Star, Cpu, Globe, Rocket
} from 'lucide-react';
import './index.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000');

const App = () => {
  const [view, setView] = useState('welcome'); // welcome, selection, quiz, result
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [timer, setTimer] = useState(15);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const timerRef = useRef(null);

  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/subjects`);
        setSubjects(response.data);
      } catch (error) {
        console.error('Error fetching subjects:', error);
      }
    };
    fetchSubjects();
  }, []);

  useEffect(() => {
    if (view !== 'quiz' || loading || isTransitioning) return;
    if (timer === 0) {
      handleOptionSelect('skip');
      return;
    }
    timerRef.current = setInterval(() => {
      setTimer((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(timerRef.current);
  }, [view, currentIndex, timer, loading, isTransitioning]);

  const startQuiz = async (subject) => {
    try {
      setLoading(true);
      setSelectedSubject(subject);
      const response = await axios.get(`${API_BASE_URL}/questions/${subject.name}`);
      setQuestions(response.data);
      setCurrentIndex(0);
      setSelectedAnswers({});
      setTimer(15);
      setView('quiz');
      setLoading(false);
    } catch (error) {
      console.error('Error starting quiz:', error);
      setLoading(false);
    }
  };

  const handleOptionSelect = async (optionKey) => {
    if (isTransitioning) return;
    clearInterval(timerRef.current);
    const questionId = questions[currentIndex].id;
    setSelectedAnswers(prev => ({ ...prev, [questionId]: optionKey }));
    setIsTransitioning(true);

    setTimeout(() => {
      if (currentIndex < questions.length - 1) {
        setCurrentIndex(prev => prev + 1);
        setTimer(15);
        setIsTransitioning(false);
      } else {
        submitQuiz({ ...selectedAnswers, [questionId]: optionKey });
      }
    }, 800);
  };

  const submitQuiz = async (answers) => {
    try {
      setLoading(true);
      const formattedAnswers = questions.map(q => ({
        question_id: q.id,
        selected_option: answers[q.id] || ''
      }));

      const response = await axios.post(`${API_BASE_URL}/submit`, {
        answers: formattedAnswers
      });
      setResult(response.data);
      setView('result');
      setLoading(false);
    } catch (error) {
      console.error('Error submitting quiz:', error);
      setLoading(false);
    }
  };

  const restartQuiz = () => startQuiz(selectedSubject);
  const goHome = () => { setView('welcome'); setSelectedSubject(null); setResult(null); };

  const getFeedback = (score, total) => {
    const percentage = (score / total) * 100;
    if (percentage >= 80) return { 
        message: "Excellent! You're a pro!", 
        color: "#04AA6D", 
        bg: '#e6f7ef',
        emoji: "🏆",
        subMessage: "Incredible feat! You have mastered this tech subject. 🎉"
    };
    if (percentage >= 50) return { 
        message: "Good Job! Keep it up.", 
        color: "#f39c12", 
        bg: '#fef5e7',
        emoji: "🌟",
        subMessage: "Great effort! A bit more practice and you'll reach the top. 👨‍💻"
    };
    return { 
        message: "Don't give up! Try again.", 
        color: "#e74c3c", 
        bg: '#fdecea',
        emoji: "📚",
        subMessage: "Focus on the review notes below and give it another shot. 💡"
    };
  };

  const getSubjectIcon = (iconName) => {
    switch(iconName) {
      case 'Layout': return <Layout size={32} />;
      case 'Palette': return <Palette size={32} />;
      case 'Code2': return <Code2 size={32} />;
      case 'Py': return <Terminal size={32} />;
      case 'Coffee': return <Coffee size={32} />;
      default: return <BookOpen size={32} />;
    }
  };

  const pageVariants = {
    initial: { opacity: 0, x: 20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -20 }
  };

  const WelcomeHeroSVG = () => (
    <div className="hero-svg-container">
        <svg viewBox="0 0 400 300" className="hero-svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style={{stopColor: '#04AA6D', stopOpacity: 1}} />
                    <stop offset="100%" style={{stopColor: '#27ae60', stopOpacity: 1}} />
                </linearGradient>
            </defs>
            <rect x="50" y="50" width="300" height="200" rx="30" fill="url(#grad1)" opacity="0.25" />
            <circle cx="200" cy="150" r="60" fill="url(#grad1)" opacity="0.2" />
            <motion.path 
                d="M160 150 L190 180 L240 130" 
                fill="none" 
                stroke="#04AA6D" 
                strokeWidth="15" 
                strokeLinecap="round" 
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1, repeat: Infinity, repeatType: 'reverse' }}
            />
            <motion.circle 
                cx="100" cy="80" r="10" fill="#04AA6D" 
                animate={{ y: [0, 20, 0], opacity: [0.3, 0.8, 0.3] }} 
                transition={{ duration: 3, repeat: Infinity }}
            />
            <motion.circle 
                cx="300" cy="220" r="15" fill="#f39c12" 
                animate={{ y: [0, -30, 0], opacity: [0.2, 0.6, 0.2] }} 
                transition={{ duration: 4, repeat: Infinity, delay: 1 }}
            />
        </svg>
    </div>
  );

  if (loading) {
    return (
      <div className="main-app-container">
        <div className="bg-mask"></div>
        <div className="loader-container">
          <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }} className="loader"></motion.div>
          <p>Analyzing tech stack...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="main-app-container">
      <div className="bg-mask"></div>
      
      <AnimatePresence mode="wait">
        {view === 'welcome' && (
          <motion.div key="welcome" variants={pageVariants} initial="initial" animate="animate" exit="exit" className="welcome-view">
            <div className="welcome-card hero-animation">
              <WelcomeHeroSVG />
              <div className="icon-badge">
                <Rocket size={48} color="white" />
              </div>
              <motion.h1 initial={{ scale: 0.8 }} animate={{ scale: 1 }} transition={{ delay: 0.2 }}>Modern Tech Quiz</motion.h1>
              <p className="subtitle">Select your tech stack and validate your knowledge levels.</p>
              <button className="primary-btn" onClick={() => setView('selection')}>
                Start Quiz <ChevronRight size={18} />
              </button>
            </div>
            <div className="tech-bar">
                <Cpu size={24} color="#666" />
                <Globe size={24} color="#666" />
                <Code2 size={24} color="#666" />
                <Terminal size={24} color="#666" />
            </div>
          </motion.div>
        )}

        {view === 'selection' && (
          <motion.div key="selection" variants={pageVariants} initial="initial" animate="animate" exit="exit" className="selection-view">
            <div className="selection-header">
                <button className="back-btn" onClick={() => setView('welcome')}><ArrowLeft size={20} /> Back</button>
                <h1>Select Technology</h1>
                <p>Choose the tech domain for your adaptive challenge.</p>
            </div>
            <div className="subject-grid">
              {subjects.map((subject, idx) => (
                <motion.div 
                  key={subject.name} 
                  initial={{ opacity: 0, scale: 0.9, y: 20 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className="subject-card" 
                  onClick={() => startQuiz(subject)}
                >
                  <div className="subject-icon-box">{getSubjectIcon(subject.icon)}</div>
                  <h3>{subject.name}</h3>
                  <p>20 Adaptive MCQs</p>
                  <div className="start-hint">Select Domain <ChevronRight size={16} /></div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {view === 'quiz' && (
          <motion.div key="quiz" variants={pageVariants} initial="initial" animate="animate" exit="exit" className="quiz-view">
            <div className="quiz-header">
                <div className="quiz-info">
                    <h2>{selectedSubject?.name} Assessment</h2>
                    <span className="q-counter">Question {currentIndex + 1} of {questions.length}</span>
                </div>
                <div className={`timer-badge ${timer <= 5 ? 'timer-warning' : ''}`}>
                    <Timer size={20} />
                    <span>{timer}s</span>
                </div>
            </div>

            <div className="progress-bar-wrapper">
              <motion.div className="progress-fill" animate={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}></motion.div>
            </div>

            <AnimatePresence mode="wait">
              <motion.div 
                key={currentIndex} 
                initial={{ opacity: 0, x: 50 }} 
                animate={{ opacity: 1, x: 0 }} 
                exit={{ opacity: 0, x: -50 }} 
                className="question-content"
              >
                <h2 className="question-title">{questions[currentIndex]?.question}</h2>
                <div className="options-list">
                  {['option1', 'option2', 'option3', 'option4'].map((opt, i) => (
                    <motion.button
                      key={opt}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className={`modern-option-btn ${selectedAnswers[questions[currentIndex]?.id] === opt ? 'selected' : ''}`}
                      onClick={() => handleOptionSelect(opt)}
                      disabled={isTransitioning}
                    >
                      <span className="opt-label">{opt.replace('option', '')}</span>
                      <span className="opt-text">{questions[currentIndex]?.[opt]}</span>
                      {selectedAnswers[questions[currentIndex]?.id] === opt && <Check size={20} className="check-icon" />}
                    </motion.button>
                  ))}
                </div>
              </motion.div>
            </AnimatePresence>
          </motion.div>
        )}

        {view === 'result' && result && (
          <motion.div key="result" variants={pageVariants} initial="initial" animate="animate" exit="exit" className="result-view">
            <div className="result-hero">
                <div className="celebrate-bg"></div>
                {/* Score-based mixed color particle effect */}
                <div className="mixed-color-pulse" style={{ backgroundColor: getFeedback(result.score, result.total).bg }}></div>
                
                <motion.div 
                    className="report-status"
                    initial={{ scale: 0, rotate: -180 }} 
                    animate={{ scale: 1, rotate: 0 }} 
                    transition={{ type: "spring", stiffness: 260, damping: 20 }}
                >
                    <div style={{ fontSize: '80px', marginBottom: '10px' }}>{getFeedback(result.score, result.total).emoji}</div>
                    <Trophy size={48} color={getFeedback(result.score, result.total).color} strokeWidth={2.5} />
                </motion.div>
                
                <h1 style={{ color: getFeedback(result.score, result.total).color, marginTop: '1rem' }}>
                    {getFeedback(result.score, result.total).message}
                </h1>
                <p className="result-submessage">{getFeedback(result.score, result.total).subMessage}</p>
                
                <div className="final-score-box">
                    <span className="big-score">{result.score}</span>
                    <span className="total-score">/ {result.total}</span>
                    <p className="perc-label">{Math.round((result.score / result.total) * 100)}% Proficiency Rank</p>
                </div>

                <div className="action-row">
                    <button className="primary-btn" onClick={restartQuiz}><RotateCcw size={18} /> New Round</button>
                    <button className="outline-btn" onClick={goHome}><Globe size={18} /> All Domains</button>
                </div>
            </div>

            <div className="review-container">
                <h2 className="section-title"><Sparkles size={22} color="var(--primary-color)" /> Knowledge Graph Review</h2>
                {result.details.map((detail, index) => {
                    const question = questions.find(q => q.id === detail.question_id);
                    return (
                        <motion.div 
                          key={index} 
                          initial={{ opacity: 0, y: 30 }}
                          whileInView={{ opacity: 1, y: 0 }}
                          viewport={{ once: true }}
                          className="review-card"
                          style={{ borderLeftColor: detail.is_correct ? 'var(--success)' : 'var(--error)' }}
                        >
                            <div className="review-q-header"><span className="q-num">#{index + 1}</span><p>{question?.question}</p></div>
                            <div className="review-ans-grid">
                                <div className={`ans-pill ${detail.is_correct ? 'correct' : 'wrong'}`}>
                                    <span className="pill-title">Your Submit</span>
                                    <div className="pill-content">
                                        {detail.is_correct ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
                                        {question?.[detail.selected_option] || 'Unselected'}
                                    </div>
                                </div>
                                {!detail.is_correct && (
                                    <div className="ans-pill correct">
                                        <span className="pill-title">Master Correct</span>
                                        <div className="pill-content">
                                            <CheckCircle size={16} />
                                            {question?.[detail.correct_answer]}
                                        </div>
                                    </div>
                                )}
                            </div>
                            <div className="explanation-box">
                                <div className="exp-label"><HelpCircle size={14} /> Master Key:</div>
                                <p>{detail.explanation}</p>
                            </div>
                        </motion.div>
                    );
                })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default App;
