// DIS 1.7 — UtterancePolicy
// Canonical source. JSON Schema is GENERATED from this file:
//   cue def cue/UtterancePolicy.cue -e '#UtterancePolicy' --out jsonschema
package dis

#PolicyType:     "OBLIGATION" | "PROHIBITION" | "DISCLOSURE_LIMIT" | "LIFECYCLE"
#Enforcement:    "STRUCTURAL" | "INSTRUCTED" | "ADVISORY"
#LiabilityClass: "STANDARD" | "REGULATORY" | "MEDICAL" | "FINANCIAL" | "SAFETY"
#Violation:      "REFUSE" | "ESCALATE" | "SUPPRESS" | "REDACT" | "LOG_ONLY"
#Lifecycle:      "GREETING" | "HOLDING" | "ERROR" | "CLOSING" | "HANDOFF"

#uuid: =~"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"

// A constraint on what an agent may SAY, independent of what it may DO.
// AccessGate governs reach; this governs the form of the utterance once reach is granted.
#UtterancePolicy: {
	policyId:    #uuid
	name:        string & !=""
	description: string & !=""

	policyType: #PolicyType

	// The rule, as a condition. Never copy, never steps.
	requirement: string & !=""

	// Where the rule is actually enforced. Required — the whole value of the
	// field is that it is a deliberate choice, not a default.
	enforcement: #Enforcement

	liabilityClass?: #LiabilityClass
	onViolation?:    #Violation

	appliesToRoleIds?:    [...#uuid]
	appliesToTripletIds?: [...#uuid]
	appliesToEntityIds?:  [...#uuid]

	// For OBLIGATION: values the utterance must carry.
	boundValueRefs?: [...string]

	// When the policy is active. Absent = always.
	condition?: string

	// Only meaningful for LIFECYCLE.
	lifecyclePhase?: #Lifecycle

	primaryKey?:  string
	foreignKeys?: [...string]
	appliedTags?: [...string]

}

// ---------------------------------------------------------------------------
// Conditional constraints live HERE, not in #UtterancePolicy.
//
// CUE's JSON Schema exporter silently drops a definition containing `if`
// comprehensions — it emits the description and nothing else, with no error.
// So the flat shape above stays exportable and is the published contract, and
// the conditionals are enforced by `cue vet` locally and by SHACL on the graph.
//
// This is the documented delta: the published JSON Schema is WEAKER than the
// full contract. SHACL `sh:or` carries the difference.
// ---------------------------------------------------------------------------
#UtterancePolicyStrict: #UtterancePolicy & {
	policyType: _pt
	let _pt = policyType

	// An OBLIGATION that binds no value obliges nothing.
	if _pt == "OBLIGATION" {
		boundValueRefs: [_, ...]
	}
	// A LIFECYCLE policy names its phase.
	if _pt == "LIFECYCLE" {
		lifecyclePhase: #Lifecycle
	}
}
