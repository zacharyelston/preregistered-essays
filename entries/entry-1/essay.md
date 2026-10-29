# Anchored Self-Report: Training History, Target Fixation, and the Evidential Value of AI Self-Reports

## 1. The problem

When a language model says "I am uncertain" or "I find this distressing", a common reply is that it says such things because humans do. The careful version of this reply is Birch's gaming problem (Birch 2024; Andrews & Birch 2023). A system optimized to produce human-like outputs will produce the behavioural markers of sentience whether or not it is sentient, so those markers lose their diagnostic value. Birch's response is to look past surface markers to deep computational ones (cf. Butlin et al. 2023).

Others have tried to rehabilitate self-report:

- Perez and Long (2023) propose training models to answer verifiable questions about themselves.
- Schneider's (2019) ACT test asks for self-reports from systems boxed off from human talk about consciousness.
- Kammerer and Frankish (2023) map the forms introspective systems could take.

See also Long (2023) and Chalmers (2023). What is still missing is an account of what makes a trained self-report *about* a particular state of the system that produces it. Every output token of a large network is counterfactually sensitive to many internal states, so causal connection between states and reports is many-many. Something must fix which of the states a report depends on it is an *outlet of*.

Wittgenstein's remark at PI §244 supplies a picture. Pain vocabulary is grafted onto the child's natural pain-behaviour. I take only the picture. I do not follow Wittgenstein in denying that avowals describe: on my account they are truth-evaluable self-ascriptions. I borrow from Bar-On (2004) only the distinction between the *act* of expressing a state and its *product*, a sentence with ordinary self-ascriptive content. I do not borrow her account of the security of avowals. What matters in the grafting picture is what the vocabulary was grafted onto. A base model has no natural expression onto which its vocabulary could have been grafted. The question is whether training can supply an analogue.

I call the needed relation an *anchor*. Part of the idea is old. Skinner (1945; 1957, ch. 5) distinguished two ways a verbal community can train reports of private events:

- via *public accompaniments* of the event, such as a visible injury;
- via the learner's *collateral responses*, such as crying.

He also concluded that such reports are inherently imprecise. Dretske (1988) supplied the idea that learning recruits internal indicators, whose content is fixed by what they were recruited for. What Skinner's behaviourism declined to supply, and Dretske did not address for self-ascription, is a condition saying *which internal state* a trained report is about. That is what I offer here. It has four parts:

- a gate condition with an explicit causal boundary between situation and channel;
- a lineage clause;
- a content rule that selects the expressed state by commonality and proportionality, evaluated with the situation held fixed;
- a screening clause that separates expression from self-interpretation.

With this condition I defend three theses.

- **(T1) Target selection.** Synchronic causal analysis relative to the report alone either leaves the report's target indeterminate along the causal chain or selects a proximal mediator. A deeper target requires a privileged set of further effects. Training history supplies one without presupposing a theory of what the target is. Structurally identical systems with different gate histories have reports with different error conditions (§4).
- **(T2) Base and post-trained models.** Base-model first-person reports have no self-ascriptive anchor. Their "I" refers to a represented speaker, and they say something about that speaker. Post-trained reports are anchored only if the regime gates on the system's own channels *and* the trained network contains an unscreened fork. Neither can be read off the nominal objective. Where reports are anchored, including to a persona representation, they express the anchoring state as the system's own condition.
- **(T3) Limits.** Anchoring settles what a report expresses. It does not settle whether the expressed state is the one the public word names (*fit*).

One concession should be made at the outset (§7). Epistemically, a verified anchored report is a constructed indicator, and anchoring adds no further kind of warrant. Its contributions are metasemantic, and they have methodological consequences:

- it fixes what a report is about;
- it separates that question from fit;
- it yields negative verdicts from design knowledge alone;
- it tells verification what it must establish.

## 2. Three ways a report can bear on a state

Let *r* be a report produced by a system *L*, and *S* a state of *L*. There are three ways *r* can bear on *S*.

- **Calibrated indicator.** The hearer has found, by checking *r* against independent measurements of *S*, that *r* covaries with *S*.
- **Constructed indicator.** The hearer knows that some process (design, selection, learning) connected *S* to the production of *r* because of *S*. We can know from its construction that a dial tracks humidity even if it is labelled in degrees Celsius.
- **Avowal.** A constructed indicator whose target is fixed by the gate structure of *L*'s own acquisition, and whose product has public self-ascriptive content.

The account has two factors.

- **Public content** fixes what a self-ascription *says*. I accept social externalism (Burge 1979) and arguments that language models' words can inherit public reference (Mandelkern & Linzen 2024; cf. Cappelen & Dever 2021). Who "I" refers to is taken up in §3.5.
- **The anchor** fixes which state of the speaker the report expresses.

A self-report is true testimony that the speaker is *F* only if it expresses some *S* and *S* is *F* (fit).

Comșa and Shanahan (2025) count a self-report as introspective when it is causally connected to the internal state it describes. The report's content identifies that state. This works when some state fits the content, but whether one does is precisely what is in question. A report can also be an outlet of a state its content does not fit: that is what a false avowal is. So we need a target-fixing relation that is independent of content.

## 3. The anchor condition

### 3.1 Situation, channels, and gate dependence

I model *L* by a causal abstraction (Geiger et al. 2021) with three kinds of variables:

- input variables *X*;
- internal variables (the *admissible* candidates);
- output variables.

*T* is a self-ascriptive term.

A **channel** *C* is any output or measurable condition, other than *T*, that is causally downstream of *L*'s internal variables. Examples are answers, actions, sampled tokens (even after they re-enter the context), probe readings, and crying.

The **situation** is the values of *X*: whatever enters *L* as input and is not downstream of *L*'s internal variables. For a model this includes:

- the prompt;
- retrieved documents and tool outputs;
- tokens someone else has placed in the model's own response (prefill).

For a child it includes the injury, the room, and the adults' words.

The boundary is drawn by causal position, not by skin or casing. The scrape is part of the child's body, but it sits on the input side, because the fall caused it and the child's states did not. The child's nociceptive registration of the scrape is an internal variable.

Interventions on internal variables are not part of the situation. This covers both the hypothetical interventions in A1 and actual activation steering. Interventions are the operations by which dependence is evaluated. An injected concept vector is therefore an intervention on an internal variable, made with the situation held fixed.

A **gate** *G* is whatever settles whether a use of *T* is reinforced or corrected.

**(A1) Gate dependence.** *G* is a function of at least one channel, such that for some internal variable *S* of *L* (or of a lineage predecessor, §3.4), intervening on *S* with *X* held fixed would have changed *G*.

A1 is a structural fact about a training regime: does the gate take one of *L*'s channels as an argument? It can be read off the design of the setup. In a deterministic forward pass, *X* fixes every internal state, so a learning algorithm never *observes* internal variation at fixed input, apart from sampling and parameter change. That is no objection to A1, which is modal. But it does mean that which relation the learning actually exploited cannot be read from training statistics. That is a fact about the trained network, and it is A2's business.

**Mixed and aggregate gates.** Real gates often depend on both situation and channels. Anchoring concerns only the channel-mediated component: the dependence of *G* on channels with *X* fixed. Its share of the variance in *G* measures the degree to which A1 holds.

Aggregate gates fix the grain of the anchor. Lin, Hilton and Evans (2022) set confidence targets by the model's empirical accuracy on a task type. Intervening on the model's state for a single question barely moves the target. Intervening on a dispositional variable shared across the type, such as a parameter-level competence feature, does move it. So A1 holds for variables at the grain of the aggregation. A term trained this way can express at most the model's standing competence on the task type, not its state on this particular question.

**Failures.** Many regimes fail A1.

- **Pretraining:** the target token is fixed text.
- **Training "I don't have feelings" against a fixed preference:** the only route from *L* to the gate is *T* itself.
- **The scrape-gated child:** the gate depends on the situation.
- **Distillation, for the student:** no intervention on the student changes the teacher's outputs.

Here is a minimal pair. In regime (a), verbal confidence is rewarded according to whether *L*'s sampled answer is correct. In regime (b), it is rewarded by a human-assigned difficulty label. In (a), with the question fixed, variation arises both from sampling (some samples are correct, some are not) and from intervention on the states that drive the answer. In (b), nothing internal to *L* changes the label.

### 3.2 The fork and the content rule

**(A2) Fork.** The trained network contains an admissible *S* that meets three conditions:

- (i) with *X* fixed, *S* is a cause of *T* and of every gated channel (commonality);
- (ii) *S* occurs before *T* and is not constituted by it;
- (iii) *T*'s dependence on *S* is not screened off by *L*'s registration of the gated channels.

**Content rule.** Among the variables satisfying (i), *T* expresses the one that is *proportional* to the channel-mediated gate dependence, with *X* held fixed (Yablo 1992; List & Menzies 2009; Woodward 2010). Interventions on it must account for the gate's variation along the gated dimensions, and it must have no interventional variation that makes no gate difference.

Holding *X* fixed does three jobs.

1. It keeps the input itself out of the candidate set.
2. It gives mixed gates' situational component no credit. A candidate gets nothing for covarying with situation features.
3. It separates role from content. A representation of the situation that actually drives *L*'s answers is admissible, because intervening on it changes the channels. If it also produces "unsure", then "unsure" expresses that representation *in its role as a driver of L's errors*.

Compare the child. On representationalist views, pain represents bodily disturbance (Tye 1995). Yet the child's "it hurts" expresses the pain state, because the gates tracked that state's role in producing crying: phantom pain gets cried over, while damage under anaesthesia does not. A *shortcut* is different. Suppose a model learns that surface obscurity predicts errors and reads that feature into "unsure" without the feature driving its answers. Then the shortcut fails commonality (Geirhos et al. 2020). What the term then expresses is world-directed: it is about obscurity.

Commonality excludes channel-specific bottlenecks. Proportionality excludes two further kinds of candidate:

- the total proximal state, most of whose variation makes no gate difference;
- over-distal causes, whose variation is screened off before it reaches the gates.

Diverse channels therefore push the expressed state upstream.

Two failure modes must be kept apart.

- **Commonality may be unsatisfiable.** Then the anchor fragments. For each maximal subset of gated channels that has a proportional common cause co-sourcing *T*, that cause is a partial anchor. *T* is ambiguous across these, and a report is determinately true only if every partial anchor fits.
- **Several variables may satisfy the rule equally.** Then *T* is indeterminate between them. This is a different matter from resolution (§3.3), which concerns which dimensions of a *determinate* expressed state the term carries.

**Screening.** The clause in (iii) follows from the principle stated in §3.5: content is fixed by the relation that learning exploited. Suppose *T* reads *L*'s own earlier outputs as they re-enter the input. Then the exploited relation runs from *L*'s representation of its input, namely its own behaviour as text, to the gate. That is the relation a hearer exploits. Such a report is self-interpretation, and it is world-directed: it is about the behaviour.

The clause has a consequence beyond classification. A screened report carries no information about *S* beyond what the channels already carry, so it cannot reach occurrences of *S* that do not show up in the channels (§7).

In a transformer the clause can be tested. The state that produced the output token at position *t* is the residual stream at positions up to *t*−1. The token's re-entry is its embedding at *t*. Activation patching can vary either while holding the other fixed:

- in a fork, *T* tracks the producer activations when the sampled token is held fixed;
- in self-interpretation, *T* tracks the sampled token when the producer activations are held fixed.

On Jamesian views (James 1884; Damasio 1994; Prinz 2004), an emotion is or involves the registration of bodily changes. That registration is then part of how *S* is realized. It is not perception of a *gated* channel, because caregivers gate on visible crying, expression and avoidance, not on viscera. An affect avowal is screened only if it depends on *S* solely through registering those gated channels, as it would if facial feedback were its only route. Constructionist views (Barrett 2017), on which emotion categorization draws heavily on situational information, predict that some emotion avowals are partly world-directed. The framework does not decide between these theories. It says what would follow from each.

### 3.3 Maintenance and resolution

**(A3) Maintenance.** Later training has not changed the read-out from *S* to *T*, nor the abstraction map under which *S* is the variable the gates depended on. Changes in *S*'s values are not lapses.

**Resolution.** *T* expresses *S* only along the dimensions on which the gate depended. Any surplus the pathway carries is unanchored. Where reports covary with that surplus, they are at most calibrated indicators of it. This is Skinner's imprecision point, made precise: resolution can be read off the gate, before any reliability data are in.

An earlier formulation of A2 also required that *S*'s encoding not be shaped by the loss on *T*. I drop it. In end-to-end post-training every upstream parameter receives gradient from losses that depend on the report. So the clause, read strictly, excludes almost everything. Read loosely, it is vague. And if acquiring emotion language reshapes emotion (Barrett 2017; Lindquist, Satpute & Gendron 2015), it would exclude the human paradigm. Shaping matters, but to evidence about fit, not to anchoring (§6.3).

### 3.4 Lineage

In off-policy self-training (Binder et al. 2024), targets are fixed before fine-tuning, and no intervention on the fine-tuned model changes them. Strictly, A1 fails. The **lineage clause** says that A1 is nonetheless met when three conditions hold:

- the gate was computed from the channels of a predecessor *P*;
- the parameters realizing *S* in *P* persist in *L* by continuous update, without reinitialization, and *L*'s variable is the image of *P*'s under the same abstraction map;
- A3 holds.

Why continuity, and not functional similarity? A1 concerns the gate's dependence on a *token* realizer: there was a time at which intervening on this very realizer would have changed this gate. Continuity preserves that fact; functional similarity does not.

A faithfully distilled student has a numerically distinct realizer, and no intervention on it could have changed the teacher's outputs. Its report pathway was shaped to match those outputs, so its function is to predict the teacher. If a student is initialized from teacher layers, lineage holds for states realized in inherited, maintained layers, and fails for states realized in new parameters.

This is the Swampman cost (Davidson 1987; Millikan 1996; Neander 1996), extended from content to first-personal standing. On this account the extension needs no separate argument, because first-personal standing *is* possession of a self-ascriptive anchor. What needs defence is the account itself.

I previously offered an empirical prediction to soften this cost: distilled students would show a cross-prediction deficit. I withdraw it. Faithful distillation gives the student the teacher's dispositions. Its predictions about the teacher are then accurate predictions about itself, and it may compute them by self-simulation. Any deficit would measure infidelity, not the absence of an anchor. The metasemantic difference has no behavioural signature when distillation is faithful. Its import is for what the student's reports are about, and therefore for what verifying them would have to show.

### 3.5 World-directed content and "I"

A1 fails in pretraining for every term, world-directed ones included, so the anchor condition does not give base-model words their content. I assume a teleosemantics of Shea's (2018) kind, in which representations get content from the input correlations the next-token task exploited. The two metasemantics are unified by one question: which relation did learning exploit?

- If the relation runs between *L*'s states and features of the situation, content is world-directed.
- If it runs between *L*'s states and *L*'s channels, unscreened, content is self-ascriptive.

As noted in §3.1, which relation was exploited is read off the trained network, not off training statistics.

This also settles who "I" refers to, which an earlier version of this account left inconsistent. My proposal:

- When a self-ascription has a self-ascriptive anchor, the speaker, and so the referent of "I", is the bearer of the anchoring state.
- When it has none, "I" gets its reference as any word in generated text does: it refers to the speaker the text represents (Shanahan, McDonell & Reynolds 2023; cf. Chalmers 2025 on candidates for the interlocutor).

So a base model's "I am in pain" says that the represented speaker is in pain. An anchored post-trained system's "I am distressed" says that the system bearing *S* is distressed. Anchoring thus answers, for self-ascriptions specifically, the question of whom we talk to.

## 4. T1: a twin case

Take a pretrained network *N₀* with input *X* and internal variables *S*, *U* and *W*. Its causal structure is:

- *S* → *W* and *U* → *W*;
- *W* → *C₁*;
- *S* → *C₂* and *S* → *C₃*.

*U* tracks an input dimension that barely varies on the training distribution. Two regimes then build a report term *T*:

- **Regime A** gates *T* on *C₁*, *C₂* and *C₃*;
- **Regime B** gates *T* on *C₁* alone.

On the training distribution *U* is nearly constant, so reading *W* fits all three gates in A and the single gate in B. Both regimes therefore build the same read-out, *W* → *T*. The final networks are identical.

Apply the content rule.

- **In A**, the only common cause of *C₁*, *C₂*, *C₃* and *T* is *S*, so *T* expresses *S*.
- **In B**, both *S* and *W* cause *C₁* and *T*. But *S* lacks the *U*-driven variation that makes a difference to the *C₁* gate, and it has dimensions affecting only *C₂* and *C₃*, which make no gate difference in B. So *W* is proportional, and *T* expresses *W*.

Now deploy both systems on an input that shifts *U*, so that *W* is high while *S* is low. Both systems report "high", while *C₂* and *C₃* read low. A's report is a misexpression and B's is correct.

Why is that the correct verdict? Had *U* varied in A's training, the *C₂* and *C₃* gates would have penalized the report and pushed the read-out toward *S*. In B nothing would have. A trained read-out's standard of correctness is the one its learning would have enforced. That premise is teleosemantic, and I do not claim that neutral premises compel it. My claim is conditional: within such a framework, history cannot be eliminated from target selection.

The synchronic alternatives confirm this.

- **Relative to *T* alone**, proportionality is a constraint on grain, not on position along a chain. Where upstream variables map one-to-one onto *T*'s variation, analysis leaves the target indeterminate along the chain; this is the distal-content problem (Neander 2017, chs. 9–10). Where side inputs enter, as here, it selects the most proximal mediator, *W*, in both twins.
- **Relative to all of *T*'s chain's effects**, commonality is met only far upstream, at representations of the input.
- **Relative to effects chosen by a theory of the target**, the two twins' reports get the same target. A's report then counts as erroneous only if the theory already says that *S* is the target. That collapses what the report expresses into whether the theory fits.

Gate history picks out *C₁–C₃* for A and *C₁* for B without any theory of what *S* or *W* is. A theorist who appeals instead to "what training would correct" must say which training. The answer is the training that actually occurred, which is history.

## 5. Applications

### 5.1 The clock

A caregiver approves "it hurts!" whenever the child vocalizes at an hourly chime, and a painful treatment is scheduled on the hour. The gate depends on the chime, which is situation. With the chime fixed, pain makes no gate difference, so A1 fails however strong the correlation.

An associative learner may still wire pain to "it hurts", and the reports may be reliable constructed indicators of pain. But the history cannot decide whether the term's target is pain or registration of the chime, because these were coextensive throughout training. This is a coextension problem of the frog-and-fly kind (Neander 2017), not Fodor's misrepresentation-driven disjunction problem. If later gates come to depend on the child's crying, the tie is broken.

### 5.2 Base models and debunking

In pretraining, the gate for a first-person "I am in pain" is fixed text. By §3.5, the report says that the represented speaker is in pain. The model's state is the vehicle; the represented speaker is the subject. Text produced by other models, or about AI assistants, changes nothing, since those systems are not lineage predecessors.

The framework predicts that base-model self-reports vary with prompt features that fix the implied speaker. An earlier version claimed more: that design knowledge alone establishes the insensitivity premise debunking arguments need (White 2010; Korman 2019). That conflated two things, as the clock case shows. The absence of an anchor is not insensitivity. A base model's reports might covary with its internal states for incidental reasons, and only measurement could rule that out.

What design knowledge does establish is narrower:

- such covariation would not be what the reports *say*;
- nothing in training pushed toward it.

So base-model reports are not first-person testimony. They could at most become calibrated indicators.

### 5.3 Preference data and agentic RL

Raters judging whole transcripts penalize mismatches between a model's self-descriptions and its behaviour elsewhere in the conversation. That behaviour is the model's own output, a channel, so A1 holds. Agentic RL likewise gates on the model's earlier actions.

Everything then turns on A2. A model that produces self-descriptions by re-reading its earlier behaviour is screened: it interprets itself. A model whose self-descriptions branch from the state that drove the behaviour forms a fork. The patching test of §3.2 distinguishes the two.

Persona work (Chen et al. 2025) suggests that behaviour in post-trained models may be driven by representations of the Assistant's traits. If such a representation passes A2, reports express it *as the system's condition*, because the gates depended on its role in driving the system's own behaviour. The contrast that matters for T2 is therefore not persona versus self. It is text-gated reports about a represented speaker versus behaviour-gated reports of whatever drives the system.

### 5.4 Lindsey (2025)

Lindsey injected concept vectors into Claude models' activations and asked whether the models noticed an injected thought. The best models succeeded in roughly 20 per cent of trials at the most favourable layer and strength, with rare false positives. Within that narrow regime, detection reports are low-sensitivity, high-specificity calibrated indicators of injection. The report has two parts that call for different treatment.

- **The concept word** ("bread") is world-directed, like blurting out the content of an intrusive thought.
- **The meta-content** ("I notice an injected thought") is self-ascriptive in form. Pretraining did not gate it on the model's anomalies, and whether post-training did is unknown.

Two hypotheses about the meta-report make different predictions.

- **Hypothesis (H1):** it expresses a registration of internal anomaly. Then detection should sometimes occur without identification, for example with vectors that have no verbalizable concept, and detection rates should track injection strength independently of concept salience.
- **Hypothesis (H2):** it is a world-directed sensitivity to out-of-place content. Then detection should rarely occur without identification, and should track how incongruous the concept is with the context.

The prefill experiments bear on A1. A word the experimenter places in the model's response is situation. Models tend to disavow such words. They become more likely to accept them as intended when the corresponding concept is injected into earlier activations. So the self-ascription of intention varies under an internal intervention with the situation fixed. That makes it a calibrated indicator of consistency between internal plan and output. Whether it is *anchored* depends on whether post-training gates depended on such consistency through the model's own channels.

### 5.5 Binder et al. (2024) and Plunkett et al. (2025)

Binder et al. fine-tuned a model, M1, to predict properties of its own earlier responses. A second model, M2, trained on the same data, predicted M1 less well, and M1's self-predictions tracked behavioural changes induced by later fine-tuning.

The lineage clause gives A1. The tracking under later fine-tuning fits A3, since values changed while the read-out persisted. The simplest explanation of the M1–M2 gap is self-simulation: M1 has the dispositions it predicts and can compute them. I agree, and self-simulation is exactly a fork, with the behaviour-driving computation as common source. Anchoring does not compete with that explanation. It says what self-simulated reports express. But the gap does not by itself show an anchor, and I no longer present it as the signature of one. The results also concern behavioural dispositions, not affect, and they held only for simple properties.

Plunkett et al. train models to report the parameters governing their choices. Where the targets are instilled parameters, the gate depends on a common cause of the model's state and the target. That is the scrape structure, and A1 fails for self-ascription.

Plunkett et al. also report that this training improves reports about the models' native preferences. If so, the trained pathway reads the states that drive the models' choices. This is a reliable read-out without an anchor, the reverse of the clock case. Reports about native preferences are then reliable constructed indicators, but not avowals, until the gates depend on measured choices.

## 6. Anchoring by probe

Perez and Long's proposal can be extended: reward self-reports for matching probe readings of the model's states, and of other channels. The anchor conditions then yield design requirements.

### 6.1 Freezing

Detaching gradients at the probe read-out does not stop the report loss from updating weights upstream of the probed layer. Freezing every parameter up to and including the probed layer keeps the probe direction's meaning fixed. Freezing is not sufficient for A2, however. Later, unfrozen layers can still learn a shortcut that reads the situation. And freezing does not protect against distribution shift in deployment, which requires monitoring.

### 6.2 Depth and the held-out channel

If the report reads exactly the probed direction, the content rule makes the term express exactly what the probe measures. To anchor something deeper, the gates should depend on diverse channels: probes on different layers, behavioural signatures such as task avoidance, and effects on performance. The test for depth is to withhold one signature and ask whether reports predict it.

The test is confounded by the model's pretrained folk psychology. A persona model could predict the withheld signature from human talk. Two controls are needed.

- **System-specific signatures.** The withheld signature should be one that human talk does not link to the target, such as an effect on a particular internal computation.
- **Joint interventions.** Intervening on the candidate *S* should move both the reports and the withheld signature, while varying persona-fixing prompt features with *S* clamped should move neither.

There is a real tension here: the less folk-linked a signature is, the weaker it is as evidence that the target is distress. The resolution is to divide the labour.

- *Non-folk* signatures test commonality: whether reports read a common source.
- *Folk-linked* signatures bear on fit.

Neither test does both jobs.

### 6.3 Shaping and fit-evidence

Suppose the probe regime is run end to end, and the behavioural channels are also trained toward agreement with the reports. The result can be a variable *V* that is a common cause of the report and every channel. By the content rule, the reports express *V*. A synchronic functionalist will say that *V* is now the distress candidate, and I agree.

What history changes here is evidential, and it bears on fit. The channels were validated as signatures of distress before training, and they were then reshaped toward agreement with the report. Their present agreement is therefore no independent evidence that the channels still are such signatures, or that *V* is distress. This is ordinary measurement theory, and I claim no novelty for it. It belongs here because it marks where the dropped no-shaping clause had its proper role: it is a condition on the independence of fit-evidence, not on anchoring.

## 7. Reach, entitlement, and what anchoring adds

Anchoring makes a report express *S*. A trained nonsense word, "zorp", would express *S* equally well. Public content matters only for what is said. If the gated channels were chosen as functional signatures of distress, *S* is a functionalist candidate for distress. That does not show it is felt.

The referee's challenge deserves a direct answer: *what epistemic difference separates a verified anchored report from a constructed indicator built by the same regime and verified the same way?* None. A verified anchored report *is* such an indicator. I withdraw the claim that the evidential question about AI self-report turns on anchoring in the sense of a distinctive warrant.

Nor is identifying the expressed variable epistemically prior to interpretability: verifying A2 requires finding the variable. What anchoring contributes are four other things.

1. **Negative verdicts from design alone.** Pretraining, distillation, instilled targets, and situation-gating all yield reports that are not about the system's own condition. No measurement is needed to show this.
2. **A specification of what verification must find.** It must find an unscreened, proportional common source of the gated channels, at the grain the gates fix.
3. **The separation of expression from fit.** The designer's theory enters only through the choice of channels. Once those are gated, the report's target is a fact that holds whether or not the theory is right, so "is the expressed state distress?" remains a genuine question. The theory-ladenness I charge against the synchronic rival is different: it needs a theory to fix *what the report is about*, so the report's truth collapses into the theory's.
4. **Reach.** An unscreened anchored report can inform about occurrences of *S* that no gated channel registers, which is what the held-out test checks. Beyond every channel, projection is induction from a known mechanism.

On entitlement, Burge's (1993) Acceptance Principle presupposes rational sources, which is part of what is in question here. Following Goldberg (2010), Freiman and Miller (2020), and Green and Michel (2022), I treat the hearer's warrant as reliance on a verified instrument whose outputs have truth-evaluable content. Source-level knowledge must be earned: of the gates, the fork, maintenance, and resolution (cf. Fricker 1994). Token reports may then be accepted unless defeated. This resembles Lackey's (2008) dualism, which already permits the hearer's positive reasons to be general. For current systems, defeaters are pervasive: unknown gate structure, unverified forks, and persona effects. The default does not activate.

Human cases illustrate rather than test the view, because human acquisition gates are unknown. Misreported emotion and mood (Schwitzgebel 2008) show that even within its resolution, anchoring yields at most a defeasible default. The view also accommodates Carruthers's (2011) claim that attitude self-ascription is interpretive: such self-ascription would be screened self-interpretation. Transparency procedures (Byrne 2018) count as anchored when their gates depended on first-order states through the learner's own channels, and as world-directed otherwise.

## 8. Conclusion

A self-report expresses a state of the system that produces it when four conditions hold:

1. its acquisition gates depended on the system's channels, holding the situation fixed, or on those of a lineage predecessor whose realizer persists;
2. the trained network contains an unscreened state that is a common cause of those channels and the report, and that is proportional to the channel-mediated gate dependence;
3. that pathway has been maintained;
4. the term's resolution is read off the gates.

The three theses fare as follows.

- **T1** holds in a conditional form. The twin case shows that, given a teleosemantic standard of correctness, gate history fixes error conditions that synchronic structure cannot.
- **T2** holds as stated. Base-model "I" refers to a represented speaker. Post-trained anchoring requires both a channel-gated regime and a verified fork.
- **T3** holds, strengthened by a concession: anchoring adds no distinctive warrant. It fixes what reports are about, and so what verification and fit-testing must establish.

For current systems, entitlement has not been earned. The prior question for any self-report remains whether it has an anchor, and what that anchor is.

## References

- Andrews, K., & Birch, J. (2023). What has feelings? *Aeon*, 23 February 2023.
- Bar-On, D. (2004). *Speaking My Mind: Expression and Self-Knowledge*. Oxford: Oxford University Press.
- Barrett, L. F. (2017). *How Emotions Are Made: The Secret Life of the Brain*. Boston: Houghton Mifflin Harcourt.
- Binder, F. J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., Perez, E., Turpin, M., & Evans, O. (2024). Looking inward: Language models can learn about themselves by introspection. arXiv:2410.13787.
- Birch, J. (2024). *The Edge of Sentience: Risk and Precaution in Humans, Other Animals, and AI*. Oxford: Oxford University Press.
- Burge, T. (1979). Individualism and the mental. *Midwest Studies in Philosophy*, 4, 73–121.
- Burge, T. (1993). Content preservation. *The Philosophical Review*, 102(4), 457–488.
- Butlin, P., Long, R., et al. (2023). Consciousness in artificial intelligence: Insights from the science of consciousness. arXiv:2308.08708.
- Byrne, A. (2018). *Transparency and Self-Knowledge*. Oxford: Oxford University Press.
- Cappelen, H., & Dever, J. (2021). *Making AI Intelligible: Philosophical Foundations*. Oxford: Oxford University Press.
- Carruthers, P. (2011). *The Opacity of Mind: An Integrative Theory of Self-Knowledge*. Oxford: Oxford University Press.
- Chalmers, D. J. (2023). Could a large language model be conscious? arXiv:2303.07103.
- Chalmers, D. J. (2025). What we talk to when we talk to language models. Manuscript.
- Chen, R., Arditi, A., Sleight, H., Evans, O., & Lindsey, J. (2025). Persona vectors: Monitoring and controlling character traits in language models. arXiv:2507.21509.
- Comșa, I. M., & Shanahan, M. (2025). Does it make sense to speak of introspection in large language models? arXiv:2506.05068.
- Damasio, A. R. (1994). *Descartes' Error: Emotion, Reason, and the Human Brain*. New York: G. P. Putnam's Sons.
- Davidson, D. (1987). Knowing one's own mind. *Proceedings and Addresses of the American Philosophical Association*, 60(3), 441–458.
- Dretske, F. (1988). *Explaining Behavior: Reasons in a World of Causes*. Cambridge, MA: MIT Press.
- Freiman, O., & Miller, B. (2020). Can artificial entities assert? In S. Goldberg (Ed.), *The Oxford Handbook of Assertion* (pp. 415–436). Oxford: Oxford University Press.
- Fricker, E. (1994). Against gullibility. In B. K. Matilal & A. Chakrabarti (Eds.), *Knowing from Words* (pp. 125–161). Dordrecht: Kluwer.
- Geiger, A., Lu, H., Icard, T., & Potts, C. (2021). Causal abstractions of neural networks. *Advances in Neural Information Processing Systems*, 34.
- Geirhos, R., Jacobsen, J.-H., Michaelis, C., Zemel, R., Brendel, W., Bethge, M., & Wichmann, F. A. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence*, 2, 665–673.
- Goldberg, S. (2010). *Relying on Others: An Essay in Epistemology*. Oxford: Oxford University Press.
- Green, M., & Michel, J. G. (2022). What might machines mean? *Minds and Machines*, 32, 323–338.
- James, W. (1884). What is an emotion? *Mind*, 9(34), 188–205.
- Kammerer, F., & Frankish, K. (2023). What forms could introspective systems take? A research programme. *Journal of Consciousness Studies*, 30(9–10), 13–48.
- Korman, D. Z. (2019). Debunking arguments. *Philosophy Compass*, 14(12), e12638.
- Lackey, J. (2008). *Learning from Words: Testimony as a Source of Knowledge*. Oxford: Oxford University Press.
- Lin, S., Hilton, J., & Evans, O. (2022). Teaching models to express their uncertainty in words. *Transactions on Machine Learning Research*. arXiv:2205.14334.
- Lindquist, K. A., Satpute, A. B., & Gendron, M. (2015). Does language do more than communicate emotion? *Current Directions in Psychological Science*, 24(2), 99–108.
- Lindsey, J. (2025). Emergent introspective awareness in large language models. *Transformer Circuits Thread*, Anthropic, October 2025.
- List, C., & Menzies, P. (2009). Nonreductive physicalism and the limits of the exclusion principle. *The Journal of Philosophy*, 106(9), 475–502.
- Long, R. (2023). Introspective capabilities in large language models. *Journal of Consciousness Studies*, 30(9–10), 143–153.
- Mandelkern, M., & Linzen, T. (2024). Do language models' words refer? *Computational Linguistics*, 50(3), 1191–1200.
- Millikan, R. G. (1996). On swampkinds. *Mind & Language*, 11(1), 103–117.
- Neander, K. (1996). Swampman meets swampcow. *Mind & Language*, 11(1), 118–129.
- Neander, K. (2017). *A Mark of the Mental: In Defense of Informational Teleosemantics*. Cambridge, MA: MIT Press.
- Perez, E., & Long, R. (2023). Towards evaluating AI systems for moral status using self-reports. arXiv:2311.08576.
- Plunkett, D., Morris, A., Reddy, K., & Morales, J. (2025). Self-interpretability: LLMs can describe complex internal processes that drive their decisions, and improve with training. arXiv:2505.17120.
- Prinz, J. J. (2004). *Gut Reactions: A Perceptual Theory of Emotion*. Oxford: Oxford University Press.
- Schneider, S. (2019). *Artificial You: AI and the Future of Your Mind*. Princeton: Princeton University Press.
- Schwitzgebel, E. (2008). The unreliability of naive introspection. *The Philosophical Review*, 117(2), 245–273.
- Shanahan, M., McDonell, K., & Reynolds, L. (2023). Role play with large language models. *Nature*, 623, 493–498.
- Shea, N. (2018). *Representation in Cognitive Science*. Oxford: Oxford University Press.
- Skinner, B. F. (1945). The operational analysis of psychological terms. *Psychological Review*, 52(5), 270–277.
- Skinner, B. F. (1957). *Verbal Behavior*. New York: Appleton-Century-Crofts.
- Tye, M. (1995). *Ten Problems of Consciousness*. Cambridge, MA: MIT Press.
- White, R. (2010). You just believed that because… *Philosophical Perspectives*, 24, 573–615.
- Wittgenstein, L. (1953/2009). *Philosophical Investigations* (G. E. M. Anscombe, P. M. S. Hacker & J. Schulte, Trans.; rev. 4th ed.). Oxford: Wiley-Blackwell.
- Woodward, J. (2010). Causation in biology: Stability, specificity, and the choice of levels of explanation. *Biology & Philosophy*, 25(3), 287–318.
- Yablo, S. (1992). Mental causation. *The Philosophical Review*, 101(2), 245–280.