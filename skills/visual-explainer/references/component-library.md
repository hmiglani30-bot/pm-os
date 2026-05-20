# Visual Explainer Component Library

CSS patterns extracted from the towards-jarvis visual explainer + cognitive science components. Copy these directly — they're proven to work.

## 0. Cognitive Science Components (NEW in v0.2.0)

### Concept Adjacency Map
Interactive node graph placed after hero. Center node = main concept, surrounding nodes = related concepts.
Color-code by domain: technical (blue), business (accent/copper), governance (accent2/purple), user (cyan).

```css
.concept-map { position: relative; min-height: 520px; padding: 40px 20px; }
.cm-node {
  position: absolute; padding: 16px 20px; border-radius: 12px; border: 2px solid;
  text-align: center; z-index: 2; min-width: 130px; cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.cm-node:hover { transform: scale(1.08); box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
.cm-node h5 { font-size: 13px; margin-bottom: 3px; }
.cm-node p { font-size: 10px; color: var(--text-muted); line-height: 1.3; }
.cm-center { background: rgba(204,120,92,0.12); border-color: var(--accent); }
.cm-center h5 { color: var(--accent); font-size: 15px; }
.cm-tech { background: rgba(41,128,185,0.08); border-color: rgba(41,128,185,0.4); }
.cm-tech h5 { color: var(--blue); }
.cm-biz { background: rgba(204,120,92,0.08); border-color: rgba(204,120,92,0.35); }
.cm-biz h5 { color: var(--accent); }
.cm-gov { background: rgba(124,111,205,0.08); border-color: rgba(124,111,205,0.4); }
.cm-gov h5 { color: var(--accent2); }
.cm-user { background: rgba(23,162,184,0.08); border-color: rgba(23,162,184,0.35); }
.cm-user h5 { color: var(--cyan); }
/* Edge labels */
.cm-edge-label {
  position: absolute; font-size: 9px; color: var(--text-dim);
  background: var(--bg); padding: 2px 6px; border-radius: 4px; z-index: 3;
  letter-spacing: 0.04em; text-transform: uppercase; font-weight: 600;
}
/* SVG connector lines */
.cm-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; }
.cm-svg line { stroke: var(--border); stroke-width: 1.5; stroke-dasharray: 6 4; }
```

JS for click-to-scroll:
```javascript
document.querySelectorAll('.cm-node[data-section]').forEach(node => {
  node.addEventListener('click', () => {
    const target = document.getElementById(node.dataset.section);
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
```

### Analogy Bridge
Visual side-by-side mapping familiar concept → new concept. 3 structural mappings per bridge.

```css
.analogy-bridge {
  display: grid; grid-template-columns: 1fr 60px 1fr; gap: 0; align-items: stretch;
  background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
  padding: 28px; margin: 24px 0; overflow: hidden;
}
@media (max-width: 700px) { .analogy-bridge { grid-template-columns: 1fr; } }
.analogy-source, .analogy-target {
  padding: 20px; border-radius: 10px; border: 1px solid;
}
.analogy-source { background: rgba(41,128,185,0.05); border-color: rgba(41,128,185,0.2); }
.analogy-source h4 { color: var(--blue); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; }
.analogy-target { background: rgba(204,120,92,0.05); border-color: rgba(204,120,92,0.2); }
.analogy-target h4 { color: var(--accent); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; }
.analogy-arrows { display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 16px; }
.analogy-arrows span { color: var(--text-dim); font-size: 18px; }
.analogy-mapping {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 12px; font-size: 13px; color: var(--text-muted);
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.analogy-mapping:last-child { border-bottom: none; }
.analogy-mapping .map-icon { font-size: 10px; color: var(--text-dim); }
.analogy-label {
  text-align: center; font-size: 13px; font-style: italic; color: var(--text-muted);
  margin-top: 12px; padding: 0 20px;
}
```

### "Why This Matters" Callout
Placed before each section's visual.

```css
.why-callout {
  background: rgba(204,120,92,0.06); border-left: 3px solid var(--accent);
  padding: 14px 20px; border-radius: 0 10px 10px 0; margin-bottom: 20px;
}
.why-callout .why-label {
  font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--accent); display: block; margin-bottom: 4px;
}
.why-callout p { font-size: 14px; color: var(--text-muted); line-height: 1.6; margin: 0; }
```

### Enhanced Quiz Block (with score tracking)

```css
.quiz-block {
  background: var(--surface); border: 2px solid var(--accent2); border-radius: 14px;
  padding: 32px; margin: 48px 0;
}
.quiz-block h4 { color: var(--accent2); font-size: 16px; margin-bottom: 8px; }
.quiz-tier-label { font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 20px; }
.quiz-q { margin-bottom: 28px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }
.quiz-q:last-of-type { border-bottom: none; }
.quiz-q p { font-size: 14px; margin-bottom: 12px; line-height: 1.6; }
.quiz-options { display: flex; flex-direction: column; gap: 8px; }
.quiz-options button {
  text-align: left; padding: 12px 16px; border: 1px solid var(--border);
  background: var(--surface2); color: var(--text-muted); border-radius: 8px;
  font-size: 13px; cursor: pointer; transition: all 0.2s; line-height: 1.5;
}
.quiz-options button:hover { border-color: var(--accent); color: var(--text); }
.quiz-options button.correct { background: var(--green-bg); border-color: var(--green); color: var(--green); }
.quiz-options button.wrong { background: var(--red-bg); border-color: var(--red); color: var(--red); }
.quiz-options button.disabled { pointer-events: none; opacity: 0.6; }
.quiz-feedback { font-size: 13px; margin-top: 10px; padding: 12px 16px; border-radius: 8px; display: none; line-height: 1.5; }
.quiz-feedback.show { display: block; }
.quiz-feedback.correct-fb { background: var(--green-bg); color: var(--green); }
.quiz-feedback.wrong-fb { background: var(--red-bg); color: var(--red); }

/* Score tracker */
.score-tracker {
  display: flex; align-items: center; gap: 16px; margin-top: 20px;
  padding: 14px 20px; background: var(--surface2); border-radius: 10px;
}
.score-tracker .score-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; }
.score-tracker .score-value { font-size: 20px; font-weight: 700; color: var(--accent); }
.score-bar { flex: 1; height: 6px; background: var(--surface3); border-radius: 3px; overflow: hidden; }
.score-bar-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent2)); border-radius: 3px; transition: width 0.5s ease; }

/* Final score summary */
.score-summary {
  background: var(--surface); border: 2px solid var(--accent); border-radius: 14px;
  padding: 40px; margin: 48px 0; text-align: center;
}
.score-summary .final-score { font-size: 48px; font-weight: 700; color: var(--accent); }
.score-summary .final-label { font-size: 14px; color: var(--text-muted); margin: 8px 0 20px; }
.score-summary .final-feedback { font-size: 15px; color: var(--text); line-height: 1.7; max-width: 500px; margin: 0 auto; }
```

JS for quiz with scoring:
```javascript
let totalCorrect = 0;
let totalAnswered = 0;
const totalQuestions = 15;

function checkAnswer(btn, selected) {
  const q = btn.closest('.quiz-q');
  if (q.dataset.answered) return;
  q.dataset.answered = 'true';
  const correct = q.dataset.answer;
  const feedback = q.querySelector('.quiz-feedback');
  totalAnswered++;

  q.querySelectorAll('button').forEach(b => {
    b.classList.add('disabled');
    if (b.dataset.choice === correct) b.classList.add('correct');
  });

  if (selected === correct) {
    btn.classList.add('correct');
    totalCorrect++;
    feedback.textContent = '✓ Correct!';
    feedback.className = 'quiz-feedback show correct-fb';
  } else {
    btn.classList.add('wrong');
    feedback.textContent = '✗ ' + (q.dataset.explanation || 'Incorrect.');
    feedback.className = 'quiz-feedback show wrong-fb';
  }
  updateScoreTracker();
}

function updateScoreTracker() {
  document.querySelectorAll('.score-value').forEach(el => {
    el.textContent = totalCorrect + '/' + totalAnswered;
  });
  document.querySelectorAll('.score-bar-fill').forEach(el => {
    el.style.width = (totalAnswered > 0 ? (totalCorrect / totalAnswered) * 100 : 0) + '%';
  });
}

function showFinalScore() {
  const pct = Math.round((totalCorrect / totalQuestions) * 100);
  document.getElementById('finalScore').textContent = totalCorrect + '/' + totalQuestions;
  const fb = document.getElementById('finalFeedback');
  if (totalCorrect >= 12) fb.textContent = 'Expert level — you could present this to stakeholders with confidence.';
  else if (totalCorrect >= 8) fb.textContent = 'Solid grasp — review the sections you got wrong for a deeper understanding.';
  else fb.textContent = 'Review recommended — re-read the Overview tab in each section, then retake the quizzes.';
}
```

## 1. Funnel Diagram
Shows sequential narrowing (pipeline stages, conversion funnels).

```css
.funnel { display: flex; flex-direction: column; align-items: center; gap: 0; }
.funnel-step {
  display: flex; align-items: center; justify-content: center;
  padding: 16px 24px; text-align: center;
  border: 1px solid; border-radius: 10px;
  font-weight: 600; font-size: 14px;
  transition: transform 0.2s; position: relative;
}
.funnel-step:hover { transform: scale(1.03); }
.funnel-arrow { color: var(--text-dim); font-size: 20px; margin: 4px 0; }
/* Width decreases per step: 90% → 75% → 60% → 45% */
.funnel-s1 { width: 90%; max-width: 600px; background: rgba(124,111,205,0.08); border-color: rgba(124,111,205,0.3); color: var(--accent2); }
.funnel-s2 { width: 75%; max-width: 500px; background: rgba(204,120,92,0.08); border-color: rgba(204,120,92,0.3); color: var(--accent); }
.funnel-s3 { width: 60%; max-width: 400px; background: rgba(212,160,23,0.08); border-color: rgba(212,160,23,0.3); color: var(--yellow); }
.funnel-s4 { width: 45%; max-width: 300px; background: rgba(192,57,43,0.1); border-color: rgba(192,57,43,0.3); color: var(--red); font-size: 16px; font-weight: 700; }
```

## 2. Architecture Layer Stack
Shows hierarchical system layers (tech stack, platform layers).

```css
.arch-stack { display: flex; flex-direction: column; gap: 6px; max-width: 800px; margin: 0 auto; }
.arch-layer {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 20px; border-radius: 10px; border: 1px solid;
  font-size: 14px; font-weight: 600; transition: transform 0.15s;
}
.arch-layer:hover { transform: translateX(4px); }
.arch-layer .arch-num {
  width: 32px; height: 32px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; flex-shrink: 0;
}
.arch-layer .arch-desc { font-weight: 400; font-size: 13px; color: var(--text-muted); margin-left: auto; }
```

Color each layer with its own rgba background + border:
```css
.al-layer1 { background: rgba(124,111,205,0.06); border-color: rgba(124,111,205,0.25); }
.al-layer1 .arch-num { background: rgba(124,111,205,0.2); color: var(--accent2); }
```

## 3. Split Comparison Diagram
Shows side-by-side comparison (before/after, us vs. them).

```css
.split-diagram { display: grid; grid-template-columns: 1fr 60px 1fr; gap: 0; align-items: stretch; }
@media (max-width: 700px) { .split-diagram { grid-template-columns: 1fr; } }
.split-side { padding: 28px 24px; border-radius: 12px; border: 1px solid; }
.split-side h4 { font-size: 15px; margin-bottom: 12px; }
.split-side ul { list-style: none; padding: 0; }
.split-side li { font-size: 13px; color: var(--text-muted); padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.split-side li::before { content: ''; display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 10px; vertical-align: middle; }
.split-left { background: rgba(41,128,185,0.05); border-color: rgba(41,128,185,0.2); }
.split-left h4 { color: var(--blue); }
.split-left li::before { background: var(--blue); }
.split-right { background: rgba(204,120,92,0.05); border-color: rgba(204,120,92,0.2); }
.split-right h4 { color: var(--accent); }
.split-right li::before { background: var(--accent); }
.split-center { display: flex; align-items: center; justify-content: center; font-size: 24px; color: var(--text-dim); font-weight: 700; }
```

## 4. Mental Map (Node Graph)
Shows relationships between concepts (system components, stakeholder map).

```css
.mental-map { position: relative; min-height: 520px; padding: 40px 20px; }
.mm-node {
  position: absolute; padding: 16px 20px; border-radius: 12px; border: 2px solid;
  text-align: center; z-index: 2; min-width: 140px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.mm-node:hover { transform: scale(1.06); box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
.mm-node h5 { font-size: 13px; margin-bottom: 3px; }
.mm-node p { font-size: 11px; color: var(--text-muted); line-height: 1.4; }
```

Position nodes with absolute positioning. Use SVG overlay for connecting lines:
```css
.mm-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; }
.mm-svg line { stroke: var(--border); stroke-width: 1.5; stroke-dasharray: 6 4; }
```

## 5. Maturity Ladder
Shows progression levels (adoption stages, capability maturity).

```css
.maturity-track { display: flex; flex-direction: column; gap: 4px; max-width: 750px; margin: 0 auto; }
.maturity-step {
  display: flex; align-items: center; gap: 14px;
  padding: 10px 16px; border-radius: 8px; border: 1px solid var(--border);
  background: var(--surface); font-size: 13px; transition: transform 0.15s, background 0.15s;
}
.maturity-step:hover { transform: translateX(6px); background: var(--surface2); }
.maturity-step .phase-num {
  width: 28px; height: 28px; border-radius: 7px;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 800; flex-shrink: 0;
}
.maturity-step .phase-name { font-weight: 600; color: var(--text); flex: 1; }
.maturity-step .phase-status { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 6px; }
.phase-done { background: var(--green-bg); color: var(--green); }
.phase-wip { background: var(--yellow-bg); color: var(--yellow); }
.phase-future { background: rgba(136,136,160,0.1); color: var(--text-dim); }
```

## 6. Decision Flowchart
Shows branching decisions (build vs. buy, go/no-go).

```css
.flow-chart { display: flex; flex-direction: column; align-items: center; gap: 0; }
.flow-node {
  padding: 14px 24px; border-radius: 10px; border: 2px solid;
  text-align: center; font-size: 14px; font-weight: 600; min-width: 200px;
  transition: transform 0.2s;
}
.flow-node:hover { transform: scale(1.03); }
.flow-diamond {
  padding: 16px 24px; border-radius: 4px; border: 2px solid var(--accent2);
  background: rgba(124,111,205,0.08); color: var(--accent2);
  text-align: center; font-size: 13px; font-weight: 600;
}
.flow-branches { display: flex; gap: 24px; justify-content: center; flex-wrap: wrap; }
.flow-branch { display: flex; flex-direction: column; align-items: center; gap: 8px; max-width: 200px; }
.flow-branch-label { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; }
.flow-arrow { color: var(--text-dim); font-size: 18px; }
```

## 7. Comparison Table
Shows feature-by-feature comparison.

```css
.cmp-table-wrap { overflow-x: auto; }
.cmp-table { border-collapse: collapse; width: 100%; min-width: 700px; }
.cmp-table th {
  background: var(--surface2); color: var(--text-muted); font-size: 11px;
  font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
  padding: 12px 16px; text-align: left; border: 1px solid var(--border);
}
.cmp-table td {
  padding: 14px 16px; border: 1px solid var(--border); font-size: 13px;
  background: var(--surface); color: var(--text-muted); vertical-align: top;
}
.cmp-table tr:hover td { background: var(--surface2); }
.cmp-table td:first-child { font-weight: 600; color: var(--text); white-space: nowrap; }
.cmp-table .best { color: var(--green); font-weight: 700; }
```

## 8. Tab System
For progressive disclosure within sections.

```css
.tab-bar { display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 24px; }
.tab-btn {
  padding: 10px 20px; font-size: 13px; font-weight: 600; color: var(--text-muted);
  background: none; border: none; border-bottom: 2px solid transparent;
  cursor: pointer; transition: all 0.2s;
}
.tab-btn:hover { color: var(--text); }
.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }
.tab-panel { display: none; }
.tab-panel.active { display: block; }
```

JS for tab switching:
```javascript
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const group = btn.closest('.tab-group');
    group.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    group.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    group.querySelector(`#${btn.dataset.tab}`).classList.add('active');
  });
});
```

## 9. Collapsible Sections

```css
.collapsible-header {
  display: flex; align-items: center; gap: 12px; padding: 16px 20px;
  background: var(--surface2); border: 1px solid var(--border); border-radius: 10px;
  cursor: pointer; user-select: none; transition: background 0.15s; margin-bottom: 2px;
}
.collapsible-header:hover { background: var(--surface3); }
.collapsible-header h4 { font-size: 15px; flex: 1; }
.collapsible-header .chev { color: var(--text-dim); transition: transform 0.2s; font-size: 14px; }
.collapsible-header.open .chev { transform: rotate(90deg); }
.collapsible-body { display: none; padding: 20px 24px; background: var(--surface); border: 1px solid var(--border); border-top: none; border-radius: 0 0 10px 10px; margin-bottom: 12px; }
.collapsible-body.open { display: block; }
```

## 10. Quiz Block

```css
.quiz-block {
  background: var(--surface); border: 2px solid var(--accent2); border-radius: 14px;
  padding: 32px; margin: 40px 0;
}
.quiz-block h4 { color: var(--accent2); font-size: 16px; margin-bottom: 24px; }
.quiz-q { margin-bottom: 24px; }
.quiz-q p { font-size: 14px; margin-bottom: 12px; }
.quiz-options { display: flex; flex-direction: column; gap: 8px; }
.quiz-options button {
  text-align: left; padding: 12px 16px; border: 1px solid var(--border);
  background: var(--surface2); color: var(--text-muted); border-radius: 8px;
  font-size: 13px; cursor: pointer; transition: all 0.2s;
}
.quiz-options button:hover { border-color: var(--accent); color: var(--text); }
.quiz-options button.correct { background: var(--green-bg); border-color: var(--green); color: var(--green); }
.quiz-options button.wrong { background: var(--red-bg); border-color: var(--red); color: var(--red); }
.quiz-options button.disabled { pointer-events: none; opacity: 0.6; }
.quiz-feedback { font-size: 13px; margin-top: 8px; padding: 10px 14px; border-radius: 8px; display: none; }
.quiz-feedback.show { display: block; }
.quiz-feedback.correct { background: var(--green-bg); color: var(--green); }
.quiz-feedback.wrong { background: var(--red-bg); color: var(--red); }
```

JS for quiz:
```javascript
function checkAnswer(btn, selected) {
  const q = btn.closest('.quiz-q');
  const correct = q.dataset.answer;
  const feedback = q.querySelector('.quiz-feedback');
  q.querySelectorAll('button').forEach(b => {
    b.classList.add('disabled');
    if (b.textContent.startsWith(correct.toUpperCase() + ')')) b.classList.add('correct');
  });
  if (selected === correct) {
    btn.classList.add('correct');
    feedback.textContent = '✓ Correct!';
    feedback.className = 'quiz-feedback show correct';
  } else {
    btn.classList.add('wrong');
    feedback.textContent = '✗ ' + q.dataset.explanation;
    feedback.className = 'quiz-feedback show wrong';
  }
}
```

## 11. Utility JS (always include)

```javascript
// Scroll progress bar
window.addEventListener('scroll', () => {
  const h = document.documentElement;
  const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
  document.getElementById('scrollProgress').style.width = pct + '%';
});

// Sticky nav active section highlighting
const sections = document.querySelectorAll('.section');
const navLinks = document.querySelectorAll('.sticky-nav a');
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      navLinks.forEach(l => l.classList.remove('active'));
      const target = document.querySelector(`.sticky-nav a[href="#${e.target.id}"]`);
      if (target) target.classList.add('active');
    }
  });
}, { rootMargin: '-40% 0px -60% 0px' });
sections.forEach(s => observer.observe(s));

// Collapsibles
document.querySelectorAll('.collapsible-header').forEach(h => {
  h.addEventListener('click', () => {
    h.classList.toggle('open');
    h.nextElementSibling.classList.toggle('open');
  });
});
```
