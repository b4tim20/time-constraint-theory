# This paper develops a general theory of entity freedom grounded in time rather than preference, permission, or sentiment. The central claim is that the freedom of any entity is best understood as the residual portion of its available time that is not consumed by required obligations. Required obligations divide into two kinds: intrinsic obligations, which arise from the entity's substrate and persistence conditions, and extrinsic obligations, which arise from external systems, dependencies, and interacting agents. Extrinsic obligation is further divided into raw obligation and effective obligation, where effective obligation is raw obligation net of the entity's constraint-avoidance capacity. The theory generalizes across persons, firms, machines, institutions, and other bounded systems. It provides a formal core, axioms, comparative-statics results, a dynamic extension, an empirical measurement program, and falsifiable hypotheses. It also explains why formally similar entities can exhibit sharply unequal effective freedom: the difference lies not only in what they must do, but in what capacities they possess to buffer, understand, negotiate, restructure, delegate, or bypass imposed constraints #
 
## 1. Introduction ##

All persistent entities operate under finite time. Every entity that continues through a time horizon must allocate some of that time to maintenance, some to compliance with surrounding structures, and some to discretionary action. The problem of freedom, under this view, is not primarily the problem of formal permission. It is the problem of residual control over time.

This paper treats time as the primitive quantity of analysis. The key question is not merely what an entity is allowed to do, but how much of its available time remains under its own control after required obligations have been satisfied. This framing transforms freedom from a vague moral abstraction into a measurable structural quantity.

The theory originates in a time-constraint model that distinguishes total time, physical obligation, agent-imposed obligation, and constraint avoidance. Here that structure is generalized from persons to entities in the broad sense: organisms, organizations, machines, institutions, and composite systems. The aim is to preserve the original logic while extending it into a more explicit and portable formal theory. fileciteturn1file0

## 2. Domain and Ontology ##

Let \(\mathcal{E}\) denote the set of entities. An entity \(x \in \mathcal{E}\) is any bounded system that persists through time, performs operations, and allocates process-time across maintenance and action. The definition is intentionally general. A human being is an entity. A firm is an entity. A software service, a machine fleet, a state institution, or a distributed network can also be treated as an entity provided that it exhibits persistence, operational continuity, and temporally allocated activity.

Let \(H = [t_0,t_1]\) denote a time horizon with duration \(|H| = t_1 - t_0\).

For any entity \(x\) over horizon \(H\), define the following primitives:

- \(T_x(H)\): total available process-time.
- \(I_x(H)\): intrinsic obligation.
- \(E^{raw}_x(H)\): raw extrinsic obligation.
- \(V_x(H)\): constraint avoidance.
- \(E^{eff}_x(H)\): effective extrinsic obligation.
- \(F_x(H)\): time freedom.

The original draft uses the terms total time, physical obligation, agent-imposed obligation, and constraint avoidance. In the generalized theory, physical obligation becomes intrinsic obligation, and agent-imposed obligation becomes extrinsic obligation. The underlying structure remains the same. fileciteturn1file0

## 3. Definitions ##

### 3.1 Total Available Process-Time ###

\(T_x(H)\) is the total time available to entity \(x\) for allocation within horizon \(H\). For continuously active entities, \(T_x(H)\) may approximate \(|H|\). For intermittently active or capacity-limited entities, \(T_x(H) \le |H|\).

### 3.2 Intrinsic Obligation ###

\(I_x(H)\) is the minimum time required to preserve the entity's continuity, viability, or identity given its substrate and environment. These are obligations imposed by the entity's own structure rather than by external systems.

For different entities, intrinsic obligation takes different forms. For a person it includes sleep, food, hygiene, and bodily maintenance. For a machine it includes charging, cooling, inspection, downtime, and repair cycles. For an organization it includes baseline coordination, upkeep of essential infrastructure, and minimal administrative continuity necessary to remain operational.

Intrinsic obligation is not absolutely fixed in all cases, but within a given technological and environmental regime it behaves as a hard or near-hard lower bound.

### 3.3 Raw Extrinsic Obligation ###

\(E^{raw}_x(H)\) is the time demanded of entity \(x\) by external systems, dependencies, and interacting agents. It includes compliance, approvals, queueing, coordination, reporting, access maintenance, contractual performance, and other time claims imposed from outside the entity's intrinsic persistence requirements.

### 3.4 Constraint Avoidance ###

\(V_x(H)\) is the time reclaimed by reducing, restructuring, bypassing, prepaying, automating, transferring, or otherwise mitigating extrinsic obligation. Constraint avoidance does not remove intrinsic obligation. It applies only to externally imposed burdens.

### 3.5 Effective Extrinsic Obligation ###

Effective extrinsic obligation is raw extrinsic obligation net of successful mitigation:

\[
E^{eff}_x(H) = \max\{0, E^{raw}_x(H) - V_x(H)\}.
\]

The max operator imposes a saturation condition: avoidance cannot reduce effective extrinsic obligation below zero.

### 3.6 Time Freedom ###

Time freedom is the residual time not claimed by intrinsic or effective extrinsic obligation:

\[
F_x(H) = T_x(H) - I_x(H) - E^{eff}_x(H).
\]

Substituting the definition of effective extrinsic obligation yields the theory's general reduced form:

\[
F_x(H) = T_x(H) - I_x(H) - \max\{0, E^{raw}_x(H) - V_x(H)\}.
\]

Define required time as

\[
R_x(H) = I_x(H) + E^{eff}_x(H).
\]

Then the minimal law of the theory is simply

\[
F_x(H) = T_x(H) - R_x(H).
\]

This preserves the fundamental law in the original model while removing the restriction to human entities. fileciteturn1file0

## 4. Structural Determinants of Extrinsic Obligation ##

The original model proposes that agent-imposed obligation rises with system dependence and falls with resource access, rule literacy, and negotiation power. Generalized to entities, raw extrinsic obligation is a function of dependence on external systems and the capacities that moderate those burdens. fileciteturn1file0

Let:

- \(S_x(H)\): system dependence.
- \(R_x(H)\): resource access.
- \(L_x(H)\): rule literacy.
- \(N_x(H)\): negotiation power.
- \(B_x(H)\): gross burden intensity of the environment.

Then raw extrinsic obligation may be represented generally as

\[
E^{raw}_x(H) = B_x(H)\, h\big(S_x(H), R_x(H), L_x(H), N_x(H)\big),
\]

with the following monotonic properties:

\[
\frac{\partial h}{\partial S} > 0, \qquad
\frac{\partial h}{\partial R} < 0, \qquad
\frac{\partial h}{\partial L} < 0, \qquad
\frac{\partial h}{\partial N} < 0.
\]

One admissible functional form, consistent with the source model, is a ratio form:

\[
E^{raw}_x(H) = B_x(H)\,\frac{S_x(H)}{\varepsilon + \beta_R R_x(H) + \beta_L L_x(H) + \beta_N N_x(H)},
\]

where \(\varepsilon > 0\) prevents division by zero and the \(\beta\) terms scale the contribution of each capacity.

This formulation captures the intuition that dependence amplifies burden while usable buffers and navigation capacities dampen it.

## 5. Structural Determinants of Constraint Avoidance ##

The original model treats constraint avoidance as a function of capital, legal literacy, institutional access, and delegation power. In generalized form, let:

- \(C_x(H)\): capital or stored resources.
- \(Q_x(H)\): optimization literacy, meaning the ability to understand and exploit formal rule structures.
- \(U_x(H)\): institutional access.
- \(D_x(H)\): delegation power.

Then

\[
V_x(H) = g\big(C_x(H), Q_x(H), U_x(H), D_x(H)\big),
\]

subject to

\[
\frac{\partial g}{\partial C} \ge 0, \qquad
\frac{\partial g}{\partial Q} \ge 0, \qquad
\frac{\partial g}{\partial U} \ge 0, \qquad
\frac{\partial g}{\partial D} \ge 0,
\]

and

\[
0 \le V_x(H) \le E^{raw}_x(H).
\]

In many settings \(g\) should be modeled as concave, reflecting diminishing marginal returns to additional capital, access, or delegation:

\[
\frac{\partial^2 g}{\partial z_i^2} \le 0
\quad \text{for each component } z_i \in \{C,Q,U,D\}.
\]

Constraint avoidance is therefore not magic. It is a capacity to convert stored resources, literacy, access, and transfer power into time recovery.

## 6. Axioms of the Theory ##

### Axiom 1. Temporal Finitude ###

For any entity \(x\) and finite horizon \(H\), total available process-time is finite:

\[
0 \le T_x(H) < \infty.
\]

### Axiom 2. Constraint Partition ###

Required time partitions into intrinsic obligation and effective extrinsic obligation:

\[
R_x(H) = I_x(H) + E^{eff}_x(H).
\]

### Axiom 3. Dependence Monotonicity ###

Holding other factors constant, higher system dependence weakly increases raw extrinsic obligation.

### Axiom 4. Capacity Monotonicity ###

Holding other factors constant, increases in resource access, rule literacy, negotiation power, capital, optimization literacy, institutional access, and delegation power weakly decrease required time through either lower raw burden or higher avoidance.

### Axiom 5. Saturation ###

Constraint avoidance cannot exceed raw extrinsic obligation, and effective extrinsic obligation cannot be negative.

### Axiom 6. Path Dependence ###

The state variables that determine future burdens and future mitigation capacities are themselves affected by prior time allocations. Hence freedom is not merely static; it evolves.

## 7. Core Propositions ##

### Proposition 1. Intrinsic Burden Reduces Freedom ###

For fixed \(T_x(H)\) and fixed extrinsic terms,

\[
\frac{\partial F_x(H)}{\partial I_x(H)} = -1.
\]

**Proof.** Directly from the reduced form \(F_x = T_x - I_x - E^{eff}_x\).

### Proposition 2. Dependence Reduces Freedom ###

Under Axiom 3 and fixed mitigation,

\[
\frac{\partial F_x(H)}{\partial S_x(H)} \le 0.
\]

**Proof sketch.** Because higher \(S_x\) weakly raises \(E^{raw}_x\), and because \(E^{eff}_x\) is weakly increasing in \(E^{raw}_x\), freedom weakly falls.

### Proposition 3. Constraint-Avoidance Capacity Increases Freedom ###

For any mitigation component \(z_i \in \{C,Q,U,D\}\),

\[
\frac{\partial F_x(H)}{\partial z_i} \ge 0,
\]

subject to saturation.

**Proof sketch.** \(F_x\) is weakly increasing in \(V_x\), and \(V_x\) is weakly increasing in each mitigation component.

### Proposition 4. Formal Equality Does Not Imply Freedom Equality ###

Let two entities \(x\) and \(y\) satisfy

\[
T_x = T_y, \qquad I_x = I_y, \qquad E^{raw}_x = E^{raw}_y,
\]

but suppose

\[
V_x > V_y.
\]

Then

\[
F_x > F_y.
\]

**Interpretation.** Two entities can face the same nominal obligations while possessing different effective freedom because they differ in mitigation capacity.

### Proposition 5. Recurring Burden Reduction Dominates One-Time Time Gains Over Sufficient Horizons ###

Suppose an intervention incurs a one-time time cost \(c\) and permanently reduces effective recurring burden by \(\delta > 0\) per period for \(n\) future periods. Then the intervention is time-positive iff

\[
n\delta > c.
\]

**Interpretation.** This formally explains why eliminating recurring obligations is structurally more important than obtaining one-time time windfalls of equal size.

### Proposition 6. Freedom Can Compound ###

If a positive fraction of current freedom can be invested into state variables that reduce future dependence or increase future mitigation capacity, then an increase in current freedom can produce an increase in expected future freedom.

**Proof sketch.** By Axiom 6, prior time allocation affects future \(S_x\), \(C_x\), \(Q_x\), \(U_x\), and \(D_x\). Since future \(F_x\) is monotone in those variables, current freedom can generate a positive feedback loop.

## 8. Dynamic Extension ##

The static theory describes a horizon-level balance. A fuller theory requires dynamics.

Let the state vector be

\[
z_t = (S_t, R_t, L_t, N_t, C_t, Q_t, U_t, D_t).
\]

For discrete periods \(t = 0,1,2,\dots\), define

\[
F_t = T_t - I_t - \max\{0, E^{raw}_t - V_t\},
\]

with

\[
E^{raw}_t = B_t\, h(S_t,R_t,L_t,N_t),
\]

and

\[
V_t = g(C_t,Q_t,U_t,D_t).
\]

Let the state transition rule be

\[
z_{t+1} = \Phi(z_t, a_t, \omega_t),
\]

where \(a_t\) is the entity's allocation decision and \(\omega_t\) is an exogenous shock. A simple but important case is one in which discretionary time is partly reinvested into reducing future dependence or increasing future avoidance capacity:

\[
C_{t+1} = C_t + \gamma_C m(F_t), \qquad D_{t+1} = D_t + \gamma_D m(F_t), \qquad S_{t+1} = S_t - \gamma_S m(F_t),
\]

for nonnegative coefficients \(\gamma_C, \gamma_D, \gamma_S\) and some increasing reinvestment function \(m\).

This dynamic extension implies that freedom can be path-dependent and self-reinforcing. Entities with slightly greater present freedom may accumulate larger future buffers, while entities with very low present freedom may be trapped in states where all available time is consumed by immediate obligation and no time remains to reduce future obligation.

## 9. Measurement and Operationalization ##

The theory is intended to be empirically tractable. Each term can be approximated using observable proxies.

First, measure \(T_x(H)\) as the total process-time available within the horizon. For humans this may be clock time; for firms or machines it may be uptime or available operating windows.

Second, estimate \(I_x(H)\) from maintenance and continuity requirements: sleep, hygiene, energy cycles, downtime, staffing floors, baseline coordination, and similar substrate-level necessities.

Third, estimate \(E^{raw}_x(H)\) from externally imposed time claims: approvals, compliance tasks, queueing, contract performance, reporting, coordination with external actors, and time spent maintaining access to critical systems.

Fourth, estimate \(V_x(H)\) from time reclaimed by mitigation: delegation, automation, outsourcing, prepayment, legal or structural optimization, tooling, and use of institutional intermediaries.

A useful normalized measure is the freedom ratio:

\[
\phi_x(H) = \frac{F_x(H)}{T_x(H)}.
\]

This ratio permits comparison across entities of different scale.

System dependence \(S_x\) may be proxied by dependency concentration, absence of fallback options, penalty exposure, liquidity or redundancy shortfall, and the proportion of essential functions controlled externally. Resource access \(R_x\) may be proxied by buffers, tooling, infrastructure, and network reach. Rule literacy \(L_x\) and optimization literacy \(Q_x\) may be proxied by error rates, compliance costs, or the time required to navigate procedural environments. Negotiation power \(N_x\) may be proxied by replaceability, market leverage, or contractual flexibility. Institutional access \(U_x\) may be proxied by access to formal intermediaries and structured channels. Delegation power \(D_x\) may be proxied by the share of required tasks that can be transferred to labor, tooling, or automated systems.

## 10. Falsifiable Hypotheses ##

The theory generates clear empirical expectations.

**H1. Dependence hypothesis.** Holding intrinsic burden constant, entities with higher system dependence will exhibit lower time freedom.

**H2. Mitigation inequality hypothesis.** Entities with similar nominal extrinsic obligations will nonetheless show significant variation in effective freedom, explained by differences in mitigation capacity.

**H3. Recurrence hypothesis.** Interventions that reduce recurring effective burden will produce larger cumulative gains in time freedom than equal-cost one-time time windfalls over sufficiently long horizons.

**H4. Compounding hypothesis.** Entities with greater present time freedom will, on average, more rapidly accumulate future mitigation capacity and lower future dependence.

**H5. Externalization hypothesis.** Some observed increases in one entity's time freedom will correspond to transferred or externalized obligations borne by another entity.

These hypotheses make the theory falsifiable rather than merely interpretive.

## 11. Implications ##

The theory carries several implications.

First, freedom is operational, not merely declarative. A formally permitted action does not constitute meaningful freedom if the time required to sustain access, compliance, or viability eliminates practical control.

Second, equality of formal rules does not imply equality of freedom. Two entities may operate under the same nominal conditions while exhibiting divergent effective freedom because one can buffer, navigate, restructure, or delegate constraints more effectively.

Third, capital and knowledge matter because they are time-conversion mechanisms. Their significance lies not in symbolic possession alone, but in their capacity to reduce recurring obligations or to prevent external systems from claiming time.

Fourth, system design can be evaluated by its burden profile. A system is freedom-efficient to the extent that it minimizes recurring extrinsic obligation for a given level of output, coordination, or stability.

Fifth, freedom analysis becomes portable across domains. For persons, the theory clarifies labor, class, and bureaucracy. For firms, it clarifies overhead, vendor lock-in, and regulatory load. For machines and digital services, it clarifies maintenance, compute overhead, operator dependence, and protocol burden. For institutions, it clarifies the time cost of legitimacy maintenance, coordination, and enforcement.

## 12. Limitations ##

Several limitations should be made explicit.

The first is that time quantity is not identical to time quality. Two entities may possess equal residual time while differing in the usability, fragmentation, or strategic value of that time.

The second is that obligations may overlap. Some tasks simultaneously satisfy intrinsic and extrinsic requirements, complicating clean partitioning.

The third is that one entity's freedom may be produced by another entity's unfreedom. Delegation, outsourcing, and system restructuring may transfer burden rather than eliminate it globally.

The fourth is that the theory does not, by itself, resolve moral questions. It measures and explains control over time; it does not determine whether any particular distribution of that control is just.

The fifth is that empirical implementation requires calibration. The theory specifies structure and directionality, but functional forms and coefficients remain domain-specific and must be estimated.

## 13. Conclusion ##

The Time-Constraint Theory of Entity Freedom defines freedom as residual temporal control. For any entity, time freedom is total available process-time minus intrinsic obligation minus effective extrinsic obligation. Effective extrinsic obligation is raw extrinsic burden net of the entity's capacity to avoid, restructure, delegate, or otherwise mitigate external claims on its time.

This formulation generalizes the source model into a broader theory with clear ontology, explicit equations, monotonic assumptions, comparative-statics results, dynamic extension, and empirical testability. Its central claim is simple: the lived or operational freedom of an entity is not adequately described by rights, options, or preferences alone. It is described by how much of that entity's finite time remains unclaimed after reality and surrounding systems have taken what they can take.

In minimal form, the theory reduces to:

\[
F_x(H) = T_x(H) - R_x(H).
\]

And because

\[
R_x(H) = I_x(H) + \max\{0, E^{raw}_x(H) - V_x(H)\},
\]

the theory implies that any durable increase in freedom must come from one of only three sources: an increase in available time, a reduction in intrinsic maintenance burden, or a reduction in effective extrinsic obligation. Of these, the third is the most structurally variable and the most politically, economically, and strategically consequential.
EOF