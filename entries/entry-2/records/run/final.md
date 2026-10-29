# Two Objects of Evaluation: Selection, Scope, and the Prediction/Accommodation Dispute

## 1. The problem and the proposal

Predictivism is the claim that evidence a hypothesis predicted supports it more than evidence the hypothesis was built or chosen to fit. Bayesians typically deny this (Howson and Urbach 2006). On their view the posterior P(H | e) is fixed by the prior of H and the likelihoods of e under H and its rivals. The history of how H came to be entertained is irrelevant except where it changes those quantities.

Error statisticians affirm predictivism, at least for an important class of cases (Mayo 1996, 2018). If a hypothesis is hunted out of a large space because it fits, then the procedure that produced the fit would have produced some fit or other whether or not the output was true. A passing result from such a procedure therefore has little probative force.

Particle physicists build the second view into practice. The look-elsewhere effect requires that a bump found by scanning a mass range be assessed by a *global* significance. The global significance is smaller than the *local* significance, which is computed as if the mass had been fixed in advance (Gross and Vitells 2010).

My proposal concerns *selection* cases, where a search S picks a hypothesis from a space Ω because of its fit to data e. In such cases there are two objects of evaluation. The first is the selected hypothesis H, picked out rigidly. The second is the proposition that *whatever S returns is true*. The thesis has three parts.

**(T1) De re invariance.** The confirmation e provides for H does not depend on whether H was selected by S or proposed in advance, holding fixed the agent's credences over Ω.

**(T2) De dicto discount.** The confirmation e provides for the proposition that S's output is true is smaller, by a factor I call the *reach* of the search.

**(T3) Allocation.** The Bayesian denial of predictivism is correct about the object in (T1). The error-statistical affirmation, including the physicists' global significance, is correct about the object in (T2). Scientific acceptance, reporting and reliance usually concern the second object.

A referee raised an objection that I take to be the strongest available. Its first part is correct, and I grant it in full: once the agent conditions on total evidence, the de re and de dicto propositions have the same posterior. My original formulation put the discount in the posterior of the de dicto proposition, and that was a mistake.

The discount lives in *confirmation*, the relation between evidence and the change it makes to a proposition's credibility. Two propositions with the same posterior and different priors are differently confirmed. I will also show that the referee's recommended move, conditioning on the fact that S returned H, is exactly the operation that produces the de dicto quantity.

The plan is as follows. Section 2 sets up the apparatus and Section 3 states the objection. Sections 4–8 answer its three parts. Section 9 marks the limits of the view.

## 2. Setup

Let Ω = {H₁, …, Hₙ} be mutually exclusive hypotheses. They need not be exhaustive: there may be a residual possibility H₀, such as "no signal." Let E be the random data, with values e. A search S is a function, known to the agent, from data values to members of Ω. In the actual case the data are e and S(e) = H. Two propositions are relevant.

- **The de re object** is H itself. Its truth at a world does not depend on what data arrive there.
- **The de dicto object** is σ, the proposition that the hypothesis S returns on the data is true. As a set of worlds, σ is the union over i of the propositions [S(E) = Hᵢ ∧ Hᵢ]. At worlds with different data, the truth of σ turns on a different hypothesis.

The contrast is the familiar one between "Smith is from Boston" and "the winner of the lottery is from Boston," evaluated when Smith in fact won.

A third proposition does much of the work below:

- **A** = [S(E) = H], the proposition that the search selects H. The actual data entail A.

I measure confirmation by the Bayes factor, the ratio of posterior to prior odds: B(X, e) = O(X | e) / O(X). I write B(X, e | Y) for the same ratio computed relative to background that includes Y. Section 4.3 notes that the direction of every result carries over to the difference and ratio measures (Fitelson 1999).

## 3. The objection

I state the objection at full strength, in three parts.

**(O1) Total evidence.** After the search, the agent knows e and knows that S returned H on e. Given that knowledge, "S's output is true" and "H is true" are equivalent, so P(σ | e) = P(H | e).

The discount I attributed to σ came from averaging over the hypotheses S *could* have returned. That average ranges over counterfactual data and counterfactual outputs. It is therefore a pre-data reliability of the procedure, not a credence given e. What I called a scope distinction is the familiar contrast between a conditional probability and an unconditional error rate. That contrast is the Bayesian/error-statistical dispute itself, restated rather than dissolved.

**(O2) The look-elsewhere effect.** In Bayesian treatments of mass scans, the trials factor reappears as dilution of the prior over the search window, an Occam factor in the Bayes factor. That penalty attaches to "there is a resonance at m₀," which is the rigid, de re hypothesis. This gives a dilemma:

- Either the reach of the search is already in the de re prior, so the de re posterior is penalized and (T1) is false.
- Or the global p-value is a frequentist property of the procedure with no credal counterpart.

Either way, the local/global contrast is not the de re/de dicto contrast.

**(O3) Misattribution.** Mayo's severity claim is that H itself, de re, has passed a test of low probative capacity. Telling her she is right about a different proposition assigns her a view she rejects.

## 4. Posteriors coincide; confirmations do not

### 4.1 The coincidence, granted

**Proposition 1.** P(σ | e) = P(H | e).

*Proof.* The data e entail A. The conjunction of A with σ is equivalent to the conjunction of A with H. Hence σ ∧ e is equivalent to H ∧ e, and the conditional probabilities are equal. ∎

This is (O1)'s first claim. I accept it, and it follows that no coherent agent with the evidence e can have different credences in the two objects. Any version of the thesis that relies on such a difference fails.

### 4.2 Where the discount actually lives

Predictivism, in the Bayesian and error-statistical debates alike, is a claim about *support*: how much e counts in favour of a hypothesis, not how probable the hypothesis ends up. Carnap distinguished confirmation as firmness from confirmation as increase in firmness (Carnap 1962). The prediction/accommodation debate concerns the second.

Proposition 1 fixes the posteriors but says nothing about the priors, and the priors of H and σ differ. From Proposition 1 it follows at once that

  B(σ, e) = B(H, e) / ρ, where ρ = O(σ) / O(H).

I call ρ the **reach factor**. In searches over large spaces it is typically much greater than 1, for the following reasons.

- Because the agent did not know where to look, her credence in any particular Hᵢ is spread thin, with O(H) of order 1/n.
- Her credence that the search's output, whatever it turns out to be, is true equals her expectation of the search's success, which does not shrink like 1/n.

A search that scans a thousand cells with reasonable power has a reach factor in the hundreds.

My original sketch said that the de dicto *posterior* is discounted because it averages over what S could have returned. The averaging is real, but it belongs to the de dicto *prior*:

  P(σ) = Σᵢ P(S(E) = Hᵢ ∧ Hᵢ).

Since the posteriors coincide, a larger prior means less confirmation. The corrected thesis holds that e confirms σ less than it confirms H while leaving them equally probable.

### 4.3 Measure-robustness and direction

With the posterior fixed, a proposition with a higher prior is less confirmed on the difference measure, the ratio measure and the likelihood-ratio measure alike. When ρ > 1, (T2) is therefore not an artefact of choosing the Bayes factor.

The account also predicts when the asymmetry reverses. Suppose a weak search happens to select a hypothesis that was antecedently more credible than the search's expected success. Then ρ < 1, and e confirms the de dicto proposition *more* than the de re one.

The predictivist asymmetry is therefore not a law about accommodation as such. It concerns the ratio between two quantities: the antecedent credibility of a method's output, and the antecedent credibility of what the method happened to output. In searches over large, undifferentiated spaces, the cases that motivate predictivism, that ratio is large.

### 4.4 The selection decomposition

(O1) has a second claim: the discounted quantity is a pre-data error rate, not a post-data quantity. To answer it I show that the de dicto confirmation equals a post-data quantity concerning H alone. That quantity is the confirmation e gives H *relative to background that already includes A*.

**Proposition 2.** Suppose two symmetry conditions hold:

- (i) the agent's joint credence over hypotheses and data is invariant under any relabelling of the indices of Ω applied jointly to hypotheses and data, so that she distinguishes candidates only through the data bearing on them;
- (ii) S is equivariant, so that relabelling the data relabels the output.

Then P(A) = 1/n, P(H | A) = P(σ), and P(σ | A) = P(σ). Consequently

  B(H, e) = B(H, A) · B(H, e | A), with B(H, A) = ρ and B(H, e | A) = B(σ, e).

*Proof.* By symmetry each Hᵢ is selected with equal probability, so P(A) = 1/n. Again by symmetry, each term in the sum defining P(σ) is equal, so P(H ∧ A) = P(σ)/n and hence P(H | A) = P(σ). Since σ ∧ A is equivalent to H ∧ A, the same argument gives P(σ | A) = P(σ).

The factorization is the chain rule for odds ratios together with the fact that e entails A. Because O(H | A) = O(σ), the second factor equals O(H | e)/O(σ). By Proposition 1 this is O(σ | e)/O(σ) = B(σ, e). ∎

Proposition 2 splits the de re confirmation of H into two factors:

- **(a)** the confirmation H receives from the bare fact that the search selected it;
- **(b)** the confirmation H receives from the rest of the evidence, given that fact.

The de dicto confirmation is exactly (b). The reach factor ρ is exactly (a).

This gives precise content to the old intuition that evidence used to construct a hypothesis cannot also count as independent support for it (Worrall 2014). The use is A, and the independent support is (b). It also shows what each side gets right.

- The Bayesian is right that (a) is genuine confirmation of H: learning that the maximum excess fell in H's cell is evidence for H.
- The predictivist is right that (a) is no evidence that *the search got it right*. The search was certain to select something. Under symmetry, the identity of what it selected is irrelevant to whether its selection is correct (P(σ | A) = P(σ)).

Proposition 2 also turns (O1) around. The referee asks us to suppose that the agent knows A. Take that seriously and put A into the background. Relative to that background, e's confirmation of H is B(H, e | A), which is the de dicto value.

The posterior is the same whether A is counted as evidence or as background, as it must be. The *support* differs, and the question predictivism asks concerns support. An agent who "already knows that S returned H" and then asks how strongly the data back H is asking for confirmation relative to background including A, and the answer is discounted. The referee's conditioning move does not erase the scope distinction; it produces the de dicto side of it.

Where symmetry fails, the chain rule still holds, and B(H, e | A) = B(σ, e | A), since σ and H are equivalent given A. A may then carry information about σ. For instance, if S lands on a hypothesis the agent already favoured, that bears on whether the search is working.

In such cases I take the conditional quantity B(H, e | A) as the general explicans of "support beyond selection." The unconditional B(σ, e) is its special case under symmetry. The symmetric case is the paradigm because uniform priors over a scan window and equivariant algorithms are standard.

### 4.5 Why this is not the dispute restated

The referee's diagnosis is that I have relabelled the contrast between a conditional credence and an unconditional error rate. Three features of the account show otherwise.

First, P(σ) is a *credence*: the agent's prior predictive expectation of the search's success, computed under her own mixture over hypotheses rather than under a fixed null. Bayesians compute such quantities routinely in preposterior analysis and prior predictive checking (Box 1980). Every confirmation measure needs some prior in its denominator; P(σ) is simply the prior of a different proposition.

Second, the discounted quantity B(H, e | A) is a post-data conditional confirmation of H. It mentions no counterfactual outputs except through the probability of A, which is a datum.

Third, the place where the procedure enters is exactly specified, and it does not violate the likelihood principle. Since e entails A,

  B(H, e | A) = LR(e) / LR(A), where LR(A) = P(A | H) / P(A | ¬H).

The total import of e for H is LR(e), which does not depend on the procedure. This is the Bayesian's point, and the account leaves it intact. What the procedure determines is which data values make up A. It therefore determines how that fixed total divides between "being selected" and "beyond selection."

The genuine dispute between the two schools is whether the *total* evidential import of e depends on the procedure. I side with the Bayesian on that. My claim is that the *partition* depends on the procedure, and that the error statistician's verdicts concern the second part of the partition. Neither school has made that claim, and it is consistent with the likelihood principle.

## 5. A worked case

Consider a scan for a narrow resonance across a mass window divided into n = 1000 resolution cells. The setup is:

- The agent's prior that some resonance lies in the window is 0.5, with location uniform, so P(Hᵢ) = 0.0005 for each "resonance in cell i."
- S returns the cell with the largest local excess.
- Under the agent's prior predictive, if a resonance exists S finds its cell with probability 0.6, so P(σ) = 0.3.
- The prior and the algorithm satisfy the symmetry conditions.
- The data place the largest excess in cell k, large enough that P(H_k | e) = 0.8.

The quantities then come out as follows.

| Quantity | Value |
|---|---|
| Prior odds O(H_k) | ≈ 0.0005 |
| Prior odds O(σ) | ≈ 0.43 |
| Reach factor ρ | ≈ 857 |
| Posterior odds O(H_k \| e) = O(σ \| e) | 4 |
| De re Bayes factor B(H_k, e) | ≈ 8000 |
| De dicto Bayes factor B(σ, e) | ≈ 9.3 |
| P(H_k \| A) | 0.3 |

Every figure uses the agent's priors in full. The low base rate of a resonance in any given cell is what makes O(H_k) small. The posterior of 0.8 is a stipulated outcome of strong data, not an inference that bypasses that base rate.

By Proposition 2, learning only that the maximum fell in cell k raises the credence in a resonance there from 1 in 2000 to 3 in 10. Of the total factor of 8000, about 860 is earned by k's being where the search's maximum fell, which was bound to be true of some cell. Only about 9 is support for the proposition that the search found something real.

Now take the counterfactual in (T1). Suppose a theorist with no special information, say one who chose cell k by lottery, had announced k before the data. Her announcement carries no information, so the agent's prior for H_k is still 0.0005, and B(H_k, e) is still 8000. That is (T1).

In this scenario the natural de dicto object is "the theorist's announced cell contains a resonance," and the theorist's procedure does not depend on the data. Across all worlds that proposition is equivalent to H_k, so ρ = 1 and the de dicto confirmation is also 8000. The two scenarios therefore agree de re and disagree de dicto, and the disagreement has a simple source:

- "The bump fell in the theorist's cell" was improbable unless the theorist was right: P(A | σ_T false) ≈ 1/1000, where σ_T is the theorist-indexed proposition.
- "The bump fell in the search's cell" was certain either way.

If we summarize e by the maximal local significance Z, the same structure appears in sampling terms:

- The de re likelihood under falsity, P(Z_k ≥ z | ¬H_k), is approximately the **local** p-value.
- The de dicto likelihood under falsity, P(Z_max ≥ z | ¬σ), is approximately the **global** p-value. It equals the global p-value exactly when no resonance exists, and nearly so otherwise.

The slogan "it would have looked this good anyway" is ambiguous in scope.

- It is false of H_k: had there been no resonance in cell k, cell k would very probably not have shown this excess.
- It is true of σ: had the search's output been spurious, some cell would very probably still have shown an excess this large.

## 6. The look-elsewhere dilemma answered

**First horn.** (O2) says that if the search's reach is already in the de re prior, the de re posterior is penalized and (T1) is contradicted. The de re *prior* is indeed diluted, in the example to 1 in 2000. But (T1) concerns the Bayes factor.

In any case, the dilution is not a penalty *for searching*. It represents the ignorance that made a search necessary. The lottery-theorist scenario has the same dilution, the same Bayes factor and the same posterior. (T1) compares searching with advance proposal *at fixed credences over Ω*, and on that comparison nothing changes.

Sometimes advance proposal would have raised the prior, as when a theorist derives the predicted mass from an electroweak fit. Then the posterior is higher. That difference comes from the theorist's reasons, not from how the data bear on H. It is an evidential difference about H's antecedent credibility. It falls under the familiar Bayesian treatment of predictivism (Maher 1988; White 2003), which Section 9 sets aside.

**Second horn.** (O2) says that otherwise the global p-value has no credal counterpart. It has one: the sampling-theoretic analogue of the denominator of the de dicto likelihood ratio, as Section 5 showed. The Bayesian Occam factor that the referee cites makes the same point from the Bayesian side, once we are careful about *which* hypothesis's Bayes factor carries it.

The standard calculation (see Cousins 2017) compares a composite alternative, "there is a resonance somewhere in the window, mass unknown," with background-only. Take a uniform mass prior over a window of width Δm and mass resolution δm. Then this Bayes factor is approximately the maximized likelihood ratio multiplied by an Occam factor of order δm/Δm.

The rigid point hypothesis "there is a resonance at m₀" is different. Against background-only, its Bayes factor is approximately the *local* likelihood ratio, with no Occam factor. For that hypothesis the dilution sits in the prior, not in the Bayes factor. The Occam penalty therefore attaches to the Bayes factor of the *existential* hypothesis, not to that of the rigid one.

The existential hypothesis behaves almost exactly like σ:

- Once the data localize the excess, P(∃ | e) ≈ P(H_k | e) = P(σ | e).
- Antecedently, P(σ) = P(∃) × (the search's power).

So B(∃, e) and B(σ, e) differ only by a factor reflecting the search's power. That factor is of order 1, whereas the factor separating either of them from the rigid Bayes factor is of order n. In the example:

| Hypothesis | Bayes factor |
|---|---|
| Rigid point hypothesis H_k | ≈ 8000 |
| Existential hypothesis ∃ | ≈ 4 |
| De dicto proposition σ | ≈ 9.3 |

The Occam factor separating the rigid from the existential Bayes factor is about 1/2000. The reach factor separating the rigid from the de dicto one is about 1/857. The residual factor of 2.3 is the price of 60% power.

The Bayesian "reappearance of the trials factor" is therefore the de re/de dicto distinction expressed in Bayesian terms. The penalty sits in two places:

- in the Bayes factor of the description-level proposition, which is existential and outcome-indexed;
- in the prior of the rigid proposition.

Scott and Berger's (2010) analysis of Bayesian multiplicity adjustment points the same way. Multiplicity enters through the prior over which, and how many, effects are real, not through the likelihood of any fixed configuration. (T1) and (T2) are the two sides of that bookkeeping.

I do not claim that the frequentist trials factor and the Bayesian Occam factor are numerically equal. The frequentist factor depends on the significance threshold through the expected number of upcrossings (Gross and Vitells 2010). The Bayesian one depends on the ratio of resolution to window width. The claim is structural: both discount the same object, the proposition that the search's find is real, and neither discounts the support for the rigid hypothesis.

## 7. Why acceptance, reporting and reliance take the de dicto object

If the posteriors coincide, why does it matter which object is endorsed? It matters because science transmits *support* and not posteriors. An experimental collaboration does not tell readers how probable a resonance is. It reports a strength of evidence, which readers combine with their own priors. The combination is correct only if the reported support and the reader's prior concern the same proposition.

**The double-counting argument.** A typical reader first learns of H through the report. The reader had no credence about cell k as such, and would never have considered it had the search not selected it. The prior the reader brings is a base rate for propositions of the form "the result this kind of analysis turns up is real." That is a prior for σ. By Proposition 2, under symmetry it equals P(H | A). Such a reader has in effect already conditioned on A, simply by evaluating the hypothesis that the report presents.

Suppose the analysts report the de re Bayes factor, which includes A's contribution of ρ. Then the reader counts A twice: once in forming a prior about "the reported finding," and again in the support figure. In the example this would yield posterior odds of 0.43 × 8000 ≈ 3400 instead of 4.

The support figure that combines correctly with a σ-prior is B(σ, e), and the global significance is its frequentist counterpart. That is why the discount belongs in what gets reported. The discount is correct for this reason, not because the local figure misdescribes the bearing of e on H.

The same argument explains when the local figure is the right one to report. A reader who had an independent prior for the specific mass, because a theory predicted it, holds a de re prior and needs the de re support. The major collaborations reported both local and global significances in the 2012 Higgs announcements. On this account, that dual reporting is not an uneasy compromise. It serves readers whose priors attach to different objects.

**Reliance and policy.** Institutional rules have the form "act on outputs of procedure P when statistic T exceeds threshold c." Whether such a rule is a good one depends on how often the outputs it licenses are true, weighted by the stakes. That is a property of σ-type propositions, conditional on the statistic. It holds whether the rule is assessed by error rates or by Bayesian expected utility. What a policy endorses is the method's verdict, whatever the verdict turns out to be, which is the de dicto object by construction.

**Replication.** The account also explains why fresh data cure selection effects without any change in the support e gave to H. A replication tests the already-identified H on new data e′, with no search over e′. For e′, the selection step plays no role, ρ = 1, and the de re and de dicto confirmations coincide.

Once replicated, H detaches from its description. It no longer needs to be evaluated as "the search's output," because there is evidence for it that the search did not use. This is why replication is decisive in practice even though, de re, the original data were already strong support.

Not all acceptance is de dicto. A theorist who takes up H, works out its consequences and assesses its coherence with other physics is evaluating H itself. For her project, the de re support is the right measure of what e contributes. The claim is about the default: in the speech acts and institutional commitments through which findings are transmitted and relied on, the object is the method's verdict.

## 8. The error statistician's own computations

(O3) says that Mayo's severity verdict concerns H itself, so my allocation assigns her a view she rejects. I agree that she would reject the gloss. My claim is that her central counterfactual is true only under the de dicto reading. I also claim that her own requirement in hunting cases is that the de dicto reading be used.

The severity requirement (Mayo and Spanos 2006) says that data x₀ are good evidence for H to the extent that H passes a severe test. That requires two conditions:

- (i) x₀ agrees with H;
- (ii) with very high probability, the test would have produced a result according less well with H than x₀ does, were H false.

In a hunting procedure, "H" inside the counterfactual of (ii) has two readings.

- **Rigid reading.** Were H_k false, would the test very probably have produced a worse fit *to H_k*? In the example, yes. Without a resonance in cell k, cell k would almost never show a 5σ excess. The relevant error probability is the local p-value, and severity is high.
- **Descriptive reading.** Were the hypothesis the procedure outputs false, would the procedure very probably have produced a worse fit *to its output*? No. It would have found some cell with a large excess. The relevant probability is the global one, and severity is low.

Mayo's position on hunting is unambiguous. She holds that "nominal" error probabilities, computed for the selected hypothesis as though it had been fixed in advance, are not the "actual" ones, and that selection effects must be included (Mayo 1996, 2018). Her treatment of use-constructed hypotheses (Mayo 1996) holds that hunting matters exactly when it makes it probable that the procedure would output a false hypothesis that passes.

Both are descriptive-reading computations. The quantity is the probability that the procedure's output passes while false, which quantifies over what the procedure would have output.

On the rigid reading, her signature claim that the hunted hypothesis "would have passed even if false" is simply false in cases like the resonance scan. So either the claim has its de dicto content, or it is false. I am not imposing a reading she rejects. I am identifying the reading on which her verdict is true and on which her error probabilities are computed.

What remains disputed is the attribution. Mayo moves from "the test of the procedure's output had low capacity" to "x₀ is poor evidence for H." The Bayesian holds that x₀ gave H a Bayes factor of about 8000. The scope distinction resolves the dispute without declaring either computation wrong:

- x₀ is poor evidence that *the search's verdict* is correct (B(σ, e) ≈ 9).
- x₀ is strong evidence for *H* (B(H, e) ≈ 8000).
- Both parties should give H and σ the same posterior.

The practical recommendations do not conflict, because what an agent should *believe* is fixed by Proposition 1. The disagreement concerns where to locate support, and each side's correct computation supports a claim about a different object.

Mayo's account of harmless use-construction tests this allocation, and it forces a refinement. When a procedure is built so that its output is rarely false, as with a confidence-interval estimator, she holds that use-construction does not lower severity. Here the descriptive counterfactual, read as a likelihood, does *not* deliver her verdict. An interval centred on the sample mean fits the data whether or not it covers the parameter, so P(pass | ¬σ) ≈ 1 and B(σ, e) ≈ 1.

Her positive verdict rests on a different quantity. It is the probability, under each parameter value, that the procedure outputs a false interval, which is at most 0.05. The Bayesian counterpart of that low error rate is a high P(σ). This quantity still ranges over what the procedure would have output, so its object is σ rather than the rigid H. But it measures something closer to firmness than to increase in support.

The allocation in (T3) should therefore be stated with care. What is uniform across error-statistical verdicts on selected hypotheses is their *object*. It is the method's output, both where hunting is penalized and where use-construction is harmless. Their *measure* is not uniform:

- In the scan, the global error probability tracks the de dicto confirmation B(σ, e).
- In the estimator case, the verdict tracks the de dicto error rate.

I do not claim that severity just is a de dicto Bayes factor. I claim only that wherever Mayo counts selection effects, the proposition whose errors she counts is σ. Nor does the account reduce her view to procedural reliability, as though she cared about methods rather than hypotheses. Her claims about H are made through the procedure's error properties, and the scope account says those properties belong to σ.

## 9. Scope and limits

**Selection cases only.** Some canonical predictivist arguments do not concern selection. Two examples are Maher's (1988) coin-prediction case and White's (2003) analysis of prediction as evidence of reliable theory construction. Both locate the advantage of prediction in the fact that a *successful advance prediction is itself evidence* about the predictor's method, and hence about the theory. In such cases the total evidence differs between the predictor and the accommodator, and the de re posteriors genuinely differ. Ordinary Bayesian conditioning accounts for that difference.

The scope account neither competes with nor absorbs these cases. My earlier claim that "most canonical predictivist cases" have a true de dicto and a false de re reading should be restricted to cases of selection for fit. These include data dredging, model search, post hoc subgroup analysis and look-elsewhere scans.

Over-fitting arguments (Hitchcock and Sober 2004) occupy a middle position. They concern the predictive accuracy of a *fitted* model, which is a property of the output of a fitting procedure. They therefore fit the de dicto template naturally. I do not pursue that here.

**The symmetry conditions.** Proposition 2 requires symmetry in the prior and equivariance in S. Without them, the identity of the selected hypothesis can carry information about the search's success, and B(σ, e) and B(H, e | A) come apart. I have proposed the conditional quantity as the general notion of support beyond selection. Which notion better fits the error statistician's practice in strongly asymmetric searches is a further question. My conjecture is that practice there is unsettled for the same reason the two notions diverge.

**The error statistician's measures.** Section 8 showed that error-statistical verdicts share an object, σ, but not a measure. Where a procedure's fit is guaranteed, severity tracks the de dicto error rate rather than de dicto confirmation. So (T3) is a claim about which proposition each school is right about. It is not a claim that every error-statistical number equals a de dicto Bayes factor.

**Whether the de dicto object is "really" a proposition.** One may worry that σ, whose content shifts with the data, is a gerrymandered object of credence. It is a perfectly good set of worlds, and agents have attitudes towards such propositions all the time: "whoever wins will be a Bostonian," "whatever the committee decides will be implemented."

Its distinctive feature is that the evidence does two jobs. It fixes which hypothesis σ is equivalent to, and it bears on that hypothesis. The de re/de dicto split separates these two jobs. Proposition 2 says that, under symmetry, the first job confirms H without confirming σ. The multiplicative form of that decomposition is specific to odds-based measures. The ordering is not, as Section 4.3 showed.

## 10. Conclusion

The referee's objection rests on a correct theorem: conditional on all the evidence, the selected hypothesis and the proposition that the search's output is true are equally probable. My original formulation, which located the discount in the latter's posterior, was wrong. The theorem does not undermine the reconciliation, because the prediction/accommodation dispute concerns support. Equally probable propositions with different priors receive different support.

Under natural symmetry conditions the difference has an exact form. The de re confirmation of the selected hypothesis is the product of two factors:

1. the confirmation it gets merely from having been selected;
2. the confirmation it gets beyond selection.

The de dicto confirmation is the second factor alone. This is what the referee's recommended conditioning on "S returned H" yields when one asks about support rather than credence.

The physicists' global significance, and the Bayesian Occam factor that the referee rightly invokes, attach to this de dicto, existential object and leave the rigid hypothesis's Bayes factor untouched. Mayo's actual-versus-nominal error probabilities take the de dicto object, and her counterfactual "it would have passed even if false" is true only under the de dicto reading. Her verdicts do not always measure de dicto confirmation; where fit is guaranteed, they measure the de dicto error rate.

The Bayesian is therefore right that how H was found makes no difference to how strongly e supports H. The error statistician is right that it makes a large difference to how strongly e supports the search's verdict. The search's verdict is the object that scientific reporting and reliance usually put at stake.

## References

Box, G. E. P. (1980). Sampling and Bayes' inference in scientific modelling and robustness. *Journal of the Royal Statistical Society, Series A*, 143(4), 383–430.

Carnap, R. (1962). *Logical Foundations of Probability* (2nd ed.). Chicago: University of Chicago Press.

Cousins, R. D. (2017). The Jeffreys–Lindley paradox and discovery criteria in high energy physics. *Synthese*, 194(2), 395–432.

Fitelson, B. (1999). The plurality of Bayesian measures of confirmation and the problem of measure sensitivity. *Philosophy of Science*, 66 (Proceedings), S362–S378.

Gross, E., and Vitells, O. (2010). Trial factors for the look elsewhere effect in high energy physics. *European Physical Journal C*, 70, 525–530.

Hitchcock, C., and Sober, E. (2004). Prediction versus accommodation and the risk of overfitting. *British Journal for the Philosophy of Science*, 55(1), 1–34.

Howson, C., and Urbach, P. (2006). *Scientific Reasoning: The Bayesian Approach* (3rd ed.). Chicago: Open Court.

Maher, P. (1988). Prediction, accommodation, and the logic of discovery. In A. Fine and J. Leplin (Eds.), *PSA 1988*, Vol. 1 (pp. 273–285). East Lansing: Philosophy of Science Association.

Mayo, D. G. (1996). *Error and the Growth of Experimental Knowledge*. Chicago: University of Chicago Press.

Mayo, D. G. (2018). *Statistical Inference as Severe Testing: How to Get Beyond the Statistics Wars*. Cambridge: Cambridge University Press.

Mayo, D. G., and Spanos, A. (2006). Severe testing as a basic concept in a Neyman–Pearson philosophy of induction. *British Journal for the Philosophy of Science*, 57(2), 323–357.

Scott, J. G., and Berger, J. O. (2010). Bayes and empirical-Bayes multiplicity adjustment in the variable-selection problem. *Annals of Statistics*, 38(5), 2587–2619.

White, R. (2003). The epistemic advantage of prediction over accommodation. *Mind*, 112(448), 653–683.

Worrall, J. (2014). Prediction and accommodation revisited. *Studies in History and Philosophy of Science Part A*, 45, 54–61.
