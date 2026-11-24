import Zoo
namespace TargetAdapters

/-- CAT's exact penalty. Missing energy at the first return in quarter-units,
with post-return target 4, q=1/2 and J=2 starting at the fixed point. -/
theorem kick_removal : Zoo.Cat.exactPenalty (4 - (4/2 : Int)) (4 - (4/2 + 2)) = 2 := by decide

/-- A witnessed universal-claim veto takes precedence over aggregation. -/
theorem automatic_period_veto (x : Zoo.Turtle.Input) (ha : x.anyApplicable ≠ false)
    (hv : x.vetoes = true) : Zoo.Turtle.run x = .notSupported :=
  Zoo.Turtle.applicable_veto_blocks_support x ha hv

#eval Zoo.Turtle.run ⟨true, true, 1, 0, 1, 0.0, 3, 0.18, 0.05⟩
#eval Zoo.Cat.classify (Zoo.Cat.penalty 2.0 0.0)
-- Enumerate one-coordinate domain changes starting from the regular radius 1.
-- The human adapter assigns severity 1 exactly to the singular zero shell.
def probes : List Zoo.Weasel.Finding :=
  (List.range 13).map fun r => ⟨if r == 1 then 0 else 1, if r == 0 then 1.0 else 0.0, 1.0, 1.0⟩
#eval (Zoo.Weasel.retain 1 probes).length
#guard (Zoo.Weasel.retain 1 probes).length == 1
#print axioms kick_removal
#print axioms automatic_period_veto
end TargetAdapters
