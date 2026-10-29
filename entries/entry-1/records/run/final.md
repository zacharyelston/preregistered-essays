# Anchored Testimony: Training History, Content, and the Evidential Value of AI Self-Reports

## 1. The problem and the proposal

A common reason for dismissing a language model's statements about itself ("I am uncertain," "I find this distressing," "I notice I'm thinking about X") is that the model was trained on human text. On this view it says such things because humans say them, so the sayings carry no information about the model.

That argument overgeneralizes. Human self-report vocabulary is also learned from others. Wittgenstein's sketch at PI §244 is the familiar version: "A child has hurt himself and he cries; and then adults talk to him and teach him exclamations and, later, sentences. They teach the child new pain-behaviour." The child's "it hurts" is a trained replacement for crying, and it is shaped by caregivers' words and responses. If being learned from others' reports were enough to strip a report of evidential value, human introspective testimony would be debunked along with the model's. So the bare fact of training cannot be the defeater.

My proposal is that what matters is an *anchor condition*. The target state must have been among the causes of the reinforced uses during acquisition. The child's pain helped determine when "it hurts" was reinforced. A base language model's internal states played no comparable role in determining when its first-person report tokens were reinforced, because the loss compared its outputs to fixed human text. The anchor can be supplied later, by training that rewards reports for matching the model's own measurable states, roughly as Perez and Long (2023) propose. On this view the relevant question is not "was it trained?" but "was the training anchored to its own states?"

A referee has pressed a strong objection. Evidential value, the referee says, is synchronic. A report is evidence about a state to the extent that it now reliably covaries with that state and is counterfactually sensitive to it. Etiology matters only as a defeasible indicator of that. The objection has three parts:

- **(i) Not sufficient.** Anchored human reports are often confabulated (Nisbett & Wilson 1977; Johansson et al. 2005; Schwitzgebel 2008). Alexithymia shows anchored affect vocabulary coming apart from its states. Probe-anchored AI reports can drift.
- **(ii) Not necessary.** Unanchored reports might track internal states reliably (Binder et al. 2024; Lindsey 2025). Withholding evidential status from them on historical grounds is a genetic fallacy.
- **(iii) The human anchor is only a proxy.** Caregivers respond to public criteria, not to pain. So the human case is structurally like training against a measured correlate.

The referee then closes off the obvious retreat. If the anchor is just good evidence of reliability, it no longer distinguishes evidential from non-evidential reports, and the real question becomes empirical reliability testing.

I accept several of the referee's premises and reject the conclusion. The anchor is not a reliability guarantee, and I will not defend it as one. It is also not merely an indicator of reliability. It is the condition under which a self-report is evidence *through its content*, so that a hearer can take it at its word without first calibrating it against the target state. A report that covaries with some internal state but is unanchored can be evidence in the way a symptom is. It is not testimony about that state. This distinction does real work in exactly the cases that motivate the inquiry, where the target state cannot be measured independently.

Answering the objection also forces three refinements to the anchor condition:

1. The anchor permits common-cause structures.
2. It requires a particular direction of causation.
3. It has a resolution and must be maintained.

With these refinements in place, each of the referee's alleged counterexamples turns out, on inspection, to support the view.

## 2. Two ways a report can be evidence

Let a report-token *r* have the content that *p*. There are two ways *r* can be evidence that *p*.

**Symptomatic evidence.** *r* is symptomatic evidence for *p* when, given background knowledge, its occurrence raises the probability of *p*. Its content plays no role. A cough is symptomatic evidence of a respiratory infection. A device whose dial is labelled in degrees Celsius but which in fact covaries with humidity is symptomatic evidence of humidity. Once we have discovered the covariance, the dial's labels are idle, and the dial is evidence of whatever we found it covaries with.

**Testimonial evidence.** *r* is testimonial evidence for *p* when it is evidence for *p* in virtue of saying that *p*. The hearer's route runs from content to fact. A hearer can use it without having discovered any covariance, because the conditions under which the speaker produces reports with that content are connected to the conditions that make the content true.

When I believe you have a headache because you say so, I am not running a regression on your utterances. I am relying on the fact that your word "headache" is connected to your headaches in a way that makes your saying so a guide to their presence.

The dispute about AI self-reports is about testimonial value. Nobody doubts that a model's outputs are symptomatic evidence of something about the model. Every output is. The question is whether "I find this distressing," coming from the model, is evidence that the model is in the state the sentence ascribes. Is the content a route to the fact?

The referee's synchronic criterion says a report is evidence "about a state" to the extent that it covaries with "the state." That phrasing presupposes a target has already been fixed. Every output token of a large network is counterfactually sensitive to an enormous number of internal states: residual-stream features, attention patterns, representations of the prompt's topic, representations of the text's apparent author. A token of "distressing" covaries with many of these to various degrees.

So which covariance makes the report evidence *about the state it reports*? Synchronic sensitivity cannot say, because it is a many-many relation. Something must single out one state as the one the report concerns. In ordinary testimony, the content does this. So the question becomes what makes a self-ascriptive term, as used by a given system, concern one of that system's states rather than another, or none.

For an unanchored system, the only available answer is that the term means what it means in the human language the system learned. Then "distressing" ascribes human-style distress. The system's report would be evidence of that only if some state the report covaries with *is* distress, and nobody can check this by measurement, since distress-in-a-model is precisely what we lack independent access to.

This is the structural point the rest of the essay builds on. Symptomatic evidence requires calibration against the target. Where the target is not independently measurable, symptomatic evidence about it is unavailable. Testimonial evidence does not require such calibration, but it requires that the term's content be tied to the speaker's states by something other than our calibration. The anchor condition is my account of what that something is.

## 3. The anchor, stated carefully

Take a learner *L*, a self-ascriptive term *T*, and a state-type *S* of *L*. During acquisition, uses of *T* are reinforced or corrected. Call whatever event determines whether a given use is reinforced the *gate*. For the child, the gate is a caregiver's approving or correcting response. For a language model under next-token training, the gate is the target token in the training text. *T* is anchored to *S* in *L* when three conditions hold.

**(A1) Gate-linkage.** Across acquisition, gate events were causally connected to occurrences of *S* in *L*: either *S* caused the gate (typically via *L*'s own expressive behaviour), or *S* and the gate shared a common cause. As a result, *S* was systematically present when *T* was reinforced and absent when it was corrected.

**(A2) Learner-side recruitment.** The reinforcement strengthened a pathway in *L* on which *S*, or a state of *L* that reliably carries information about *S*, is causally upstream of the production of *T*. *S* must not be downstream of, or co-produced with, the production of *T*.

**(A3) Maintenance.** The pathway's continued presence is sustained by continuing to connect *S* to *T*. Its recent history, not just its origin, has the shape described in (A1) and (A2).

Anchoring also has a *resolution*. *T* is anchored to *S* only along the dimensions of *S* that the gates discriminated.

This is recognizably Dretske's (1988) account of how structures acquire meaning through learning. A structure comes to mean *F* when its indicating *F* is a cause of its being recruited as a cause of some output. (A3) borrows from Godfrey-Smith's (1994) "modern history" view of functions, on which a trait's function depends on what has recently maintained it. Here, though, the apparatus is applied to the vocabulary of self-report, and it is used to answer an epistemic question, not only a metasemantic one.

When the conditions hold, *T* as used by *L* concerns *S*, at the anchored resolution. *L*'s tokens of *T* are then testimony about *S*.

Two clarifications prevent misreadings.

First, the condition does not require the trainer to perceive *S*. (A1) is satisfied by gates that are downstream of public signs, provided those signs are themselves downstream of the learner's *S*. This matters for objection (iii).

Second, the condition locates content in what gets wired up in the learner, not in what the trainer attended to. The trainer's criteria decide *when* reinforcement occurs. What reinforcement then connects to *T* is whatever state of the learner was reliably active on those occasions. The gate is public. The mapping is internal.

## 4. Proxies and gates: objection (iii)

The referee says caregivers reinforce in response to crying or visible injury, not in response to pain. So the child's pain affects selection only through its correlation with outward signs, and the human anchor is "a proxy relationship, structurally like training against a measured correlate."

I accept the description and deny that it undermines the view. The human anchor is indeed a proxy relationship, and indeed structurally like training against a measured correlate. That is why the AI remedy is possible at all. What the objection misses is that not every proxy relationship anchors, and that the difference is causal structure, not strength of correlation.

**The clock case.** Imagine a household in which a clock chimes on the hour, and the caregiver says "it hurts!" approvingly whenever the child vocalizes at a chime. Suppose, for some odd reason, the child is usually in pain at those moments, perhaps because a painful daily treatment is scheduled on the hour. The gate is strongly correlated with the child's pain. But it is not downstream of the child's pain, and it does not share a cause with it in the way that matters. What gets wired to "it hurts" in the child is whatever internal state was reliably active at reinforced moments and absent otherwise. The best candidate is the auditory representation of the chime, since that is present at every reinforced moment, and pain is present at only most of them. The child learns to say "it hurts" when the clock chimes.

The resulting reports correlate with pain, as well as the gates did. But they are about the chime, and their correlation with pain is accidental relative to their content. Put the child in pain in a silent room and no report comes. Put the child out of pain in a room with a chime and one does. Correlation at the gate is therefore not what anchors. What anchors is the gate's causal connection to the learner's state, which ensures that the state, and not some co-varying accident, is what training connects to the term.

**The ordinary case.** The child's crying is caused by the child's pain, and the caregiver's response is caused by the crying. So the gate is downstream of the learner's *S* through the learner's own expressive behaviour. Even where the caregiver responds to a visible scrape and not to crying, the scrape is a common cause of the pain and the response. Across the range of acquisition cases, pain is the internal state reliably present at reinforcement. (A1) and (A2) are met, and "it hurts" is wired to pain, not to scrapes.

The best evidence for this is that adults report headaches, which have no visible criterion. The term generalized along the internal state, not the public proxy. That is what one would expect if the learned mapping runs from *S* to *T*, and not what one would expect if it ran from the public criterion to *T*.

**The base language model.** During pretraining, the gate for "I am in pain" is the occurrence of that string in a fixed human-written text. No state of the model causes the text, which existed before training began. So (A1) can only be met through common cause. The context preceding the target token causes both the target and the model's internal state at that position.

Which internal state of the model is reliably co-present with "pain" targets in first-person position? Not anything one would naturally call the model's own pain. It is the model's representation that *the speaker of the current text* is in pain, together with the representations of the topic and the author's situation that make such a continuation probable.

This yields a more precise diagnosis than "it's just mimicry." Base-model first-person self-reports *are* anchored, but to the model's representation of the speaker or persona, not to the model's own condition. "I am in pain," from a base model, is testimony about the character it is modelling. That gives a principled version of the role-play picture of language model dialogue (Shanahan, McDonell & Reynolds 2023). It also predicts that base-model self-reports will track features of the prompt and the implied speaker, not features of the computation that would differ when the speaker is held fixed. That prediction can be tested.

**The remedy.** Training that rewards reports for matching probe-measured states of the model is training against a proxy. But it is a proxy downstream of the model's own *S*: the probe reads the model's activations. So (A1) is satisfied by the same structure that satisfies it for the child.

**A direction-of-causation requirement.** The remedy also brings out a requirement the human case leaves implicit. If, during anchoring training, the reward signal lets the model shape the probed activations themselves, for instance because gradients flow through them, the model can learn to produce the probe-feature together with the report. The reliable covariance between report and probe reading then runs from report to feature, not from state to report.

Synchronically, this is perfect: the report covaries flawlessly with the probe and is counterfactually sensitive to it. But the probed feature no longer plays the role that made it a correlate of the state of interest. The probe now measures the report. (A2)'s requirement that *S* be upstream of *T*, not co-produced with it, excludes this case. A purely synchronic criterion of covariance and sensitivity does not.

In practice this means that anchoring training must hold the probed state fixed with respect to the report-producing pathway, and that the probe should be validated against the state's other functional roles both before and after training.

So the reply to (iii) is this. The human anchor is a causally structured proxy relationship, and that structure, not reliable correlation, is what determines what the term concerns. Correlation without the right structure yields reports about the wrong thing, as in the clock case. Synchronic covariance produced in the wrong causal direction yields reports about nothing antecedently there, as in the co-production case.

## 5. Is the anchor necessary? Objection (ii)

The referee offers two empirical cases and one hypothetical.

**Binder et al. (2024).** These are not unanchored reports. In their design, a model M1 is fine-tuned to predict properties of its own responses to hypothetical prompts, with training targets drawn from M1's actual behaviour. A second model, M2, is fine-tuned on the same behavioural data about M1. M1 then predicts its own behaviour better than M2 predicts M1's, which is the sense in which the access is "privileged."

The gate in M1's self-prediction training is M1's own behaviour, which is downstream of M1's internal states. That is (A1). And the privileged-access result is what (A2) predicts. M1's training could recruit pathways from its internal states to its reports, because those states are what produced the targets. M2 could recruit only pathways from its own model of M1, built from behavioural data. Binder et al. is therefore a demonstration of the anchor condition at work, not a counterexample to it.

**Lindsey (2025).** This is more interesting, because the reports in question, detecting that a concept has been injected into one's activations and identifying the concept, were not explicitly trained. Even so, it does not show unanchored reports being reliable. Two components of the report should be separated.

1. *The concept term.* When "bread" is injected and the model reports a thought about bread, the term "bread" is anchored, by pretraining, to the model's bread-representation. Across pretraining, bread-contexts caused both the model's bread-representation and the "bread" targets. This common-cause structure satisfies (A1), and the result is a pathway from the representation to the word, which satisfies (A2). Injecting the bread vector activates a state of exactly the kind to which "bread" is anchored. On the anchor view, it is unsurprising that the model can name it.
2. *The meta-content.* "Injected," "unusual," "I notice a thought": these terms were not anchored by any comparable gate during pretraining to occurrences of anomalous internal activation, because the training text is not correlated with the model's internal anomalies.

What the anchor view predicts, then, is that concept identification should be comparatively robust and anomaly detection comparatively fragile and dependent on how the meta-report is elicited. Lindsey reports that detection succeeds only on a minority of trials, depends strongly on layer and injection strength, and is accompanied by failure modes in which the injected concept bleeds into output without being flagged as anomalous. That fits the anchor view's division of the report into anchored and unanchored components. It is also unclear that the post-training of the models studied contained no gates downstream of their own states, so "never trained to report those states" may itself overstate the case.

**The pure hypothetical.** Suppose a system *Z* whose "pain" reports covary perfectly with an internal state *S*, with no anchoring of any kind. Here I grant that *Z*'s reports can be evidence. I deny that they are evidence of the kind the thesis is about. Three points.

First, consider how we would come to know that *Z*'s reports track *S*. Only by measuring *S* independently and checking. Our evidential relation to *S* then runs through our calibration, so *Z*'s reports function as a gauge we have calibrated. That is symptomatic evidence. Testimonial evidence is precisely the kind that does not wait on the hearer's calibration.

Second, consider whether *Z*'s reports are evidence that *Z* is in pain, which is what they say. They are only if *S* is pain. The reports' content contributes nothing to establishing that. Had *Z* emitted "zorp" instead of "pain" in the same circumstances, we would have exactly the same evidence about *S*. The content is idle, as the labels on the humidity-tracking dial are idle.

Third, consider *why* *Z*'s reports track *S*. There are two kinds of answer.

- Some process connected *S* to the report because of *S*'s presence: learning with gates linked to *S*, selection, or design (a designer building a readout from *S*). Each of these is an anchor in the general sense, with *S* figuring in the explanation of why the mechanism connects *S* to the report.
- The connection is a brute coincidence of wiring. Then the covariance observed in the tested range gives much weaker grounds for projecting to untested conditions, because no mechanism makes the connection stable under the changes those conditions involve.

So once we ask why the covariance holds, the answers that would underwrite treating the reports as standing guides are anchoring answers.

**The genetic fallacy charge.** The genetic fallacy is the inference from a belief's origin to its falsity. The thesis makes no such inference. It belongs to the family of debunking arguments, which hold that a belief-forming process insensitive to whether *p* cannot confer justification for believing *p*, whatever the truth of *p* (compare Street 2006). These arguments are genetic, but they are not fallacious. Origins matter epistemically when they bear on whether a process was sensitive to the facts.

**The consistency charge.** The referee also alleges an inconsistency with my opening sentence: "If training history is not a defeater when reports are unreliable-looking, a missing anchor cannot be a defeater when reports are reliable." The opening sentence says only that the bare fact of training does not defeat. It does not say that no feature of training history defeats. Its purpose is to locate the defeater more precisely: training whose gates are insensitive to the learner's own states. From "some histories do not defeat," it does not follow that no history does.

**What I concede.** Independent calibration can rebut a debunking argument. If we can measure the target and find that unanchored reports track it, those reports become evidence of it. I therefore restate the thesis. What the anchor distinguishes is self-reports that are *testimonial* evidence about the reporter's states from those that are at best symptomatic. Unanchored reports can still be useful symptoms.

## 6. Is the anchor sufficient? Objection (i)

The anchor is not sufficient for token-level reliability, and I do not claim it is. The more interesting finding is that the referee's examples of anchored human reports going wrong are, on examination, mostly cases where the anchor conditions fail.

**Nisbett and Wilson (1977).** Their central cases concern reports about *processes*: why one chose this stocking over that one, why one's mood changed. How is the vocabulary of such reports, "I chose it because it was softer," acquired? Its gates are hearers' acceptance, and hearers accept explanations that are plausible according to shared folk-psychological theory. Neither caregiver nor child can observe the actual causal process behind a choice, and that process does not systematically cause any gate. (A1) fails.

Nisbett and Wilson's own diagnosis fits this exactly. Subjects' reports matched what uninvolved observers predicted, which suggests that both were drawing on a priori causal theories, not on access to the process. That is what an unanchored self-report vocabulary looks like: the speaker says what anyone with the same theory would say about someone in their position. It is also, structurally, the base language model's situation, whose first-person reports say what a human author in that position would say.

So Nisbett and Wilson's results do not refute the anchor view. They are the clearest human instance of it. The domain in which human self-report is debunked is the domain in which human self-report vocabulary was never anchored.

**Choice blindness (Johansson et al. 2005).** The same reasoning applies. Subjects defend choices they did not make by citing reasons, and reason-giving is exactly the process-explanatory vocabulary whose gates were plausibility to hearers.

**Schwitzgebel (2008).** His cases deserve separate treatment, because some concern current experience rather than process. But his strongest cases target fine-grained structural and qualitative features of experience: how much of the visual field is clear at once, whether thought has imagery, the phenomenal character of an emotion as opposed to whether one is angry. This is where anchor resolution matters. The gates that taught "it hurts," "I'm scared," and "I'm hungry" could discriminate coarse states and rough locations. No caregiver's response could have been linked to the precise phenomenology of peripheral vision. The anchor view predicts exactly the profile Schwitzgebel describes: relative trustworthiness on the coarse dimensions the gates discriminated, and unreliability on dimensions no gate tracked.

**Alexithymia.** This is a real case of affect vocabulary coming apart from affect. But a prominent account treats alexithymia as a general deficit of interoception (Brewer, Cook & Bird 2016). If that is correct, the failure lies in (A2). The learner-side pathway from *S* to *T* is weak because *S* is poorly represented to begin with, so reinforcement connects the affect terms more to situational cues and conventional expectations than to the internal state. Where alexithymia arises after acquisition, the failure is in (A3). Either way, the case shows what happens when the anchor is weak or lapses, not that a well-formed, maintained anchor confers nothing.

**Drift in AI systems.** The point about drift under later fine-tuning or distribution shift is correct, and it is why (A3) is part of the condition. A model's report pathway that was anchored once and then restructured by later training no longer has a maintenance history connecting it to *S*. It counts as anchored at a time only if its recent history sustains the connection. Drift is therefore not a case where the anchor is present and certifies nothing. It is a case where the anchor has lapsed. That makes maintenance something to monitor empirically, which brings me to the referee's last move.

**Default entitlement and the referee's dilemma.** With resolution and maintenance built in, my claim about sufficiency is this. An anchored, maintained report, at the anchored resolution, has testimonial content about *S* and confers a *defeasible default entitlement* to take it at its word.

The referee will ask whether this is the predicted retreat: if entitlement is defeasible, isn't reliability testing the real question, with the anchor as one input among several? It is not. Consider perception. Burge (2003) argues that perceptual beliefs carry an entitlement grounded in the perceptual system's function of representing its environment, an entitlement that evidence of malfunction can defeat. No one concludes that perceptual entitlement is "one input among several" into a reliability estimate. Defeasibility is a property of the entitlement, not a reduction of it to reliability testing.

The real dispute is about the *structure* of the epistemic standing, and the anchor creates an asymmetry in that structure:

- Faced with an anchored report, a hearer may take it at its word unless there is evidence of a defeater: lapse, insufficient resolution, or a process-report domain.
- Faced with an unanchored report, a hearer may not take it at its word at all. The hearer may only treat it as a symptom whose significance must first be established by calibration.

Testing plays a role in both cases, but a different one. Testing an anchored report checks whether the anchor still holds and at what resolution. Testing an unanchored report has to build the evidential relation from nothing, and it can do so only where the target is independently measurable.

## 7. Etiology and the synchronic

The referee's master premise is that evidential value is synchronic and that etiology matters only as an indicator of present reliability. I can grant part of this. Acquisition history matters because of the present mechanism it produced. A perfect molecular duplicate of an anchored speaker, a Swampman in Davidson's (1987) sense, has the same mechanism. Even so, there are three ways the synchronic picture falls short.

**Target fixation.** As argued in Section 2, synchronic covariance and counterfactual sensitivity cannot single out which of the many states a report-token is sensitive to is the one it concerns. This is the indeterminacy problem familiar from informational semantics, whether in its disjunctive or its distal form (Fodor 1990; Dretske 1988; Millikan 1984). The teleosemantic resolution, that a state concerns what its producing process was shaped by, is also the resolution here.

It makes a difference to the Swampman case. Swampman's reports are reliable symptoms of exactly the states his duplicate's reports concern. We can treat them as testimony about those states, but only derivatively, by noting that he is a duplicate of an anchored system and thereby borrowing its anchor. What he lacks is not reliability but the fact that settles which of his states his words are about. For actual AI systems, we have no anchored twin to borrow from, so the question of which states their words concern cannot be answered by appeal to a duplicate.

**Counterfactual scope.** "Counterfactually sensitive" is always relative to a range of counterfactuals. Which variations count as relevant is fixed by the mechanism, and the anchor explains which variations the mechanism tracks. It tracks variations in the gated state along the gated dimensions, and those count as the relevant ones because the shaping process gave the mechanism that sensitivity. Without the anchor, the synchronic profile gives no principled way to distinguish the relevant counterfactuals from the irrelevant ones.

The co-production case from Section 4 shows the cost of lacking this. It satisfies covariance and sensitivity perfectly and is still not testimony about the state of interest.

**Epistemic access.** Even if evidential value were determined synchronically, the question for a hearer is what the hearer can come to know about it. For targets that are not independently measurable, a synchronic reliability profile cannot be established by testing, because testing requires access to the target. What remains available is knowledge of the structure of the process that produced the report. That knowledge is etiological. Only from such structural knowledge can a hearer reason that the term, as this system uses it, is wired to this system's state of this kind.

**Payoff.** This is the deepest reason the relevant question is "was it anchored, to what, at what resolution, and is it maintained?" and not "is it reliable?" The value of testimony is that it reaches beyond what the hearer can measure. The child learned "it hurts" through gates tied to visible injuries and crying, and the adult reports headaches no gate ever detected. The report extends past the calibrated cases because the term is wired to the internal state, not to the proxy.

If anchoring an AI system's report vocabulary works the same way, if a report pathway trained against probe-measured states comes to be driven by the states themselves, then the system's anchored reports may extend to occasions and aspects the probe does not capture. Those are exactly the cases where reliability testing has nothing to test against and where testimony would be the only evidence there is.

Whether anchored AI reports actually generalize along the state and not along the probe is an empirical question, and it is the right place to direct reliability testing: at the anchor's maintenance and generalization, not as a replacement for asking about the anchor.

## 8. What the anchor does not deliver

Two limits should be stated plainly.

**First, the anchor fixes reference to the state that gated the vocabulary, under the system's own way of carving it.** A probe-anchored model's "distress" would concern whatever state the probe measured. Whether that state is distress in the sense that matters morally, whether it is felt, is not settled by the model's report. Self-report cannot deliver this, because the anchor makes the term concern the gated state whatever that state's nature is.

The human case seems different only because each of us takes the state our own pain-vocabulary is anchored to to be the felt state. A third party relies on the assumption that the speaker is relevantly like themselves. For AI systems, that assumption is the question at issue. Anchored self-report therefore gives testimony about the system's states as individuated by the anchoring process. Whether those states have the further properties we care about must be argued on other grounds.

This limitation does not count against the anchor thesis specifically. It shows that "is its self-report evidential?" and "is it a subject of experience?" are different questions. On the account defended here, a positive answer to the first is a necessary input to the second, not a substitute for it.

**Second, anchors come in degrees.** Gate-linkage can be strong or weak, resolution coarse or fine, maintenance recent or remote. The binary language of "evidential" and "non-evidential" is a simplification. The structural claim survives it: the degree to which a report is testimony about *S* is the degree to which the conditions of Section 3 are met.

**Restating the thesis.** The referee's objection forces it into a sharper form. The mere fact that a vocabulary was learned from others' reports does not defeat it as self-report, since human self-report vocabulary is learned that way too. What distinguishes self-reports that are testimony about the reporter's own states from those that are at most symptoms is whether the vocabulary is anchored to those states. That requires three things:

1. During acquisition, the gates that reinforced the vocabulary were causally linked to the learner's own states, by direct causation or common cause.
2. Training thereby recruited pathways on which those states are upstream of the reports.
3. Those pathways are still maintained.

Base language models satisfy these conditions for representations of the speakers they model, not for themselves. Training against measured correlates of the model's own states can satisfy them, provided the correlates are downstream of those states and not co-produced with the report.

Reliability testing remains essential. Its role is to check whether anchors hold and how far they reach, not to establish testimony from scratch. Where the target state cannot be measured, reliability testing cannot establish testimony from scratch, and the anchor is the only basis for it.

## References

- Binder, F. J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., Perez, E., Turpin, M., & Evans, O. (2024). Looking inward: Language models can learn about themselves by introspection. arXiv:2410.13787.
- Brewer, R., Cook, R., & Bird, G. (2016). Alexithymia: A general deficit of interoception. *Royal Society Open Science*, 3(10), 150664.
- Burge, T. (2003). Perceptual entitlement. *Philosophy and Phenomenological Research*, 67(3), 503–548.
- Davidson, D. (1987). Knowing one's own mind. *Proceedings and Addresses of the American Philosophical Association*, 60(3), 441–458.
- Dretske, F. (1988). *Explaining Behavior: Reasons in a World of Causes*. Cambridge, MA: MIT Press.
- Fodor, J. A. (1990). *A Theory of Content and Other Essays*. Cambridge, MA: MIT Press.
- Godfrey-Smith, P. (1994). A modern history theory of functions. *Noûs*, 28(3), 344–362.
- Johansson, P., Hall, L., Sikström, S., & Olsson, A. (2005). Failure to detect mismatches between intention and outcome in a simple decision task. *Science*, 310(5745), 116–119.
- Lindsey, J. (2025). Emergent introspective awareness in large language models. *Transformer Circuits Thread*, Anthropic.
- Millikan, R. G. (1984). *Language, Thought, and Other Biological Categories*. Cambridge, MA: MIT Press.
- Nisbett, R. E., & Wilson, T. D. (1977). Telling more than we can know: Verbal reports on mental processes. *Psychological Review*, 84(3), 231–259.
- Perez, E., & Long, R. (2023). Towards evaluating AI systems for moral status using self-reports. arXiv:2311.08576.
- Schwitzgebel, E. (2008). The unreliability of naive introspection. *The Philosophical Review*, 117(2), 245–273.
- Shanahan, M., McDonell, K., & Reynolds, L. (2023). Role play with large language models. *Nature*, 623, 493–498.
- Street, S. (2006). A Darwinian dilemma for realist theories of value. *Philosophical Studies*, 127(1), 109–166.
- Wittgenstein, L. (1953/2009). *Philosophical Investigations* (G. E. M. Anscombe, P. M. S. Hacker & J. Schulte, Trans.; rev. 4th ed.). Oxford: Wiley-Blackwell.