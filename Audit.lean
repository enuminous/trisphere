import TriSphere
import Lean

#check TriSphere.mirror_involution
#print axioms TriSphere.mirror_involution
#check TriSphere.midpoint_unique
#print axioms TriSphere.midpoint_unique
#check TriSphere.coarse_mirror
#print axioms TriSphere.coarse_mirror
#check TriSphere.coarse_surjective
#print axioms TriSphere.coarse_surjective
#check TriSphere.no_coarse_step
#print axioms TriSphere.no_coarse_step
#check TriSphere.phase_period
#print axioms TriSphere.phase_period
#check TriSphere.phase_orientation_loss
#print axioms TriSphere.phase_orientation_loss
#check TriSphere.face_pairs
#print axioms TriSphere.face_pairs
#check TriSphere.hopf_norm
#print axioms TriSphere.hopf_norm
#check TriSphere.hopf_phase
#print axioms TriSphere.hopf_phase
#check TriSphere.shell_zero
#print axioms TriSphere.shell_zero
#check TriSphere.radius_two_control
#print axioms TriSphere.radius_two_control
#check TriSphere.radius_branch
#print axioms TriSphere.radius_branch
#check TriSphere.stationary_crossing
#print axioms TriSphere.stationary_crossing
#check TriSphere.energy_rate
#print axioms TriSphere.energy_rate
#check TriSphere.periodic_level
#print axioms TriSphere.periodic_level
#check TriSphere.fixed_drive_periodic_velocity_zero
#print axioms TriSphere.fixed_drive_periodic_velocity_zero
#check TriSphere.coast_accel_ne_zero
#print axioms TriSphere.coast_accel_ne_zero
#check TriSphere.kick_fixed
#print axioms TriSphere.kick_fixed
#check TriSphere.kick_deviation
#print axioms TriSphere.kick_deviation
#check TriSphere.kick_iterate
#print axioms TriSphere.kick_iterate
#check TriSphere.filter_conservation
#print axioms TriSphere.filter_conservation
#check TriSphere.a_destination_does_not_fix_a_path
#print axioms TriSphere.a_destination_does_not_fix_a_path
#check TriSphere.drive_primitive
#print axioms TriSphere.drive_primitive
#check TriSphere.kick_converges
#print axioms TriSphere.kick_converges

open Lean in
run_cmd do
  let env ← getEnv
  let modules : Array Name := #[`TriSphere]
  let allowed : Array Name := #[``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut theoremCount := 0
  for (name, info) in env.constants.toList do
    let isProject := match env.getModuleIdxFor? name with
      | some idx => modules.contains env.header.moduleNames[idx.toNat]!
      | none => (`AuditProbe).isPrefixOf (privateToUserName name)
    if isProject && !info.isUnsafe then
      count := count + 1
      if info matches .thmInfo _ then
        theoremCount := theoremCount + 1
      for ax in (← collectAxioms name) do
        unless allowed.contains ax do
          throwError "Unapproved axiom {ax} used by {name}"
  if count == 0 then
    throwError "Audit matched no project declarations"
  logInfo m!"Axiom audit passed: {count} safe declarations, {theoremCount} theorem declarations (including generated lemmas)."
