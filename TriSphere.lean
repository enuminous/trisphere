import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Algebra.Ring.Periodic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Mathlib.Analysis.SpecificLimits.Basic

namespace TriSphere

abbrev Layer := Fin 13

def mirror (n : Layer) : Layer := ⟨12 - n.val, by omega⟩

theorem mirror_involution (n : Layer) : mirror (mirror n) = n := by
  apply Fin.ext
  simp only [mirror]
  omega

theorem midpoint_unique (n : Layer) : mirror n = n ↔ n = 6 := by decide +revert

def coarse (n : Layer) : Fin 5 :=
  if n = 0 then 0 else if n < 6 then 1 else if n = 6 then 2 else if n < 12 then 3 else 4

def coarseMirror (n : Fin 5) : Fin 5 := ⟨4 - n.val, by omega⟩

theorem coarse_mirror (n : Layer) : coarse (mirror n) = coarseMirror (coarse n) := by decide +revert

theorem coarse_surjective (n : Fin 5) : ∃ x : Layer, coarse x = n := by decide +revert

def stepOut (n : Layer) : Layer := ⟨min (n.val + 1) 12, by omega⟩

theorem no_coarse_step : ¬ ∃ f : Fin 5 → Fin 5, ∀ x, f (coarse x) = coarse (stepOut x) := by
  rintro ⟨f, h⟩
  have h1 : f 1 = 1 := h 1
  have h5 : f 1 = 2 := h 5
  have hn : (1 : Fin 5) ≠ 2 := by decide
  exact hn (h1.symm.trans h5)

/-- An explicit periodic comparison construction: phase is distinct from radius. -/
def phaseRadius (p : Fin 24) : Layer :=
  ⟨min p.val (24 - p.val), by omega⟩

def phaseAt (t : ℕ) : Fin 24 := ⟨t % 24, Nat.mod_lt _ (by decide)⟩

theorem phase_period (t : ℕ) : phaseRadius (phaseAt (t+24)) = phaseRadius (phaseAt t) := by
  have h : phaseAt (t+24) = phaseAt t := by apply Fin.ext; simp [phaseAt]
  rw [h]

theorem phase_orientation_loss :
    phaseRadius (phaseAt 5) = phaseRadius (phaseAt 19) ∧
    phaseRadius (phaseAt 6) ≠ phaseRadius (phaseAt 20) := by decide

theorem face_pairs : 12 * 12 = 144 := by decide

def norm4 (a b c d : ℝ) := a^2 + b^2 + c^2 + d^2
def hx (a b c d : ℝ) := a^2 + b^2 - c^2 - d^2
def hy (a b c d : ℝ) := 2 * (a*c + b*d)
def hz (a b c d : ℝ) := 2 * (b*c - a*d)

theorem hopf_norm (a b c d : ℝ) :
    hx a b c d ^ 2 + hy a b c d ^ 2 + hz a b c d ^ 2 = norm4 a b c d ^ 2 := by
  unfold hx hy hz norm4
  ring

theorem hopf_phase (a b c d u v : ℝ) (hu : u^2 + v^2 = 1) :
    let A := a*u-b*v
    let B := a*v+b*u
    let C := c*u-d*v
    let D := c*v+d*u
    hx A B C D = hx a b c d ∧ hy A B C D = hy a b c d ∧ hz A B C D = hz a b c d := by
  dsimp [hx, hy, hz]
  constructor
  · linear_combination (a^2+b^2-c^2-d^2)*hu
  constructor
  · linear_combination (2*(a*c+b*d))*hu
  · linear_combination (2*(b*c-a*d))*hu

theorem shell_zero (a b c d : ℝ) (h : norm4 a b c d = 0) :
    a = 0 ∧ b = 0 ∧ c = 0 ∧ d = 0 := by
  unfold norm4 at h
  refine ⟨?_, ?_, ?_, ?_⟩ <;> apply (sq_eq_zero_iff).mp <;> nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg c, sq_nonneg d]

theorem radius_two_control : hx 2 0 0 0 = 4 ∧ hx 2 0 0 0 ≠ 1 := by norm_num [hx]

theorem radius_branch (t : ℝ) :
    HasDerivAt (fun s : ℝ => 12 + s^3) (3*t^2) t := by
  convert (((hasDerivAt_id t).pow 3).const_add (12:ℝ)) using 1
  simp

theorem stationary_crossing :
    HasDerivAt (fun s : ℝ => 12 + s^3) 0 0 ∧
    (∀ t : ℝ, 0 < t → 12 < 12+t^3) ∧ (∀ t : ℝ, t < 0 → 12+t^3 < 12) := by
  refine ⟨by simpa using radius_branch 0, ?_, ?_⟩
  · intro t ht
    nlinarith [pow_pos ht 3]
  · intro t ht
    nlinarith [mul_pos_of_neg_of_neg ht ht, mul_neg_of_pos_of_neg (mul_pos_of_neg_of_neg ht ht) ht]

noncomputable def energy (r v U : ℝ → ℝ) (t : ℝ) := v t ^ 2 / 2 + U (r t)

/-- U is the effective potential V minus a primitive of the fixed position drive. -/
theorem energy_rate (r v U g : ℝ → ℝ) (γ t : ℝ)
    (hr : HasDerivAt r (v t) t)
    (hv : HasDerivAt v (-g (r t) - γ * v t) t)
    (hU : HasDerivAt U (g (r t)) (r t)) :
    HasDerivAt (energy r v U) (-γ * v t ^ 2) t := by
  convert (((hv.pow 2).div_const 2).add (hU.comp t hr)) using 1
  dsimp [energy]
  ring

/-- A periodic antitone real observable is constant. -/
theorem periodic_level (E : ℝ → ℝ) (T : ℝ) (hT : 0 < T)
    (hm : Antitone E) (hp : Function.Periodic E T) : ∀ x, E x = E 0 := by
  have forward : ∀ a b : ℝ, a ≤ b → E a = E b := by
    intro a b hab
    obtain ⟨n, hn⟩ := exists_nat_gt ((b-a)/T)
    have bound := (div_lt_iff₀ hT).mp hn
    have hab' : b ≤ a + (n:ℝ)*T := by linarith
    have hba := hm hab'
    rw [hp.nat_mul n a] at hba
    exact le_antisymm hba (hm hab)
  intro x
  rcases le_total x 0 with h | h
  · exact forward x 0 h
  · exact (forward 0 x h).symm

/-- On a smooth trajectory with fixed position-only drive and positive damping,
a periodic position AND velocity force the velocity to vanish everywhere. -/
theorem fixed_drive_periodic_velocity_zero (r v U g : ℝ → ℝ) (γ T : ℝ)
    (hγ : 0 < γ) (hT : 0 < T)
    (hr : ∀ t, HasDerivAt r (v t) t)
    (hv : ∀ t, HasDerivAt v (-g (r t) - γ * v t) t)
    (hU : ∀ x, HasDerivAt U (g x) x)
    (pr : Function.Periodic r T) (pv : Function.Periodic v T) (t : ℝ) : v t = 0 := by
  have rate := fun x => energy_rate r v U g γ x (hr x) (hv x) (hU (r x))
  have hm : Antitone (energy r v U) := antitone_of_hasDerivAt_nonpos rate
    (fun x => by dsimp; nlinarith [mul_nonneg hγ.le (sq_nonneg (v x))])
  have hp : Function.Periodic (energy r v U) T := by
    intro x
    simp only [energy, pr x, pv x]
  have hc : energy r v U = fun _ => energy r v U 0 :=
    funext (periodic_level _ _ hT hm hp)
  have ht := (rate t).deriv
  rw [hc, deriv_const] at ht
  have hz : γ * v t ^ 2 = 0 := by linarith
  exact pow_eq_zero_iff (by decide : 2 ≠ 0) |>.mp ((mul_eq_zero.mp hz).resolve_left hγ.ne')

theorem coast_accel_ne_zero (γ v : ℝ) (hg : 0 < γ) (hv : v ≠ 0) : -γ*v ≠ 0 :=
  mul_ne_zero (neg_ne_zero.mpr hg.ne') hv

def kick (q J E : ℝ) := q * E + J

theorem kick_fixed (q J : ℝ) (hq : q < 1) : kick q J (J/(1-q)) = J/(1-q) := by
  unfold kick
  field_simp [ne_of_gt (sub_pos.mpr hq)]
  ring

theorem kick_deviation (q J E A : ℝ) (h : kick q J A = A) :
    kick q J E - A = q*(E-A) := by unfold kick at *; linarith

theorem kick_iterate (q J E A : ℝ) (h : kick q J A = A) (n : ℕ) :
    (kick q J)^[n] E - A = q^n * (E-A) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Function.iterate_succ_apply', kick_deviation q J _ A h, ih, pow_succ]
    ring

theorem filter_conservation (total kept : ℕ) (h : kept ≤ total) :
    kept + (total - kept) = total := by omega

theorem a_destination_does_not_fix_a_path :
    (fun t : ℝ => 12*(1-t)) 0 = (fun t : ℝ => 12*(1-t)^2) 0 ∧
    (fun t : ℝ => 12*(1-t)) 1 = (fun t : ℝ => 12*(1-t)^2) 1 ∧
    (fun t : ℝ => 12*(1-t)) (1/2) ≠ (fun t : ℝ => 12*(1-t)^2) (1/2) := by norm_num

theorem drive_primitive (V W slope drive : ℝ → ℝ)
    (hV : ∀ x, HasDerivAt V (slope x) x) (hW : ∀ x, HasDerivAt W (drive x) x) (x : ℝ) :
    HasDerivAt (fun y => V y - W y) (slope x - drive x) x := (hV x).sub (hW x)

theorem kick_converges (q J E : ℝ) (h0 : 0 ≤ q) (h1 : q < 1) :
    Filter.Tendsto (fun n : ℕ => (kick q J)^[n] E) Filter.atTop (nhds (J/(1-q))) := by
  let A := J/(1-q)
  have h := kick_iterate q J E A (kick_fixed q J h1)
  have hlim := (tendsto_pow_atTop_nhds_zero_of_lt_one h0 h1).mul
    (tendsto_const_nhds (x := E-A) (f := Filter.atTop))
  have hlim' := hlim.add (tendsto_const_nhds (x := A))
  convert hlim' using 1
  · ext n
    have := h n
    linarith
  · simp [A]

end TriSphere
