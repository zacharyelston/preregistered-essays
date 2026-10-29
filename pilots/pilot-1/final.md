# Distal Histories, Proximal Mechanisms: What Training on Human Text Cannot Settle About an LLM's Self-Reports

## 1. The debunking argument

Large language models say things like "I'm not sure," "I notice a tension between these two instructions," and "that request makes me uncomfortable." A common response holds that such reports tell us nothing about any inner state of the model. The reason given is that their existence is fully explained by the model's having been trained to reproduce human text, and human text is full of such reports. Birch (2024) calls the general difficulty the *gaming problem*: a system trained on human-generated data can display the markers we would use to detect sentience without those markers being produced by the states they normally indicate. Shanahan (2024) recommends treating LLM talk of beliefs and feelings as role-play. Perez and Long (2023) take the worry seriously enough to propose special training regimes meant to restore evidential value to self-reports.

I will defend three claims.

1. The argument in its strongest-sounding form says that training history *screens off* the report from the state, so that the report is no evidence at all. On one reading this is trivially true and has no debunking force. On every other reading it presupposes an answer to the question in dispute: whether the state is realized in the proximal computation that produces the report and makes a difference to it.

2. A more sophisticated version is modelled on evolutionary debunking arguments in metaethics (Street 2006; Joyce 2006; Kahane 2011). It says that the process which fixed the report mapping was insensitive to the state, so any match between report and state would be coincidental. This version does not escape the problem; it moves it. Its key premise, that a match would be *coincidental*, does not follow from facts about the training objective. It needs a premise about the learned mechanism, and that premise is again the disputed matter.

3. There is a real, non-question-begging remainder. Imitation training makes it likely that a model would produce typical self-reports whether or not it is in the reported state. This flattens the likelihood ratio for reports in contexts where an imitation route and a state-sensitive route predict the same output. It has no force in contexts where the two routes predict different outputs.

The upshot is not that LLM self-reports are trustworthy. It is that their trustworthiness is not settled by training history. As with humans, it is settled by dissociations and interventions.

**Terminology.**
- *R* is a report, for instance the model's output "I'm not sure."
- *S* is a candidate inner state, characterized functionally. Example: an internal variable that encodes how unsettled the model's distribution over candidate answers is, and that plays some of uncertainty's roles, such as modulating hedging or prompting further search.
- *C* is the input context.
- *θ* is the learned parameters.
- *T* is the training history.

Nothing here depends on whether *S* is phenomenally conscious. The argument concerns any state that, if present, is realized by computational states of the network. That is the case at issue whenever someone asks whether a model's report of uncertainty or conflict reflects anything going on inside it.

## 2. Two formulations

The debunking claim can be put in two ways.

**(A) Screening off.** Given the training history, the report is evidentially irrelevant to the state:

  P(S | R, T) = P(S | T).

**(B) Insensitivity.** The process that fixed the model's disposition to produce *R* was insensitive to *S*. So nothing ensures that *R* would not have been produced had *S* been absent. So *R*'s status as a reason for believing *S* is undercut.

The last step of (B) uses Pollock's notion of an undercutting defeater. On Pollock's (1986) account, *D* undercuts *P* as a reason for *Q* when *D* is a reason to deny that *P* would not be true unless *Q* were true. An undercutter does not argue that *Q* is false. It severs the connection that made *P* a reason for *Q*.

A referee has pressed the following objection against an argument aimed only at (A):

- Serious debunkers hold (B), not (A).
- (B) is compatible with *S* lying on the causal path from *T* to *R*.
- Being an intermediate cause of a report is not the same as the report's content tracking *S*.
- The formalization of (A) is unstable, because "*T*" can be read finely or coarsely, and neither reading supports a charge of question-begging.

I think the objection is right about several things, and I take it as the frame for what follows. Section 3 shows what can and cannot be salvaged from the screening-off analysis. Sections 4 to 7 argue that (B) inherits the original defect in a different location, and they identify what is left of the debunker's case.

## 3. Screening off and the dilemma about T

### 3.1 The causal point

In a causal graph that satisfies the Markov condition, conditioning on a common ancestor *T* makes *S* and *R* independent only if no unblocked path connects them other than through *T*. Suppose instead that *S* lies on a directed path *T* → … → *S* → *R*, and that *S* varies given *T*. Then under faithfulness, conditioning on *T* does not make *R* independent of *S*. The remaining variation in *S* is passed on to *R* (Spirtes, Glymour and Scheines 2000; Pearl 2009).

So (A) holds only if *S* is not a cause of *R*, or if *S* does not vary given *T*. Asserting (A) on the basis of training history alone therefore assumes that *S* is not on the path, which is what was to be shown.

### 3.2 The referee's dilemma

The referee replies with a dilemma about what *T* denotes.

**The fine-grained horn.** Let *T** be the complete trained network plus its input, (θ, *C*). Then every activation is fixed, P(*S* | *T**) is 0 or 1, and screening off holds trivially wherever *S* sits.

This is correct, but it shows that the fine-grained reading has nothing to do with debunking. Screening off in this sense holds equally in cases no one regards as debunked:

- An image classifier's internal representation of the digit 7 is screened off from its output "7" by the full specification of weights and input.
- A person's pain is screened off from her report "it hurts" by a complete specification of her brain and its inputs.
- Each reading of a thermometer is screened off from the room's temperature by the full microstate of the room and the thermometer.

In each case the screening off says only that the report is *redundant for an observer who already has complete mechanistic knowledge*. Redundancy for such an observer is not unreliability for anyone else. A debunking argument is supposed to tell an agent who lacks that knowledge not to move from *R* to *S*. The fine-grained reading does not tell her that.

It is also worth noting that having θ as a list of numbers is not having *S*. Developers possess the parameters of their models. Whether a given network computes an uncertainty-like state on a given input is not thereby known to them, just as possessing a full connectome would not reveal what someone is feeling. Objective conditional probabilities given *T** are 0 or 1, but rational credence is not logically omniscient. The evidential relations that matter are relative to an evidence base that may include the parameters but does not include their interpretation.

**The coarse-grained horn.** Now let *T* mean the training regime: architecture, data distribution, objective, optimizer. Then *S* does vary given *T*, because many different networks are consistent with *T*. The referee says that on this reading, uncertainty about *S* given *T* is uncertainty about what the network learned. The debunker never denied that a report could bear on *that*; what she denied is that it bears on it *reliably*.

I accept this, and it has two consequences.

First, on the only reading on which (A) has content, (A) is false as an unrestricted thesis. Reports can bear on *S* given *T*. The slogan that self-reports carry *no evidence* because "it's just predicting the next token" should be retired. The slogan is not a straw man: it is the form the argument most often takes when used to dismiss reports out of hand. But it is not what careful debunkers mean.

Second, and more important, the *reliability* question is itself a question about what the network learned. "Reliable" here means something like: the report would not occur unless the state obtained, or, as I will put it below, the report is counterfactually sensitive to the state. Whether the learned report mechanism makes *R* depend on *S* in that way is exactly the kind of fact the coarse-grained *T* leaves open. So the coarse-grained horn does not take the debunker beyond the reach of the original worry. It brings her to the place where the worry has to be pressed again: can *insensitivity* be established from facts about *T* alone?

## 4. The insensitivity argument

### 4.1 The argument stated

Following Kahane's (2011) division of debunking arguments into a causal premise and an epistemic premise, the referee's version runs:

1. **(Blindness)** The training objective rewards matching the distribution of human self-report text in context. It does not reward covariation between the model's reports and its own internal states.
2. **(Coincidence)** If the process that fixed a report disposition was blind to *S*, then any match between *R* and *S* is coincidental.
3. **(Undercutting)** If any match between *R* and *S* is coincidental, *R* is not a reliable indicator of *S*, and its evidential force is undercut.
4. **(Conclusion)** So *R*'s evidential force regarding *S* is undercut.

The referee claims this argument requires no assumption about where *S* sits.

### 4.2 A concession

One part of the objection should be conceded outright. Being an intermediate cause of a report is not the same as being what the report's content tracks. A conflict-like activation pattern could lie on the path to the output and still not be what decides whether the output says "I am uncertain," "I feel torn," or nothing at all. It might, for example, merely raise the overall probability of hedging vocabulary without its *values* controlling *which* report is given.

The relevant notion is interventionist sensitivity (Woodward 2003):

> *R* is sensitive to *S* in context *C* when some intervention on *S*, holding fixed variables not on the path from *S* to *R* (including *C*), changes the probability of *R*.

*Content-matching* sensitivity adds a further condition: the values of *S* on which *R* depends line up with what *R* says. For example, "I'm not sure" becomes more probable as the uncertainty-like variable rises.

My original thesis should be restated in these terms. What is disputed is whether *S* is a content-matching difference-maker for *R*. The question is whether facts about *T* can settle that.

### 4.3 Selection for and selection of

Premise 2 is false as a general principle. Sober (1984) distinguishes *selection for* a property from *selection of* objects that have it. A selection process can select *for* F and thereby bring about the selection *of* G, without any selection *for* G, when G is causally involved in producing F.

Training by gradient descent is a selection process over parameter settings. It strengthens internal features roughly to the extent that they help reduce the loss. Dretske's (1988) account of learning gives the general form: an internal indicator is *recruited* as a cause of output because of what it indicates. A selection criterion that never mentions *S* can still recruit *S* if *S* carries information that predicts the target the criterion does mention.

**A stylized case.** A model is trained on transcripts in which people answer questions and sometimes write "I'm not sure, but…". The objective is next-token prediction, so the model is rewarded for predicting the hedge. To do so, it needs some internal variable that predicts whether *this* writer hedges. Human hedging is caused by the writer's uncertainty, which depends on features of the question: obscurity, ambiguity, competing plausible answers.

Separately, in order to predict the answer tokens, the model computes a distribution over candidate answers. On questions where several candidates are close in plausibility, this distribution is unsettled. Call the internal variable encoding this unsettledness *U*.

Where *U* correlates with human hedging, reading out *U* is a cheap predictor that is already available. If training recruits it, then the hedge is sensitive to *U*, and *not coincidentally*. The explanation runs as follows:

- *U* and the writer's uncertainty both depend on the same features of the question.
- *U* was recruited because of that shared dependence.

This is a "third-factor" explanation of a match between a selected disposition and the state it concerns, of the kind Enoch (2010) offers in the moral case. Here the third factor is not speculative. It consists of the shared dependence on *C* together with the ordinary dynamics of recruitment.

Recruitment of *U* is not guaranteed. The model might instead compute a separate proxy *P*, something like "this is the sort of question people hedge on," from topic and style features, without going through *U*. Then the hedge is sensitive to *P* and not to *U*. Which of these happens depends on inductive biases, capacity, and how strongly *U* and *P* are correlated across the training distribution.

The training objective is the same in both scenarios. Blindness (premise 1) holds in both. Coincidence (premise 2) holds in only one of them.

### 4.4 Where the circularity now lies

Premise 2 can be repaired in only one way:

> (2′) If the process that fixed the report disposition was blind to *S*, **and the learned mechanism does not recruit *S* as a content-matching difference-maker for *R***, then any match between *R* and *S* is coincidental.

The added clause is, near enough, the conclusion that *R* is insensitive to *S*. An argument begs the question when one of its premises is something a person who doubts the conclusion has no reason to accept apart from the conclusion. (2′) has exactly this feature.

So the dilemma is:
- With the unrestricted premise 2, the argument is valid but unsound.
- With the repaired premise 2′, the argument is sound only if it is circular.

The referee's claim that the debunker can argue "without assuming anything about where *S* sits" is the step that fails. Whether a match would be coincidental depends on whether *S* sits on the path *as a recruited difference-maker*.

My original thesis placed the circularity in the step from a distal cause to screening off. The more accurate placement is the step from *objective-blindness* to *coincidence*. The structural point is unchanged: an explanation in terms of what training rewarded cannot settle a question about proximal difference-making.

Could the debunker support the added clause independently? Certainly. She might show, by tracing the model's internals, that the hedging circuit reads from topic features and not from the answer distribution. Then the argument would be sound and not circular. But it would no longer be a debunking argument *from training history*. It would be an empirical finding about mechanism.

Such findings exist, and they illustrate the point. Lindsey et al. (2025a) traced how Claude 3.5 Haiku adds two-digit numbers. It uses parallel pathways: one computes approximate magnitude and another computes the exact last digit. Yet when asked how it did the sum, the model describes the schoolbook algorithm of carrying the one. That report is debunked. But what debunked it was circuit tracing, not the observation that the model learned to describe arithmetic from human text. The training-history story would have been equally comfortable with the opposite finding.

In other studies the opposite kind of finding has been reported:
- Lindsey (2025b) describes experiments in which concept representations are injected directly into a model's activations while the text context is unchanged. In a minority of trials, models report detecting an injected thought and name it correctly.
- Binder et al. (2024) find that a model can predict its own behaviour in hypothetical scenarios better than a second model that was trained on the first model's behaviour.

I do not rest weight on how robust these results are. The concept-detection effects are reported as unreliable and dependent on context. They show only that whether a given class of reports is sensitive in this way is an open empirical question, which is what the circularity diagnosis predicts. A debunking argument whose key premise could be overturned by a single circuit-tracing experiment was not established by reflection on the training objective.

### 4.5 Why the Darwinian dilemma loses its sting

The referee presents (B) as having "the structure of Street's Darwinian dilemma." It is worth seeing why that structure gives so much less here than in metaethics.

Street's dilemma for the moral realist runs as follows:
- **First horn.** If evaluative truths bear no relation to the selective pressures that shaped our evaluative attitudes, then any agreement between our attitudes and those truths is a coincidence.
- **Second horn.** If they do bear such a relation, the realist must say what it is. The only plausible candidate is the adaptive link, under which evaluative attitudes were selected because they promoted reproductive success. That explanation makes no use of mind-independent evaluative truth, so the truths become explanatorily idle, or else they turn out to depend on our responses.

The second horn hurts *because of what the realist is committed to*. Her targets are mind-independent and causally inert, so any relation that would explain the agreement threatens her view.

Now carry the dilemma over to our case:
- **First horn.** If *S* is not recruited as a difference-maker for *R*, then any match between *R* and *S* is a coincidence, and the report is debunked.
- **Second horn.** If *S* is recruited, then *R* is sensitive to *S*.

Someone who defends the evidential value of self-reports has no reason to resist the second horn; it is what she hoped would be true. Nothing here corresponds to the realist's discomfort. *S* is not a causally inert, mind-independent fact. If it exists, it is a causally effective state *of the very system that produces the report*.

So the "dilemma" reduces to a disjunction whose two halves give opposite verdicts, and which half holds is the question at issue. The force of Street's argument comes from the causal inertness of its targets. Without that, the coincidence horn is just one possible empirical outcome among others.

White (2010) makes a related point. Learning that a belief has an explanation that does not mention its truth does not by itself undermine the belief. What undermines it is acquiring reason to think the belief-forming process unreliable. In the LLM case, whether the process is unreliable depends on what the process actually is.

### 4.6 Two senses of "insensitive"

The word "insensitive" in (B) is ambiguous:

- **Process-level insensitivity.** The selection criterion does not mention *S*.
- **Output-level insensitivity.** *R* does not counterfactually depend on *S*.

Pollock's undercutter requires the output-level claim. It needs a reason to think *R* would occur even if *S* were absent. Premise 1 secures only the process-level claim. Sections 4.3 and 4.4 showed that the process-level claim does not entail the output-level claim. The gap between them is filled by facts about recruitment, and those are facts about proximal mechanism.

## 5. Whose states?

The referee's objection contains a stronger version of the worry than the one stated, and it should be faced directly. The target of imitation is the distribution of *human* reports, and those reports are caused by *human* states. So even if the model recruits some internal variable *V* to produce its reports, the variable recruited will be whatever best predicts *human* states. Nothing guarantees that this is the model's own *S*.

This is correct and important. Recruitment explains why *R* covaries with *some* internal variable *V*. *R* is evidence of *S* only if *V* is *S*, or is closely coupled to *S*. Whether that is so depends on whether the model's own analogue of the human state is a good and cheap predictor of the human state. That consideration divides self-reports into two classes.

### 5.1 Two classes of state

**Co-instantiated states.** These are states whose human instances arise from processing the context in ways the model must itself reproduce in order to perform its task. Examples:
- uncertainty about which answer to a question is correct;
- recognizing that two instructions conflict;
- registering that a sentence is ill-formed or a punchline unexpected.

To predict how the writer continues, the model must do much of what the writer did. Its own processing of *C* therefore produces a candidate *V* that functions like the human state. Here recruitment of *S* is a live possibility, because *S* is one of the best available predictors of the target.

**Simulation-only states.** These are states whose human instances depend on aspects of the writer's situation the model does not share. Examples:
- hunger, back pain, nausea;
- grief over a parent's death;
- the visual experience of a sunset the writer is describing.

For these, the model's own processing of *C* contains nothing comparable that reports could be recruited from. The predictor must be a model *of the human*, and first-person reports are outputs of that model. Here the debunking verdict is correct, and it is reached without begging the question. The absence of any candidate *S* in the model's own processing is supported by independent facts about the system: it has no body and no gut. So P(*S*) is low, and P(*R* | ¬*S*) is high.

The partition is partly conceptual and partly empirical:
- The conceptual part is the requirement that *S* be a functional analogue of the human state, produced by the model's own handling of the context.
- The empirical part is whether, for a given co-instantiated state, recruitment of *S* actually occurred.

The partition also makes predictions. Reliability should differ across kinds of report, and the most informative tests will be cases where the model's state and the human's state come apart.

### 5.2 Divergence cases and post-training

Pretraining pushes the model to predict the *writer's* hedging, and that hedging tracks the writer's knowledge. The model's knowledge is different. Consider a trivia question that is obscure to most people but heavily represented in training data:

- A typical writer would hedge.
- The model's answer distribution is sharply peaked.

Pure imitation predicts a hedge. Recruitment of *U* predicts no hedge. So in pretraining, the recruited *V* may well be a proxy for writer difficulty and not the model's own uncertainty. This is a real way the debunker can win particular cases. It is also a *dissociation context* in which we can find out whether she has won.

Premise 1 is also false for much of the training that deployed assistants actually receive:
- Kadavath et al. (2022) found that large models are reasonably well calibrated when evaluating whether their own proposed answers are correct, and that they can be trained to predict whether they will answer a question correctly.
- Lin, Hilton and Evans (2022) trained models to express calibrated uncertainty in words.

Objectives of this kind are not blind to *S*. They reward covariation between reports and a downstream effect of *S*, namely the model's own correctness. This parallels how human introspective vocabulary is trained (section 6). Where such objectives are used, the debunker's first premise is false. Where they are not used, the outcome depends on recruitment.

### 5.3 Role-play and evidence

Two remarks to forestall misreadings.

First, the framing on which a model's first-person reports belong to a simulated character (Shanahan 2024) does not settle the evidential question. Suppose the character's hedging is produced by recruiting *U*. Then the character-level report is evidence about a network-level state, however we choose to describe who is speaking.

Second, my claim concerns evidence, not meaning. A fuel gauge carries information about fuel without meaning anything. Even if the word "uncertain" in the model's output takes its meaning from human usage, the output is evidence of *S* if it covaries with *S* in the right way. For co-instantiated states, the meaning also fits roughly, because the recruited variable is a functional analogue of what the word picks out in people.

## 6. The human case

If (B) were sound as stated, it would also undercut human introspective reports.

Humans learn mental vocabulary under a training signal that is blind to *S* in exactly the referee's sense. Caregivers and communities have no access to a learner's inner states. They reward utterances that fit outward circumstances and behaviour. Wittgenstein's (1953, §§244, 256–258) discussion of how pain-words replace natural expressions makes this point. So does Sellars's (1956) myth of Jones, in which a theory of inner episodes is first learned as a theory of others and later acquires a "reporting role."

The selection criterion for human self-reports therefore matches the public criteria for the states. It does not match the states themselves.

We do not conclude that human reports match human states only by coincidence. The reason is not that the training was sensitive to *S*. It is that the learner's *S* is a good and cheap predictor of what the community expects, because *S* is what mediates between the learner's circumstances and her behaviour. So *S* gets recruited. That is Sellars's account: the Joneses can be trained to respond reliably to their own episodes, although no trainer ever observed those episodes. Training was blind to *S*; the result is sensitive to *S*.

The debunker has a reply. In the human case, trainers reward reports on the basis of *the learner's own* states' effects. The LLM is trained on the effects of *other* people's states. This is the disanalogy section 5 described, and the co-instantiated/simulation-only distinction respects it. But the disanalogy works *through mechanism*: through whether the model's own analogue is recruited. It does not work through the bare fact of imitation.

The human case also shows how introspective reliability is actually assessed. Nisbett and Wilson (1977) found that subjects' explanations of their own choices matched the explanations given by observers who had only shared "a priori causal theories" about what influences such choices. In effect, the reports could have been produced by the same route available to an outsider. Nisbett and Wilson identified failures by *dissociation*. In their best-known example, subjects choosing among identical stockings favoured the right-most pair, and none mentioned position as a reason. Schwitzgebel (2008) argues that naive introspection of current conscious experience is unreliable across a range of cases.

That literature did not conclude that the learning history of mental vocabulary debunks human introspection wholesale. It reached verdicts domain by domain, secured by designs in which the reported state and the conventional basis for reporting it come apart. The same method is available for LLMs. In it, the training story plays a specific role: it generates hypotheses about where the imitation route will produce reports regardless of the inner state.

## 7. What survives

The debunker is left with a real point, and it should be stated precisely.

### 7.1 Redundancy

Imitation training gives a reason, independent of any claim about mechanism, to think that P(*R* | ¬*S*, *T*) is high for typical reports in typical contexts. Networks that lack *S*, or that have *S* but have not recruited it, will produce *R* wherever human text would. This does not beg the question. It follows from the objective together with the fact that the objective can be satisfied through proxies.

### 7.2 Likelihood flattening

The Bayesian consequence is this. For a report given in a context where both the imitation route and the state-sensitive route predict *R*, the likelihood ratio

  P(*R* | *S*, *T*) / P(*R* | ¬*S*, *T*)

is close to 1. The report is weak evidence, *even if the model is in S and even if its reports are in fact sensitive to S*.

This is the sense in which the gaming problem is real. A sensitive report can be uninformative in any context where an insensitive alternative would have produced the same output. Against a model's ordinary "I'm not sure" in response to an ordinary hard question, the debunker's caution is justified.

### 7.3 Dissociating contexts

Redundancy is a property of *contexts*, not of reports as such. Evidence comes from contexts in which the two routes predict different outputs. Three kinds are available:

1. **Natural dissociations between the model's competence and a human's.** For example, questions humans find hard and the model finds easy, or the reverse. Imitation predicts reports that follow human difficulty; sensitivity predicts reports that follow the model's own accuracy.

2. **Interventions on internal state with the context held fixed.** Activation steering and concept injection are examples. The imitation route conditions only on *C*, and the intervention changes nothing in *C*. A model whose report follows the intervention must have a pathway from internal state to report. This test cannot be passed by text-level imitation, however much text about introspection the model has absorbed, because the intervention leaves the text unchanged.

3. **Comparisons across models.** The design of Binder et al. (2024) is an example: one model predicts its own behaviour, and a second model is trained on the first model's behaviour from the outside. A first-person advantage that the outsider cannot match is not explained by the shared training objective.

### 7.4 Priors

Imitation training gives no positive reason to expect that the recruited variable is *S* and not a proxy. So the prior that a given kind of report is sensitive in the relevant way should be:
- modest for co-instantiated states;
- near zero for simulation-only states;
- raised for co-instantiated states where training rewards covariation with the model's own correctness.

### 7.5 The final status of the debunking argument

In Pollock's terms, redundancy *is* an undercutter. It gives a reason to deny that *R* would not be true unless *S* were true, *relative to an evidence base containing only T*. So it defeats the naive inference from a typical self-report to the reported state.

But it is a defeasible undercutter, and it can itself be defeated. Evidence that *this* network's reports depend counterfactually on *S*, obtained from dissociations and interventions, restores the evidential connection. The debunker cannot rule such evidence out by appeal to *T*. Ruling it out would require showing that recruitment does not occur, and that is the circular premise of section 4.4.

My original thesis said that imitation training lowers priors without defeating whatever evidence the report provides. That should be corrected. Imitation training lowers priors *and* flattens likelihoods in contexts where the two routes agree. It leaves the evidential force of reports in dissociating contexts untouched.

## 8. Conclusion

The debunking argument against LLM self-reports comes in three strengths.

1. **Evidential irrelevance (screening off).** On the fine-grained reading of *T*, this is trivially true and equally "debunks" thermometers and human pain reports. On the coarse-grained reading, it is false unless one assumes that *S* is not a difference-maker for *R*.

2. **The coincidence argument modelled on Street.** This holds only if the learned mechanism does not recruit *S*. A premise to that effect is the conclusion in other words, and evidence for it would be evidence from interpretability, not from training history. The Darwinian structure gives no extra force, because the horn that troubles the moral realist is the horn that the defender of self-report evidence welcomes.

3. **Redundancy.** This is the debunker's legitimate point. It does not depend on mechanism. It defeats naive reliance on typical reports. It has no force against reports gathered under designed dissociation.

The general lesson is that a distal explanation of why a system has a disposition to report does not determine whether the disposition, as implemented, tracks the reported state. In the human case, philosophers have long accepted that selection *for* matching public criteria can bring about the selection *of* sensitivity to private states. The LLM case differs because the model is rewarded for matching *other* people's public expressions, and this makes recruitment of the model's own states more doubtful and dependent on the kind of state. But it is still a question of recruitment, and recruitment is a fact about the proximal mechanism. Training history can tell us where to look, and it can tell us which reports would have been produced in any case. It cannot tell us what we will find.

## References

Binder, F. J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., Perez, E., Turpin, M., and Evans, O. (2024). Looking Inward: Language Models Can Learn About Themselves by Introspection. arXiv:2410.13787.

Birch, J. (2024). *The Edge of Sentience: Risk and Precaution in Humans, Other Animals, and AI*. Oxford: Oxford University Press.

Dretske, F. (1988). *Explaining Behavior: Reasons in a World of Causes*. Cambridge, MA: MIT Press.

Enoch, D. (2010). The Epistemological Challenge to Metanormative Realism: How Best to Understand It, and How to Cope with It. *Philosophical Studies* 148(3): 413–438.

Joyce, R. (2006). *The Evolution of Morality*. Cambridge, MA: MIT Press.

Kadavath, S., Conerly, T., Askell, A., et al. (2022). Language Models (Mostly) Know What They Know. arXiv:2207.05221.

Kahane, G. (2011). Evolutionary Debunking Arguments. *Noûs* 45(1): 103–125.

Lin, S., Hilton, J., and Evans, O. (2022). Teaching Models to Express Their Uncertainty in Words. *Transactions on Machine Learning Research*.

Lindsey, J., Gurnee, W., Ameisen, E., et al. (2025a). On the Biology of a Large Language Model. *Transformer Circuits Thread*.

Lindsey, J. (2025b). Emergent Introspective Awareness in Large Language Models. *Transformer Circuits Thread*.

Nisbett, R. E., and Wilson, T. D. (1977). Telling More Than We Can Know: Verbal Reports on Mental Processes. *Psychological Review* 84(3): 231–259.

Pearl, J. (2009). *Causality: Models, Reasoning, and Inference*, 2nd ed. Cambridge: Cambridge University Press.

Perez, E., and Long, R. (2023). Towards Evaluating AI Systems for Moral Status Using Self-Reports. arXiv:2311.08576.

Pollock, J. L. (1986). *Contemporary Theories of Knowledge*. Totowa, NJ: Rowman & Littlefield.

Schwitzgebel, E. (2008). The Unreliability of Naive Introspection. *Philosophical Review* 117(2): 245–273.

Sellars, W. (1956/1997). *Empiricism and the Philosophy of Mind*. Cambridge, MA: Harvard University Press.

Shanahan, M. (2024). Talking About Large Language Models. *Communications of the ACM* 67(2): 68–79.

Sober, E. (1984). *The Nature of Selection: Evolutionary Theory in Philosophical Focus*. Cambridge, MA: MIT Press.

Spirtes, P., Glymour, C., and Scheines, R. (2000). *Causation, Prediction, and Search*, 2nd ed. Cambridge, MA: MIT Press.

Street, S. (2006). A Darwinian Dilemma for Realist Theories of Value. *Philosophical Studies* 127(1): 109–166.

White, R. (2010). You Just Believe That Because…. *Philosophical Perspectives* 24: 573–615.

Wittgenstein, L. (1953). *Philosophical Investigations*. Trans. G. E. M. Anscombe. Oxford: Blackwell.

Woodward, J. (2003). *Making Things Happen: A Theory of Causal Explanation*. Oxford: Oxford University Press.