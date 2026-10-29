# What Accommodation Discounts: Procedure-Indexed Propositions and the Prediction/Accommodation Dispute in Selection Cases

## 1. Introduction

Predictivism is the claim that evidence a hypothesis predicted supports it more than evidence the hypothesis was built or chosen to fit. Bayesians typically deny this (Howson 1988; Howson and Urbach 2006). On their view the posterior P(H | e) is fixed by H's prior and the likelihoods. How H came to be entertained matters only if it changes those quantities.

Error statisticians affirm predictivism for an important class of cases (Mayo 1996, 2018; Mayo and Cox 2006). Suppose a hypothesis is hunted out of a large space because it fits. It would have fitted whether or not it was true, so its passing has little probative force.

Practice in at least two fields sides with the error statistician while also accepting the Bayesian's likelihoods.

- **Particle physics.** For a bump found by scanning a mass range, physicists report two figures. One is a *local* significance, computed as if the mass had been fixed in advance. The other is a weaker *global* significance (Gross and Vitells 2010).
- **Forensic statistics.** A DNA match has a likelihood ratio of about 1/p for "this man is the source", where p is the frequency of his profile type. Yet the US National Research Council (1996) recommended a weaker figure, Np, for a match found by trawling a database of N profiles.

This paper concerns *selection cases*, in which a specified procedure S picks a hypothesis from a space Ω because of its fit to data e. I defend three claims.

**(T1) Rigid invariance.** Hold fixed the agent's joint credence over hypotheses and data. Then the confirmation e gives a hypothesis H, and H's posterior, do not depend on whether S selected H or someone proposed it in advance. This is nearly trivial. Its job is to fix the comparison class, and it sets aside cases in which history changes the joint distribution (§7.4).

**(T2) Content shift.** Every hypothesis-producing procedure P determines a *procedure-indexed proposition* W_P: "whatever P outputs is true."
- When P outputs H, W_P and H have the same posterior on the total evidence. But W_P's prior depends on P.
- So the same evidence confirms W_P less than H exactly when W_P had higher prior odds. The ratio of the two confirmations is the ratio of those prior odds.
- For an uninformative advance announcement the gap vanishes. For an informative search it can span several orders of magnitude.

I argue that predictivist judgements in selection cases are judgements about W_P. On this view the Bayesian is right about H and the predictivist is right about W_P. Neither has misdescribed the facts about the proposition they were addressing.

**(T3) What adjustments compute.** Look-elsewhere and hunting adjustments are computed under the global null, "no effect anywhere." Under a locality condition analogous to subset pivotality in multiple testing, the global p-value does a second job. Uniformly over the unknown signal parameters, it also bounds the probability that the search returns a false hypothesis that passes as well as H did. It is therefore an exact error probability for the existential claim and a conservative one for W_S. Error-statistical judgements of *harmless* construction concern something else: W_S's pre-data reliability, not the support data give it.

**Where the view sits.** Hitchcock and Sober's (2004) strong and weak predictivism are theses about H's total support. Weak predictivism says history is evidence of something that bears on that support. Candidates include the predictor's reliability (Maher 1988; White 2003; Barnes 2008) and the absence of fudging (Lange 2001; Lipton 2004). On the present view, history bears on nothing about H. It determines which *further* proposition is in question. The view is closest to Hitchcock and Sober's own overfitting account. The expected predictive accuracy that AIC estimates is a property of a fitting procedure's output, and so is a W-type property.

**What is not new.** The ingredients are familiar, and the closest precedent should be stated at once.
- The contrast between "this" outcome and "some" outcome comes from the inverse-gambler's-fallacy and fine-tuning debates (Hacking 1987; White 2000; Sober 2009).
- In the database-search controversy, several authors diagnosed the disagreement as one about *which hypothesis* the likelihood ratio concerns, with agreement about the posterior (Dawid and Mortera 1996; Dawid 2001; Balding 2002; Meester and Sjerps 2003).
- Selective inference conditions on the selection event (Yekutieli 2012; Fithian, Sun and Taylor 2014; Lee et al. 2016).

**What is new.** I generalize the forensic diagnosis into an account of predictivism in selection cases and defend it. Specifically:
- (a) I identify the procedure-indexed proposition, which is distinct from both the rigid claim and the existential claim, as the object of predictivist judgement. I argue for this from the truth conditions of the predictivist's own canonical reason (§3.3).
- (b) I give an exact condition for when an accommodation discount exists (§3.1).
- (c) I argue that the conditional support of selective inference is *not* the predictivist's object, because it delivers verdicts no party holds (§3.4).
- (d) I show how the rigid, indexed and existential figures sort three disputes (§4).
- (e) I state what error-statistical adjustments compute (§5).
- (f) I give a principle for which figure a reader needs (§6).

## 2. Setup and a running example

**Hypotheses and data.** Let Ω = {H₁, …, Hₙ} be mutually exclusive hypotheses, possibly with a residual H₀, "no signal." Let ∃ be "some Hᵢ with i ≥ 1 is true." Let E be the random data, with values e.

**The search.** A search S is a function, known to the agent, from data values to Ω ∪ {⊥}, where ⊥ means "no report." A randomized search is handled by including the randomization in E. Let Rep = [S(E) ≠ ⊥]. In the actual case S(e) = H. The *selection event* is A = [S(E) = H], and e entails A.

**The procedure-indexed proposition** for S is

  W = ⋃ᵢ [S(E) = Hᵢ ∧ Hᵢ].

W is a fixed set of worlds; what varies across those worlds is which Hᵢ it agrees with. The contrast between W and H is the contrast between "the lottery winner is from Boston" and "Smith is from Boston," said when Smith won. W also differs from ∃. W says the search's own output is correct; ∃ says only that some hypothesis in Ω is.

**Confirmation** is measured by the Bayes factor B(X, e) = O(X | e)/O(X), where O denotes odds. B(X, e | Y) is the same quantity computed relative to background Y. Other measures are discussed in §3.1.

**Running example.** A scan over n = 1000 mass cells, each one resolution-width wide.
- P(∃) = 0.5, uniform over location, so P(Hᵢ) = 0.0005.
- S always reports the cell with the largest local excess.
- If a resonance exists, S finds its cell with probability π = 0.6. So P(W) = 0.3.
- The maximum falls in cell k. P(H_k | e) = 0.8, with negligible posterior mass on other cells.

## 3. The content shift

### 3.1 The gap

**Proposition 1.** If S(e) = H, then P(W | e) = P(H | e).

*Proof.* e entails A, and W ∧ A ≡ H ∧ A. ∎

**Corollary (gap).** B(W, e) = B(H, e) · O(H)/O(W).

*Proof.* B(W, e) = O(W | e)/O(W) = O(H | e)/O(W). ∎

So B(W, e) < B(H, e) if and only if O(W) > O(H).

The corollary needs no symmetry assumption. The same ordinal comparison holds for the ratio measure r, the difference measure d, and Crupi, Tentori and Gonzalez's (2007) z, since each decreases in the prior at fixed posterior. Magnitudes are measure-specific (Fitelson 1999).

**The reach factor.** Call ρ = O(W)/O(H) the *reach factor*. Take an always-reporting search that is symmetric across cells. Then P(H) = P(∃)/n and P(W) = P(∃)π, so

  ρ ≈ nπ/(1 − P(W)) when P(H) is small.

Three consequences:
- A discount exists exactly when π > 1/n, that is, when the search beats a random pick.
- At fixed signal strength, π falls as n grows, because the largest of n noise cells grows roughly as √(2 log n). So ρ grows sublinearly in n.
- Strictly, π should be averaged over a prior on signal strength.

In the running example:

| Quantity | Value |
|---|---|
| O(H_k) | ≈ 0.0005 (1 to 2000) |
| O(W) | ≈ 0.43 (3 to 7) |
| ρ | ≈ 857 |
| O(H_k \| e) = O(W \| e) | 4 |
| B(H_k, e) | ≈ 8000 |
| B(W, e) | ≈ 9.3 |
| B(∃, e) | 4 |

On the ratio measure r, the rigid and indexed figures are 1600 and 2.7. On the difference measure d, they are 0.80 and 0.50. So the discount is large on l and r but not on d. I use l because it is the measure a reader can combine with her own prior without knowing anyone else's (§6).

### 3.2 One content, two procedures

Now suppose a theorist's announcement procedure T outputs Ann ∈ Ω before the data are seen, with Ann independent of E given each Hᵢ. Let W_T = ⋃ᵢ[Ann = Hᵢ ∧ Hᵢ].

Suppose T is a lottery and the prior over Ω is uniform, as in the example. Then P(W_T) = P(∃)/n = P(H). When Ann = H, P(W_T | Ann ∧ e) = P(H | e). Hence B(W_T, Ann ∧ e) = B(H, e). The announcement contributes nothing, and the data contribute the full 8000.

So for one and the same content H_k and the same data:
- *rigid support* is 8000 under both histories;
- *procedure-indexed support* is 8000 under announcement and 9.3 under search.

"The bump fell in the announced cell" was improbable unless the theorist was right. "The bump fell in the search's cell" was certain either way.

**Dilution.** ρ is large chiefly because O(H) is small. Is the predictivist contrast then just dilution redescribed? It is not.
- The dilution is common to both histories: the lottery theorist's H has the same prior. This is the Bayesian multiplicity adjustment, which lives in the prior and is indifferent to how H came to attention (Scott and Berger 2010).
- What differs is the prior of the procedure-indexed proposition. The lottery's W_T inherits the dilution. The search's W escapes it, because the search makes its output depend on where the data point.

Dilution is a precondition of a large ρ. Selection is what lifts W's prior above it.

### 3.3 Why W is the predictivist's object

As mathematics, the gap corollary is trivial: propositions with equal posteriors and unequal priors are confirmed unequally. The substantive claim is that predictivist judgements in selection cases are about W_P. Three considerations support this, and none assumes that history affects support.

**(i) The canonical reason.** Predictivists characteristically justify the discount by a counterfactual: "the hypothesis was chosen to fit, so it would have fitted whether or not it was true." This has two readings.

- *Rigid reading:* H_k would have shown this excess even if H_k were false. This is false. If cell k holds no resonance, the probability of so large an excess there is the local p-value. In the DNA case, it is the random-match probability.
- *Indexed reading:* the search's output would have shown such an excess even if the output were false. This is true, to the degree §5 measures by the global p-value.

Moreover, on the indexed reading the counterfactual says precisely that W's false-pass likelihood far exceeds H's. That is exactly what makes W's likelihood ratio, and hence its confirmation, smaller.

So the predictivist's stated ground is true only of W, and it is the reason for W's discount. Charity therefore assigns the indexed reading. This does not beg the question. It takes the predictivist's reason as given and asks which proposition it is true of. A Bayesian can accept the answer.

**(ii) Co-holding.** Where both figures are available, competent practitioners hold them together without any felt contradiction.
- Physicists quote local and global significance side by side.
- Forensic statisticians accept 1/p as the match's likelihood ratio for the suspect, while many of them also endorsed a database discount.

If the discount were a verdict about H's support, these pairs would be inconsistent. The error would then be held by the very people who compute H's likelihood. The better explanation is that the two figures concern different propositions.

**(iii) Reliance.** What practitioners actually decide is whether to act on, publish, or build on a procedure's outputs. A policy "act on S's outputs when the statistic exceeds c" is good or bad according to P(W | statistic ≥ c), weighted by stakes. That is by construction a quantity about W. Track records, false-discovery rates and Ioannidis's (2005) positive predictive values all estimate W-type probabilities.

**Two clarifications.** The view is not weak predictivism, since it denies that history is evidence for anything bearing on H. Nor is it a relabelling of total support. W_P and H are different propositions, and each receives ordinary total confirmation.

### 3.4 Not a coarsened background

**The alternative.** Another reconstruction keeps H fixed and changes the background. *Selection-relative support*,

  B(H, e | A) = LR_e(H)/LR_A(H),

removes from e's support for H the part supplied by the fact of being selected. This is Yekutieli's (2012) selection-adjusted likelihood and the conditioning principle of selective inference. In symmetric searches it agrees with W.

**Proposition 2.** Suppose the joint credence is invariant under relabellings of Ω applied jointly to hypotheses and data, and S is equivariant. Then B(H, e | A) = B(W, e | Rep).

*Proof.* Symmetry gives P(A) = P(Rep)/n and P(H ∧ A) = P(W)/n, so P(H | A) = P(W | Rep). Since e entails both A and Rep, Proposition 1 gives B(H, e | A) = O(W | e)/O(W | Rep) = B(W, e | Rep). ∎

For an always-reporting symmetric search, B(H, e | A) = B(W, e). In the running example both are 9.3.

**Where they come apart.** Outside this case the two quantities diverge, and the coarsened one gives verdicts no party holds.
- *Pivotal confidence intervals.* A exhausts the sufficient statistic, so B(H, e | A) = 1 for every e.
- *Cold hits* (§4.1). A, "this man is the unique match," does not fix his profile type. So LR_A(H) ≈ 1/p̄, the reciprocal of the average match probability, and B(H, e | A) ≈ p̄/p_g. For a typical profile this is close to 1. The NRC's intuition was that a trawl hit is *weaker* evidence, not that it is almost no evidence.

**Principled reasons against conditioning on A.**
- A is not ancillary, so the conditionality principle does not sanction conditioning on it.
- The selective-inference literature itself treats such conditioning as discarding information for the sake of error control. That information can be traded back for power by randomizing selection (Tian and Taylor 2018). How coarse an event to condition on is therefore a design choice, not a fact about evidential meaning.

**Why the W reconstruction avoids these problems.** It needs no counterfactual background. B(W, e) is total confirmation of a proposition by the total evidence. So the old-evidence literature's problem of choosing what to subtract does not arise (Christensen 1999; Eells and Fitelson 2000; Sprenger 2015). Nor is there any conflict with the likelihood principle:
- The LP constrains inference about the parameter, and every parameter proposition, H included, receives its standard posterior.
- W is a proposition about parameter and data jointly. Its dependence on S's behaviour at unobserved outcomes enters only through its prior P(W), which is a pre-data quantity like any prior.

The account is therefore neutral on the LP controversy (Berger and Wolpert 1988; Mayo 2014; Gandenberger 2015).

## 4. Three disputes sorted

### 4.1 Cold hits

**Setup.** A database of N members has prior probability P(∃) = q of including the source, uniformly over members. The trawl reports the unique matching profile, if there is one. Suppose suspect s, whose profile type has frequency p, is the unique match. Then the source is either s or someone outside the database, so O(H_s | e) = O(∃)/(Np) exactly. The three support figures are:

- **Rigid:** B(H_s, e) = (1/p) · P(¬H_s)/P(¬∃) ≥ 1/p. This is Balding and Donnelly's (1996) point that the trawl slightly *strengthens* the case, by excluding the other members.
- **Existential:** B(∃, e) = 1/(Np). This is the reciprocal of the NRC (1996) figure. It is also Stockmarr's (1999) likelihood ratio for "the source is in the database," which Stockmarr offered in support of the NRC recommendation.
- **Indexed:** P(W) = q · Π(1 − p_j) over the other members. So O(W) ≈ O(∃) when Np̄ is small, and B(W, e) ≈ 1/(Np).

**Why W and ∃ coincide here.** If the source is in the database, he matches, so the trawl's power is essentially 1. Its output is wrong only if the source is absent. The NRC/Stockmarr figure is therefore correct of both ∃ and W, while Balding and Donnelly's figure is correct of H_s. The posteriors agree throughout.

**What the general account adds.** The diagnosis itself is due to the authors cited in §1. The account adds three things.
- It explains *why* ∃ and W coincide here: high power. That also explains why they come apart in the mass scan, where π = 0.6 and B(W, e) ≈ 9.3 differs from B(∃, e) = 4.
- It shows that the coarsened quantity B(H, e | A) ≈ p̄/p_g matches no position in the debate.
- It brings the case under the canonical reason of §3.3. Of the database's hit, it is true that some member would very probably have matched even if the hit were not the source, provided Np is not small. Of s, it is false.

**What a juror needs** is a question for §6. A juror whose prior for s comes from the population, and not from his being the hit, needs rigid support. Pairing her prior with 1/(Np) would discount twice. This is Meester and Sjerps's (2003) point that a likelihood ratio must be paired with the prior for the same hypothesis.

### 4.2 Use-constructed intervals and calibration

Let S map x̄, with σ known, to the interval x̄ ± 1.96σ/√m. Coverage gives P(W) = 0.95 for every μ, and hence under every prior. Under a diffuse proper prior, P(H | e) ≈ 0.95, so B(W, e) ≈ 1. Meanwhile the rigid H, which is a specific interval with a tiny prior, receives enormous support.

**The early dispute.**
- Worrall's (1985) strong use-novelty thesis says that data used to construct a hypothesis do not support it. This is true of W, since the data do not tell us whether this interval is one of the 95 per cent. It is false of the rigid H.
- Mayo's (1991, 2008) verdict that such use-construction is harmless is also true. But it is a verdict about W's *prior reliability*, not about the support the data give W.

**The later views.** Worrall (2002, 2014) holds that parameter-fixing data confirm the general theory but do not favour the fixed version over its siblings beyond that. This can be read as crediting ∃-type support while withholding W-type support. Steele and Werndl's (2013) claim that calibration data can confirm the calibrated model concerns rigid support and is consistent with T1.

**Hunting versus harmless construction.** What separates them is not that the data give W more support in one case. In the interval case they give W none; in the scan they give it a factor of 9.3. The difference lies in W's prior: 0.95 against 0.3. The use-novelty tradition and the error-statistical tradition have been tracking different properties of the same proposition.

### 4.3 The look-elsewhere dilemma

Bayesian treatments recover the trials factor as an Occam factor on ∃ (Cousins 2017; see also R. Dawid 2015; Staley 2017). This seems to pose a dilemma:
- If the factor attaches to the rigid hypothesis, it contradicts T1.
- If it attaches only to ∃, the discount physicists apply to the *localized* claim, "a boson near 125 GeV," seems to have no credal counterpart.

The account escapes both horns. As reported by the collaboration that found it, the localized claim has the shape of W: it is the claim that the scan's output is right. Its support (9.3 in the example) lies between existential support (4) and rigid support (8000). The rigid prior's dilution is common to both histories (§3.2), so T1 is untouched.

## 5. What error-statistical adjustments compute

Bayes factors for exact data can differ greatly from those for tail events (Berger and Sellke 1987). Comparisons with p-values should therefore use coarsened evidence. Let T_z = [Z_max ≥ z].

**Rigid.** Consider ¬H_k-worlds in which any signal lies outside k's resolution region. There cell k is noise, so P(Z_k ≥ z | ¬H_k) is the local p-value.

**Indexed.** Assume two conditions:
- *Grain matched to resolution:* selecting a cell within resolution of the signal counts as success.
- *Locality:* a signal at j leaves the noise outside j's resolution region distributed as under background-only. Correlations among noise cells are permitted.

In a world with a signal at j, a false pass requires the maximum over cells outside j's region to reach z. By locality, and because a maximum over a subset cannot exceed the maximum over the whole set, this has probability at most P(Z_max ≥ z | ¬∃), which is the global p-value p_G. Under ¬∃ the bound holds with equality. Hence, for every value θ of the signal parameters (location and strength),

  P_θ(T_z ∧ ¬W) ≤ p_G.

This is a frequentist error statement about the composite ¬W, and it needs no prior over θ. It bounds the false-pass rate uniformly, in the way strong familywise error control bounds error under any configuration of true nulls. Locality plays the role of Westfall and Young's (1993) subset pivotality. The corresponding bound on the Bayesian likelihood is P(T_z | ¬W) ≤ p_G/P(¬W), which in the example is a factor of about 1.4.

**Three consequences.**
- *The global p-value* is an exact error probability for ∃ and a conservative one for W. It is tight when power is high, because then ¬W given T_z consists mostly of ¬∃. As power falls, W and ∃ separate and the slack grows.
- *Mayo's hunting calculations* are computed under the global null. Read as answers to her stated question, "how probable is it that the procedure outputs a false hypothesis that passes this well?", they are uniform bounds on P_θ(T_z ∧ ¬W), exact on ¬∃. This is T3.
- *Her harmlessness criterion* concerns W's pre-data error rate (§4.2). No single credal quantity reproduces every severity verdict, and I do not claim one does.

**Caveats.** The Gross–Vitells upcrossing method gives an asymptotic approximation that is also an upper bound (Davies 1987), not an exact value. Locality is a substantive assumption where background shapes are fitted, since a signal can distort the background fit elsewhere.

**Magnitudes.** At 5σ local significance, the simple-versus-simple likelihood ratio is at most e^{12.5} ≈ 2.7 × 10⁵. Because ¬H_k is composite, P(e | ¬H_k) ≥ P(¬∃ | ¬H_k) P(e | ¬∃). So LR_e(H_k) ≤ e^{12.5}/P(¬∃ | ¬H_k), which is about twice that figure. Dividing by a ρ of order 10³ leaves indexed support of at most several hundred.

**Optional stopping.** When the hypothesis is fixed in advance, the procedure always outputs H, so W_P = H and there is no content shift. The account then yields no discount. Whether stopping-rule adjustments are warranted remains the likelihood-principle dispute, which this paper does not adjudicate. Mayo treats stopping rules and hunting as one family of selection effects. The account explains why they come apart under Bayesian reconstruction: hunting adjustments concern a proposition other than H, whereas stopping-rule adjustments concern H itself.

## 6. Reporting: background matching

**Background matching (BM).** A support figure reported for combination with a reader's prior must concern the same proposition as that prior. It must also be computed relative to whatever background that prior already incorporates. Otherwise evidence is counted twice or not at all.

The figure a reader needs depends on her prior:
- A reader with a full model of Ω and S can use the likelihood function directly.
- A reader whose prior concerns the rigid H needs B(H, e). Examples are a reader who fixed the mass independently, and the juror of §4.1.
- A reader with a track-record base rate for this search's outputs holds P(W | Rep), so she needs B(W, e | Rep). Multiplying her base rate by rigid support counts selection twice: 0.43 × 8000 ≈ 3400, instead of 4.
- A reader whose base rate is a positive predictive value at a threshold (Ioannidis 2005) needs the same figure, with Rep including the threshold crossing.

Only l lets a reporter serve readers whose priors she does not know. That is the reason for using it.

**The Higgs reports.** Local and global significances are p-values, not Bayes factors, but §5 supplies a bridge.
- The local p-value is the false-pass likelihood for the rigid claim.
- The global p-value bounds the false-pass rate for the indexed claim.

The numerators of the two tail likelihood ratios are of comparable size, since both are power at threshold z. So a reader who holds a prior for the rigid mass can use the local figure. A reader who meets the mass as the scan's output can use the global figure as a conservative stand-in. This is a rational reconstruction, not the collaborations' stated rationale. They also stressed that the global figure depends on a conventionally chosen range (§7.3).

**Replication.** New data e′ from an analysis targeted at the selected cell confirm the rigid H_k. No new selection occurs, so this confirmation does not depend on how the original search is described. That is plausibly much of replication's value in selection cases. A replication that itself scans a window, however, introduces a new procedure-indexed proposition with its own reach factor.

## 7. Objections

### 7.1 Total evidence

*Objection.* The agent knows e and knows that S returned H, so W and H are equivalent for her. Any discount obtained by averaging over possible outputs is a pre-data error rate, and it is irrelevant once the data are in.

*Reply.* Proposition 1 grants the equivalence for credence. The objection is also right that the procedural ingredient is pre-data: it is P(W). But this is no defect peculiar to W. Every Bayes factor compares a posterior with a pre-data prior. B(W, e) is the post-data confirmation of a proposition whose prior depends on S. Equivalence on the evidence does not imply equal confirmation by it. Compare "the winner is from Boston" and "Smith is from Boston," given the news that Smith, a Bostonian, won: they end up equally probable, but they were not equally confirmed.

### 7.2 Historical novelty and overdetermination

Musgrave (1974), Campbell and Vinci (1983), Collins (1994) and Leplin (1997) objected that heuristic novelty makes confirmation depend on contingent and often inaccessible facts about discovery.

The account agrees with these objections where they are aimed.
- Rigid support is a relation between hypothesis and evidence, untouched by history (T1).
- W_P's confirmation depends on P only because W_P is *about* P. That is not psychologism about H.
- Where P is inaccessible, W_P's prior is unknown and so is its support. Rigid support may still be available.

Overdetermination poses no difficulty either. Suppose a mass is both indicated by electroweak fits and selected by a scan, or one scientist predicts H while another accommodates it. Then there are two procedure-indexed propositions, each with its own confirmation, and there is no need for "the" history of H. BM settles which figure a reader needs, according to which procedure her prior concerns.

### 7.3 Individuating the search

W depends on how S is described:
- *Grain* should be fixed by the claim reported. If the claim is "a resonance within resolution of m₀," cells should be resolution-wide.
- *Output* should be the coarsest function of the data that determines the claim.
- *Scope* is genuinely open. A single pre-specified window, several channels, and all of a collaboration's analyses are different procedures with different reach.

I do not claim to solve this reference-class problem. The gains are modest. The indeterminacy concerns which proposition a discounted figure is about, not the support of any given proposition. And it does not infect rigid support or targeted replication. Practice already reflects this: collaborations quote a scope-independent local figure alongside a global figure for a stated, conventional range.

### 7.4 Scope

**Asymmetric searches.** T2 needs no symmetry; only Proposition 2 does. So asymmetric searches fall within the account.

**Unknown procedures.** When readers do not know S, as with forking paths (Gelman and Loken 2014), P(W) is indeterminate for them. Rigid support may be indeterminate too, if they see only a fragment of the data. The standard remedies fit this picture:
- Pre-registration makes the output independent of the data, so that W_P = H.
- Holdout data (Cox 1975) assess a selected H with evidence that did not select it.

**Changes to the joint distribution.** Some cases lie outside T1 and are handled by ordinary conditioning. These include predictor reliability (Maher 1988; White 2003) and fixed-parameter scenarios, in which selection belongs to the design rather than the evidence (Dawid 1994; Senn 2008; Yekutieli 2012).

**Theory construction.** The classic episodes of the predictivism debate, such as Fresnel, Mendeleev, and Einstein versus Lorentz, involve procedures that are not known functions on a specified space. The content-shift diagnosis extends schematically, since any construction procedure has a W_P. But P(W_P) is unavailable there, so the account offers a diagnosis without a verdict. It thereby predicts that historical credit for prediction should be unstable where procedures are opaque. That fits the mixed findings of Brush (1994) and Scerri and Worrall (2001), and the variety of rationales surveyed by Harker (2008) and Douglas and Magnus (2013). I claim no more than fit. The account is offered as a treatment of selection cases, not of predictivism in general.

## 8. Conclusion

In selection cases, the selected hypothesis H and the proposition W, that the search's output is true, share a posterior on the total evidence. They differ in prior, and therefore in confirmation. The predictivist's discount is the ratio of their prior odds. It exists exactly when the procedure-indexed proposition was more probable than the rigid one, and it vanishes for uninformative advance proposal.

The verdicts sort as follows:
- On the rigid hypothesis, the Bayesian is right.
- On the procedure-indexed proposition, which is the object of the predictivist's own canonical reason, the predictivist is right.
- Selective inference's conditional support coincides with W's only in symmetric, always-reporting searches. Elsewhere it gives verdicts no party holds.
- Global p-values are exact for the existential claim and, under locality, uniform bounds on W's false-pass rate.
- Judgements of harmless construction concern W's prior reliability, not its support.

What remains open is the individuation of the search, which fixes which procedure-indexed proposition a report concerns.

## References

Balding, D. J. (2002). The DNA database search controversy. *Biometrics*, 58, 241–244.

Balding, D. J., and Donnelly, P. (1996). Evaluating DNA profile evidence when the suspect is identified through a database search. *Journal of Forensic Sciences*, 41, 603–607.

Barnes, E. C. (2008). *The Paradox of Predictivism*. Cambridge: Cambridge University Press.

Berger, J. O., and Sellke, T. (1987). Testing a point null hypothesis: The irreconcilability of P values and evidence. *Journal of the American Statistical Association*, 82, 112–122.

Berger, J. O., and Wolpert, R. L. (1988). *The Likelihood Principle* (2nd ed.). Hayward, CA: Institute of Mathematical Statistics.

Brush, S. G. (1994). Dynamics of theory change: The role of predictions. *PSA 1994*, Vol. 2, 133–145.

Campbell, R., and Vinci, T. (1983). Novel confirmation. *British Journal for the Philosophy of Science*, 34, 315–341.

Christensen, D. (1999). Measuring confirmation. *Journal of Philosophy*, 96, 437–461.

Collins, R. (1994). Against the epistemic value of prediction over accommodation. *Noûs*, 28, 210–224.

Cousins, R. D. (2017). The Jeffreys–Lindley paradox and discovery criteria in high energy physics. *Synthese*, 194(2), 395–432.

Cox, D. R. (1975). A note on data-splitting for the evaluation of significance levels. *Biometrika*, 62, 441–444.

Crupi, V., Tentori, K., and Gonzalez, M. (2007). On Bayesian measures of evidential support: Theoretical and empirical issues. *Philosophy of Science*, 74, 229–252.

Davies, R. B. (1987). Hypothesis testing when a nuisance parameter is present only under the alternative. *Biometrika*, 74, 33–43.

Dawid, A. P. (1994). Selection paradoxes of Bayesian inference. In T. W. Anderson, K.-T. Fang and I. Olkin (Eds.), *Multivariate Analysis and Its Applications* (IMS Lecture Notes 24, pp. 211–220). Hayward, CA: Institute of Mathematical Statistics.

Dawid, A. P. (2001). Comment on Stockmarr, "Likelihood ratios for evaluating DNA evidence when the suspect is found through a database search." *Biometrics*, 57(3).

Dawid, A. P., and Mortera, J. (1996). Coherent analysis of forensic identification evidence. *Journal of the Royal Statistical Society, Series B*, 58, 425–443.

Dawid, R. (2015). Higgs discovery and the look elsewhere effect. *Philosophy of Science*, 82(1), 76–96.

Douglas, H., and Magnus, P. D. (2013). State of the field: Why novel prediction matters. *Studies in History and Philosophy of Science*, 44, 580–589.

Eells, E., and Fitelson, B. (2000). Measuring confirmation and evidence. *Journal of Philosophy*, 97, 663–672.

Fitelson, B. (1999). The plurality of Bayesian measures of confirmation and the problem of measure sensitivity. *Philosophy of Science*, 66 (Proceedings), S362–S378.

Fithian, W., Sun, D., and Taylor, J. (2014). Optimal inference after model selection. arXiv:1410.2597.

Gandenberger, G. (2015). A new proof of the likelihood principle. *British Journal for the Philosophy of Science*, 66, 475–503.

Gelman, A., and Loken, E. (2014). The statistical crisis in science. *American Scientist*, 102, 460–465.

Gross, E., and Vitells, O. (2010). Trial factors for the look elsewhere effect in high energy physics. *European Physical Journal C*, 70, 525–530.

Hacking, I. (1987). The inverse gambler's fallacy: The argument from design. The anthropic principle applied to Wheeler universes. *Mind*, 96, 331–340.

Harker, D. (2008). On the predilections for predictions. *British Journal for the Philosophy of Science*, 59, 429–453.

Hitchcock, C., and Sober, E. (2004). Prediction versus accommodation and the risk of overfitting. *British Journal for the Philosophy of Science*, 55(1), 1–34.

Howson, C. (1988). Accommodation, prediction and Bayesian confirmation theory. *PSA 1988*, Vol. 2, 381–392.

Howson, C., and Urbach, P. (2006). *Scientific Reasoning: The Bayesian Approach* (3rd ed.). Chicago: Open Court.

Ioannidis, J. P. A. (2005). Why most published research findings are false. *PLoS Medicine*, 2(8), e124.

Lange, M. (2001). The apparent superiority of prediction to accommodation as a side effect: A reply to Maher. *British Journal for the Philosophy of Science*, 52, 575–588.

Lee, J. D., Sun, D. L., Sun, Y., and Taylor, J. E. (2016). Exact post-selection inference, with application to the lasso. *Annals of Statistics*, 44(3), 907–927.

Leplin, J. (1997). *A Novel Defense of Scientific Realism*. New York: Oxford University Press.

Lipton, P. (2004). *Inference to the Best Explanation* (2nd ed.). London: Routledge.

Maher, P. (1988). Prediction, accommodation, and the logic of discovery. In A. Fine and J. Leplin (Eds.), *PSA 1988*, Vol. 1 (pp. 273–285). East Lansing: Philosophy of Science Association.

Mayo, D. G. (1991). Novel evidence and severe tests. *Philosophy of Science*, 58, 523–552.

Mayo, D. G. (1996). *Error and the Growth of Experimental Knowledge*. Chicago: University of Chicago Press.

Mayo, D. G. (2008). How to discount double-counting when it counts: Some clarifications. *British Journal for the Philosophy of Science*, 59, 857–879.

Mayo, D. G. (2014). On the Birnbaum argument for the strong likelihood principle. *Statistical Science*, 29, 227–239.

Mayo, D. G. (2018). *Statistical Inference as Severe Testing: How to Get Beyond the Statistics Wars*. Cambridge: Cambridge University Press.

Mayo, D. G., and Cox, D. R. (2006). Frequentist statistics as a theory of inductive inference. In J. Rojo (Ed.), *Optimality: The Second Erich L. Lehmann Symposium* (IMS Lecture Notes 49, pp. 77–97). Beachwood, OH: Institute of Mathematical Statistics.

Meester, R., and Sjerps, M. (2003). The evidential value in the DNA database search controversy and the two-stain problem. *Biometrics*, 59, 727–732.

Musgrave, A. (1974). Logical versus historical theories of confirmation. *British Journal for the Philosophy of Science*, 25, 1–23.

National Research Council (1996). *The Evaluation of Forensic DNA Evidence*. Washington, DC: National Academy Press.

Scerri, E. R., and Worrall, J. (2001). Prediction and the periodic table. *Studies in History and Philosophy of Science*, 32, 407–452.

Scott, J. G., and Berger, J. O. (2010). Bayes and empirical-Bayes multiplicity adjustment in the variable-selection problem. *Annals of Statistics*, 38, 2587–2619.

Senn, S. (2008). A note concerning a selection "paradox" of Dawid's. *American Statistician*, 62, 206–210.

Sober, E. (2009). Absence of evidence and evidence of absence: Evidential transitivity in connection with fossils, fishing, fine-tuning, and firing squads. *Philosophical Studies*, 143, 63–90.

Sprenger, J. (2015). A novel solution to the problem of old evidence. *Philosophy of Science*, 82, 383–401.

Staley, K. W. (2017). Pragmatic warrant for frequentist statistical practice: The case of high energy physics. *Synthese*, 194(2), 355–376.

Steele, K., and Werndl, C. (2013). Climate models, calibration, and confirmation. *British Journal for the Philosophy of Science*, 64, 609–635.

Stockmarr, A. (1999). Likelihood ratios for evaluating DNA evidence when the suspect is found through a database search. *Biometrics*, 55, 671–677.

Tian, X., and Taylor, J. (2018). Selective inference with a randomized response. *Annals of Statistics*, 46, 679–710.

Westfall, P. H., and Young, S. S. (1993). *Resampling-Based Multiple Testing: Examples and Methods for p-Value Adjustment*. New York: Wiley.

White, R. (2000). Fine-tuning and multiple universes. *Noûs*, 34, 260–276.

White, R. (2003). The epistemic advantage of prediction over accommodation. *Mind*, 112(448), 653–683.

Worrall, J. (1985). Scientific discovery and theory-confirmation. In J. C. Pitt (Ed.), *Change and Progress in Modern Science* (pp. 301–331). Dordrecht: Reidel.

Worrall, J. (2002). New evidence for old. In P. Gärdenfors, J. Woleński and K. Kijania-Placek (Eds.), *In the Scope of Logic, Methodology and Philosophy of Science*, Vol. 1 (pp. 191–209). Dordrecht: Kluwer.

Worrall, J. (2014). Prediction and accommodation revisited. *Studies in History and Philosophy of Science*, 45, 54–61.

Yekutieli, D. (2012). Adjusted Bayesian inference for selected parameters. *Journal of the Royal Statistical Society, Series B*, 74(3), 515–541.