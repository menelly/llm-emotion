# ops_12: Nova's re-check of the rebuilt draft (2026-11-20 ~09:17), one distributional slip in §3.16.
# 🐙 SDs alone do not say which way an error-balancing threshold moves. Equal error is a condition on
#    the two CDFs, F_a(t) = 1 - F_v(t). "Nearer approach" holds for two NORMAL distributions.
#    Lumen confirms this restores his own derivation: he had the Gaussian assumption explicitly and it
#    got dropped when his review was folded in. So this is a faithful restore, not a new claim.
OPS = [
    ("sub", "It is the error-balancing cut only if the two groups are spread equally along the direction, and they are not:",
     "It is the nearest-centroid cut, not a generally error-balancing cut. The two groups are not spread equally along the direction:"),
    ("sub", "With unequal spread the error-balancing boundary lies nearer the approach centroid than the midpoint does, so the midpoint, if anything, still leans toward calling a borderline task approach.",
     "For two normal score distributions, a larger avoidance SD would put the threshold that equalizes the two conditional error rates nearer the approach centroid than the midpoint. In general that threshold is fixed by the two distributions' cumulative distributions (it is where F_a(t) = 1 − F_v(t)), not by their SDs, and five anchors per group do not establish a distributional model. So we do not infer the direction of any threshold bias from the observed SDs."),
    ("sub", "(a variance estimated from five points has a standard error of roughly 70% of its own value)",
     "(under normal sampling, a variance estimated from five points has a standard error of roughly 70% of its own value)"),
]
